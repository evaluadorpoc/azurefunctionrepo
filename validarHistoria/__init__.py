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

def evaluar_descripcion(texto: str) -> int:
    """
    Cuenta las ocurrencias de las palabras clave y
    devuelve un porcentaje entero (0-100).
    """
    claves = ["como", "quiero", "para"]
    count = sum(1 for p in claves if p in texto.lower())
    score = int((count / len(claves)) * 100)
    return score

def update_jira_field(issue_key: str, score: int) -> None:
    """
    Actualiza el campo CUSTOM_FIELD_ID de Jira asegurando
    que se envíe un entero redondeado.
    """
    # Preparar Basic Auth
    auth_str     = f"{JIRA_USER}:{JIRA_API_TOKEN}"
    auth_encoded = base64.b64encode(auth_str.encode()).decode()

    # Forzar entero
    score_value = int(round(score))

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Accept":        "application/json",
        "Content-Type":  "application/json"
    }
    payload = {
        "fields": {
            CUSTOM_FIELD_ID: score_value
        }
    }

    res = requests.put(url, headers=headers, json=payload)
    if res.status_code in (200, 204):
        logging.info(f"✅ Jira [{issue_key}] actualizado con {score_value}%")
    else:
        logging.warning(
            f"⚠️ Error al actualizar Jira [{res.status_code}]: {res.text}"
        )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔄 Webhook recibido en validarHistoria")
    try:
        data        = req.get_json()
        issue       = data["issue"]
        key         = issue["key"]
        description = issue["fields"].get("description", "")

        score = evaluar_descripcion(description)
        update_jira_field(key, score)

        body = {
            "key":    key,
            "valida": score >= 60,
            "mensaje": f"Puntaje asignado: {score}%"
        }
        return func.HttpResponse(
            json.dumps(body),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"❌ Error en ejecutar validarHistoria: {e}")
        return func.HttpResponse(f"Error interno: {e}", status_code=500)
