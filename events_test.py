import io
import csv

import events
import util

def test_to_event_stream():
    test_data = """entry_time,exit_time
2012-12-01 05:48:00,2012-12-01 11:02:00
2012-12-01 06:57:00,2012-12-01 09:52:00
2012-12-01 10:25:00,2012-12-01 12:01:00
2012-12-01 10:40:00,2012-12-01 10:59:00
2012-12-01 10:46:00,2012-12-01 11:27:00
"""
    expected = [
        ("entry", util.destringify("2012-12-01 05:48:00")),
        ("entry", util.destringify("2012-12-01 06:57:00")),
        ("exit", util.destringify("2012-12-01 09:52:00")),
        ("entry", util.destringify("2012-12-01 10:25:00")),
        ("entry", util.destringify("2012-12-01 10:40:00")),
        ("entry", util.destringify("2012-12-01 10:46:00")),
        ("exit", util.destringify("2012-12-01 10:59:00")),
        ("exit", util.destringify("2012-12-01 11:02:00")),
        ("exit", util.destringify("2012-12-01 11:27:00")),
        ("exit", util.destringify("2012-12-01 12:01:00")),
        ]

    ifil = io.StringIO(test_data)
    recordgen = util.recordsFromStream(ifil)
    for ii, event in enumerate(events.to_event_stream(recordgen)):
        assert event == expected[ii]
