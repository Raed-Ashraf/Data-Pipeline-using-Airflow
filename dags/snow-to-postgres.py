from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import timedelta
import requests
import psycopg2

default_args = {
    'owner': 'raed',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    'snow-to-postgres',
    default_args=default_args,
    description = 'ServiceNow to Postgres database',
    schedule_interval = timedelta(days=1),  # Runs every 2 hours
)

def extract_data():
    url = 'https://dev201420.service-now.com/api/now/table/incident?sysparm_exclude_reference_link=false&sysparm_fields=sys_id%2Cnumber%2Cshort_description%2Ccaller_id.name%2Cpriority%2Cstate%2Cassigned_to.name'
    username = 'admin'
    password = '**Enter Password Here**'
    
    response = requests.get(url, auth=(username, password))
    snow_data = response.json()
    
    return snow_data

extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag
)

def parse_response(**context):

    # read the context from previous task
    response = context['ti'].xcom_pull(task_ids='extract_data')

    # Get the 'result' object from the response
    result = response.get('result', [])  
    parsed_data = []
    for item in result:
        parsed_item = {
            'sys_id': item.get('sys_id', ''),
            'number': item.get('number', ''),
            'short_description': item.get('short_description', ''),
            'caller_name': item.get('caller_id.name', ''),
            'state': item.get('state', ''),
            'priority': item.get('priority', ''),
            'assigned_to': item.get('assigned_to.name', '')
        }
        parsed_data.append(parsed_item)
    return parsed_data
 
parse_response_task = PythonOperator(
    task_id='parse_response',
    python_callable=parse_response,
    provide_context=True,
    dag=dag
)

def priority_state_mapping(**context):

    # read the context from previous task
    data = context['ti'].xcom_pull(task_ids='parse_response')   

    priority_mapping = {1: 'Critical', 2: 'Hight', 3: 'Moderate', 4: 'Low', 5: 'Planning'}
    state_mapping = {1: 'New', 2: 'In Progress', 3: 'On Hold', 7: 'Closed'}

    for row in data:

        # priority mapping
        if int(row['priority']) in priority_mapping:
            row['priority'] = priority_mapping[int(row['priority'])]

        # state mapping
        if int(row['state']) in state_mapping:
            row['state'] = state_mapping[int(row['state'])]

    return data 
 
priority_state_mapping_task = PythonOperator(
    task_id='priority_state_mapping',
    python_callable=priority_state_mapping,
    provide_context=True,
    dag=dag
)

def load_data_to_postgres(**context):

    # read the context from previous task
    data = context['ti'].xcom_pull(task_ids='priority_state_mapping')   
   
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host='10.218.121.82',
        port='5432',
        database='staging_import',
        user='etluser_import',
        password='**Enter Password Here**'
    )
    
    # Create a cursor
    cursor = conn.cursor()
    
    for row in data:
        # Define the SQL query with placeholders for parameters
        sql_query = "INSERT INTO incident (sys_id, number, short_description, caller_name, state, priority, assigned_to) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        # Define the values to be inserted
        values = (row['sys_id'], row['number'], row['short_description'], row['caller_name'], row['state'], row['priority'], row['assigned_to'])
    
        # Execute the SQL query
        cursor.execute(sql_query, values)

    # See the result of last query
    result = cursor.statusmessage

    # Commit the changes
    conn.commit()
    
    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return result

load_data_to_postgres_task = PythonOperator(
    task_id='load_data_to_postgres',
    python_callable=load_data_to_postgres,
    provide_context=True,
    dag=dag
)

# Define the task dependencies
extract_data_task >> parse_response_task >> priority_state_mapping_task >> load_data_to_postgres_task
