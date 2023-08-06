import asyncio
import aiohttp
from aiohttp import ClientConnectorError
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, FormField, FormGroup, Form, FormComponent
from tracardi_plugin_sdk.domain.result import Result
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_dot_notation.dict_traverser import DictTraverser

from tracardi_zapier_webhook.model.configuration import ZapierWebHookConfiguration


def validate(config: dict) -> ZapierWebHookConfiguration:
    return ZapierWebHookConfiguration(**config)


class ZapierWebHookAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):

        try:

            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:

                converter = DictTraverser(self._get_dot_accessor(payload))
                body_as_dict = self.config.body
                async with session.request(
                        method="POST",
                        url=str(self.config.url),
                        json=converter.reshape(body_as_dict)
                ) as response:
                    # todo add headers and cookies
                    result = {
                        "status": response.status,
                        "json": await response.json()
                    }

                    if response.status in [200, 201, 202, 203, 204]:
                        return Result(port="response", value=result), Result(port="error", value=None)
                    else:
                        return Result(port="response", value=None), Result(port="error", value=result)

        except ClientConnectorError as e:
            return Result(port="response", value=None), Result(port="error", value=str(e))

        except asyncio.exceptions.TimeoutError:
            return Result(port="response", value=None), Result(port="error", value="Zapier webhook timed out.")


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_zapier_webhook.plugin',
            className='ZapierWebHookAction',
            inputs=['payload'],
            outputs=["response", "error"],
            init={
                "url": None,
                "body": "{}",
                "timeout": 30
            },
            form=Form(groups=[
                FormGroup(
                    name="Zapier webhook settings",
                    fields=[
                        FormField(
                            id="url",
                            name="Webhook URL",
                            description="Type webhook URL to be called.",
                            component=FormComponent(type="text", props={"label": "Url"})
                        ),
                        FormField(
                            id="body",
                            name="Request body",
                            description="Type content to be send.",
                            component=FormComponent(type="json", props={"label": "JSON"})
                        ),
                    ]),
                FormGroup(
                    name="Zapier advanced settings",
                    fields=[
                        FormField(
                            id="timeout",
                            name="Timeout",
                            description="Type value in seconds for call time-out.",
                            component=FormComponent(type="text", props={"label": "Time-out"})
                        ),
                    ])
            ]),
            version="0.6.0",
            author="Risto Kowaczewski",
            license="MIT",
            manual="zapier_webhook_action"
        ),
        metadata=MetaData(
            name='Zapier webhook',
            desc='Sends message to zapier webhook.',
            type='flowNode',
            width=200,
            height=100,
            icon='zapier',
            group=["Connectors"]
        )
    )
