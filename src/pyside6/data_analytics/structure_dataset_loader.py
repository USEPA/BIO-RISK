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

from __future__ import annotations
import geopandas as gpd
from shapely.geometry import Polygon, LineString, MultiPolygon, MultiLineString
from pyproj import Transformer, CRS
from rtree import index
import pandas as pd
import logging
import time
from collections import defaultdict
from arcgis.geometry import Geometry
from arcgis.geometry.filters import intersects
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import arcgis.auth.api as arcgis_auth_api
import logging
import copy

from .config import CONFIG, lookup

logger = logging.getLogger(__name__)

class LayerData:
    """
    This class stores individual layer data from a FeatureLayer

    Parameters
    ----------  
    lyr: arcgis.features.FeatureLayer
        The feature layer to store.
    """
    instances = []
    names = []

    def __init__(self, lyr: FeatureLayer):
        self.id = id
        self.lyr = lyr
        self.name = self.lyr.properties.name
        try:
            self.s_ref = self.lyr.estimates['extent']['spatialReference']
        except:
            self.s_ref = self.lyr.extent['spatialReference']
        LayerData.instances.append(self)
        LayerData.names.append(self.name)

class BoundingBox:
    def __init__(self, min_lat, min_long, max_lat, max_long):
        self.min_lat = min_lat
        self.min_long = min_long
        self.max_lat = max_lat
        self.max_long = max_long

    def to_list(self) -> list[float]:
        """
        Convert the bounding box to a list representation.

        Returns
        -------
        list
            A list containing [min_lat, min_long, max_lat, max_long].
        """
        return [self.min_lat, self.min_long, self.max_lat, self.max_long]
    
def convert_esri(bounding_box: BoundingBox, s_ref: dict) -> BoundingBox:
    """
    Convert bounding box coordinates from lat/long to the spatial reference of the input dataset.

    Parameters
    ----------
    bounding_box: BoundingBox
        The bounding box defined in lat/long coordinates.
    s_ref: dict
        The spatial reference of the input dataset.
    
    Returns
    -------
    BoundingBox
        A new BoundingBox object with coordinates converted to the spatial reference of the input dataset.
    """
    # Converting all lat/long values to the s_ref of the input data set
    if 'latestWkid' in s_ref.keys():
        ts_ref = s_ref['latestWkid']
    else:
        ts_ref = s_ref['wkid']
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:"+str(ts_ref))
    # Note -- transformer.transform returns (easting, northing),
    # which is technically a (long, lat) format.
    # We use the original lat/long variable names for consistency with
    # the definition of the BoundingBox class, but technically they are long/lat values.
    # This doesn't end up causing issues because this bounding box is only used to store values for the query,
    # and the values are stored in the right order.
    min_lat, min_long = transformer.transform(bounding_box.min_lat, bounding_box.min_long)
    max_lat, max_long = transformer.transform(bounding_box.max_lat, bounding_box.max_long)
    return BoundingBox(min_lat, min_long, max_lat, max_long), ts_ref


class StructureDatasetLoader:
    """
    Data loader class for loading and processing structure datasets from ArcGIS Online based on provided layer IDs and bounding box. This class handles querying the data, converting it to GeoDataFrames, checking for duplicates/similar geometries, and preparing the data for risk analysis.
    """
    def __init__(self, ids: list[str] = None):
        if ids is None:
            self.ids = CONFIG["GIS_dataset_IDs"]
        else:
            self.ids = ids
        logger.info('Connecting to geographic data sources...')

        # In frozen Windows builds, ArcGIS auth may auto-select IWA/Kerberos,
        # which can require local MIT Kerberos (KfW). Force non-Kerberos path.
        arcgis_auth_api.HAS_GSSAPI = False
        arcgis_auth_api.HAS_KERBEROS = False

        try:
            # Force anonymous ArcGIS Online access to avoid enterprise
            # Windows/Kerberos auth dependencies on end-user machines.
            self.gis = GIS(
                "https://www.arcgis.com",
                verify_cert=False,
                trust_env=False,
            )
            logger.info('GIS connection: Success (ArcGIS Online anonymous)')
        except Exception as e:
            logger.warning(f'ArcGIS Online anonymous connection failed: {e}')
            # Fallback to previous behavior if needed by a specific environment.
            self.gis = GIS(verify_cert=False, trust_env=False)
        logger.info('GIS connection: Success')
    
    
    def load(self, bounding_box: BoundingBox) -> gpd.GeoDataFrame:
        """
        Load and process structure datasets from ArcGIS Online based on the provided bounding box.
        
        Parameters
        ----------
        bounding_box: BoundingBox
            Object defining the area of interest

        Returns
        -------
        geopandas.GeoDataFrame
            Combined and processed structure data
        """
        # Get layer data for each layer type
        layers = self.get_layer_data()

        # Create a gdf for each layer and add risk information
        gdfs = []
        for layer in layers:
            if not (
                'structure' in layer.name.lower() 
                or 'park' in layer.name.lower() 
                or layer.name in CONFIG["road_layer_line_widths"]
            ):
                logger.warning(f'Skipping "{layer.name}" layer data because it cannot be processed')
                continue
            new_bounding_box, s_ref = convert_esri(bounding_box, layer.s_ref)
            gdf = self.query_layer(new_bounding_box, layer, s_ref)
            if gdf is None:
                continue
            gdf = standardize_column_names(gdf, source=layer.name)
            if gdf is None:
                logger.warning(f"Standardizing column names failed for layer {layer.name}")
                continue
            gdf.reset_index(drop=True, inplace=True)
            e_gdf = self.customize_layer_geometry(layer, gdf, new_bounding_box)

            gdfs.append(e_gdf.copy(deep=True))
            logger.info(f'Finished processing {layer.name} layer')
        
        # Combine gdfs and perform final processing
        gdf = self.create_combined_gdf(gdfs)
        gdf = self.compute_structure_areas(gdf, bounding_box)
        return gdf

    def compute_structure_areas(self, gdf: gpd.GeoDataFrame, bounding_box: BoundingBox) -> gpd.GeoDataFrame:
        """
        Compute the area of each structure in the GeoDataFrame.

        Parameters
        ----------
        gdf: geopandas.GeoDataFrame
            GeoDataFrame containing the structure geometries
        bounding_box: BoundingBox
            Object defining the area of interest

        Returns
        -------
        geopandas.GeoDataFrame
            GeoDataFrame with an additional column for structure areas in square meters
        """
        longs_list = [bounding_box.max_long, bounding_box.min_long]
        central_long = sum(longs_list) / len(longs_list)
        utm_zone = get_utm_zone(central_long)
        utm_zone += CONFIG["constants"]["UTM_BASE_NORTHERN_HEMISPHERE"]
        tgdf = gdf.copy(deep=True)
        tgdf = gdf.to_crs(epsg=utm_zone) # convert to appropriate UTM zone for area calculation
        tgdf['Structure Size (m^2)'] = abs(tgdf['geometry'].area)
        gdf['Structure Size (m^2)'] = tgdf['Structure Size (m^2)'] # Revert back to original gdf to keep original projections
        return gdf

    def customize_layer_geometry(self, layer: LayerData, gdf: gpd.GeoDataFrame, bounding_box: BoundingBox) -> gpd.GeoDataFrame:
        """
        Customizes geometry to the GeoDataFrame based on the layer type. For transportation layers, it converts lines to polygons based on a specified buffer distance. For park layers, it explodes multi-part geometries into single parts. For structure layers, it retains the original geometries.

        Parameters
        ----------
        layer: LayerData
            The layer information
        gdf: geopandas.GeoDataFrame
            The GeoDataFrame containing the geometries
        bounding_box: BoundingBox
            Object defining the area of interest
        Returns
        -------
        geopandas.GeoDataFrame
            The customized GeoDataFrame
        """
        if 'structure' in layer.name.lower(): # FEMA updated their layer name, so I am making this less specific
            e_gdf = gdf.copy(deep=True)
        elif 'park' in layer.name.lower():
            gdf = gpd.clip(gdf, bounding_box.to_list())
            e_gdf = gdf.explode(column='geometry', ignore_index=True)
        elif layer.name in CONFIG["road_layer_line_widths"]: # transportation layers
            gdf = gpd.clip(gdf, bounding_box.to_list())
            e_gdf = gdf.explode(column='geometry', ignore_index=True)
            for idx, row in e_gdf.iterrows():
                if row['geometry'].geom_type == 'LineString' or row['geometry'].geom_type == 'MultiLineString': # Turn road lines into polygons
                    line = row['geometry']
                    line_thickness = CONFIG["road_layer_line_widths"][layer.name]
                    e_gdf.at[idx, 'geometry'] = line.buffer(line_thickness)
                elif row['geometry'].geom_type == 'Polygon':
                    continue
                else: # Turn points into polygon
                    for j in row['geometry']:
                        poly_list = points_edit(line, line_thickness)
                    e_gdf.at[idx, 'geometry'] = Polygon(poly_list)
        return e_gdf

    def create_combined_gdf(self, gdf_list: list[gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
        """
        Creates a combined GeoDataFrame from a list of GeoDataFrames, ensuring uniqueness and handling similar geometries.
        
        Parameters
        ----------
        gdf_list: list of GeoDataFrames
            List of GeoDataFrames to combine
        
        Returns
        -------
        geopandas.GeoDataFrame
            Combined GeoDataFrame with unique geometries
        """
        gdf = pd.concat(gdf_list)
        if 'NAME' not in gdf.columns:
            gdf['NAME'] = ''
        if 'NAME' in gdf.columns:
            gdf.sort_values(by='NAME', inplace=True) #Ensure the same duplicate is retained
        elif 'PROP_ADDR' in gdf.columns:
            gdf.sort_values(by='PROP_ADDR', inplace=True) #Ensure the same duplicate is retained
        gdf.drop_duplicates(subset='geometry', keep='first', inplace=True, ignore_index=True) # Drop exact duplicates first to save time
        unique_mask = self.is_similar(gdf)# Looking for similarities across the data sets
        sim_polys = len(unique_mask) - sum(unique_mask)
        if sim_polys > 0:
            logger.info(f'Found {sim_polys} similar structures within tolerance between all layers')
        gdf = gdf[unique_mask] # Confirming similarities between data layers don't exist 
        return gdf

    def get_layer_data(self) -> list[LayerData]:
        """
        Retrieves layer data from the GIS content.
        
        Returns
        -------
        list of LayerData
            List of LayerData objects
        """
        layer_list = []
        for id in self.ids:
            feature_layer = self.gis.content.get(id)
            for layer in feature_layer.layers:
                lyr = LayerData(layer)
                layer_list.append(lyr)
        return layer_list
    
    def convert_to_gdf(self, df: pd.DataFrame, s_ref: dict) -> gpd.GeoDataFrame:
        """
        Converts a DataFrame to a GeoDataFrame, ensuring the geometry column is properly identified and duplicates are removed.
        
        Parameters
        ----------
        df: pandas.DataFrame
            The input DataFrame containing spatial data.
        s_ref: dict
            The spatial reference of the geometries in the DataFrame.
        Returns
        -------
        geopandas.GeoDataFrame
            GeoDataFrame with unique geometries
        """
        geo_col = self._geo_col_finder(df)
        if geo_col != 'geometry':
            df['geometry'] = df[geo_col]
            df = df.drop(columns=[geo_col])
        logger.info('Checking for duplicate geometries. This can take a few minutes')
        if 'NAME' in df.columns:
            df.sort_values(by='NAME', inplace=True) #Ensure the same duplicate is retained
        elif 'PROP_ADDR' in df.columns:
            df.sort_values(by='PROP_ADDR', inplace=True) #Ensure the same duplicate is retained
        df.drop_duplicates(subset='geometry', keep='first', inplace=True, ignore_index=True) # Drop exact duplicates first (faster)
        gdf = gpd.GeoDataFrame(df, crs=s_ref)
        unique_mask = self.is_similar(gdf)
        similar_geoms = len(unique_mask) - sum(unique_mask)
        if similar_geoms > 0:
            logger.info(f'Found {similar_geoms} geometries that are similar within tolerance')
        return gdf
    
    def _geo_col_finder(self, df: pd.DataFrame) -> str:
        """
        Identify the column in the DataFrame that contains geometry data. If no geometry column is found, it defaults to 'SHAPE'.
        
        Parameters
        ----------
        df: pandas.DataFrame
            The input DataFrame to search for a geometry column.

        Returns
        -------
        str
            The name of the geometry column, or 'SHAPE' if no geometry column is found.
        """
        out = None
        for col in df.columns:
            a = str(type(df.loc[0,col]))
            if 'geometry' in a:
                out = col
        if out == None:
            return 'SHAPE'
        else:
            return out 
        
    def is_similar(self, gdf: gpd.GeoDataFrame, tolerance: float = 0.05) -> list[bool]:
        """
        Check for polygon uniqueness within a GeoDataFrame based on a specified tolerance.
        
        Parameters
        ----------
        gdf: geopandas.GeoDataFrame
            The input GeoDataFrame containing geometries to check for uniqueness.
        tolerance: float, optional
            The tolerance value for geometry comparison. Default is 0.05.

        Returns
        -------
        list of bool
            A list indicating whether each geometry is unique (True) or not (False).
        """
        unique_mask = [True] * len(gdf)
        spatial_index = index.Index()
        for i, geom in enumerate(gdf.geometry):
            spatial_index.insert(i, geom.bounds)
        for i, geom1 in enumerate(gdf.geometry):
            if unique_mask[i]: # Only check if this geometry is still marked as unique
                possible_matches = list(spatial_index.intersection(geom1.bounds)) # Reduce geometry comparison to intersecting geometries
                for j in possible_matches:
                    if i != j and unique_mask[j]:
                        geom2 = gdf.geometry[j]
                        if geom1.equals_exact(geom2, tolerance):
                            unique_mask[j] = False # Mark duplicates (but not the original)
        return unique_mask
    
    def query_layer(self, bounding_box: BoundingBox, layer: LayerData, s_ref: dict, max_record_count: int = 1000) -> gpd.GeoDataFrame | None:
        """
        Query a layer within a specified bounding box and return the results as a GeoDataFrame.
        
        Parameters
        ----------
        bounding_box: BoundingBox
            The bounding box to query.
        layer: LayerData
            The layer to query.
        max_record_count: int, optional
            The maximum number of records to return per query. Default is 1000.

        Returns
        -------
        geopandas.GeoDataFrame or None
            A GeoDataFrame containing the query results, or None if no results are found.
        """
        query_filter = self._build_query(bounding_box, layer)
        all_features = []
        result_offset = 0
        while True:
            try:
                results = layer.lyr.query(
                    geometry_filter=query_filter, 
                    as_df=False, 
                    sr=layer.s_ref,
                    return_all_records=False,
                    result_offset = result_offset,
                    result_record_count = max_record_count
                )
            except Exception as e: # Handle too many requests by waiting one minute and trying again
                if "quota exceeded" in str(e).lower() or "too many requests" in str(e).lower():
                    time.sleep(65)  # Wait 65 seconds for quota reset
                    continue  # Retry the same request
                else:
                    raise e  # Re-raise other exceptions
            for feature in results:
                attributes = feature.attributes
                geometry = feature.geometry
                combined_entry = {**attributes, 'SHAPE': geometry}
                all_features.append(combined_entry)

            if len(results) < max_record_count:
                break
            result_offset += max_record_count

        if all_features:
            rdf = pd.DataFrame(all_features)
            if 'structure' in layer.name.lower() or 'park' in layer.name.lower():
                #Convert point data into polygons (if it is a closed set of points)
                rdf['SHAPE'] = rdf['SHAPE'].apply(convert_geometry)
            else:
                #Don't convert circular roads into polygons
                rdf['SHAPE'] = rdf['SHAPE'].apply(convert_geometry2)
            rdf = self.convert_to_gdf(rdf, s_ref)
            return rdf
        else: 
            return None
      
    def _build_query(self, bounding_box: BoundingBox, layer: LayerData) -> dict:
        """
        Build a spatial query for the specified layer and bounding box.

        Parameters
        ----------
        bounding_box: BoundingBox
            The bounding box to query.
        layer: LayerData
            The layer to query.

        Returns
        -------
        dict
            A dict that can be used to query the layer within the bounding box.
        """
        query_extent = {
            "xmin": bounding_box.min_lat,
            "ymin": bounding_box.min_long,
            "xmax": bounding_box.max_lat,
            "ymax": bounding_box.max_long,
            "spatialReference": layer.s_ref 
        }
        qe_geo = Geometry(query_extent)
        query_filter = intersects(qe_geo, sr=layer.s_ref)
        return query_filter  



def get_utm_zone(lon: float) -> int:
    """
    Determine the UTM zone for a given longitude.

    Parameters
    ----------
    lon: float
        Longitude in decimal degrees.

    Returns
    -------
    int
        UTM zone number.
    """
    return int((lon + 180) / 6) + 1

def points_edit(line: LineString, edit_val: float) -> list[tuple[float, float]]:
    """
    Create a polygon from a line by buffering the line with a specified edit value.

    Parameters
    ----------
    line: shapely.geometry.LineString
        The line to buffer.
    edit_val: float
        The buffer distance.

    Returns
    -------
    list
        A list of coordinates representing the buffered polygon.
    """
    coords = list(line.coords)
    poly_out = [(t[0]-edit_val, t[1]-edit_val) for t in coords]
    poly_out2 = [(t[0]+edit_val, t[1]+edit_val) for t in coords]
    poly_list = poly_out.copy()
    r = [poly_out2[i] for i in range(len(poly_out2)-1,-1,-1)]
    poly_list.extend(r)
    return(poly_list)

def convert_geometry(geom: dict) -> Polygon | MultiPolygon | LineString | None:
    """
    Convert ESRI geometry to Shapely geometry. Handles both polygon and line geometries, and accounts for cases where roads may be represented as closed lines.

    Parameters
    ----------
    geom: dict
        The geometry dictionary from ESRI, which may contain 'rings' for polygons or 'paths' for lines.
    
    Returns
    -------
    shapely.geometry.Polygon or shapely.geometry.LineString or shapely.geometry.MultiPolygon or None
        The converted Shapely geometry object, or None if the geometry type is not recognized.
    """
    geom_type = list(geom.keys())[0]
    if geom_type == 'rings':
        if len(geom['rings']) > 1:
            pass
        exterior = geom['rings'][0]
        interiors = geom['rings'][1:] if len(geom['rings']) > 1 else []
        if len(interiors) > 0:
            pass
        return Polygon(exterior, interiors)
    elif 'paths' in geom:
        closed_paths = [path for path in geom['paths'] if path[0] == path[-1]]
        if closed_paths:
            polygons = [Polygon(path) for path in closed_paths]
            if len(polygons) == 1:
                return polygons[0]
            else:
                return MultiPolygon(polygons) # Assume only one polygon per structure
        else:
            line_shape = [LineString(x) for x in geom['paths']]
            if len(line_shape) == 1:
                return line_shape[0] # Assume only one line per unclosed path (e.g. road)
            else:
                return None
    else:
        return None
    
def convert_geometry2(geom: dict) -> Polygon | LineString | None:
    """
    Convert ESRI geometry to Shapely geometry for transportation layers, which may include lines that are closed but should not be converted to polygons.

    Parameters
    ----------
    geom: dict
        The geometry dictionary from ESRI, which may contain 'rings' for polygons or 'paths' for lines.
    
    Returns
    -------
    shapely.geometry.Polygon or shapely.geometry.LineString or None
        The converted Shapely geometry object, or None if the geometry type is not recognized.
    """
    # This works for street data points to not convert a circular road into a polygon
    geom_type = list(geom.keys())[0]
    if geom_type == 'rings':
        exterior = geom['rings'][0]
        interiors = geom['rings'][1:] if len(geom['rings']) > 1 else [] 
        return Polygon(exterior, interiors)
    elif 'paths' in geom:
        line_shape = [LineString(x) for x in geom['paths']]
        if len(line_shape) == 1:
            return line_shape[0]
        else:
            return None
    else:
        return None
    
def _build_fema_nsi_key_registry() -> dict:
    """
    Builds a registry that maps FEMA and NSI keys to their corresponding full names. This registry is used for standardizing column names in the datasets.

    Returns
    -------
    dict
        A dictionary where the keys are the full names of locations and the values are lists of corresponding FEMA and NSI keys.
    """
    registry = defaultdict(list)
    fema_registry = {
        loc["full_name"]: loc["fema_keys"] if loc["fema_keys"] is not None else []
        for loc in CONFIG["locations"]
    }
    nsi_registry = {
        loc["full_name"]: loc["nsi_keys"] if loc["nsi_keys"] is not None else []
        for loc in CONFIG["locations"]
    }
    for d in (nsi_registry, fema_registry):
        for key, value in d.items():
            registry[key].extend(value)
    return registry


def standardize_column_names(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Standardizes data columns using FEMA and NSI key registries. It maps the relevant columns from the input dataset to standardized column names based on the source of the data (e.g., structures, parks, transportation). For structure datasets, it uses the FEMA and NSI key registries to map the appropriate columns to 'RWF_desc', 'RWF_desc2', and 'Structure Type'. For park and transportation datasets, it directly maps specific columns to these standardized names.

    Parameters
    ----------
    df : pd.DataFrame
        The input dataset to be standardized.
    source : str
        The source of the dataset, used to determine the appropriate standardization.

    Returns
    -------
    pd.DataFrame
        The standardized dataset with renamed columns.
    """
    registry = _build_fema_nsi_key_registry()
    if 'structures' in source.lower():
        c1 = 'OCC_CLS'
        c2 = 'PRIM_OCC'
    elif source == 'NSI':
        c1 = 'st_damcat'
        c2 = 'occtype'
    elif 'park' in source.lower():
        c1 = 'FEATTYPE'
        df['RWF_desc'] = df[c1]
        df['RWF_desc2'] = 'Park'
        df['Structure Type'] = 'Park'
        return df
    elif source.lower() == 'Primary_Roads'.lower():
        c1 = 'PRETYPEABRV'
        df['RWF_desc'] = df[c1]
        df['RWF_desc2'] = 'PrimRd'
        df['Structure Type'] = 'Primary Roads'
        return df
    elif source.lower() == 'Secondary_Roads_72_1k_scale'.lower():
        c1 = 'PRETYPEABRV'
        df['RWF_desc'] = df[c1]
        df['RWF_desc2'] = 'SecRd'
        df['Structure Type'] = 'Secondary Roads'
        return df
    elif source.lower() == 'Local_Roads'.lower():
        c1 = 'PRETYPEABRV'
        df['RWF_desc'] = df[c1]
        df['RWF_desc2'] = 'LocalRd'
        df['Structure Type'] = 'Local Roads'
        return df  
    else:
        return None
    df['RWF_desc'] = df[c2].map(lambda x: next((k for k, v in registry.items() if x in v), "None"))
    df['RWF_desc2'] = df[c1].map(lambda x: next((k for k, v in registry.items() if x in v), "None"))
    df['Structure Type'] = df['RWF_desc']
    df['Structure Type'] = df['Structure Type'].mask(df['Structure Type'].isin(["None", "Unclassified"]), df['RWF_desc2'])
    return df
