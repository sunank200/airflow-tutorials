AIRFLOW_VERSION=2.0.0
PYTHON_VERSION=3.7

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# install apache-airflow with constraints
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# install extras 
pip install "apache-airflow[postgres,google,providers-amazon]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"