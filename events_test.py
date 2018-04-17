import io
import csv

import pytest

import events
import util


@pytest.fixture
def smalldatafile():
    test_data = """entry_time,exit_time
2012-12-01 05:48:00,2012-12-01 11:02:00
2012-12-01 06:57:00,2012-12-01 09:52:00
2012-12-01 10:25:00,2012-12-01 12:01:00
2012-12-01 10:40:00,2012-12-01 10:59:00
2012-12-01 10:46:00,2012-12-01 11:27:00
"""
    ifil = io.StringIO(test_data)
    return ifil

@pytest.fixture
def smalldataevents():
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
    return expected

@pytest.fixture
def multidayevents():
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
        ("entry", util.destringify("2012-12-02 05:48:00")),
        ("entry", util.destringify("2012-12-02 06:57:00")),
        ("exit", util.destringify("2012-12-02 09:52:00")),
        ("entry", util.destringify("2012-12-02 10:25:00")),
        ("entry", util.destringify("2012-12-02 10:40:00")),
        ("exit", util.destringify("2012-12-02 11:02:00")),
        ("exit", util.destringify("2012-12-02 11:27:00")),
        ("exit", util.destringify("2012-12-02 12:01:00")),
        ]
    return expected

def test_to_event_stream(smalldatafile, smalldataevents):
    recordgen = util.recordsFromStream(smalldatafile)
    for ii, event in enumerate(events.to_event_stream(recordgen)):
        assert event == smalldataevents[ii]

def test_tallyPop(smalldatafile, smalldataevents):
    expected = []
    pop = 0
    for ev in smalldataevents:
        if ev[0] == "entry":
            pop += 1
        else:
            pop -= 1
        expected.append(pop)

    for ii, event in enumerate(events.tallyPopulation(smalldataevents)):
        assert event[0] == smalldataevents[ii][0]
        assert event[1] == smalldataevents[ii][1]
        assert event[2]['pop'] == expected[ii]

def test_daily_highs(multidayevents):
    c, r = events.makeHighestDaysMonitorReporter(2)

    events.consumePEvent(events.tallyPopulation(multidayevents), c)

    results = r()
    assert len(results) == 2
    print(results)
    assert False
