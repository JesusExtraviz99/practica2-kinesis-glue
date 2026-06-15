import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, [
    "JOB_NAME",
    "GLUE_DATABASE",
    "GLUE_TABLE",
    "OUTPUT_PATH"
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Lectura de los datos catalogados por AWS Glue Crawler
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=args["GLUE_DATABASE"],
    table_name=args["GLUE_TABLE"]
)

# Conversion a DataFrame de Spark para aplicar transformaciones
df = dynamic_frame.toDF()

# Transformacion simple:
# se conservan solo registros con ocupacion mayor o igual a 10
df_filtrado = df.filter(df["ocupacion"] >= 10)

# Escritura del resultado procesado en S3 en formato JSON
df_filtrado.write.mode("overwrite").json(args["OUTPUT_PATH"])

job.commit()
