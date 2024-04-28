
# YOUTUBE DATA HARVESTING AND WAREHOUSING

The objective of the project is to get details of youtube channels like videodetails,commentdetails,channeldetails,playlistdetails with the use of streamlit in a table format.


## API Reference

#### Get all items

```https://developers.google.com/youtube/v3
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | "AIzaSyAs-6vWveOKwzrzbxGacCNnpOWTtDJ9lbE" |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| channel_details      | dictionary |get channel items |    



## Documentation

[Documentation](https://linktodocumentation)

START:
   The channelid is taken from youtube and entered in streamlit app and press the upload button .This uploads the data into a sql table.
OUTPUT:
    The output is either already exists if the channel details are already in the sql table or uploaded successfully if the channel details are not in sql table.
VIEW TABLE DETAILS:
    There are four tables in the sql database namely channeltable,playlisttable,videostable,commentstable.
OUTPUT:
    These tables can be viewed by clicking the name on streamlit.
GET RESULTS TABLE FOR QUERIES:
    By clicking on the dropdown in streamlit select the query for which answer has to be seen.
OUTPUT:
    The answer to every query is viewed in streamlit in the form of a table
## Environment Variables

PANDAS,
SQL-CONNECTOR-PYTHON,
ISODATE,
SQLALCHEMY


## Deployment

streamlit run streamlityoutube.py





## Features

- Error free
- Fullscreen mode
- Cross platform

