# BTC/USD ETL

## Description
This project consists of a basic data pipeline that ingests several years worth of Bitcoin trading data into a database. The technologies used are Docker, Python (Polars, Pandas), and PostgreSQL.

## Table of Contents
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [More details](#more-details)
- [Possible improvements](#possible-improvements)

## Installation Instructions
1. Clone this repo to a local directory.
2. Run Docker Desktop.
3. `cd` into the project directory.
4. Run `docker compose up`.

## Usage
Once the code finishes running, the data will be available under table `market_data.btcusd`. It consists of the following columns:

`date_time`
`open_price`
`high_price`
`low_price`
`close_price`
`volume_btc`
`volume_usd`
`weighted_price`

This data can be queried by running `docker ps`, in order to grab the ID of the container that is running postgres. With that in hand, run `docker exec -it <container_id> psql -U <postgres_user> <postgres_database>`, which give us access to the database. This project uses a volume to make the data persistent, so it won't be erase if the container is stopped. 

We can then run many different queries, such as

```
SELECT *
FROM market_data.btcusd
WHERE extract(year from date_time) = 2019;
```

### Scheduling 

There are many different ways to schedule the execution of the code. For this particular project, I used Windows Task Scheduler. Here are the steps that I followed:

1. Create a new task called `BTC/USD ETL Scheduling`.
2. Scheduled it to run `daily`. This works because new files always arrive chronologically.
3. In `actions`, configure it to open Powershell, specifing the command `docker compose up`, and the path to the project folder. If postgres is active, this will only start the python script.
4. Save.

## More details

Docker and PostgreSQL were chosen due to their ease of use, and large community. PostgreSQL is ACID compliant, so it ensures data integrity and efficient retrieval. Docker simplifies dependency management, isolates the application from the host system, and ensures that the ETL pipeline runs reliably.

Polars is able to read data from the many .csv files available in the dataset folder very efficiently (which is one of the main challenges in this project), and Pandas is used due to its easy connectivity to PostgreSQL.

The `date_time` column combines the date and the time in a single column, and we have made the decision of omitting rows with only null values. When the code runs, it queries PostgreSQL to look for existing data, in order to only ingest new information.

## Possible improvements

### 1. Secrets handling

All secrets and environment variables are stored in a plain `config.py`, which would never be suitable for an actual application in production. One possible solution would be using [secrets in Docker Compose][def4]

### 2. Implementing a staging folder 

This project is structured in a way that new files always arrive in the `dataset` folder, but they are never deleted. This means the code always has to read many years of data, instead of just reading what is new. In the future, I could set up a process that deletes/moves the current contents of the folder once the process finishes running.

### 3. Adding more tests and data quality checks

This project has basic data validation in `data_reader.py`. The code checks if the data has all necessary columns, and if they are of the correct datatypes. In the future, I could potentially add testing to the individual functions, and add more data quality checks (such as anomaly detection)

### 4. Scheduling

The proposed scheduling solution is very barebones. One solution could be [setting up an Airflow instance][def], which has a [FileSensor][def2] solution. Meaning, it would be possible to trigger the execution of the code when a new file arrives, instead of running it in a particular time of the day. It would also be possible to modify the code in a way that it only targets the new file.

### 5. Different architecture 

Another possibility would be developing this project using AWS services. The code could be deployed in an AWS Lambda function, that would listen for [new files arriving in S3][def3]. The table `market_data.btcusd` could be defined using AWS Glue, and it could be queried using AWS Athena.

[def]: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
[def2]: https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/file.html
[def3]: https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
[def4]: https://docs.docker.com/compose/use-secrets/