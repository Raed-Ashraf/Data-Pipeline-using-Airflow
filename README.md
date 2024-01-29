# Data Pipeline using Apache Airflow: ServiceNow to PostgreSQL
This GitHub repository contains a data pipeline project built using Apache Airflow to extract data from the ServiceNow platform, specifically the "incidents" table, using its REST API. The extracted data is then parsed and transformed to map two fields, namely "Priority" and "State," from integers to strings based on a specific mapping list. Finally, the transformed data is loaded into a PostgreSQL database table. Docker is used to initiate and run the Airflow server on your local machine.

# Prerequisites
Before running this data pipeline, ensure that you have the following dependencies installed on your local machine:
- Python
- Docker
- Docker Compose

# Setup
1- 

# Project Structure
The project's directory structure is as follows:  
.  
├── dags  
│   └── snow-to-postgres.py  
├── logs  
├── plugins  
├── docker-compose.yml  
├── .env  
└── README.md  
- **dags**: Contains the DAG (Directed Acyclic Graph) file, snow-to-postgres.py, which defines the workflow of the data pipeline.
- **plugins**: Contains the plugin file, if exist, which defines the custom operators and hooks used in the pipeline.
- **logs**: Contains the logging file of each running DAG in Airflow server.
- **docker-compose.yaml**: Defines the Docker containers and services required for running Airflow and PostgreSQL.
- **.env**: An environment variables file that needs to be configured.
- **README.md**: This file.



