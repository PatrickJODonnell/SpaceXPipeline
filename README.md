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
    </ol>
<ol>
</div>


