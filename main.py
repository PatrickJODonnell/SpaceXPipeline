# Import statements
import asyncio
import aiohttp
from pprint import pprint
from numpy import NaN
import pandas as pd
from flatten_json import flatten
import pyarrow as pa
import pyarrow.parquet as pq
import os
import boto3
from dotenv import load_dotenv
import json

# Loading environmental variables
load_dotenv()

# Initializing flattened launch list as global for manipulaton by data processor
flat_launch_list = [] 

async def apiInteraction():
    """
    Function that fetches data from the provided API URL
    """
    # Setting up API call variables
    base_url = 'https://api.spacexdata.com'
    route = '/v5/launches/query'
    query = {
        "query": {},
        "options": {
            "select":['date_utc', 'rocket', 'payloads', 'success'],
            "pagination": False, 
            "populate": ["payloads", "rocket"],
        }
    }
    # Calling SpaceX API with query options so we only pull data that we want
    async with aiohttp.ClientSession() as session:
        async with session.post(base_url + route, headers={"Conetent-Type": "application/json"}, json = query) as response:
            raw_response = await response.json()
            response = raw_response['docs']
            return(response)
        
def dataExtraction(launch):
    """
    Function that pulls all data from each launch that it is passed as adds it to a launch list
    """
    # Flattening JSON object and adding it to our list
    flattened_launch = flatten(launch)
    flat_launch_list.append(flattened_launch)

def dataProcessing():
    """
    Function that will turn take each input of the flattened_launch_list and enter it into a pandas df.
    Will then clean data of any empty cells and convert boolean vals to more meaningful vals.
    Finally, the df will be split by launch year.
    """
    # Removing emptry lists from entries
    for entry in flat_launch_list:
        for k in entry:
            if entry[k] == []:
                entry[k] = NaN
    # Adding launch list to a df
    df = pd.DataFrame(flat_launch_list)
    # Cleaning data of any NaN or None types and dropping meaninless columns (columns with No Data)
    df = df.dropna(axis=1, how='all')
    df.fillna('No Data', inplace = True)

    # Determining list of launch years and adding a year column to df
    launch_years = []
    launch_col = []
    for date in df['date_utc']:
        year = date.split('-')[0]
        launch_col.append(year)
        if year not in launch_years:
            launch_years.append(year)
    df.insert(0, "year", launch_col, True)
    # Splitting pandas df into multiple based on launch year
    split_data = {}
    for year in launch_years:
        split_data[year] = df[df['year'] == year]
    # Returning the dictionary of data
    return split_data
        
async def parquetConversion(data, split_data):
    """
    Async function for converting the seperated Dataframes into seperate parquet files 
    """
    # Creating year folders
    if ('SpaceXPipeline' not in os.getcwd()):
        os.chdir('./BearCognition/SpaceXPipeline')
        path = f'./spacex-data/{data}'
        if not os.path.exists(path):
            os.mkdir(path)
    # Converting all df columns to strings for parquet file
    for col in split_data[data]:
        split_data[data][col] = split_data[data][col].astype("string")
    # Creating parquet file in newly created folder
    table = pa.Table.from_pandas(split_data[data].astype(str))
    pq.write_table(table, f'./spacex-data/{data}/launch_data_{data}.parquet')

async def uploadToS3(data):
    """
    Function for uploading the parquet files to AWS S3
    """
    # Getting to the correct directory
    if ('SpaceXPipeline' not in os.getcwd()):
        os.chdir('./BearCognition/SpaceXPipeline')
    # Setting up connection to S3 client and bucket information
    s3 = boto3.resource('s3', 
                        region_name = 'us-east-2',
                        aws_access_key_id = os.environ.get("ACCESS_KEY_ID"),
                        aws_secret_access_key = os.environ.get("SECRET_ACCESS_KEY"))
    s3.Bucket("spacexpipeline").put_object(
        Key = f'spacex-data/year={data}/launch_data_{data}.parquet',
        Body = open(f'./spacex-data/{data}/launch_data_{data}.parquet', 'rb')
    )

if __name__ == "__main__":
    """
    Running if Python file is running natively 
    """
    # Calling the fetchData function
    print('Beginning API calls')
    try:
        response = asyncio.run(apiInteraction())
        print('API call passed')
    except Exception as error:
        print('API call failed')
    # Looping through the response and sending each launch to the data extractor
    print('Beginning data extraction')
    try:
        for launch in response:
            dataExtraction(launch)
        print('Data extraction passed')
    except Exception as error:
        print('Data extraction failed: ' + error)
    # Running the dataProcessesor
    print('Beginning data processing')
    try:
        split_data = dataProcessing()
        print('Data processing passed')
    except Exception as error:
        print('Data processing failed: ' + error)
    # Running the parquet format converter
    print('Beginning conversion to parquet format')
    try:
        for data in split_data:
            asyncio.run(parquetConversion(data, split_data))
        print('Parquet formatting passed')
    except Exception as error:
        print('Parquet formatting failed: ' + error)
    # Running the uploadToS3 functuon
    print('Beginning file upload to AWS S3')
    try:
        for data in split_data:
            asyncio.run(uploadToS3(data))
        print('File upload passed')
    except Exception as error:
        print('File upload failed: ' + error)

