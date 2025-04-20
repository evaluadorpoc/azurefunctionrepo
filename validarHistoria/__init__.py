import logging
import azure.functions as func
import json
import requests
import base64

# ——— Configuración Jira ———
JIRA_BASE_URL     = "https://evaluadorpoc.atlassian.net"
JIRA_USER         = "evaluadorpoc@outlook.com"
JIRA_API_TOKEN    = "ATATT3xFfGF0NiXT8BjAGR_6LZdT-vHVPS_b2j7aJ0SQRKZiCQS53Xl957bfqK8Ps28nbaWk8LKe9BCAKZFRJX8T2b6_8Z1dbdOwbi0bReAZFuUzd24Ti6ESUKrFvugMPsff0sQeypgNyP4xzhKtIH6yKn3YSgrvC4TIxJZstGQeq1e0GwOrLnY"
CUSTOM_FIELD_ID   = "customfield_10058"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("📥 Webhook recibido desde Jira")

    try:
        # Extraer datos del request
        data  = req.get_json()
        issue = data["issue"]
        key   = issue["key"]

        description = issue["fields"].get("description", "")
        logging.info(f"📝 Descripción del issue {key}: {description}")

        # Siempre escribir 50 en el campo personalizado
        score_value = 50

        # Preparar autenticación
        auth = base64.b64encode(f"{JIRA_USER}:{JIRA_API_TOKEN}".encode()).decode()

        # Enviar PUT a Jira
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{key}"
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "fields": {
                CUSTOM_FIELD_ID: score_value
            }
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code in (200, 204):
            logging.info(f"✅ Campo actualizado con {score_value} en issue {key}")
        else:
            logging.warning(f"⚠️ Error al actualizar Jira: {response.status_code} - {response.text}")

        # Respuesta a quien llame al endpoint
        return func.HttpResponse(
            json.dumps({
                "key": key,
                "mensaje": "Campo actualizado con 50",
                "descripcion": description
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"❌ Error procesando webhook: {e}")
        return func.HttpResponse(f"Error interno: {e}", status_code=500)
