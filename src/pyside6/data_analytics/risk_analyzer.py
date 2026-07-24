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

from shapely.geometry import Polygon
import numpy as np
from pyproj import CRS, Transformer
import logging

from .config import CONFIG, lookup
from .structure_dataset_loader import get_utm_zone


logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """
    Class to analyze risk based on a given risk model and structure dataset

    Parameters
    ----------
    risk_model: RiskModel
        Risk model object containing the risk model and associated parameters
    risk_method: str
        method to calculate risk (e.g. "perAreaRadio", "perStructureRadio", "perAreaFraction", "perStructureFraction")
    banded_risk: bool
        whether to perform risk banding for visualization purposes
    nRiskBands: int
        number of risk bands to use for banding (if banded_risk is True)
    """
    def __init__(self, risk_model, risk_method, banded_risk, nRiskBands):
        self.risk_model = risk_model
        self.banded_risk = banded_risk
        if risk_method in CONFIG["risk_method_settings"]:
            self.risk_method = risk_method
        else:
            self.risk_method = "default"
        self.nRiskBands = nRiskBands

        self.risk_col = CONFIG["risk_method_settings"][self.risk_method]["risk_col"]
        self.risk_fldr = CONFIG["risk_method_settings"][self.risk_method]["risk_fldr"]


        self.n_bands = int(self.nRiskBands) + 1
        self.risk_groups = list(np.linspace(start=0, stop=1, num=self.n_bands))

    def analyze(self, gdf: "GeoDataFrame", bounding_box: "BoundingBox") -> dict:
        """
        Analyze risk based on the given risk model and structure dataset
        
        Parameters
        ----------
        gdf: GeoDataFrame
            GeoDataFrame containing the structure dataset with risk values added
        bounding_box: BoundingBox
            Bounding box defining the area of interest
        
        Returns
        -------
        dict
            Dictionary containing the results of the analysis, including:
            - "gdf": GeoDataFrame with risk values added
            - "area_summary": DataFrame with risk weighted by area
        """
        result = {"gdf": None, "area_summary": None}
        result["gdf"] = self.build_gdf(self.risk_model, gdf)
        result["area_summary"] = self.build_area_summary(result["gdf"], bounding_box, self.risk_col)
        return result


    def build_gdf(self, risk_model: "RiskModel", gdf: "GeoDataFrame") -> "GeoDataFrame":
        """
        Build a GeoDataFrame with risk values added based on the given risk model and structure dataset
        
        Parameters
        ----------
        risk_model: RiskModel
            Risk model object containing the risk model and associated parameters
        gdf: GeoDataFrame
            GeoDataFrame containing the structure dataset
        
        Returns
        -------
        GeoDataFrame
            GeoDataFrame with risk values added
        """
        gdf = add_risk_to_gdf(gdf, risk_model.get_simplified_risk_df())
        gdf = compute_risk_per_structure(gdf, self.risk_col)

        if self.banded_risk:
            logger.info('Performing risk banding')
            gdf = risk_banding(
                gdf, 
                self.risk_groups, 
                f'{self.risk_col} - Banded Risk for Visualization',
                f'{self.risk_col} - Banded Risk'
            )
        return gdf
    
    def build_area_summary(self, gdf, bounding_box, risk_col):
        return calc_area_summary(gdf, bounding_box, risk_col)

def add_risk_to_gdf(df: "GeoDataFrame", rwf: "GeoDataFrame", sub_col: str="location") -> "GeoDataFrame":
    """
    Add risk values from the risk model to the structure dataset GeoDataFrame
    Parameters
    ----------
    df: GeoDataFrame
        GeoDataFrame containing the structure dataset
    rwf: GeoDataFrame
        GeoDataFrame containing the risk values from the risk model, with a column matching sub_col for merging
    sub_col: str
        Name of the column to use for merging the risk values with the structure dataset (default is "location")
    
    Returns
    -------
    GeoDataFrame
        GeoDataFrame with risk values added
    """
    conv_dict = {
        loc["short_name"]: loc["full_name"] 
        for loc in CONFIG["locations"]
    }
    rwf = rwf.reset_index(names=sub_col)
    rwf['merge'] = rwf[sub_col].map(conv_dict).fillna(rwf[sub_col])
    df = df.merge(rwf, left_on=['Structure Type'], right_on=['merge'])
    return df

def risk_banding(gdf: "GeoDataFrame", risk_grouping: list, bcol: str, bcol2: str) -> "GeoDataFrame":
    """
    Perform risk banding for visualization purposes based on the given risk grouping thresholds

    Parameters
    ----------
    gdf: GeoDataFrame
        GeoDataFrame containing the structure dataset with risk values added
    risk_grouping: list
        List of risk thresholds to use for banding (e.g. [0.25, 0.5, 0.75] for quartiles)
    bcol: str       
        Name of the column to create for the banded risk values with thresholds for visualization purposes (e.g. "Risk Band - Visualization")
    bcol2: str
        Name of the column to create for the banded risk values (e.g. "Risk Band")
    """
    gdf[bcol] = risk_grouping[0]
    gdf[bcol2] = f'{round(risk_grouping[0], 2)} - {round(risk_grouping[1], 2)}'
    for i, risk in enumerate(risk_grouping):
        if i == (len(risk_grouping)-1): # Don't apply the logic with the last group (1)
            break
        mask = gdf['Normalized Risk'] > round(risk,2) # round to align with reported value
        gdf.loc[mask, bcol] = risk_grouping[i]
        gdf.loc[mask, bcol2] = f'{round(risk_grouping[i], 2)} - {round(risk_grouping[i+1], 2)}'
    gdf['Number of Risk Bands'] = len(risk_grouping) - 1
    return gdf

def compute_risk_per_structure(gdf: "GeoDataFrame", risk_col: str) -> "GeoDataFrame":
    """
    Compute risk per structure based on the structure size and risk per area, and add it as a new column to the GeoDataFrame

    Parameters
    ----------
    gdf: GeoDataFrame
        GeoDataFrame containing the structure dataset with risk values added
    risk_col: str
        Name of the column containing the risk per area values (e.g. "Risk per Area (Acre)")
    
    Returns
    -------
    GeoDataFrame
        GeoDataFrame with a new column for individual structure risk values (e.g. "Individual Structure Risk")
    """
    gdf[CONFIG["risk_method_settings"]["perFractionRadio"]["risk_col"]] = compute_individual_structure_risk(
        gdf['Structure Size (m^2)'], 
        convert_risk_from_acres_to_sq_meters(gdf[CONFIG["risk_method_settings"]["perAreaRadio"]["risk_col"]])
    )
    gdf['Normalized Risk'] = gdf[risk_col] / gdf[risk_col].max()
    temp_df = gdf.groupby(by=['location'])[CONFIG["risk_method_settings"]["perFractionRadio"]["risk_col"]].sum().to_frame()
    temp_df = temp_df.rename(columns={CONFIG["risk_method_settings"]["perFractionRadio"]["risk_col"]: 'Sum of Individual Structure Risk by Type'}).reset_index()
    merge_df = gdf.merge(temp_df, how='left', on='location')
    return merge_df

def convert_risk_from_acres_to_sq_meters(risk_per_area_acres: float) -> float:
    """
    Convert risk per area from acres to square meters

    Parameters
    ----------
    risk_per_area_acres: float or Series
        Risk per area value(s) in acres to be converted to square meters
    """
    return risk_per_area_acres / CONFIG["constants"]["SQ_METERS_PER_ACRE"] 

def compute_individual_structure_risk(structure_size: float, risk_per_area: float) -> float:
    """
    Compute the individual structure risk based on the structure size and risk per area.

    Parameters
    ----------
    structure_size: float
        Size of the structure in square meters
    risk_per_area: float
        Risk per area value in square meters
    
    Returns
    -------
    float
        Individual structure risk value
    """
    return structure_size * risk_per_area


def total_area(min_lat: float, min_long: float, max_lat: float, max_long: float) -> tuple:
    """
    Calculate the total area of the bounding box defined by the given latitude and longitude coordinates in both square meters and square miles.

    Parameters
    ----------
    min_lat: float
        Minimum latitude of the bounding box
    min_long: float
        Minimum longitude of the bounding box
    max_lat: float
        Maximum latitude of the bounding box
    max_long: float
        Maximum longitude of the bounding box

    Returns
    -------
    tuple
        Total area of the bounding box in square meters and square miles (area_sq_meters, area_sq_miles)
    """
    longitudes = [min_long, max_long]
    central_long = sum(longitudes) / len(longitudes)
    utm_zone = get_utm_zone(central_long)
    
    crs_wgs84 = CRS.from_epsg(CONFIG["constants"]["WGS84_EPSG"])
    crs_utm = CRS.from_epsg(CONFIG["constants"]["UTM_BASE_NORTHERN_HEMISPHERE"] + utm_zone)  
    
    # Create a transformer object
    transformer_to_utm = Transformer.from_crs(crs_wgs84, crs_utm, always_xy=True)
    bottom_left_utm = transformer_to_utm.transform(min_long, min_lat)
    bottom_right_utm = transformer_to_utm.transform(max_long, min_lat)
    top_left_utm = transformer_to_utm.transform(min_long, max_lat)
    top_right_utm = transformer_to_utm.transform(max_long, max_lat)

    # Create a polygon using the transformed coordinates
    utm_polygon = Polygon([
        bottom_left_utm,
        bottom_right_utm,
        top_right_utm,
        top_left_utm
    ])
    area_sq_meters = utm_polygon.area
    area_sq_miles = area_sq_meters / CONFIG["constants"]["SQ_METERS_PER_SQ_MILE"]
    return area_sq_meters, area_sq_miles

def calc_area_summary(gdf: 'GeoDataFrame', bounding_box: 'BoundingBox', risk_col: str) -> 'DataFrame':
    """
    Calculate a summary of the area of structures and associated risk within the bounding box, including fractional area of structures and region, and relative risk.
    
    Parameters
    ----------
    gdf: GeoDataFrame
        GeoDataFrame containing the structure dataset with risk values added
    bounding_box: BoundingBox
        Bounding box defining the area of interest
    risk_col: str
        Name of the column containing the risk values to use for calculating relative risk (e.g. "Risk per Area (Acre)")
        
    Returns    
    -------
    DataFrame
        DataFrame containing the area summary with columns for structure type, total area of structures, fractional area of structures, fractional area of region, total area of region, and relative risk.
    """
    ta_meters, ta_miles = total_area(*bounding_box.to_list())
    tot_area = ta_meters

    risk_col_sum = risk_col + "_sum"
    risk_col_mean = risk_col + "_mean"
    risk_cols = [
        'Structure Type', 
        'Structure Size (m^2)', 
        CONFIG["risk_method_settings"]["perAreaRadio"]["risk_col"], 
        CONFIG["risk_method_settings"]["perDURadio"]["risk_col"],
        CONFIG["risk_method_settings"]["perFractionRadio"]["risk_col"],
        'Normalized Risk'
    ]
    if risk_col not in risk_cols:
        risk_cols.append(risk_col)

    risk_cols = [x for x in risk_cols if x in gdf.columns]

    area_summary = gdf[risk_cols].groupby(by=['Structure Type']).agg(['sum', 'mean'])
    area_summary.columns = ['_'.join(col).strip() for col in area_summary.columns.values]
    area_summary['Fractional Area of Structures'] = area_summary['Structure Size (m^2)_sum'] / area_summary['Structure Size (m^2)_sum'].sum()
    area_summary['Fractional Area of Region'] = area_summary['Structure Size (m^2)_sum'] / tot_area
    area_summary['Total Area of Region'] = tot_area

    area_summary['RelativeRisk_sum'] = area_summary[risk_col_sum] / area_summary[risk_col_sum].sum()
    area_summary['RelativeRisk_mean'] = area_summary[risk_col_mean] / area_summary[risk_col_mean].sum()

    return area_summary
