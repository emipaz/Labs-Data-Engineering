# Quiz_2

## Según los vídeos de esta semana, ¿cuál de las siguientes afirmaciones sobre la ingesta por lotes y streaming es cierta?


- [ ] La ingesta por lotes procesa los datos en tiempo real a medida que se generan, mientras que la ingesta por flujos procesa los datos en trozos grandes a intervalos programados. 
- [ ] La ingesta por lotes es un enfoque más moderno que ha surgido con las nuevas tecnologías, mientras que la ingesta por flujos es el método tradicional de procesar los datos a medida que se generan los eventos.
- [x] La ingesta por lotes consiste en imponer límites a un flujo continuo de datos e ingerir todos los datos dentro de esos límites como una sola unidad, mientras que la ingesta por flujo consiste en ingerir los eventos individualmente a medida que se generan.
- [ ] La ingesta por lotes sólo puede utilizarse con datos limitados por el tiempo, mientras que la ingesta por flujo sólo puede utilizarse con datos limitados por el tamaño.

    > Buen trabajo Así es como se explicaron la ingesta por lotes y el streaming en los vídeos de esta semana.


## Pregunta 2

## Considere los tres casos de uso siguientes:

- Caso de uso A: Un analista de negocio quiere analizar los datos de ventas una vez al mes. 
- Caso de uso B: Un gestor de la cadena de suministro necesita nuevas actualizaciones de registros de la base de datos transaccional una vez por minuto.
- Caso de uso C: un ingeniero de software necesita datos procesados de sensores IoT en milisegundos tras su generación para crear un cuadro de mando analítico orientado al cliente.

### ¿Cuál es la forma más adecuada de ordenar estos casos de uso a lo largo del continuo de frecuencias de ingestión de datos (es decir, etiquetar los casos de uso como batch, micro-batch y streaming)?

- [ ] A
  - Caso de uso A: streaming
  - Caso de uso B: lote
  - Caso de uso C: microlotes
<BR>
- [ ] B
  - Caso de uso A: microlotes
  - Caso de uso B: lote
  - Caso de uso C: streaming
<BR>
- [x] C
  - Caso de uso A: lote
  - Caso de uso B: microlotes
  - Caso de uso C: streaming
<BR>
- [ ] D
  - Caso de uso A: microlotes
  - Caso de uso B: streaming
  - Caso de uso C: lote

> Así es A medida que se pasa de la ingesta por lotes a la ingesta por streaming en el continuo de la ingesta de datos, se aumenta la frecuencia de la ingesta. 

## ¿Cuál o cuáles de las siguientes afirmaciones son ciertas sobre el patrón de ingesta Extracción, transformación y carga (ETL)? Seleccione todo lo que corresponda.


- [ ] No se pierde información en el proceso.
- [x] La transformación se realiza en una zona intermedia.

    > Con ETL, los datos se transforman en un área de preparación intermedia antes de cargarlos en un destino de almacenamiento.

- [ ] Puedes acabar con lo que se conoce como un pantano de datos.
- [ ] No tienes que decidir de antemano cómo quieres utilizar los datos.
- [x] Transforma los datos antes de cargarlos en el destino de almacenamiento de destino.

    > Buen trabajo Con ETL, la transformación se produce antes de cargar los datos en un sistema de destino.

## ¿Cuál o cuáles de los siguientes escenarios son apropiados para el patrón de ingesta Extracción, transformación y carga (ETL)? Seleccione todo lo que corresponda.

- [ ] Proporcionar rápidamente grandes cantidades de datos transaccionales sin procesar a un analista que desee explorar los datos. 
- [X] Carga de datos en un sistema de destino, cuando los usuarios finales solicitaron que los datos estuvieran libres de errores, duplicados e incoherencias.

    > Se trata de un caso de uso de ETL porque los datos deben limpiarse (es decir, transformarse) antes de cargarlos en el sistema de destino.


- [X] Migración de datos de un sistema heredado a una base de datos de destino, cuando los datos del sistema heredado no tienen un formato compatible con la estructura de la base de datos de destino.

    > Se trata de un caso de uso de ETL porque los datos deben transformarse a un formato compatible con la base de datos de destino antes de poder cargarse en ella.

## ¿Qué significa REST en API REST?

- [ ] Transformación de símbolos de representación
- [ ] Transformación del estado de representación
- [X] Representational State Transfer
- [ ] Transferencia de símbolos de representación

    > Buen trabajo Significa que el servidor devuelve una representación del estado del objeto solicitado.

## ¿Cómo enviar solicitudes a las API REST?

- [ ] Uso de las operaciones CREAR, LEER, ACTUALIZAR, y ELIMINAR
- [ ] Uso de las operaciones ENVIAR, RESPONDER, CONECTAR y AUTORIZAR
- [X] Utilización de los métodos HTTP POST, PUT, GET y DELETE
- [ ] Utilización de los métodos SELECT, ADD, REMOVE y PATCH

    > Buen trabajo Como recordatorio, esto es lo que hacen estos métodos:<BR>
    > GET: Recupera datos del servidor.<BR>
    > POST: Envía datos al servidor para crear un nuevo recurso.<BR>
    > PUT: Actualiza un recurso existente en el servidor.<BR>
    > DELETE: Elimina un recurso del servidor.

## ¿Cuál de las siguientes afirmaciones describe correctamente los temas de Kafka y las particiones de Kafka? 

- [ ] Un tema de Kafka es una secuencia ordenada e inmutable de particiones de Kafka.
- [ ] Los eventos se dividen en particiones Kafka, donde cada partición tiene uno o más temas Kafka.
- [X] Los eventos se dividen y enrutan en temas, donde cada tema tiene una o más particiones.
- [ ] Kafka topics y Kafka partitions son términos intercambiables.

    > Así es Dentro de un clúster Kafka, los flujos de mensajes se dividen y enrutan en temas. Cada tema tiene una o más particiones, que no son más que secuencias ordenadas e inmutables de mensajes a las que continuamente se añaden nuevos mensajes.

## ¿Cuál de las siguientes afirmaciones sobre Amazon Kinesis Data Streams y Apache Kafka es cierta?

- [ ] El paralelo a un broker de Kafka es un stream de Kinesis. El paralelo a un clúster de Kafka es un fragmento de Kinesis.
- [ ] El paralelo a un tema de Kafka es un fragmento de Kinesis. El paralelo a una partición de Kafka es un flujo de Kinesis.
- [X] El paralelo a un tema de Kafka es un flujo de Kinesis. El paralelo a una partición de Kafka es un fragmento de Kinesis.
- [ ] El paralelo a un clúster de Kafka es un flujo de Kinesis. El paralelo a un tema de Kafka es un fragmento de Kinesis.

## Verdadero o Falso: Una vez que un consumidor lee un mensaje de un tema de Kafka, el mensaje se elimina inmediatamente.

- [ ] Verdadero
- [X] Falso

    > ¡Buen trabajo! El clúster Kafka retiene el mensaje durante un periodo de tiempo configurable, tanto si el mensaje se ha consumido como si no. Esto permite a los consumidores reproducir y volver a procesar los mensajes según sea necesario.