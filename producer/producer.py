import boto3
import json
import random
import time
from datetime import datetime, timezone

REGION = "us-east-1"
STREAM_NAME = "p2-gimnasio-sensores-stream"

kinesis = boto3.client("kinesis", region_name=REGION)

ZONAS = [
    "sala_pesas",
    "cardio",
    "spinning",
    "crossfit",
    "recepcion"
]

def generar_evento():
    """
    Genera un registro simulado de sensores de un gimnasio.
    Cada evento representa el estado de una zona concreta del gimnasio.
    """
    zona = random.choice(ZONAS)
    sensor_id = "SENSOR-" + str(random.randint(1, 8)).zfill(3)

    evento = {
        "sensor_id": sensor_id,
        "zona": zona,
        "temperatura": round(random.uniform(19.0, 30.0), 2),
        "humedad": random.randint(35, 75),
        "ocupacion": random.randint(0, 40),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return evento

def enviar_evento(evento):
    """
    Envia un evento al Kinesis Data Stream.
    El campo sensor_id se usa como PartitionKey.
    """
    respuesta = kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(evento),
        PartitionKey=evento["sensor_id"]
    )

    return respuesta

def main():
    print("Iniciando productor de datos de sensores de gimnasio...")
    print("Stream:", STREAM_NAME)
    print("Region:", REGION)
    print("Pulsa Ctrl + C para detener el productor.")

    try:
        while True:
            evento = generar_evento()
            respuesta = enviar_evento(evento)

            print("Evento enviado:")
            print(json.dumps(evento, indent=2))
            print("ShardId:", respuesta["ShardId"])
            print("SequenceNumber:", respuesta["SequenceNumber"])
            print("-" * 60)

            time.sleep(2)

    except KeyboardInterrupt:
        print("Productor detenido por el usuario.")

if __name__ == "__main__":
    main()
