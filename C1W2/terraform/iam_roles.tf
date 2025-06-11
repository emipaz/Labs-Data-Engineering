# Define un rol de IAM para Glue.

resource "aws_iam_role" "glue_role" {
  # Nombre del rol, utilizando el nombre del proyecto como prefijo.
  name               = "${var.project}-glue-role"
  # Política de asunción de rol, que permite a Glue asumir este rol.
  assume_role_policy = data.aws_iam_policy_document.glue_base_policy.json
}

# Define una política de rol de IAM para el rol de Glue.

resource "aws_iam_role_policy" "task_role_policy" {
  # Nombre de la política, utilizando el nombre del proyecto como prefijo.
  name   = "${var.project}-glue-role-policy"
  # Asocia la política al rol de Glue.
  role   = aws_iam_role.glue_role.id
  # Define la política de acceso para Glue.
  policy = data.aws_iam_policy_document.glue_access_policy.json
}
