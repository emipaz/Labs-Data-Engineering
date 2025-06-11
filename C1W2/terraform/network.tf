# Obtiene información sobre una VPC (Virtual Private Cloud) existente en AWS.

data "aws_vpc" "main" {
  # El ID de la VPC que se va a consultar se toma de la variable "vpc_id".
  id = var.vpc_id
}

# Obtiene información sobre una subred pública existente en AWS.

data "aws_subnet" "public_a" {
  # El ID de la subred pública que se va a consultar se toma de la variable "public_subnet_a_id".
  id = var.public_subnet_a_id
}

# Obtiene información sobre un grupo de seguridad existente en AWS.

data "aws_security_group" "db_sg" {
  # El ID del grupo de seguridad que se va a consultar se toma de la variable "db_sg_id".
  id = var.db_sg_id
}