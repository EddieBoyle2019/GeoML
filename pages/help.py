import streamlit as st

multi = '''**What does this tool do?**

This tool is for exploring the appearance and location of well-known long-lasting snowpatches in the Scottish Highlands, using web maps and satellite data.

**How can I use it?**

To use it, you first need to set up some details:

1. In the menu bar to the left enter some special authentication details at 'SentinelHub client id' and 'SentinelHub client secret' fields. This is different from your Copernicus username and password.

2. These details can be obtained by logging into the the CDSE dashboard at: https://shapps.dataspace.copernicus.eu/dashboard/ and following these instructions (Registering OAuth client) to generate the security details which are big long strings of characters (this only needs to be done once):
https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Overview/Authentication.html#registering-oauth-client

3. Paste each string into the two fields and press enter on your keyboard to input them. If this works (it may take a few seconds to start up), you should see a map showing the area around An Riabhachan, with a square showing a satellite image laid over the centre of the map. This is the least cloudy image of the area available from the last month.

4. The purpose of this is to give you a quota for accessing data, which resets every month and you shouldn't need to ever go over this for snowpatch observations using the tool.
'''

st.markdown(multi)