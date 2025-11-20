# 🏎️ Plataforma de Análisis Estratégico de Fórmula 1

### **MongoDB → BigQuery → DynamoDB → FastAPI → Streamlit**

Este documento explica cómo configurar y ejecutar el proyecto completo,
incluyendo el pipeline de ingesta, transformación y despliegue de datos,
además de la aplicación cliente basada en Streamlit.

------------------------------------------------------------------------

# 📦 **1. Estructura del Proyecto**

    ProyectoFinalF1/
    │
    └── Entrega/
        └── Core/
            └── etl/
                ├── mongo_to_bigquery.py
                ├── transform_profiles.py
                ├── bigquery_to_dynamo.py
                ├── fast_api_app.py
                ├── streamlit_app.py
                ├── __init__.py

------------------------------------------------------------------------

# ⚙️ **2. Requisitos**

### **Software**

-   Python 3.10+
-   Google Cloud SDK o credencial de servicio GCP
-   AWS IAM Access Keys (DynamoDB)
-   MongoDB Atlas (cluster disponible)
-   Streamlit
-   FastAPI + Uvicorn

### **Librerías necesarias**

``` bash
pip install pandas google-cloud-bigquery pymongo boto3 streamlit fastapi uvicorn certifi
```

------------------------------------------------------------------------

# 🔑 **3. Configuración de Credenciales**

## **3.1 Google BigQuery**

Coloca tu archivo JSON de credenciales en:

    Entrega/Core/2. From_Mongo_to_BigQuery/topicos-bases-datos.json

Y define la variable:

``` bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/al/json"
```

En Windows PowerShell:

``` powershell
setx GOOGLE_APPLICATION_CREDENTIALS "C:\ruta\al\archivo.json"
```

------------------------------------------------------------------------

## **3.2 AWS DynamoDB**

Descarga tus claves en CSV desde AWS IAM.\
Ejemplo de archivo:

    access key id,secret access key
    AKIAxxxx,xxxxxxxx

------------------------------------------------------------------------

## **3.3 MongoDB Atlas**

Tu conexión debe estar configurada en:

``` python
MONGO_URI = "mongodb+srv://..."
```

------------------------------------------------------------------------

# 🛠️ **4. Pipeline ETL Completo**

1.  **MongoDB → BigQuery**\
2.  **Transformación consolidada en BigQuery**\
3.  **BigQuery → DynamoDB**

Ejecutable desde Streamlit o desde terminal.

------------------------------------------------------------------------

# 🚀 **5. Ejecución Manual desde Terminal**

## **5.1 MongoDB → BigQuery**

``` bash
python mongo_to_bigquery.py --year 2023
```

------------------------------------------------------------------------

## **5.2 Transformación BigQuery**

``` bash
python transform_profiles.py --year 2023
```

------------------------------------------------------------------------

## **5.3 BigQuery → DynamoDB**

``` bash
python bigquery_to_dynamo.py
```

------------------------------------------------------------------------

# 🌐 **6. Backend FastAPI**

``` bash
uvicorn fast_api_app:app --reload
```

------------------------------------------------------------------------

# 🎨 **7. Frontend Streamlit**

``` bash
streamlit run streamlit_app.py
```

------------------------------------------------------------------------

# 🧠 **8. Flujo Completo**

1.  Levantar FastAPI\
2.  Levantar Streamlit\
3.  Ejecutar ETL desde la UI\
4.  Consultar pilotos

------------------------------------------------------------------------

# 🧪 **9. Pruebas**

-   Verificar latencias\
-   Verificar integraciones (FastAPI → DynamoDB)

------------------------------------------------------------------------

# ✔️ **README listo**
