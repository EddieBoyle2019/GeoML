#Python script to retrieve image using Sentinel Hub API
#Requires sentinelhub Python package/virtual environment (https://sentinelhub-py.readthedocs.io/en/latest/)
#Requires OAuth client credentials to be configured in CDSE dashboard (https://shapps.dataspace.copernicus.eu/dashboard/)
#Eddie Boyle Sep 2023

import datetime
import getpass

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

#run this if credentials have been saved 
#config = SHConfig("cdse")

config = SHConfig()
config.sh_client_id = getpass.getpass("Enter your SentinelHub client id")
config.sh_client_secret = getpass.getpass("Enter your SentinelHub client secret")
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"

#save credentials to .config/sentinelhub/config.toml
#config.save("cdse")

#Bounding box of GCM, image parameters
resolution = 10
gcm_coords_wgs84 = (-3.76, 57.06, -3.72, 57.077)
gcm_bbox = BBox(bbox=gcm_coords_wgs84, crs=CRS.WGS84)
gcm_size = bbox_to_dimensions(gcm_bbox, resolution=resolution)

#The Sentinel Hub API requires a JavaScript custom script
#RGB (B04, B03, B02) Sentinel-2 L1C bands
#Reflectance values in UINT8 format (values in 0-255 range)
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

#API request
#Month long interval, order the images w.r.t. the cloud coverage on the tile level
#True color (PNG)
request_true_color = SentinelHubRequest(
    data_folder="test1_dir",
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

#Data saved to local disk
request_true_color.save_data()