import logging
import azure.functions as func
import json
import requests
import base64

# Configuración fija
JIRA_BASE_URL   = "https://evaluadorpoc.atlassian.net"
JIRA_USER       = "evaluadorpoc@outlook.com"
JIRA_API_TOKEN  = "ATATT3xFfGF0NiXT8BjAGR_6LZdT-vHVPS_b2j7aJ0SQRKZiCQS53Xl957bfqK8Ps28nbaWk8LKe9BCAKZFRJX8T2b6_8Z1dbdOwbi0bReAZFuUzd24Ti6ESUKrFvugMPsff0sQeypgNyP4xzhKtIH6yKn3YSgrvC4TIxJZstGQeq1e0GwOrLnY"
CUSTOM_FIELD_ID = "customfield_10058"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🚀 Webhook activado para prueba PUT 300")

    try:
        data = req.get_json()
        issue_key = data["issue"]["key"]
        logging.info(f"🔑 Issue recibido: {issue_key}")

        # Preparar autenticación
        auth_str = f"{JIRA_USER}:{JIRA_API_TOKEN}"
        auth_encoded = base64.b64encode(auth_str.encode()).decode()

        # Endpoint y headers
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
        headers = {
            "Authorization": f"Basic {auth_encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Payload con valor fijo
        payload = {
            "fields": {
                CUSTOM_FIELD_ID: 300
            }
        }

        # PUT a Jira
        res = requests.put(url, headers=headers, json=payload)

        if res.status_code in (200, 204):
            logging.info(f"✅ Campo actualizado a 300 en {issue_key}")
        else:
            logging.warning(f"⚠️ Error actualizando Jira: {res.status_code} - {res.text}")

        return func.HttpResponse(
            json.dumps({"resultado": "PUT ejecutado", "issue": issue_key}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"❌ Error interno: {e}")
        return func.HttpResponse(f"Error interno: {str(e)}", status_code=500)
