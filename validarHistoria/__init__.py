import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.function_name(name="validarHistoria")
@app.route(route="validarHistoria", methods=["POST"])
def validarHistoria(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🪝 Webhook recibido para validar historia")

    try:
        req_body = req.get_json()
        issue = req_body.get("issue", {})
        fields = issue.get("fields", {})
        description = fields.get("description", "")

        score, comentario = evaluar_historia(description)

        resultado = {
            "score": score,
            "comentario": comentario
        }

        logging.info(f"✅ Resultado: {resultado}")

        return func.HttpResponse(
            json.dumps(resultado),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")
        return func.HttpResponse(
            "Error procesando la historia.",
            status_code=500
        )

def evaluar_historia(texto):
    texto = texto.lower()
    score = 0
    comentario = []

    if "como" in texto:
        score += 30
    else:
        comentario.append("Falta el rol ('como').")

    if "quiero" in texto:
        score += 30
    else:
        comentario.append("Falta la acción ('quiero').")

    if "para" in texto:
        score += 40
    else:
        comentario.append("Falta el objetivo ('para').")

    if score == 100:
        comentario = ["Historia bien redactada."]
    else:
        comentario = ["; ".join(comentario)]

    return score, comentario[0]
