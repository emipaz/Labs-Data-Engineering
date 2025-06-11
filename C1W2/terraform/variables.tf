# Define la variable "project"
variable "project" {
  type        = string
  description = "Nombre del proyecto"
}

# Define la variable "region"
variable "region" {
  type        = string
  description = "Región de AWS"
}

# Define la variable "vpc_id"
variable "vpc_id" {
  type        = string
  description = "ID de la VPC"
}

# Define la variable "public_subnet_a_id"
variable "public_subnet_a_id" {
  type        = string
  description = "ID de la subred pública A"
}

# Define la variable "db_sg_id"
variable "db_sg_id" {
  type        = string
  description = "ID del grupo de seguridad para RDS"
}

# Define la variable "host"
variable "host" {
  type        = string
  description = "Host de RDS"
}

# Define la variable "port"
variable "port" {
  type        = number
  description = "Puerto de RDS"
  default     = 3306
}

# Define la variable "database"
variable "database" {
  type        = string
  description = "Nombre de la base de datos RDS"
}

# Define la variable "username"
variable "username" {
  type        = string
  description = "Nombre de usuario de RDS"
}

# Define la variable "password"
variable "password" {
  type        = string
  description = "Contraseña de RDS"
  sensitive   = true
}

# Define la variable "data_lake_bucket"
variable "data_lake_bucket" {
  type        = string
  description = "Bucket S3 para el Data Lake"
}

# Define la variable "scripts_bucket"
variable "scripts_bucket" {
  type        = string
  description = "Bucket S3 para los scripts de Glue"
}