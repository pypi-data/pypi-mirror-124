from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_day_night_split.plugin import DayNightSplitAction


def test_plugin():
    init = {
        "latitude": "payload@x",
        "longitude": "payload@y"
    }

    result = run_plugin(DayNightSplitAction, init, {"x": "48.864716", "y": "2.349014"})
    print(result)
