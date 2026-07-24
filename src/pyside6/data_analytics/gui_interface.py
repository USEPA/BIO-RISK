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

import logging
from .main import main
from .config import CONFIG

logger = logging.getLogger(__name__)


def main_process(
        gui_state_data, 
        bounding_box_coords,
        progress_callback=None,
        cancel_callback=None,
    ):
    """ Converts GUI information to a format that is ammenable for
    GIS-based analysis
    Args:
        gui_state_data (dict): Dictionary of inputs from GUI
        bounding_box_coords (list[float]): Bounding box to be analyzed
        logger (logging, optional): non-standard logger class. Defaults to None.

    Returns:
        gdf: geodataframe with all data
        out_html_dict: dictionary matching path and file to be written
        json_dict: dictionary matching path and file to be written
        area_summary: geodataframe with integrated summaries
    """
    def _progress(percent: int, message: str):
        if callable(progress_callback):
            progress_callback(percent, message)

    _progress(5, "Preparing inputs...")
    if callable(cancel_callback) and cancel_callback():
        raise InterruptedError("Analysis cancelled by user")
    gui_state = unpack_gui_state(gui_state_data, bounding_box_coords)
    
    try:
        _progress(8, "Starting analysis engine...")
        gdf, out_html, json_dict, area_summary = main(
            gui_state["risk_model_inputs"],
            gui_state["structure_data_parameters"],
            gui_state["risk_analysis_options"],
            gui_state["output_options"],
            progress_callback=progress_callback,
            cancel_callback=cancel_callback,
        )
        _progress(79, "Analysis complete, writing outputs...")
        logger.info(f'Data stored in outputfolder: {gui_state["output_options"]["output_folder"]}')
        logger.info('Process completed successfully!')
    except Exception as e:
        logger.error(e)
        raise
    return gdf, out_html, json_dict, area_summary

def unpack_gui_state(gui_state_data, bounding_box_coords):
    """ Unpacks the GUI state into a format that is ammenable for
    GIS-based analysis
    Args:
        gui_state_data (dict): dict containing all GUI state informatio
    """
    ###################
    #  Output options
    ###################
    output_options = {
        "output_geojson": gui_state_data["geojson_output_layers"], # geojson_output_layers
        "output_html": True, # always output html
        "output_folder": gui_state_data["outputFolder"]
    }

    ###################
    #  Risk analysis options
    ###################    
    risk_analysis_options = {
        "risk_method": gui_state_data["risk_method"],
        "banded_risk": gui_state_data["banded_risk"],
        "nRiskBands": gui_state_data["nRiskBands"]
    }

    ###################
    #  Risk model inputs and parameters
    ###################
    # User defined risk model inputs
    locations = [
        loc.get("weight", "").split("_weight")[0] for loc in CONFIG["locations"]
        if loc.get("weight", "") in gui_state_data
    ]
    demographics = [
        demo.get("weight", "").split("_weight")[0] for demo in CONFIG["demographics"]
        if demo.get("weight", "") in gui_state_data
    ]

    risk_model_inputs = {}
    risk_model_inputs["location_weights"] = {
        k: v for k, v in gui_state_data.items()
        if k.split("_weight")[0] in locations
    }
    risk_model_inputs["demographic_weights"] = {
        k: v for k, v in gui_state_data.items()
         if k.split("_weight")[0] in demographics
    }
    risk_model_inputs["infectivity"] = gui_state_data["infectivity"]
    risk_model_inputs["exposure"] = gui_state_data["exposure"]

    ###################
    #  Structure data loading options
    ###################
    print(bounding_box_coords)
    structure_data_parameters = {
        "bounding_box_coords": bounding_box_coords
    }
    
    return {
        "risk_model_inputs": risk_model_inputs,
        "structure_data_parameters": structure_data_parameters,
        "risk_analysis_options": risk_analysis_options,
        "output_options": output_options
    }
