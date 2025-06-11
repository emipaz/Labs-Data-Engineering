# Obtiene la información de la cuenta actual de AWS.
data "aws_caller_identity" "current" {}

# Define una política de IAM (Identity and Access Management) para Glue.
data "aws_iam_policy_document" "glue_base_policy" {
  # Define una declaración dentro de la política.
  statement {
    # Identificador único para la declaración.
    sid    = "AllowGlueToAssumeRole"
    # Efecto de la declaración: "Allow" permite la acción.
    effect = "Allow"

    # Define los "principales" que pueden asumir el rol.
    principals {
      # Identificadores de los servicios que pueden asumir el rol (en este caso, Glue).
      identifiers = ["glue.amazonaws.com"]
      # Tipo de principal: "Service" indica que es un servicio de AWS.
      type        = "Service"
    }

    # Acciones permitidas para el principal (en este caso, asumir un rol).
    actions = ["sts:AssumeRole"]
  }
}

# Define una política de IAM para dar acceso a Glue a diferentes recursos de AWS.

data "aws_iam_policy_document" "glue_access_policy" {

  # Define una declaración dentro de la política.

  statement {

    # Identificador único para la declaración.

    sid    = "AllowGlueAccess"

    # Efecto de la declaración: "Allow" permite la acción.

    effect = "Allow"

    # Acciones permitidas para Glue (acceso a S3, Glue, IAM, Logs, etc.).
    # El uso de "*" indica que se permiten todas las acciones dentro de cada servicio.

    actions = [
      "s3:*",         # Acceso total a S3 (buckets y objetos).
      "glue:*",       # Acceso total a Glue (catálogos, tablas, crawlers, etc.).
      "iam:*",        # Acceso total a IAM (roles, políticas, usuarios, etc.).  ¡CUIDADO!  Restringe esto en producción.
      "logs:*",       # Acceso total a CloudWatch Logs (grupos de logs, streams, etc.).
      "cloudwatch:*", # Acceso total a CloudWatch (métricas, alarmas, etc.).
      "sqs:*",        # Acceso total a SQS (colas de mensajes).
      "ec2:*",        # Acceso total a EC2 (instancias, redes, etc.). ¡CUIDADO! Restringe esto en producción.
      "rds:*",        # Acceso total a RDS (bases de datos). ¡CUIDADO! Restringe esto en producción.
      "cloudtrail:*"  # Acceso total a CloudTrail (logs de auditoría).
    ]
    # Recursos a los que se aplica la política.
    # El uso de "*" indica que se aplica a todos los recursos. ¡CUIDADO! Restringe esto en producción.

    resources = [
      "*", # Todos los recursos de AWS.
    ]
  }
}