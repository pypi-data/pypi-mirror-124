import urllib.parse
import aiohttp

from tracardi.domain.resource import Resource
from tracardi.service.storage.driver import storage
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_pushover_webhook.model.pushover_config import PushOverConfiguration, PushOverAuth
from tracardi_dot_notation.dot_template import DotTemplate


def validate(config: dict) -> PushOverConfiguration:
    return PushOverConfiguration(**config)


class PushoverAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'PushoverAction':
        config = validate(kwargs)
        source = await storage.driver.resource.load(config.source.id)
        return PushoverAction(config, source)

    def __init__(self, config: PushOverConfiguration, source: Resource):
        self.pushover_config = config
        self.source = PushOverAuth(**source.config)

    async def run(self, payload):
        async with aiohttp.ClientSession() as session:

            dot = self._get_dot_accessor(payload)
            template = DotTemplate()

            data = {
                "token": self.source.token,
                "user": self.source.user,
                "message": template.render(self.pushover_config.message, dot)
            }

            result = await session.post(url='https://api.pushover.net/1/messages.json',
                                        data=urllib.parse.urlencode(data),
                                        headers={"Content-type": "application/x-www-form-urlencoded"})
            return Result(port="payload", value={
                "status": result.status,
                "body": await result.json()
            })


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_pushover_webhook.plugin',
            className='PushoverAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.6.0',
            license="MIT",
            author="Bartosz Dobrosielski, Risto Kowaczewski",
            manual="send_pushover_msg_action",
            init={
                "source": {
                    "id": "",
                    "name": ""
                },
                "message": ""
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="source",
                            name="Pushover authentication",
                            description="Select pushover resource",
                            component=FormComponent(
                                type="resource",
                                props={"label": "resource"})
                        )
                    ]
                ),
                FormGroup(
                    fields=[
                        FormField(
                            id="message",
                            name="Message",
                            description="Type message. Message can be in form of message template.",
                            component=FormComponent(
                                type="textarea",
                                props={
                                    "label": "Message template"
                                })
                        )
                    ]

                ),
            ]),

        ),
        metadata=MetaData(
            name='Pushover webhook',
            desc='Connects to Pushover app.',
            type='flowNode',
            width=200,
            height=100,
            icon='pushover',
            group=["Connectors"]
        )
    )
