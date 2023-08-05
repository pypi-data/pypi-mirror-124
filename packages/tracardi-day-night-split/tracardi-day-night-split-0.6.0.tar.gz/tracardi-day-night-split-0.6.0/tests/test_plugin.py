from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_day_night_split.plugin import DayNightSplitAction


def test_plugin():
    init = {
        "timezone": "europe/warsaw"
    }

    result = run_plugin(DayNightSplitAction, init, {})
    print(result)