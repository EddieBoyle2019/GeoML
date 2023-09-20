# shub_api_snow.py
# Python script to retrieve image using Sentinel Hub API
# Requires sentinelhub Python package/virtual environment (https://sentinelhub-py.readthedocs.io/en/latest/)
# Requires OAuth client credentials to be configured in CDSE dashboard (https://shapps.dataspace.copernicus.eu/dashboard/)
# This code is adapted from https://sentinelhub-py.readthedocs.io/en/latest/examples/process_request.html
# Eddie Boyle Sep 2023

import datetime
import getpass
import streamlit as st
import matplotlib.pyplot as plt

from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)

from utils import plot_image

st.title('Sentinel Hub API - snowpatch image request')

# Credentials
config = SHConfig()
config.sh_client_id = st.text_input("Enter your SentinelHub client id", type="password")
config.sh_client_secret = st.text_input("Enter your SentinelHub client secret", type="password")
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"

# Setting image area - GCM
resolution = 10
gcm_coords_wgs84 = (-3.76, 57.06, -3.72, 57.077)
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

# PNG image from Jun 2020. Least cloud cover mosaicking used. Reflectance values in UINT8 format (values in 0-255 range).
request_true_color = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C.define_from(
                "s2l1c", service_url=config.sh_base_url
            ),
            time_interval=("2020-06-01", "2020-06-30"),
            mosaicking_order=MosaickingOrder.LEAST_CC,
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=gcm_bbox,
    size=gcm_size,
    config=config,
)

# Retrieve and display image
if config.sh_client_id and config.sh_client_secret:
    true_color_imgs = request_true_color.get_data()
    image = true_color_imgs[0]
    plot_image(image, factor=3.5 / 255, clip_range=(0, 1))