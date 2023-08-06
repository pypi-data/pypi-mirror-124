from tracardi_zapier_webhook.plugin import ZapierWebHookAction
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

init = {
    "url": "http://localhost:8686/healthcheck",
    "body": "\"test\""
}

plugin = ZapierWebHookAction(**init)

payload = {
    "content": "send message\nssdasd",
    "username": "risto"
}

results = run_plugin(ZapierWebHookAction, init, payload)
print(results)
