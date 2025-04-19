import logging
import azure.functions as func
import json
import requests

JIRA_URL = "https://evaluadorpoc.atlassian.net"
AUTH_EMAIL = "evaluadorpoc@outlook.com"
AUTH_TOKEN = "ATATT3xFfGF0NiXT8BjAGR_6LZdT-vHVPS_b2j7aJ0SQRKZiCQS53Xl957bfqK8Ps28nbaWk8LKe9BCAKZFRJX8T2b6_8Z1dbdOwbi0bReAZFuUzd24Ti6ESUKrFvugMPsff0sQeypgNyP4xzhKtIH6yKn3YSgrvC4TIxJZstGQeq1e0GwOrLnY"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔔 Webhook recibido en validarHistoria")

    try:
        payload = req.get_json()
        issue = payload["issue"]
        key = issue["key"]
        description = issue["fields"]["description"]

        # 🧠 Lógica simple de validación (puedes extenderla)
        if all(x in description.lower() for x in ["como", "quiero", "para"]):
            score = 100  # 🎯 Tu puntaje personalizado
            mensaje = "✅ Historia válida con buen formato."
        else:
            score = 0
            mensaje = "❌ La historia no cumple con el formato."

        # 🔄 Llamada a Jira para actualizar el campo personalizado
        url = f"{JIRA_URL}/rest/api/3/issue/{key}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {requests.auth._basic_auth_str(AUTH_EMAIL, AUTH_TOKEN)}"
        }
        body = {
            "fields": {
                "customfield_10058": f"{score}%"  # puedes cambiarlo a número si el campo lo permite
            }
        }

        response = requests.put(url, headers=headers, json=body)

        if response.status_code >= 200 and response.status_code < 300:
            logging.info(f"✅ Campo actualizado en Jira para {key}")
        else:
            logging.warning(f"⚠️ Error al actualizar Jira: {response.status_code} - {response.text}")

        return func.HttpResponse(
            json.dumps({
                "key": key,
                "valida": score > 0,
                "mensaje": mensaje
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"🔥 Error inesperado: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
