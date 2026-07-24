"""
© Battelle Memorial Institute 2026
Made available under the MIT License (MIT)

BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.
"""

"""
This module contains the RiskModel class and related functions for calculating risk based on user input and structured risk parameters. The RiskModel class precomputes the risk for all locations and subpopulations based on the provided parameters and allows for easy retrieval of risk values for specific locations and subpopulations.
"""
import numpy as np
import pandas as pd
from collections import defaultdict
from pathlib import Path
import logging

from .config import CONFIG, lookup

logger = logging.getLogger(__name__)


def _resolve_risk_parameter_path(path_value: str) -> Path:
    """Resolve configured risk parameter path robustly for source and frozen app."""
    p = Path(path_value)
    if p.is_absolute():
        return p

    # Prefer package root (src/pyside6) so config value like
    # "ref_data/model_inputs-v2.xlsx" works regardless of cwd.
    package_root = Path(__file__).resolve().parents[1]
    candidate = package_root / p
    if candidate.exists():
        return candidate

    # Backward-compatible fallback to current working directory resolution.
    return p

class RiskModel:
    """
    A class to represent the risk model for different locations and subpopulations based on user input and structured risk parameters.
    
    Parameters
    ----------
    id50: float
        The ID50 value representing the infectivity level.
    hourly_exposure: float
        The hourly exposure level.
    locations: list
        A list of locations for which to calculate risk.
    indoor_weighting: int
        The weighting factor for indoor locations.
    risk_parameters: dict
        A dictionary containing the structured risk parameters for each location and subpopulation.
    user_defined_weights: dict
        A dictionary containing user-defined weights for locations and subpopulations.
    """
    def __init__(self, 
                 id50: float, 
                 hourly_exposure: float, 
                 locations: list, 
                 indoor_weighting: int, 
                 risk_parameters: dict,
                 user_defined_weights: dict):
        self.id50 = id50
        self.hourly_exposure = hourly_exposure
        self.locations = locations
        self.indoor_weighting = indoor_weighting
        self.risk_parameters = risk_parameters
        self.subpopulations = ['staff', 'customer', 'permanent', 'visitor']
        self.user_defined_weights = user_defined_weights
        self.base_risk = self._precompute_risk()
    
    def get_risk(self, location: str, subpop: str) -> float:
        """
        Get the risk for a given location and subpopulation.
        
        Parameters
        ----------
        location: str
            The location for which to get the risk.
        subpop: str
            The subpopulation for which to get the risk.
        
        Returns
        -------
        float
            The risk for the given location and subpopulation.
        """
        return self.base_risk.get(location, {}).get(subpop, 0)
    
    def get_simplified_risk_df(self) -> pd.DataFrame:
        """
        Get the simplified risk for each location by summing the risk of all subpopulations.
        
        Returns
        -------
        pd.DataFrame
            A dataframe containing the simplified risk for each location, along with the size of the structure and the risk per area in acres.
        """
        simplified_risk = {
            loc: self.get_risk_per_structure(loc) for loc in self.locations
        }
        risk_df = pd.DataFrame(simplified_risk, index=['location'])
        risk_df = risk_df.transpose()
        risk_df.columns = [CONFIG["risk_method_settings"]["perDURadio"]["risk_col"]]

        risk_df["size"] = [
            self.risk_parameters[lookup("full_name", loc, "short_name")]['structure']['size'] 
            for loc in self.locations
        ]
        risk_df[CONFIG["risk_method_settings"]["perAreaRadio"]["risk_col"]] = self.convert_sq_meters_to_acres(
            risk_df[CONFIG["risk_method_settings"]["perDURadio"]["risk_col"]], risk_df['size']
        )
        return risk_df

    def convert_sq_meters_to_acres(self, risk_per_structure: float, size_m2: float) -> float:
        """
        Convert risk per structure from per square meter to per acre.
        
        Parameters
        ----------
        risk_per_structure: float
            The risk for the structure in per square meter.
        size_m2: float
            The size of the structure in square meters.
        
        Returns
        -------
        float
            The risk per structure in per acre.
        """
        size_acres = size_m2 / CONFIG["constants"]["SQ_METERS_PER_ACRE"]
        return risk_per_structure / size_acres
    
    def get_risk_per_structure(self, location: str) -> float:
        """
        Get the risk for a given location by summing the risk of all subpopulations.
        
        Parameters
        ----------
        location: str
             The location for which to get the risk.
        
        Returns
        -------
        float
            The total risk for the given location.
        """
        return np.sum(
            [self.base_risk[location][x] for x in self.subpopulations]
        )

    def _precompute_risk(self) -> dict:
        """
        Precompute the risk for all locations and subpopulations.
        
        Returns
        --------
        dict
            A dictionary containing the precomputed risk for each location and subpopulation.
        """
        return {
            loc: {
                subpop: (
                    self._calc_multiplier(loc)
                    * self._correct_risk_for_demographic(
                        self._baseline_risk(loc, subpop), 
                        loc, subpop
                    )
                ) 
                for subpop in self.subpopulations
            }
            for loc in self.locations
        }

    def _calc_multiplier(self, location: str) -> float:
        """
        Calculate the risk multiplier for a given location based on whether it's indoor or outdoor.
        
        Parameters
        ----------
        location: str
            The location for which to calculate the risk multiplier.
        
        Returns
        -------
        float
            The risk multiplier for the given location.
        """
        if lookup("full_name", location, "indoor"):
            return self.indoor_weighting / 100
        return (100 - self.indoor_weighting) / 100
    
    def _baseline_risk(self, location: str, subpop: str) -> float:
        """
        Calculate the baseline risk for a given location and subpopulation using the provided risk parameters.
        
        Parameters
        ----------
        location: str
            The location for which to calculate the baseline risk.
        subpop: str
            The subpopulation for which to calculate the baseline risk.
        
        Returns
        -------
        float
            The baseline risk for the given location and subpopulation.
        """
        loc_key = lookup("full_name", location, "short_name") 
        pop = self.risk_parameters[loc_key][subpop]['count']
        time = self.risk_parameters[loc_key][subpop]['time']
        struct_count = self.risk_parameters[loc_key]['structure']['count']

        slope = self.risk_parameters['general']['infectivity']['slope']
        max_inf = self.risk_parameters['general']['infectivity']['max']

        if time == 0:
            return 0
        X = pop * max_inf
        Y = (time * self.hourly_exposure / self.id50)**(-slope)
        Z = struct_count
        return X / (Z * (1 + Y))
    
    def _correct_risk_for_demographic(self, base_risk: float, location: str, subpop: str) -> float:
        """
        Correct the baseline risk for a given location and subpopulation based on demographic factors.
        
        Parameters
        ----------
        base_risk: float
            The baseline risk for the given location and subpopulation.
        location: str
            The location for which to calculate the corrected risk.
        subpop: str
            The subpopulation for which to calculate the corrected risk.
        
        Returns
        -------
        float
            The corrected risk for the given location and subpopulation.
        """
        loc_key = lookup("full_name", location, "short_name")
        weight_key = lookup("full_name", location, "weight") 

        newborn_factor = self.user_defined_weights["demographic_weights"]["newborn_weight"] 
        newborn_fraction = self.risk_parameters[loc_key][subpop]['fraction_newborn']
        elder_factor = self.user_defined_weights["demographic_weights"]["elderly_weight"]
        elder_fraction = self.risk_parameters[loc_key][subpop]['fraction_elderly']
        vulnerable_factor = self.user_defined_weights["demographic_weights"]["vulnerable_weight"]
        vulnerable_fraction = self.risk_parameters[loc_key][subpop]['fraction_vulnerable']
        
        local_char = self.user_defined_weights["location_weights"][weight_key]
        char_modifier = self.risk_parameters["general"]["total"]["local_characteristics"]

        char_multiplier = local_char / char_modifier
        newborn_contribution = newborn_factor * newborn_fraction
        elder_contribution = elder_factor * elder_fraction
        vulnerable_contribution = vulnerable_factor * vulnerable_fraction
        general_contribution = 1 - newborn_fraction - elder_fraction - vulnerable_fraction
    
        return float(base_risk * char_multiplier * (newborn_contribution + elder_contribution + vulnerable_contribution + general_contribution))

def load_risk_model_parameters(fpath):
    """
    Read excel file with model parameters
    
    Parameters
    ----------
    fpath: str 
        path to excel file

    Returns
    -------
    dict 
        Model parameters from file in a structured format for use in risk calculations
    """
    try:
        input_df = pd.read_excel(fpath)
    except Exception as e:
        logger.error(e)
        raise Exception(f'Critical Error occurred while reading model parameters: {e}')
    input_df2 = input_df.dropna(axis='index', subset='Class')
    input_df2.pivot(columns=['Class'], index=['Class Group', 'SubClass'], values='Value')
    input_dict = defaultdict(dict)
    for i in input_df2['Class'].unique():
        for j in input_df2['Class Group'].unique():
            if len(input_df[(input_df['Class'] == i) &
                                (input_df['Class Group'] == j)]['Value']) > 0:
                input_dict[i][j] = defaultdict(dict)
            for k in input_df2['SubClass'].unique():
                if len(input_df[(input_df['Class'] == i) &
                                (input_df['Class Group'] == j) &
                                (input_df['SubClass'] ==  k)]['Value']) > 0:
                    input_dict[i][j][k] = input_df[(input_df['Class'] == i) &
                                                (input_df['Class Group'] == j) &
                                                (input_df['SubClass'] ==  k)]['Value'].values[0]
                    if input_dict[i][j][k] != input_dict[i][j][k]:
                        try:
                            input_dict[i][j][k] = input_dict['general']['total'][k]
                        except:
                            pass
    return input_dict


def load_risk_model(input_data: dict) -> RiskModel:
    """
    Load the risk model based on user input and precompute the risk for all locations and subpopulations.
    
    Parameters
    -----------
    input_data: dict
        User-defined parameters
    risk_parameters: dict
        Risk parameters read from file

    Returns
    -------
    RiskModel
        An instance of the RiskModel class.
    """
    risk_model_parameter_file = _resolve_risk_parameter_path(
        CONFIG["risk_model_parameter_file"]
    )
    logger.info(f"Loading risk model parameters from: {risk_model_parameter_file}")
    risk_parameters = load_risk_model_parameters(risk_model_parameter_file)
    if input_data['infectivity'] == 0:
        id50 = risk_parameters['general']['infectivity']['id50-low']
    elif input_data['infectivity'] == 1:
        id50 = risk_parameters['general']['infectivity']['id50-medium']
    elif input_data['infectivity'] == 2:
        id50 = risk_parameters['general']['infectivity']['id50-high']
    else:
        id50 = risk_parameters['general']['infectivity']['id50-medium'] # default to medium
        logger.warning(f'Invalid infectivity level selected: {input_data["infectivity"]}. Defaulting to Medium exposure level')
    if input_data['exposure'] == 0:
        hourly_exposure = risk_parameters['general']['exposure']['low']
    elif input_data['exposure'] == 1:
        hourly_exposure = risk_parameters['general']['exposure']['medium']
    elif input_data['exposure'] == 2:
        hourly_exposure = risk_parameters['general']['exposure']['high']
    else:
        hourly_exposure = risk_parameters['general']['exposure']['medium'] # default to medium
        logger.warning(f'Invalid exposure level selected: {input_data["exposure"]}. Defaulting to Medium exposure level')
    logger.info(f'Using id50 = {id50} and hourly exposure = {hourly_exposure}')

    locations = [loc["full_name"] for loc in CONFIG["locations"] if loc["weight"]]
    try:
        risk_model = RiskModel(
            id50=id50,
            hourly_exposure=hourly_exposure,
            locations=locations,
            indoor_weighting=CONFIG.get("indoor_outdoor_weighting", 80),
            risk_parameters=risk_parameters,
            user_defined_weights=input_data
        )
        return risk_model
    
    except Exception as e:
        logger.error(f"Error loading risk model: {e}")
        return None

