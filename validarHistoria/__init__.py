import logging
import azure.functions as func
import json
import requests
import base64

JIRA_BASE_URL     = "https://evaluadorpoc.atlassian.net"
JIRA_USER         = "evaluadorpoc@outlook.com"
JIRA_API_TOKEN    = "ATATT3xFfGF0NiXT8BjAGR_6LZdT-vHVPS_b2j7aJ0SQRKZiCQS53Xl957bfqK8Ps28nbaWk8LKe9BCAKZFRJX8T2b6_8Z1dbdOwbi0bReAZFuUzd24Ti6ESUKrFvugMPsff0sQeypgNyP4xzhKtIH6yKn3YSgrvC4TIxJZstGQeq1e0GwOrLnY"
CUSTOM_FIELD_ID   = "customfield_10058"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🚀 Webhook activado para prueba con PUT usando `key` lowercase")

    try:
        data = req.get_json()
        issue = data["issue"]
        key = issue["key"].lower()  # <- forzamos a minúscula

        logging.info(f"🔑 Issue recibido con key: {key}")

        # Auth básica codificada
        auth_str = f"{JIRA_USER}:{JIRA_API_TOKEN}"
        auth_encoded = base64.b64encode(auth_str.encode()).decode()

        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{key}"
        headers = {
            "Authorization": f"Basic {auth_encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "fields": {
                CUSTOM_FIELD_ID: 300
            }
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code in [200, 204]:
            logging.info("✅ PUT exitoso con `key`")
        else:
            logging.warning(f"⚠️ PUT falló con key `{key}` - {response.status_code}: {response.text}")

        return func.HttpResponse("PUT completado", status_code=200)

    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")
        return func.HttpResponse("Error interno", status_code=500)
