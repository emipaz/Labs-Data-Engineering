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
    Ejecuta una consulta SQL de Spark en los DynamicFrames de Glue.

    Args:
        glueContext: El contexto de Glue.
        query: La consulta SQL a ejecutar.
        mapping: Un diccionario que mapea los alias de las tablas en la consulta a los DynamicFrames correspondientes.
        transformation_ctx: El contexto de transformación.

    Returns:
        Un DynamicFrame que contiene los resultados de la consulta.
    """
    for alias, frame in mapping.items():
        # Crea una vista temporal para cada DynamicFrame
        frame.toDF().createOrReplaceTempView(alias) 
    # Ejecuta la consulta SQL
    result = spark.sql(query)
    # Convierte el resultado en un DynamicFrame
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


# Obtiene los argumentos del trabajo de Glue
args = getResolvedOptions(
    sys.argv, ["JOB_NAME", "glue_connection", "glue_database", "target_path"]
)

# Crea un contexto de Spark
sc = SparkContext()

# Crea un contexto de Glue
glueContext = GlueContext(sc)

# Obtiene la sesión de Spark
spark = glueContext.spark_session

# Crea un objeto Job de Glue
job = Job(glueContext)

# Inicializa el trabajo de Glue
job.init(args["JOB_NAME"], args)

# Extract data from source tables
# Crea un DynamicFrame para la tabla customers
customers = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.customers",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="customers",
)

# Crea un DynamicFrame para la tabla orders
orders = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.orders",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="orders",
)

# Crea un DynamicFrame para la tabla orderdetails
orderdetails = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.orderdetails",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="orderdetails",
)

# Crea un DynamicFrame para la tabla products
products = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.products",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="products",
)

# Crea un DynamicFrame para la tabla productlines
productlines = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.productlines",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="productslines",
)

# Transform data to build a star schema
sql_query_dim_customers = """
with dim_customers as (
    select
        customerNumber,
        customerName,
        contactLastName,
        contactFirstName,
        phone,
        addressLine1,
        addressLine2,
        creditLimit
    from customers
)
select * from dim_customers
"""

 # Crea un DynamicFrame para la tabla de dimensión customers
dim_customers = sparkSqlQuery(
    glueContext,
    query=sql_query_dim_customers,
    mapping={"customers": customers},
    transformation_ctx="dim_customers",
)

sql_query_dim_products = """
with dim_products as (
    select
        products.productCode,
        products.productName,
        products.productLine,
        products.productScale,
        products.productVendor,
        products.productDescription,
        productlines.textDescription as productLineDescription
    from products
    left join productlines using (productLine)
)
select * from dim_products
"""

# Crea un DynamicFrame para la tabla de dimensión products
dim_products = sparkSqlQuery(
    glueContext,
    query=sql_query_dim_products,
    mapping={
        "products": products,
        "productlines": productlines,
    },
    transformation_ctx="dim_products",
)

sql_query_dim_locations = """
with dim_locations as (
    select distinct
        postalCode,
        city,
        state,
        country
    from customers
)
select * from dim_locations
"""

# Crea un DynamicFrame para la tabla de dimensión locations
dim_locations = sparkSqlQuery(
    glueContext,
    query=sql_query_dim_locations,
    mapping={"customers": customers},
    transformation_ctx="dim_locations",
)

sql_query_fact_orders = """
with fact_orders as (
    select
        orderLineNumber,
        orders.orderNumber,
        orders.customerNumber,
        location.postalCode,
        orderdetails.productCode,
        orders.orderDate,
        orders.requiredDate,
        orders.shippedDate,
        orders.status,
        orders.comments,
        orderdetails.quantityOrdered,
        orderdetails.priceEach,
        (orderdetails.quantityOrdered * orderdetails.priceEach) AS orderAmount,
        products.buyPrice,
        products.MSRP
    from orders
    left join orderdetails using (orderNumber)
    left join products using (productCode)
    left join customers using (customerNumber)
    left join location using (postalCode)
)
select * from fact_orders
"""

 # Crea un DynamicFrame para la tabla de hechos orders
fact_orders = sparkSqlQuery(
    glueContext,
    query=sql_query_fact_orders,
    mapping={
        "orders": orders,
        "orderdetails": orderdetails,
        "products": products,
        "location": dim_locations,
    },
    transformation_ctx="fact_orders",
)

# Load transformed data into S3

# Crea un sink para escribir la tabla de dimensión customers en S3
dim_customers_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/dim_customers/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_customers_to_s3",
)

 # Define la información del catálogo para el sink
dim_customers_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_customers",
)

# Define el formato del archivo como parquet
dim_customers_to_s3.setFormat("glueparquet")

# Escribe el DynamicFrame en S3
dim_customers_to_s3.writeFrame(dim_customers)

# Crea un sink para escribir la tabla de dimensión products en S3
dim_products_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/dim_products/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_products_to_s3",
)

# Define la información del catálogo para el sink
dim_products_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_products",
)

# Define el formato del archivo como parquet
dim_products_to_s3.setFormat("glueparquet")

# Escribe el DynamicFrame en S3
dim_products_to_s3.writeFrame(dim_products)

# Crea un sink para escribir la tabla de dimensión locations en S3
dim_locations_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/dim_locations/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_locations_to_s3",
)

# Define la información del catálogo para el sink
dim_locations_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_locations",
)
# Define el formato del archivo como parquet
dim_locations_to_s3.setFormat("glueparquet")

# Escribe el DynamicFrame en S3
dim_locations_to_s3.writeFrame(dim_locations)

# Crea un sink para escribir la tabla de hechos orders en S3
fact_orders_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/fact_orders/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="fact_orders_to_s3",
)

# Define la información del catálogo para el sink
fact_orders_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="fact_orders",
)

# Define el formato del archivo como parquet
fact_orders_to_s3.setFormat("glueparquet")

# Escribe el DynamicFrame en S3
fact_orders_to_s3.writeFrame(fact_orders)

# Confirma el trabajo de Glue
job.commit()
