
-- Crea la extensión aws_s3 si no existe, y CASCADE asegura que también se instalen las dependencias.
CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;
-- Crea la extensión vector si no existe, necesaria para trabajar con embeddings.
CREATE EXTENSION IF NOT EXISTS vector;

-- Elimina la tabla item_emb si existe, para recrearla.
DROP TABLE IF EXISTS item_emb;
-- Elimina la tabla user_emb si existe, para recrearla.
DROP TABLE IF EXISTS user_emb;

-- Crea la tabla item_emb si no existe.
CREATE TABLE IF NOT EXISTS item_emb (
    -- id es una cadena de texto que sirve como clave primaria.
    id varchar PRIMARY KEY,
    -- embedding es un vector de 32 dimensiones que representa el embedding del item.
    embedding vector(32)
);

-- Crea la tabla user_emb si no existe.
CREATE TABLE IF NOT EXISTS user_emb (
    -- id es un entero que sirve como clave primaria.
    id int PRIMARY KEY,
    -- embedding es un vector de 32 dimensiones que representa el embedding del usuario.
    embedding vector(32)
); 

-- Importa datos desde un archivo CSV en S3 a la tabla item_emb.
SELECT aws_s3.table_import_from_s3(
   'item_emb',                       -- Nombre de la tabla a la que se importarán los datos.
   'id,embedding',                   -- Columnas de la tabla a las que se importarán los datos.
   '(format csv, header true)',      -- Formato del archivo CSV y especifica que tiene una fila de encabezado.
   '<BUCKET_NAME>',                  -- Reemplazar con el nombre del bucket de S3.
   'embeddings/item_embeddings.csv', -- Ruta al archivo CSV en S3.
   'us-east-1'                       -- Región de AWS donde se encuentra el bucket S3.
);

-- Importa datos desde un archivo CSV en S3 a la tabla user_emb.
SELECT aws_s3.table_import_from_s3(
   'user_emb',                       -- Nombre de la tabla a la que se importarán los datos.
   'id,embedding',                   -- Columnas de la tabla a las que se importarán los datos.
   '(format csv, header true)',      -- Formato del archivo CSV y especifica que tiene una fila de encabezado.
   '<BUCKET_NAME>',                  -- Reemplazar con el nombre del bucket de S3.
   'embeddings/user_embeddings.csv', -- Ruta al archivo CSV en S3.
   'us-east-1'                       -- Región de AWS donde se encuentra el bucket S3.
);