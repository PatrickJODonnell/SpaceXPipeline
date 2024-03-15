<div>
<h1>SpaceXPipeline</h1>
<p>Welcome to the repository for the SpaceX Data Pipeline project for Bear Cognition! See below for operating procedures, pipeline architecture, data partitioning strategies, and a report on SpaceX data insights!</p>
</div>
<div>
<h2>Operating procedures</h2>
<p>This section will describe how to set up and execute the SpaceX ETL pipeline.</p>
<h3>Python</h3>
<ol>
    <li>git clone the <a href='https://github.com/PatrickJODonnell/SpaceXPipeline'>SpaceXData repository</a> to a directory on your local system.</li>
    <li>In your terminal, cd to the SpaceXPipeline repository.</li>
    <li>Add a file named ".env" to this repository. Within this file, enter the environmental variables attached to the project submission.</li>
    <li>Run the following command in your terminal: pip install -r requirments.txt</li>
    <li>Run the main.py file</li>
    <p>NOTE: Your local environment must be set up with Prefect before running main.py. To set up prefect, follow steps one and two in the following <a href='https://docs.prefect.io/latest/getting-started/quickstart/'>instructions</a>.</p>
</ol>
<h3>AWS</h3>
<ol>
    <li>Login to <a href='https://us-east-2.console.aws.amazon.com/console/home?nc2=h_ct&region=us-east-2&src=header-signin#'>Amazon AWS</a> using the credentials attached to the project submision.</li>
    <li>See the following links to view AWS entites</li>
    <ol>
        <li><a href='https://us-east-2.console.aws.amazon.com/s3/buckets/spacexpipeline?region=us-east-2&bucketType=general&tab=objects'>S3 Bucket: spacexpipeline</a></li>
        <li><a href='https://us-east-2.console.aws.amazon.com/rds/home?region=us-east-2#database:id=dbspacex;is-cluster=false'>RDS MySQL Database: dbspacex</a></li>
        <li><a href='https://us-east-2.console.aws.amazon.com/gluestudio/home?region=us-east-2#/editor/job/xdatajob/graph'>Glue Job: xdatajob</a></li>
        <ul>
            <li>To load data from the S3 Bucket to the MySQL database, select "run" on the xdatajob Glue Job.</li>
        </ul>
        <li><a href='https://us-east-2.console.aws.amazon.com/glue/home?region=us-east-2#/v2/data-catalog/crawlers/view/spacexpipelinecrawler'>Glue Crawler: spacexpipelinecrawler</a></li>
    </ol>
<ol>
</div>
<div>
<h2>Pipeline Architecture</h2>
<p>This section will provide brief overviews of each element in the main flow of the ETL pipeline.</p>
<ol>
    <li>api_interaction task</li>
    <ul>
        <li>This task asynchronously calls the <a href='https://github.com/r-spacex/SpaceX-API'>SpaceX API</a> and pulls required data into the application.</li>
    </ul>
    <li>data_extraction task</li>
    <ul>
        <li>This task loops through each json object retrieved from the API, flattens it, and adds the flattened data to a global list for processing.</li>
    </ul>
    <li>data_processing task</li>
    <ul>
        <li>This task first cleans the retrieved data by replacing all empty data cells, transforming the json object into a Pandas Dataframe, and removing all empty columns in the Dataframe. Next, the task calculates the year associated with each Dataframe row, and appends a 'years' column to the Dataframe. Finally, this task partitions the data into seperate Pandas Dataframes based on the associated year.</li>
    </ul>
    <li>parquet_conversion task</li>
    <ul>
        <li>This task loops through all Dataframes, converts each Dataframe into a .parquet file, and stores this file in a created folder based on the data's associated year.</li>
    </ul>
    <li>upload_to_s3 task</li>
    <ul>
        <li>This task uses the boto3 library to upload the .parquet files and their folder structure to the connected AWS 3 Bucket.</li>
    </ul>
    <li>AWS Glue Job</li>
    <ul>
        <li>Once the data has been uploaded to S3, the AWS Glue job works with the AWS Glue Crawler to transfer the yearly data from the S3 bucket to the AWS RDS MySQL Database.</li>
    </ul>
<ol>
</div>


