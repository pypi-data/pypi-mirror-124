from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.domain.result import Result
from tracardi_string_operations.model.configuration import Configuration
from tracardi_string_operations.service.operations import convert


def validate(config: dict) -> Configuration:
    return Configuration(**config)


class StringOperatorActions(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):
        dot = self._get_dot_accessor(payload)
        string = dot[self.config.string]

        if not isinstance(string, str):
            raise ValueError("Provided string is not string it is `{}`".format(type(string)))

        return Result(port="payload", value=convert(string))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_string_operations.plugin',
            className='StringOperatorActions',
            inputs=["payload"],
            outputs=['payload'],
            version='0.6.0',
            license="MIT",
            author="Patryk Migaj",
            manual="string_properties_action",
            init={
                "string": ""
            },
            form=Form(groups=[
                FormGroup(
                    name="String transformator settings",
                    fields=[
                        FormField(
                            id="string",
                            name="Path to string",
                            description="Select source and path to string.",
                            component=FormComponent(type="forceDotPath", props={})
                        )
                    ])
            ]),
        ),
        metadata=MetaData(
            name='String properties',
            desc='This plug-in is to make a string transformations like: lowercase remove spaces split and other',
            type='flowNode',
            width=200,
            height=100,
            icon='uppercase',
            group=["Data processing"]
        )
    )
