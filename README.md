# Practica 2 - Ingesta y procesamiento de datos en AWS

Esta practica implementa un flujo de ingesta y procesamiento de datos en AWS utilizando Amazon S3, Amazon Kinesis Data Streams, Amazon Kinesis Data Firehose y AWS Glue.

El caso elegido consiste en simular datos de sensores de un gimnasio. Un productor en Python genera registros con informacion de temperatura, humedad y ocupacion de diferentes zonas del gimnasio, y los envia a un Kinesis Data Stream.

Posteriormente, Kinesis Firehose consume los datos del stream y los almacena en un bucket S3. Finalmente, AWS Glue permite catalogar y transformar los datos almacenados.

## Servicios utilizados

- Amazon S3
- Amazon Kinesis Data Streams
- Amazon Kinesis Data Firehose
- AWS Glue
- Python
- Boto3

## Flujo general

Productor Python -> Kinesis Data Stream -> Kinesis Firehose -> Amazon S3 -> AWS Glue
