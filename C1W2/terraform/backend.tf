# Configura el backend de Terraform.
terraform {
  backend "local" {
  # Define la ruta al archivo local donde se guardará el estado.
  path = "/home/coder/.local/share/code-server/User/de-c1w2-730335457346-us-east-1-terraform-state.state"
  }
}
