import re

from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

from tracardi_day_night_split.model.configuration import Configuration
from tracardi_day_night_split.service.day_night_checker import is_day


def validate(config: dict):
    return Configuration(**config)


class DayNightSplitAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    @staticmethod
    def _validate_timezone(timezone):
        regex = re.compile('^[a-zA-z\-]+\/[a-zA-z\-]+$', re.I)
        return regex.match(str(timezone))

    async def run(self, payload):
        dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)
        time_zone = dot[self.config.timezone]

        if not self._validate_timezone(time_zone):
            raise ValueError("Your configuration {} points to value {}. And the value is not valid time zone.".format(
                self.config.timezone, time_zone
            ))

        if is_day(time_zone):
            return Result(value=payload, port="day"), Result(value=None, port="night")

        return Result(value=None, port="day"), Result(value=payload, port="night")


def register() -> Plugin:
    return Plugin(
        start=False,
        debug=False,
        spec=Spec(
            module='tracardi_day_night_split.plugin',
            className='DayNightSplitAction',
            inputs=['payload'],
            outputs=["day", "night"],
            manual='day_night_split_action',
            init={
                "timezone": "session@context.time.tz"
            },
            version="0.6.0",
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id="timezone",
                            name="Timezone",
                            description="Path to timezone data or timezone itself.",
                            component=FormComponent(type="dotPath", props={"label": "timezone"})
                        )
                    ]
                ),
            ]),
        ),
        metadata=MetaData(
            name='Day/Night',
            desc='Splits workflow whether it is day or night in a given time zone.',
            type='flowNode',
            width=200,
            height=100,
            icon='dark-light',
            group=["Time"]
        )
    )
