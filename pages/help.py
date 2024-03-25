import streamlit as st

multi = '''**What does this tool do?**

This tool is for exploring the appearance and location of well-known long-lasting snowpatches in the Scottish Highlands, using web maps and satellite data.

The tool uses data from the Copernicus Data Space Ecosystem (CDSE)(https://dataspace.copernicus.eu).

The tool enables satellite images to be retrieved for various locations of snowpatch areas in the Scottish Highlands. A satellite image corresponding to the location appears in a square window, overlaid on a map allowing the wider context of the satellite image within the Scottish highlands to be visualised.

It is recommended that a desktop computer or laptop with a keyboard is used for this tool.

**How can I use this tool?**

To use this tool, you first need to set up access, go to Appendix A at the bottom of this page for instructions about how to do this. 

Once done, enter the special authentication details at 'SentinelHub client id' and 'SentinelHub client secret' fields in the menu bar to the left of the tool.

**How do I control the tool?**

1. Date  
Change the date period used by using the 'Choose start date' and 'Choose end date' fields in the lefthand menu - good ones to try to see a good image are May 1 2023 - May 31 2023. 

2. Location  
Select different areas to investigate using the 'Choose a snowpatch' field. 

3. Transparency     
Alter the transparency of the satellite image using the 'Set opacity of overlay images' slider.

4. Map data  
Zoom in and out of the map using the icons at the top left of the map. Control the data displayed on the map using the icon at the top right of the map. You can control the display of two types of satellite data, 'Sentinel-2 true colour (RGB) imagery' and 'Sentinel-2 scene classification map (snow/ice)'. Technical information about this data is contained at Appendix B.

5. Snowpatch information  
Hover with a mouse on the blue marker in the centre of the map to see the name and coordinates of the selected snowpatch. 

**Appendix A**

Setting up access:

1. Register an account with CDSE by going to https://dataspace.copernicus.eu and clicking on the 'Register' button. Keep a note of the username and password.

2. Log into the CDSE dashboard at: https://shapps.dataspace.copernicus.eu/dashboard/ using this username and password. Follow these instructions (Registering OAuth client) to generate the special authentication details ('SentinelHub client id' and 'SentinelHub client secret') which are big long strings of characters, and keep a note of these details (this only needs to be done once):
https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Overview/Authentication.html#registering-oauth-client

3. Type in (or more easily, copy and paste) each string into the two corresponding fields in the menu bar to the left of the tool, pressing enter on your keyboard to input them into each field. If this works (it may take a few seconds to start up), you should see a map showing the area around An Riabhachan, with a square showing a satellite image laid over the centre of the map. This is the least cloudy image of the area available from the last month.

4. The purpose of this process is to give you a CDSE quota for accessing data, which resets every month and you shouldn't need to ever go over this for snowpatch observations using the tool.

**Appendix B**

CDSE satellite data:

1. Sentinel-2 true colour (RGB) imagery 

This uses data from the Sentinel 2 satellite to create a 'true colour' image corresponding what a human eye might see. An important thing to note is that this data is not a 'snapshot' taken on one particular day, rather it is a combination of data from the whole date range selected, using data from the least cloudy days, to generate the 'best' image of the area available. A narrow date range will enable a particular single date to be identified, but this increases the chance that there will be no data available due to 1) the satellite orbit was not over the area selected 2) the satellite was over the area at nightime 3) there was significant cloud cover during the date range selected.

Cloud cover is probably the single most important factor affecting satellite imagery of the Scottish Highlands and it can be difficult to find an image that shows snowpatches, particularly during the winter months. There can be only 1 day a month, or even none, when suitable imagery is available. Some work is underway to try and improve this using Machine Learning so that even imagery with clouds can be used.    

To get more control over accessing this satellite imagery, it is recommended to use the Copernicus Browser at: https://browser.dataspace.copernicus.eu.

2. Sentinel-2 scene classification map (snow/ice)

The Copernicus system uses a fairly sophisticated algorithm (details at: https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm-overview) that automatically identifies areas of snow and ice in the satellite imagery, and this can be used to identify snowpatches in the Scottish Highlands, which appear in the data on the map as purple areas when this option is selected. This algorithm is not perfect, and can miss some snowpatches smaller than 10m&sup2;. The work underway to use Machine Learning strategies may improve upon this algorithm.

'''

st.markdown(multi)