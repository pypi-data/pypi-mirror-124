from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi_weather.plugin import WeatherAction


def test_weather_plugin_plain_text():
    init = {
        "system": "metric",
        "city": "Wrocław"
    }

    payload = {}
    result = run_plugin(WeatherAction, init, payload)

    assert 'temperature' in result.output.value
    assert 'humidity' in result.output.value
    assert 'wind_speed' in result.output.value
    assert 'description' in result.output.value


def test_weather_plugin_path():
    init = {
        "system": "metric",
        "city": "payload@city"
    }

    payload = {"city": "Wrocław"}

    result = run_plugin(WeatherAction, init, payload)

    assert 'temperature' in result.output.value
    assert 'humidity' in result.output.value
    assert 'wind_speed' in result.output.value
    assert 'description' in result.output.value