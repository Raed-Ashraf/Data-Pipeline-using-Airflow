# Data Pipeline using Apache Airflow: ServiceNow to PostgreSQL
This GitHub repository contains a data pipeline project built using Apache Airflow to extract data from the ServiceNow platform, specifically the "incidents" table, using its REST API. The extracted data is then parsed and transformed to map two fields, namely "Priority" and "State," from integers to strings based on a specific mapping list. Finally, the transformed data is loaded into a PostgreSQL database table. Docker is used to initiate and run the Airflow server on your local machine.

# ServiceNow Platform Overview
The ServiceNow platform is a cloud-based IT service management (ITSM) and business process automation solution that helps organizations streamline their workflows and improve operational efficiency. It offers a wide range of integrated applications and modules that allow businesses to manage various processes, including incident management, problem management, change management, asset management, and more.

In the previous project, we utilized the ServiceNow platform to extract data from the "incidents" table using its REST API. The incidents table typically stores information about reported issues, problems, or disruptions in an organization's services or systems. By accessing this table via the ServiceNow REST API, we were able to retrieve the relevant data for our data pipeline.  
[See ServiceNow Incidents Table](https://github.com/Raed-Ashraf/Data-Pipeline-using-Airflow/issues/1#issue-2105297278)

ServiceNow provides a powerful and flexible REST API that allows developers to interact with the platform and retrieve data using standard HTTP methods. With the help of the ServiceNow API, we were able to authenticate and make requests to the platform to extract the necessary data from the incidents table.

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
5. Make sure the the DAG pyhton file snow-to-postgres.py is in the dags folder.
6. Initialize the Airflow environment using the following bash command.
  
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

# DAG Description
The snow-to-postgres DAG orchestrates the following tasks:
- **Extract Data**: This task makes a request to the ServiceNow API to extract data from the "incidents" table. It retrieves the relevant fields and records from the incidents table and passes the data to the next task in the pipeline.  
- **Parse Response**: This task receives the extracted data from the previous task and performs parsing operation to required field names.  
- **Priority State Mapping**: This task receives the extracted data from the previous task and performs transformation operations. Specifically, it maps the "Priority" and "State" fields from integers such as (1, 2, 3, and so on) to strings like (Critical, Hight, Moderate, and so on) based on a predefined mapping list.
- **Load Data to Postgres**: This task is responsible for loading the transformed data into a PostgreSQL database table. It establishes a connection to the PostgreSQL database and inserts the transformed data into the appropriate table.

