<div>
<h1>SpaceXPipeline</h1>
<p>Welcome to the repository for the SpaceX Data Pipeline project for Bear Cognition! See below for operating procedures, pipeline architecture, data partitioning strategies, AWS resourece setup, and a report on SpaceX data insights!</p>
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
    <li>Login to <a href='https://us-east-2.console.aws.amazon.com/console/home?nc2=h_ct&region=us-east-2&src=header-signin#'>Amazon AWS</a> using the credentials attached to the project submission.</li>
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
<p>NOTE: If Prefect flow runs are desired, please contact patrickjodonnell@comcast.net!</p>
<ol>
    <li>api_interaction task</li>
    <ul>
        <li>This task asynchronously calls the <a href='https://github.com/r-spacex/SpaceX-API'>SpaceX API</a> and pulls required data into the application.</li>
    </ul>
    <li>data_extraction task</li>
    <ul>
        <li>This task loops through each JSON object retrieved from the API, flattens it, and adds the flattened data to a global list for processing.</li>
    </ul>
    <li>data_processing task</li>
    <ul>
        <li>This task first cleans the retrieved data by replacing all empty data cells, transforming the JSON object into a Pandas Dataframe, and removing all empty columns in the Dataframe. Next, the task calculates the year associated with each Dataframe row, and appends a 'years' column to the Dataframe. Finally, this task partitions the data into seperate Pandas Dataframes based on the associated year.</li>
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
<div>
<h2>Data Partitioning Strategy</h2>
<p>This section will provide an overview of the data partitioning strategy.</p>
</br>
<p>For this pipeline, I chose to initially store the retrieved JSON data as Pandas Dataframes. This storage option allowed for easy data cleaning and partitioning. Using a few simple commands, I was able to seperate the Dataframe of SpaceX data into seperate Dataframes and store them in a dictionary of Dataframes with their associated year as the key. This partitioning strategy allowed me to easily locate and view each piece of data. Additionally, this partitioning method allowed me to easily transfer the data from Dataframes to .parquet files using the pyarrow library. Finally, I decided to include a yearly folder structure to hold all .parquet files for more efficient data separation.</p>
</div>
<div>
<h2>AWS Resource Setup</h2>
<p>This section will provide an overview of the setup of each AWS entity.</p>
<p>NOTE: For simplicity, S3 and RDS were given public access as they did not contain confidential data.</p>
<ol>
    <li>AWS S3</li>
    <ol>
        <li>Navigate to the Amazon S3 Buckets page and select 'Create Bucket'.</li>
        <li>Enter a bucket name and deselect 'Block all public access'. Leave all other settings the same.</li>
        <li>A user role also needs to be set up to use this bucket. Navigate to AWS IAM, select 'users' and select 'create user'. Enter the user's name and the following permissions: </li>
        <ul>
            <li>AmazonS3FullAccess</li>
            <li>AmazonRDSFullDataAccess</li>
            <li>Other accesses can be added as needed.</li>
        </ul>
    </ol>
    <li>AWS RDS</li>
    <ol>
        <li>Navigate to the Amazon RDS Databases page and select 'Create database'.</li>
        <li>This database can be customizable, but I made sure to select a MySQL database, free tier template, and yes to public access. I also chose a unique master password for protection.</li>
        <li>After the database was created, I edited the rules of the VPC security group. For simplicity, the inbound rules were set to accept connections for all traffic, HTTP, and All TCP. The outbound rules were also set to the same value. These rules allowed for easy connection to other AWS services.</li>
        <li>Finally, in the configuration tab of the database's page, I selected and changed the DB instance parameter group. Here, I chose to turn off the 'innodb_strict_mode' setting which restricts the amount of row data entering the database. This was essential for my database setup and required a reboot of the database after the change was made.</li>
    </ol>
    <li>AWS Glue Job</li>
    <ol>
        <li>First, navigate to the AWS Glue Connections page and select 'Create connection'. On this page, it was important to select the JDBC connection type, enter the correct JDBC URL, and enter the correct Database password. All other settings can remain as the default.</li>
        <li>After the connection to the database is created, I created an AWS Crawler to import the Schema of the MySQL database tables that I would be using (these tables were created using MySQL workbench SQL commands). Navigate the the Crawlers page and select 'Create Crawler'. Here, enter the Crawler name, and select the database connection for the data source. For the 'include path' field, I entered table-name/%. </li>
        <li>Before selecting a Crawler role, I had to again navigate to AWS IAM, select roles, and create a role for AWS Glue. The permissions attached to the role were: </li>
        <ul>
            <li>AWSGlueServiceRole</li>
            <li>AmazonS3FullAccess</li>
            <li>AmazonRDSFullAccess</li>
            <li>AmazonRDSFullDataAccess</li>
            <li>Any other desired roles</li>
        </ul>
        <li>Back on the crawler setup, I selected this role, selected the target output databse, and chose to run the crawler on demand.</li>
        <li>Once the connection was made and the crawler was constructed and successfully run, I created the AWS Glue Job. Navigate to ETL Jobs and choose the desired option to create a job. I chose to do so visually since this was a simple data load. As the source of the job I selected Amazon S3, for the transforms I selected Change Schema, and for the target I chose MySQL. In the source, I made sure to select the correct Bucket and to set the data type to parquet. For the target I made sure to point the job to the correct database and table.</li>
        <li>Once these features were set up and saved, the Glue Job was run and data was loaded from the S3 bucket to the RDS database and the schema was preserved.</li>
    </ol>
<ol>
</div>
<div>
<h2>SpaceX Data Insights</h2>
<p>This section will provide insights into the SpaceX Data. There is a plethora of information that can be pulled from this dataset, but below is a report of four interesting insights gained from the data using SQL queries.</p>
<ol>
    <li>Launches per Year</li>
    <p>Using the SQL query: SELECT years, Count(*) FROM xdata.finaldata GROUP BY years; the following table was generated which shows that SpaceX has been increasing their launch prequency since 2006.</p>
    <img src="https://github.com/PatrickJODonnell/SpaceXPipeline/assets/130483105/6f3ba6b3-e1bb-4714-86a7-824c5524c56b">
    <li>Number of Successful Launches per Year</li>
    <p>Using the SQL query: SELECT years, count(success) FROM xdata.finaldata WHERE success = "true" GROUP BY years; the following table was generated. This data shows a healthy increase in launch successes from SpaceX as time progresses.</p>
    <img src="https://github.com/PatrickJODonnell/SpaceXPipeline/assets/130483105/a3bc356e-6d09-4088-b793-d08415bca9e8">
    <li>Average Cost of a Rocket Launch per Year</li>
    <p>Using the SQL query: SELECT years, avg(rocket_cost_per_launch) FROM xdata.finaldata GROUP BY years; the following table was generated. This table illustrates how rocket launches were less expensive in the beginning of the launch data and jumped to an average of $50 million in 2010.</p>
    <img src="https://github.com/PatrickJODonnell/SpaceXPipeline/assets/130483105/4e848c1e-0a79-49b8-ba21-bc2d393ae1c9">
    <li>Number of Launches with Payloads</li>
    <p>Using the SQL query: SELECT entry_id, years FROM xdata.finaldata WHERE payloads_0_dragon_capsule != "No Data"; the following table was generated. This table lists the launch id and year of each mission that carried a payload.</p>
    <img src="https://github.com/PatrickJODonnell/SpaceXPipeline/assets/130483105/232adbff-da35-4ae7-9b3c-44356ec81249">
</ol>
</div>


