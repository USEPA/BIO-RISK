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
This is the main file for the risk analysis module. It contains the main function that runs the analysis and calls other functions to load data, analyze risk, and produce outputs.
"""
from pathlib import Path
import geopandas as gpd
import pandas as pd
import logging

from .risk_model import load_risk_model
from .structure_dataset_loader import StructureDatasetLoader, BoundingBox
from .risk_analyzer import RiskAnalyzer

from .config import CONFIG


logger = logging.getLogger(__name__)

def main(
        risk_model_inputs: dict,
        structure_data_parameters: dict,
        risk_analysis_options: dict,
    output_options: dict,
    progress_callback=None,
    cancel_callback=None,
    ) -> tuple:
    """
    Runs the main analysis

    Parameters
    ----------
    risk_model_inputs : dict
        user-defined risk model inputs
    structure_data_parameters : dict
        contains bounding box to extract structures from GIS
    risk_analysis_options : dict
        contains options for risk analysis
    output_options : dict
        contains options for output like output folder and whether to produce geojson
    
    Returns
    -------
    tuple
        gdf: geodataframe with all data
        out_html_dict: dictionary matching path and file to be written
        out_geojson_dict: dictionary matching path and file to be written
        area_summary: dict with area summary
    """  
    def _progress(percent: int, message: str):
        if callable(progress_callback):
            progress_callback(percent, message)

    def _check_cancel():
        if callable(cancel_callback) and cancel_callback():
            raise InterruptedError("Analysis cancelled by user")

    _check_cancel()
    _progress(10, "Loading risk model...")

    # Load risk model
    risk_model = load_risk_model(
        risk_model_inputs
    ) 

    # Load structure dataset
    _check_cancel()
    _progress(30, "Loading structures...")
    structures_dataloader = StructureDatasetLoader()
    bounding_box = BoundingBox(*structure_data_parameters["bounding_box_coords"])
    gdf = structures_dataloader.load(bounding_box)

    # Analyze risk
    _check_cancel()
    _progress(55, "Analyzing risk...")
    risk_analyzer = RiskAnalyzer(
        risk_model,
        risk_analysis_options["risk_method"],
        risk_analysis_options["banded_risk"],
        risk_analysis_options["nRiskBands"]
    )
    results = risk_analyzer.analyze(gdf, bounding_box)

    # Determine which columns to include in the outputs based on what is available in the results
    city = f"lat {bounding_box.min_lat}, {bounding_box.max_lat}; long {bounding_box.min_long}, {bounding_box.max_long}"
    banding = (
        risk_analyzer.banded_risk
        and risk_analyzer.risk_groups != None 
        and len(risk_analyzer.risk_groups) >= 2
    )

    _progress(70, "Preparing outputs...")
    _check_cancel()

    # Generate outputs
    out_folder = Path(output_options['output_folder']) / Path(risk_analyzer.risk_fldr)
    out_folder.mkdir(parents=True, exist_ok=True)
    if output_options["output_html"]:
        plot_cols = [risk_analyzer.risk_col]
        if banding:
            plot_cols.append(f'{risk_analyzer.risk_col} - Banded Risk for Visualization')
        popup_columns = [
            'Structure Type', 
            CONFIG["risk_method_settings"]["perDURadio"]["risk_col"],
            CONFIG["risk_method_settings"]["perAreaRadio"]["risk_col"],
            CONFIG["risk_method_settings"]["perFractionRadio"]["risk_col"],
            f'{risk_analyzer.risk_col} - Banded Risk', 
            'Normalized Risk', 
            'Number of Risk Bands'
        ]
        plot_cols = [c for c in plot_cols if c in results["gdf"].columns]
        popup_columns = [c for c in popup_columns if c in results["gdf"].columns]

        results["html_output"] = build_html_output(results["gdf"], out_folder, city, popup_columns, plot_cols, banding)
    else:
        results["html_output"] = {}
    if output_options["output_geojson"]:
        results["geojson_output"] = build_geojson_output(results["gdf"], out_folder, risk_analyzer.risk_col, city, banding)
    else:
        results["geojson_output"] = {}

    _progress(78, "Finalizing results...")

    # Return results
    area_summary_dict = {out_folder / Path(f'area_summary.csv'): results["area_summary"]}
    return results["gdf"], results["html_output"], results["geojson_output"], area_summary_dict

def _format_popup_gdf(gdf: gpd.GeoDataFrame, columns: list, threshold: float = 0.001, sig: int = 3) -> gpd.GeoDataFrame:
    """Return a copy of gdf with numeric popup columns formatted as strings.

    - Values in (0, threshold) are shown as '<{threshold}'.
    - All integer digits are always shown in full (no scientific notation).
    - Up to `sig` significant figures are shown in the decimal portion,
      capped at 3 decimal places. Trailing zeros are stripped.
    """
    gdf = gdf.copy()
    for col in columns:
        if col not in gdf.columns:
            continue
        if pd.api.types.is_numeric_dtype(gdf[col]):
            def _fmt(v, _t=threshold, _s=sig):
                if pd.isna(v):
                    return ""
                if v == 0:
                    return "0"
                if 0 < v < _t:
                    return f"<{_t}"
                abs_v = abs(v)
                if abs_v >= 1:
                    int_digits = len(str(int(abs_v)))
                    dec_digits = max(0, min(3, _s - int_digits))
                else:
                    dec_digits = min(3, _s)
                formatted = f"{v:.{dec_digits}f}"
                if '.' in formatted:
                    formatted = formatted.rstrip('0').rstrip('.')
                return formatted
            gdf[col] = gdf[col].apply(_fmt)
    return gdf


def build_html_output(gdf: gpd.GeoDataFrame, out_folder: Path, city: str, popup_columns: list, plot_cols: list, banding: bool = False) -> dict:
    """
    Builds the HTML output using the geodataframe and the specified columns for plotting and popups.

    Parameters
    ----------
    gdf : GeoDataFrame
        The geodataframe containing the analysis results.
    out_folder : Path
        The folder where the output HTML files will be saved.
    city : str
        A string representing the city or area being analyzed, used for naming the output files.
    popup_columns : list
        A list of column names to include in the popups on the map.
    plot_cols : list
        A list of column names to use for coloring the map.
    banding : bool, optional
        Whether the risk is banded, which affects the naming of the columns, by default False

    Returns
    -------
    dict
        A dictionary where the keys are the paths to the output HTML files and the values are the corresponding map objects.
    """
    out_html_dict = {}
    for col in plot_cols:
        tile_url = 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}'
        attr = 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
        # Format numeric popup columns as strings (3 sig figs; '<0.001' for small values).
        # Use a temp column for color mapping so the formatted popup value is never overwritten,
        # even when col also appears in popup_columns (e.g. the unbanded map).
        display_gdf = _format_popup_gdf(gdf, popup_columns)
        _plot_col = '__plot__'
        display_gdf[_plot_col] = gdf[col]
        m = display_gdf.explore(column=_plot_col, cmap='turbo', 
                        popup=popup_columns,
                        popup_kwds={"localize": False},
                        tooltip=False,
                        tiles=tile_url,
                        attr=attr)

        out_html = out_folder / Path(f'outputmap-{col}.html')
        out_html_dict[out_html] = m
    return out_html_dict


def build_geojson_output(gdf, out_folder, risk_col, city, banding):
    """
    Builds the GeoJSON output by saving the geodataframe as GeoJSON files, one for each unique value in the specified risk column.

    Parameters
    ----------
    gdf : GeoDataFrame
        The geodataframe containing the analysis results.
    out_folder : Path
        The folder where the output GeoJSON files will be saved.
    risk_col : str
        The name of the column in the geodataframe that contains the risk values, used for
        determining how to split the data into different GeoJSON files.
    city : str
        A string representing the city or area being analyzed, used for naming the output files.
    banding : bool
        Whether the risk is banded, which affects the naming of the columns and files.
    
    Returns
    -------
    dict
        A dictionary where the keys are the paths to the output GeoJSON files and the values are the corresponding geodataframes that will be saved as GeoJSON. 
    """
    json_dict = {}
    if not banding:
        dc = 'Structure Type'
    else:
        dc = f'{risk_col} - Banded Risk'
    for du in gdf[dc].unique():
        gdf_temp = gdf[gdf[dc]==du]
        gdf_temp = gdf_temp.sort_values(by=['Normalized Risk'])
        gdf_temp = gdf_connector(gdf_temp) # Combine all polygons into a single "polygon"
        if banding:
            d = 'Risk Band ' + du
        else:
            d = du
        outpath = out_folder / Path(f'{d}.geojson')
        json_dict[outpath] = gdf_temp
    return json_dict

def gdf_connector(gdf):
    """
    Connects all polygons in a geodataframe to create a single polygon. This is used to create a single polygon for each unique value in the risk column when generating GeoJSON outputs.

    Parameters
    ----------
    gdf : GeoDataFrame
        The geodataframe containing the polygons to be connected.
    
    Returns
    -------
    GeoDataFrame
        A geodataframe with a single polygon that is the result of connecting all the polygons in the input geodataframe.
    """
    # This connects all the polygons in the geodataframe to form a 'single' entity
    a = gpd.overlay(gdf, gdf, how='intersection')
    gdf_out = a.dissolve()
    return gdf_out