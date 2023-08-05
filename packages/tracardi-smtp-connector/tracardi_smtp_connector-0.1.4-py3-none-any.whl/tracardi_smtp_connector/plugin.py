from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_smtp_connector.model.smtp import Configuration, Smtp
from tracardi_smtp_connector.service.sendman import PostMan
from tracardi.service.storage.driver import storage
from tracardi.domain.resource import Resource
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_dot_notation.dot_template import DotTemplate


def validate(config: dict) -> Configuration:
    return Configuration(**config)


class SmtpDispatcherAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'SmtpDispatcherAction':
        config = validate(kwargs)
        source = await storage.driver.resource.load(config.source.id)
        plugin = SmtpDispatcherAction(config, source)
        return plugin

    def __init__(self, config: Configuration, source: Resource):
        self.config = config
        self.post = PostMan(Smtp(**source.config))

    async def run(self, payload):
        try:
            dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)
            template = DotTemplate()
            self.post.send(template.render(self.config.message, dot))
            return Result(port='payload', value={"result": True})
        except Exception as e:
            self.console.warning(repr(e))
            return Result(port='payload', value={"result": False})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_smtp_connector.plugin',
            className='SmtpDispatcherAction',
            inputs=["payload"],
            outputs=['payload'],
            init={
                "source": {
                    "id": None
                },
                'message': {
                    "send_to": None,
                    "send_from": None,
                    "reply_to": None,
                    "title": None,
                    "message": None
                }
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="source",
                            name="SMTP connection resource",
                            description="Select SMTP server resource. Credentials from selected resource will be used "
                                        "to connect the service.",
                            required=True,
                            component=FormComponent(type="resource", props={"label": "resource"})
                        )
                    ]
                ),
                FormGroup(
                    fields=[
                        FormField(
                            id="message.send_to",
                            name="E-mail to send from",
                            description="Type path to E-mail or e-mail itself.",
                            component=FormComponent(type="dotPath", props={"label": "Sender e-mail"})
                        ),
                        FormField(
                            id="message.send_from",
                            name="Recipient e-mail",
                            description="Type path to E-mail or e-mail itself.",
                            component=FormComponent(type="dotPath", props={"label": "Recipient e-mail"})
                        ),
                        FormField(
                            id="message.reply_to",
                            name="Reply to e-mail",
                            description="Type path to E-mail or e-mail itself.",
                            component=FormComponent(type="dotPath", props={"label": "Reply to e-mail"})
                        ),
                        FormField(
                            id="message.title",
                            name="Subject",
                            description="Type e-mail subject.",
                            component=FormComponent(type="text", props={"label": "Subject"})
                        ),
                        FormField(
                            id="message.message",
                            name="Message",
                            description="Type e-mail message.",
                            component=FormComponent(type="textarea", props={"label": "Message"})
                        )
                    ]
                ),
            ]),

            manual="smtp_connector_action",
            version='0.1.4',
            license="MIT",
            author="iLLu"

        ),
        metadata=MetaData(
            name='Send e-mail via SMTP',
            desc='Send mail via defined smtp server.',
            type='flowNode',
            width=200,
            height=100,
            icon='email',
            group=["Connectors"]
        )
    )
