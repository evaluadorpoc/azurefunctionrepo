import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("✅ Webhook recibido para validar historia")
        data = req.get_json()

        description = data["issue"]["fields"]["description"]
        key = data["issue"]["key"]

        logging.info(f"Issue key: {key}")
        logging.info(f"Descripción recibida: {description}")

        if all(p in description.lower() for p in ["como", "quiero", "para"]):
            resultado = {
                "key": key,
                "valida": True,
                "mensaje": "La historia de usuario tiene buen formato."
            }
        else:
            resultado = {
                "key": key,
                "valida": False,
                "mensaje": "La historia de usuario NO cumple con el formato esperado."
            }

        return func.HttpResponse(
            json.dumps(resultado),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"❌ Error interno: {str(e)}")
        return func.HttpResponse(
            f"Error interno: {str(e)}",
            status_code=500
        )
