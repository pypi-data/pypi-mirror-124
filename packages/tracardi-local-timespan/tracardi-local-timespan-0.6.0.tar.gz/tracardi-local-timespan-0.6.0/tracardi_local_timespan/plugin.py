import re
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_local_timespan.model.configuration import TimeSpanConfiguration


def validate(config: dict) -> TimeSpanConfiguration:
    return TimeSpanConfiguration(**config)


class LocalTimeSpanAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    @staticmethod
    def _validate_timezone(timezone):
        regex = re.compile('^[a-zA-z\-]+\/[a-zA-z\-]+$', re.I)
        return regex.match(str(timezone))

    async def run(self, payload):
        dot = self._get_dot_accessor(payload)
        time_zone = dot[self.config.timezone]

        if not self._validate_timezone(time_zone):
            raise ValueError("Your configuration {} points to value {}. And the value is not valid time zone.".format(
                self.config.timezone, time_zone
            ))

        if self.config.is_in_timespan():
            return Result(value=payload, port="in"), Result(value=None, port="out")

        return Result(value=None, port="in"), Result(value=payload, port="out")


def register() -> Plugin:
    return Plugin(
        start=False,
        debug=False,
        spec=Spec(
            module='tracardi_local_timespan.plugin',
            className='LocalTimeSpanAction',
            inputs=['payload'],
            outputs=['in', 'out'],
            manual='local_time_span_action',
            version="0.6.0",
            author="Marcin Gaca, Risto Kowaczewski",
            init={
                "timezone": "session@context.time.tz",
                "start": None,
                "end": None,
            },
            form=Form(groups=[
                FormGroup(
                    name="Local time settings",
                    fields=[
                        FormField(
                            id="timezone",
                            name="Timezone",
                            description="Type type zone or path to time zone",
                            component=FormComponent(type="dotPath", props={})
                        ),
                        FormField(
                            id="start",
                            name="Start time",
                            description="Start time must be before end time.",
                            component=FormComponent(type="text", props={
                                "label": "Start time"
                            })
                        ),
                        FormField(
                            id="end",
                            name="End time",
                            description="End time must be after start time.",
                            component=FormComponent(type="text", props={
                                "label": "End time"
                            })
                        ),
                    ]
                )
            ]
            ),
        ),
        metadata=MetaData(
            name='Local time span',
            desc='Checks if an event is in given time span',
            type='flowNode',
            width=200,
            height=100,
            icon='profiler',
            group=["Time"]
        )
    )
