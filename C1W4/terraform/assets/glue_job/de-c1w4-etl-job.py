import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


def sparkSqlQuery(
    glueContext, query, mapping, transformation_ctx
) -> DynamicFrame:
    """
    Ejecuta una consulta SQL utilizando Spark SQL y devuelve un DynamicFrame.
    Args:
        glueContext (GlueContext): El contexto de Glue para manejar operaciones de Glue.
        query (str): La consulta SQL que se ejecutará.
        mapping (dict): Un diccionario que mapea alias a DynamicFrames.
        transformation_ctx (str): El contexto de transformación para el DynamicFrame resultante.
    Returns:
        DynamicFrame: El resultado de la consulta SQL como un DynamicFrame.
    """
    for alias, frame in mapping.items():
        # Crea vistas temporales para cada DynamicFrame
        frame.toDF().createOrReplaceTempView(alias) 
    # Ejecuta la consulta SQL
    result = spark.sql(query)
    # Convierte el resultado a DynamicFrame
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


# Obtiene los argumentos pasados al script
args = getResolvedOptions(
    sys.argv, ["JOB_NAME", "glue_connection", "glue_database", "target_path"]
)

# Inicializa el contexto de Spark y Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)  # Inicializa el trabajo de Glue


# Script generado para el nodo Products
products_node = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.products",  # Tabla de productos en la base de datos
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="products_node",
)

# Script generado para el nodo Customers
customers_node = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.customers", # Tabla de clientes en la base de datos
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="customers_node",
)

# Script generado para el nodo Ratings
ratings_node = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.ratings", # Tabla de calificaciones en la base de datos
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="ratings_node",
)

# Consulta SQL para unir las tablas
sql_join_query = """
select r.customerNumber
, c.city
, c.state
, c.postalCode
, c.country
, c.creditLimit
, r.productCode
, p.productLine
, p.productScale
, p.quantityInStock
, p.buyPrice
, p.MSRP
, r.productRating
from ratings r 
join products p on p.productCode = r.productCode 
join customers c on c.customerNumber = r.customerNumber;
"""

# Ejecuta la consulta SQL y obtiene el DynamicFrame resultante
join_node = sparkSqlQuery(
    glueContext,
    query=sql_join_query,
    mapping={
        "ratings": ratings_node,
        "products": products_node,
        "customers": customers_node,
    },
    transformation_ctx="join_node",
)

# Script generado para cargar datos en S3
s3_upload_node = glueContext.getSink(
    path=f"{args['target_path']}/ratings_ml_training/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=["customerNumber"],
    enableUpdateCatalog=True,
    transformation_ctx="s3_upload_node",
)

# Establece la información del catálogo para el DynamicFrame
s3_upload_node.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="ratings_ml_training",
)

# Establece el formato y la compresión para los datos en S3
s3_upload_node.setFormat("glueparquet", compression="snappy")

# Escribe el DynamicFrame resultante en S3
s3_upload_node.writeFrame(join_node)

# Finaliza el trabajo de Glue
job.commit()
