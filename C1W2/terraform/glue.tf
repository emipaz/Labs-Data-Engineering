# Define una base de datos en el catálogo de Glue para analítica.

resource "aws_glue_catalog_database" "analytics_database" {
  # Nombre de la base de datos, utilizando el nombre del proyecto como prefijo.
  name        = "${var.project}-analytics-db"
  # Descripción de la base de datos.
  description = "Database for performing analytics on OLTP data"
}

# Define una conexión a la base de datos RDS.

resource "aws_glue_connection" "rds_connection" {
  # Nombre de la conexión, utilizando el nombre del proyecto como prefijo.
  name = "${var.project}-rds-connection"

  # Propiedades de la conexión, incluyendo la URL JDBC, el nombre de usuario y la contraseña.
  connection_properties = {
    JDBC_CONNECTION_URL = "jdbc:mysql://${var.host}:${var.port}/${var.database}"
    USERNAME            = var.username
    PASSWORD            = var.password
  }

  # Requisitos de conexión física, incluyendo la zona de disponibilidad, el grupo de seguridad y la subred.
  physical_connection_requirements {
    availability_zone      = data.aws_subnet.public_a.availability_zone
    security_group_id_list = [data.aws_security_group.db_sg.id]
    subnet_id              = data.aws_subnet.public_a.id
  }
}

# Define un crawler de Glue para rastrear los datos en S3.

resource "aws_glue_crawler" "s3_crawler" {
  # Nombre del crawler, utilizando el nombre del proyecto como prefijo.
  name          = "${var.project}-analytics-db-crawler"
  # Nombre de la base de datos donde se almacenarán los metadatos.
  database_name = aws_glue_catalog_database.analytics_database.name
  # ARN del rol de IAM que el crawler utilizará.
  role          = aws_iam_role.glue_role.arn

  # Define el objetivo del crawler en S3.
  s3_target {
    # Ruta al bucket S3 donde se encuentran los datos.
    path = "s3://${var.data_lake_bucket}/gold"
  }

  # Define la política de re-rastreo.
  recrawl_policy {
    # Solo rastrear nuevas carpetas.
    recrawl_behavior = "CRAWL_NEW_FOLDERS_ONLY"
  }

  # Define la política de cambio de esquema.
  schema_change_policy {
    # Registrar los cambios de esquema.
    delete_behavior = "LOG"
    update_behavior = "LOG"
  }
}

# Define un trabajo de ETL de Glue.

resource "aws_glue_job" "etl_job" {
  # Nombre del trabajo, utilizando el nombre del proyecto como prefijo.
  name         = "${var.project}-etl-job"
  # ARN del rol de IAM que el trabajo utilizará.
  role_arn     = aws_iam_role.glue_role.arn
  # Versión de Glue a utilizar.
  glue_version = "4.0"
  # Conexiones a utilizar.
  connections  = [aws_glue_connection.rds_connection.name]
  # Comando a ejecutar.
  command {
    # Nombre del comando.
    name            = "glueetl"
    # Ubicación del script de Python.
    script_location = "s3://${var.scripts_bucket}/glue_job.py"
    # Versión de Python a utilizar.
    python_version  = 3
  }

  # Argumentos por defecto para el trabajo.
  default_arguments = {
    "--enable-job-insights" = "true"
    "--job-language"        = "python"
    "--glue_connection"     = aws_glue_connection.rds_connection.name
    "--glue_database"       = aws_glue_catalog_database.analytics_database.name
    "--target_path"         = "s3://${var.data_lake_bucket}/gold"
  }

  # Tiempo de espera para el trabajo.
  timeout = 5

  # Número de trabajadores a utilizar.
  number_of_workers = 2
  # Tipo de trabajador a utilizar.
  worker_type       = "G.1X"
}
