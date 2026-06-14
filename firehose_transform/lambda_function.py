import base64
import json
from datetime import datetime, timezone

def lambda_handler(event, context):
    output = []

    for record in event["records"]:
        record_id = record["recordId"]

        try:
            payload = base64.b64decode(record["data"]).decode("utf-8")
            data = json.loads(payload)

            # Enriquecimiento del evento
            data["processed_at"] = datetime.now(timezone.utc).isoformat()
            data["alerta_alta_ocupacion"] = data.get("ocupacion", 0) > 30

            transformed_payload = json.dumps(data) + "\n"
            encoded_data = base64.b64encode(
                transformed_payload.encode("utf-8")
            ).decode("utf-8")

            output.append({
                "recordId": record_id,
                "result": "Ok",
                "data": encoded_data
            })

        except Exception:
            output.append({
                "recordId": record_id,
                "result": "ProcessingFailed",
                "data": record["data"]
            })

    return {
        "records": output
    }
