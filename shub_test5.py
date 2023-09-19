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

st.title('Sentinel Hub test')

config = SHConfig()
config.sh_client_id = "sh-7fb853f3-35ce-4bc5-b0b3-6448189bf065"
config.sh_client_secret = "AN9b1KMl3r9xypCd8bJfBGrbtZvU9UEj"
#config.sh_client_id = st.text_input("Enter your SentinelHub client id", type="password")
#config.sh_client_secret = st.text_input("Enter your SentinelHub client secret", type="password")
#config.sh_client_id = getpass.getpass("Enter your SentinelHub client id")
#config.sh_client_secret = getpass.getpass("Enter your SentinelHub client secret")
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"

resolution = 10
gcm_coords_wgs84 = (-3.76, 57.06, -3.72, 57.077)
gcm_bbox = BBox(bbox=gcm_coords_wgs84, crs=CRS.WGS84)
gcm_size = bbox_to_dimensions(gcm_bbox, resolution=resolution)

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
            time_interval=("2020-06-01", "2020-06-30"),
            mosaicking_order=MosaickingOrder.LEAST_CC,
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=gcm_bbox,
    size=gcm_size,
    config=config,
)

if config.sh_client_id and config.sh_client_secret:
    true_color_imgs = request_true_color.get_data()
    image = true_color_imgs[0]
    plot_image(image, factor=3.5 / 255, clip_range=(0, 1))   

#print(f"Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.")
#print(f"Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}")
#st.write ('Returned data is of type = ', type(true_color_imgs))
#st.write (' and length = ', len(true_color_imgs))
#st.write (' Single element in the list is of type = ', type(true_color_imgs[-1]))
s##t.write (' and has shape = ', true_color_imgs[-1].shape)



#print(f"Image type: {image.dtype}")
#st.write ('Image Type: ', image.dtype)


