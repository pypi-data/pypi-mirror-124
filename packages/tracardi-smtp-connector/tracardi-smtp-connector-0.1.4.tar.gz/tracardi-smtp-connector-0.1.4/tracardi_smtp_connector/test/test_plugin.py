import os
from dotenv import load_dotenv
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi_smtp_connector.plugin import SmtpDispatcherAction

load_dotenv()

init = {
    'source': {
        'id': 'cde09c91-9ae4-4bdc-ab58-ced3ab4e441a'
    },
    'message': {
        "send_to": os.getenv('TO'),
        "send_from": os.getenv('FROM'),
        "reply_to": "jakis@main.com",
        "title": "Testowy tytuł",
        "message": "Testowa wiadomość"
    }
}


payload = {}

result = run_plugin(SmtpDispatcherAction, init, payload)
print(result)
print(result.console.__dict__)
