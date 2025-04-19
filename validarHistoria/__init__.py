import logging
import azure.functions as func
import json
import requests

JIRA_URL = "https://evaluadorpoc.atlassian.net"
AUTH_EMAIL = "evaluadorpoc@outlook.com"
AUTH_TOKEN = "ATATT3xFfGF0NiXT8BjAGR_6LZdT-vHVPS_b2j7aJ0SQRKZiCQS53Xl957bfqK8Ps28nbaWk8LKe9BCAKZFRJX8T2b6_8Z1dbdOwbi0bReAZFuUzd24Ti6ESUKrFvugMPsff0sQeypgNyP4xzhKtIH6yKn3YSgrvC4TIxJZstGQeq1e0GwOrLnY"
CUSTOM_FIELD_ID = "customfield_10058"

def evaluar_descripcion(texto):
    partes = ["como", "quiero", "para"]
    count = sum(1 for p in partes if p in texto.lower())
    score = int((count / 3) * 100)
    return score

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔄 Webhook recibido en validarHistoria")
    try:
        data = req.get_json()
        issue = data["issue"]
        key = issue["key"]
        description = issue["fields"]["description"]
        score = evaluar_descripcion(description)

        # ▶️ Paso 1: Preparar autenticación básica
        auth_str = f"{JIRA_USER}:{JIRA_API_TOKEN}"
        auth_encoded = base64.b64encode(auth_str.encode()).decode()

        # ▶️ Paso 2: Llamada a Jira API para actualizar el campo
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{key}"
        headers = {
            "Authorization": f"Basic {auth_encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "fields": {
                CUSTOM_FIELD_ID: score
            }
        }
        res = requests.put(url, headers=headers, data=json.dumps(payload))

        if res.status_code in [200, 204]:
            logging.info(f"✅ Campo actualizado en Jira [{key}] con puntaje {score}%")
        else:
            logging.warning(f"⚠️ Error al actualizar Jira: {res.status_code} - {res.text}")

        return func.HttpResponse(
            json.dumps({
                "key": key,
                "valida": score >= 60,
                "mensaje": f"Puntaje asignado: {score}%"
            }),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"❌ Error en ejecución: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
