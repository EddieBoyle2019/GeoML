# Utilities required for Sentinel Hub API
# Murray Cutforth Oct 2023
# Eddie Boyle Dec 2023 - Mar 2024

import json
import math
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import folium
from sentinelhub import SHConfig, BBox, CRS, bbox_to_dimensions, SentinelHubRequest, DataCollection, MosaickingOrder, MimeType
from streamlit_folium import st_folium
from typing import Any, Optional, Tuple

def plot_map_with_image(
        image_true: np.ndarray,
        image_scm: np.ndarray,
        bbox: list[list, list],  # SW, NE points in [lon, lat] ordering
        centre: list,  # Centre point as [lon, lat] ordering
        alpha: float = 1.0,
        name: str = None
):
    attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    tiles = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'

    m = folium.Map(
        location=[centre[1], centre[0]],  # Folium works in (lat, lon) so we need to switch
        tiles=tiles,
        attr=attr,
        zoom_control=True,
        control_scale=True,
    )

    folium.Marker(
        location=centre[::-1],
        tooltip=f"{name} snow patch; Lat/Long: {centre[1].2f, centre[0].2f}",
        icon=folium.Icon(),
    ).add_to(m)

    bbox = [x[::-1] for x in bbox]  # Convert from (lon, lat) to (lat, lon) for folium

    sw_point = bbox[0]
    ne_point = bbox[1]
    m.fit_bounds([sw_point, ne_point])  # SW, NE corners in (lat, lon) form

    folium.raster_layers.ImageOverlay(
        name="Sentinel-2 true colour (RGB) imagery",
        image=image_true,
        bounds=bbox,
        opacity=alpha,
        mercator_project=True,
    ).add_to(m)

    folium.raster_layers.ImageOverlay(
        name="Sentinel-2 scene classification map (snow/ice)",
        image=image_scm,
        bounds=bbox,
        opacity=alpha,
        mercator_project=True,
        show=False,
    ).add_to(m)

    kw = {
        "color": "blue",
        "line_cap": "round",
        "fill": False,
        "weight": 1,
        "popup": "Sentinel-2 image",
    }
    folium.Rectangle(
        bounds=[sw_point, ne_point],
        line_join="round",
        dash_array="5, 5",
        **kw,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st_folium(m, height=600, width=600, use_container_width=True)


def read_bbox_geojson(data: dict) -> dict[str, list]:
    # Parse the JSON data into a dictionary

    name_coordinates = {}

    # Iterate through features and extract name and SW / NE coordinates
    for feature in data['features']:
        name = feature['properties']['name']
        coordinate_list = feature["geometry"]["coordinates"][0]
        lon_list = [x[0] for x in coordinate_list]
        lat_list = [x[1] for x in coordinate_list]
        sw = [min(lon_list), min(lat_list)]
        ne = [max(lon_list), max(lat_list)]
        coordinates = [sw, ne]
        name_coordinates[name] = coordinates

    return name_coordinates


def read_point_geojson(data: dict) -> dict[str, list[float]]:
    # Parse the JSON data into a dictionary

    name_coordinates = {}

    # Iterate through features and extract name and top left / bottom right coordinates
    for feature in data['features']:
        name = feature['properties']['name']
        coordinates = feature['geometry']['coordinates']
        name_coordinates[name] = coordinates

    return name_coordinates


def get_coords_from_sel(sel, name_bbox_coords) -> tuple[float, float, float, float]:
    assert sel in name_bbox_coords
    result = [
        name_bbox_coords[sel][0][0],
        name_bbox_coords[sel][0][1],
        name_bbox_coords[sel][1][0],
        name_bbox_coords[sel][1][1],
    ]
    return tuple(result)


@st.cache_data
def request_sentinel_image(gcm_coords_wgs84: tuple, config: SHConfig, start_date, end_date) -> np.ndarray:
    resolution = 10
    gcm_bbox = BBox(bbox=gcm_coords_wgs84, crs=CRS.WGS84)
    gcm_size = bbox_to_dimensions(gcm_bbox, resolution=resolution)

    # Evalscript to select the RGB (B04, B03, B02) Sentinel-2 L1C bands.
    evalscript_true_color = """
        //VERSION=3
        
        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }
        
        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C.define_from(
                    "s2l1c", service_url=config.sh_base_url
                ),
                time_interval=(start_date, end_date),
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=gcm_bbox,
        size=gcm_size,
        config=config,
    )

    return request_true_color.get_data()[0]


@st.cache_data
def request_sentinel_scm(gcm_coords_wgs84: tuple, config: SHConfig, start_date, end_date) -> np.ndarray:
    resolution = 10
    gcm_bbox = BBox(bbox=gcm_coords_wgs84, crs=CRS.WGS84)
    gcm_size = bbox_to_dimensions(gcm_bbox, resolution=resolution)

    # Evalscript to select the Scene Classification Map (SCL) Sentinel-2 L2A.
    evalscript_scm = """
        //VERSION=3

        function RGBToColor (r, g, b, dataMask){
            return [r/255, g/255, b/255, dataMask];
        }

        function setup() {
            return {
                input: ["SCL", "dataMask"],
                output: { bands: 4 }
            };
        }

        function evaluatePixel(samples) {
            const SCL=samples.SCL;
            switch (SCL) {
                // Make all types transparent except snow/ice 
                // No Data (Missing data) (black)    
                //case 0: return RGBToColor (0, 0, 0, samples.dataMask);
                case 0: return RGBToColor (0, 0, 0, 0);
                // Saturated or defective pixel (red)   
                //case 1: return RGBToColor (255, 0, 0, samples.dataMask);
                case 1: return RGBToColor (255, 0, 0, 0);
                // Dark features / Shadows (very dark grey)
                //case 2: return RGBToColor (47,  47,  47, samples.dataMask);
                case 2: return RGBToColor (47,  47,  47, 0);
                // Cloud shadows (dark brown)
                //case 3: return RGBToColor (100, 50, 0, samples.dataMask);
                case 3: return RGBToColor (100, 50, 0, 0);
                // Vegetation (green)
                //case 4: return RGBToColor (0, 160, 0, samples.dataMask);
                case 4: return RGBToColor (0, 160, 0, 0);
                // Not-vegetated (dark yellow)
                //case 5: return RGBToColor (255, 230, 90, samples.dataMask);
                case 5: return RGBToColor (255, 230, 90, 0);
                // Water (dark and bright) (blue)
                //case 6: return RGBToColor (0, 0, 255, samples.dataMask);
                case 6: return RGBToColor (0, 0, 255, 0);
                // Unclassified (dark grey)
                //case 7: return RGBToColor (128, 128, 128, samples.dataMask);
                case 7: return RGBToColor (128, 128, 128, 0);
                // Cloud medium probability (grey)
                //case 8: return RGBToColor (192, 192, 192, samples.dataMask);
                case 8: return RGBToColor (192, 192, 192, 0);
                // Cloud high probability (white)
                //case 9: return RGBToColor (255, 255, 255, samples.dataMask);
                case 9: return RGBToColor (255, 255, 255, 0);
                // Thin cirrus (very bright blue)
                //case 10: return RGBToColor (100, 200, 255, samples.dataMask);
                case 10: return RGBToColor (100, 200, 255, 0);
                // Snow or ice (very bright pink)
                //case 11: return RGBToColor (255, 150, 255, samples.dataMask);
                case 11: return RGBToColor (255, 150, 255, 1);
                //default : return RGBToColor (0, 0, 0, samples.dataMask); 
                default : return RGBToColor (0, 0, 0, 0); 
            }
        }
    """

    request_scm = SentinelHubRequest(
        evalscript=evalscript_scm,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A.define_from(
                    name = "s2a", service_url=config.sh_base_url
                ),
                time_interval=(start_date, end_date),
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=gcm_bbox,
        size=gcm_size,
        config=config,
    )

    return request_scm.get_data()[0]