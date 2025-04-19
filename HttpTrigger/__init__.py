import azure.functions as func
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("✅ Webhook recibido")
    return func.HttpResponse("Hello from manual Azure Function!", status_code=200)
