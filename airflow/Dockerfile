FROM apache/airflow:2.8.4-python3.10

# Es buena práctica asegurar que somos el usuario airflow para el pip install
USER airflow

# Copiamos el archivo al HOME del usuario airflow para evitar líos de permisos
COPY --chown=airflow:0 requirements.txt /opt/airflow/requirements.txt

# Instalamos usando el path absoluto
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt