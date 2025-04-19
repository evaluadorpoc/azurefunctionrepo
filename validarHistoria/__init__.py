import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("📩 Webhook recibido para validar historia")

    try:
        data = req.get_json()
        description = data.get('descripcion', '')

        if not description:
            return func.HttpResponse("❌ Sin descripción", status_code=200)

        # Resultado simulado
        resultado = {
            "score": 88,
            "comentario": "La historia cumple bien, pero podrías precisar el objetivo ('para')."
        }

        return func.HttpResponse(json.dumps(resultado), status_code=200, mimetype="application/json")

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("❌ Error al procesar", status_code=500)
