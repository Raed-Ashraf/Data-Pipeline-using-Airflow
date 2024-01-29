# Data Pipeline using Apache Airflow: ServiceNow to PostgreSQL
This GitHub repository contains a data pipeline project built using Apache Airflow to extract data from the ServiceNow platform, specifically the "incidents" table, using its REST API. The extracted data is then parsed and transformed to map two fields, namely "Priority" and "State," from integers to strings based on a specific mapping list. Finally, the transformed data is loaded into a PostgreSQL database table. Docker is used to initiate and run the Airflow server on your local machine.

# Prerequisites
Before running this data pipeline, ensure that you have the following dependencies installed on your local machine:
- Python
- Docker
- Docker Compose

# Setup
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create Folders needed by Airflow (dags, logs, plugins) using the following bash command.  
  
    `mkdir ./dags ./plugins ./logs`
4. Create the env file that contains the needed environment variables using the following bash command.  
  
    `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env`
5. Initialize the Airflow environment using the following bash command.
  
    `docker-compose up airflow-init`
  - **"docker-compose up"**: This command starts the services defined in the docker-compose.yml file.
  - **"airflow-init"**: This is a command specific to the Airflow image in the docker-compose file, used to initialize the Airflow metadata database and create the necessary tables and default user.
4. Start the Airflow server with Docker Compose using the following bash command.  
  
    `docker-compose up`   
  The Airflow UI will be accessible at http://localhost:8080.  
5. In the Airflow UI, enable the snow-to-postgres DAG.
6. Trigger the DAG manually or wait for the scheduled interval to start the data pipeline.
7. Monitor the progress and logs in the Airflow UI.
8. Once the pipeline finishes successfully, the transformed data will be loaded into the PostgreSQL database table.

# Project Structure
The project's directory structure is as follows:  
.  
├── dags  
│   └── snow-to-postgres.py  
├── logs  
├── plugins  
├── docker-compose.yaml  
├── .env  
└── README.md  
- **dags**: Contains the DAG (Directed Acyclic Graph) file, snow-to-postgres.py, which defines the workflow of the data pipeline.
- **plugins**: Contains the plugin file, if exist, which defines the custom operators and hooks used in the pipeline.
- **logs**: Contains the logging file of each running DAG in Airflow server.
- **docker-compose.yaml**: Defines the Docker containers and services required for running Airflow and PostgreSQL.
- **.env**: An environment variables file that needs to be configured.
- **README.md**: This file.



