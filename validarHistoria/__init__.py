import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("📥 Webhook recibido para validar historia")

    try:
        data = req.get_json()
        issue_key = data['issue']['key']
        description = data['issue']['fields'].get('description', '')
        tipo = data['issue']['fields']['issuetype']['name']

        if tipo.lower() != 'story':
            return func.HttpResponse("❌ No es historia de usuario", status_code=200)

        if not description:
            return func.HttpResponse("❌ Sin descripción", status_code=200)

        # Aquí luego llamaremos a Copilot Studio
        resultado = {
            "score": 88,
            "comentario": "La historia cumple bien, pero podrías precisar el objetivo ('para')."
        }

        return func.HttpResponse(json.dumps(resultado), status_code=200, mimetype="application/json")

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("❌ Error al procesar", status_code=500)
