from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, FormGroup, Form, FormField, FormComponent
from tracardi_plugin_sdk.domain.result import Result
from tracardi_weather.model.configuration import PluginConfiguration, WeatherResult
from tracardi_weather.service.weather_client import AsyncWeatherClient


def validate(config: dict) -> PluginConfiguration:
    return PluginConfiguration(**config)


class WeatherAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)
        self.client = AsyncWeatherClient(self.config.system.upper())

    async def run(self, payload):

        city = self.config.city

        dot = self._get_dot_accessor(payload)
        city = dot[city]
        result = WeatherResult()

        weather = await self.client.fetch(city)

        result.temperature = weather.current.temperature
        result.humidity = weather.current.humidity
        result.wind_speed = weather.current.wind_speed
        result.description = weather.current.sky_text

        return Result(port="weather", value=result.dict())


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_weather.plugin',
            className='WeatherAction',
            inputs=["payload"],
            outputs=['weather'],
            version='0.6.0',
            license="MIT",
            author="Risto Kowaczewski",
            manual="weather_action",
            init={
                "system": "C",
                "city": None
            },
            form=Form(groups=[
                FormGroup(
                    name="Weather configuration",
                    fields=[
                        FormField(
                            id="system",
                            name="Metric system",
                            description="Select metric system.",
                            component=FormComponent(type="select", props={
                                "label": "Metric system",
                                "items": {
                                    "C": "Celsius",
                                    "F": "Fahrenheit"
                                }
                            })
                        ),
                        FormField(
                            id="city",
                            name="City",
                            description="Type city or path to city data.",
                            component=FormComponent(type="dotPath", props={})
                        )
                    ])
            ]),
        ),
        metadata=MetaData(
            name='Weather service',
            desc='Retrieves weather information.',
            type='flowNode',
            width=200,
            height=100,
            icon='weather',
            group=["Connectors"]
        )
    )
