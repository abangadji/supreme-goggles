import io
import csv
import itertools

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
def multidayeventstrs():
    expected = [
        ("entry", "2012-12-01 05:48:00"),
        ("entry", "2012-12-01 06:57:00"),
        ("exit", "2012-12-01 09:52:00"),
        ("entry", "2012-12-01 10:25:00"),
        ("entry", "2012-12-01 10:40:00"),
        ("entry", "2012-12-01 10:46:00"),
        ("exit", "2012-12-01 10:59:00"),
        ("exit", "2012-12-01 11:02:00"),
        ("exit", "2012-12-01 11:27:00"),
        ("exit", "2012-12-01 12:01:00"),
        ("entry", "2012-12-02 05:48:00"),
        ("entry", "2012-12-02 06:57:00"),
        ("exit", "2012-12-02 09:52:00"),
        ("entry", "2012-12-02 10:25:00"),
        ("entry", "2012-12-02 10:40:00"),
        ("exit", "2012-12-02 11:02:00"),
        ("exit", "2012-12-02 11:27:00"),
        ("exit", "2012-12-02 12:01:00"),
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

def test_tallDailyIntegral(multidayeventstrs):
    evs = [
        ("entry", "2012-12-01 01:01:00"),
        ("entry", "2012-12-01 01:02:00"),
        ("entry", "2012-12-01 01:03:00"),
        ("exit", "2012-12-01 01:04:00"),
        ("exit", "2012-12-01 01:05:00"),
        ("exit", "2012-12-01 01:06:00"),
        ("entry", "2012-12-02 01:01:00"),
        ("entry", "2012-12-02 01:02:00"),
        ("entry", "2012-12-02 01:03:00"),
        ("exit", "2012-12-02 01:04:00"),
        ("exit", "2012-12-02 01:05:00"),
        ("exit", "2012-12-02 01:06:00"),
        ("entry", "2012-12-02 02:01:00"),
        ("entry", "2012-12-02 02:02:00"),
        ("entry", "2012-12-02 02:03:00"),
        ("exit", "2012-12-02 02:04:00"),
        ("exit", "2012-12-02 02:05:00"),
        ("exit", "2012-12-02 02:06:00"),
        ("entry", "2012-12-03 23:59:00"),
        ("exit", "2012-12-04 00:01:00"),
        ]
    pops = events.tallyPopulation(multidayeventstrs)
    integrals = events.tallyDailyIntegral(pops)
    
    expected = [
            (60+120+180+12+60, "2012-12-01"),
            ((60+120+180+12+60) *2, "2012-12-02"),
            ((60), "2012-12-03"),
            ((60), "2012-12-04"),
            ]

def test_high_daily_peaks(multidayeventstrs):
    c, r = events.makeHighestDaysMonitorReporter(2)
    events.consumePEvent(events.tallyPopulation(multidayeventstrs), c)
    results = r()
    assert len(results) == 2
    print(results)
    assert results[0][0] == 3
    assert results[0][1] == "2012-12-02"
    assert results[1][0] == 4
    assert results[1][1] == "2012-12-01"

def test_low_daily_peaks(multidayeventstrs):
    c, r = events.makeLowestDaysMonitorReporter(2)
    events.consumePEvent(events.tallyPopulation(multidayeventstrs), c)
    results = r()
    assert len(results) == 2
    print(results)
    assert results[0][0] == 4
    assert results[0][1] == "2012-12-01"

    assert results[1][0] == 3
    assert results[1][1] == "2012-12-02"

def test_buildFoldOverWindow_streakcounter():
    def w(e):
        return e
    def foldfn(acc, v):
        return acc+1
    base = 0
    results = []
    def cb(w, v):
        nonlocal results
        results.append( (w, v) )
    def getval(v):
        return v
    (folder, term) = events.buildFoldOverWindow(w, base, foldfn, cb, getval)
    streams = [
            [1] * 3,
            [2] * 2,
            [1] * 5,
            [3] * 3,
            ]
    expect = [ (v[0], len(v) ) for v in streams ]
    s = itertools.chain(*streams)
    for i in s:
        folder(i)
    term()
    for ii, v in enumerate(expect):
        assert v == results[ii]

def test_buildFoldOverWindow_maxoverwindow():
    def w(e):
        return e // 10
    def foldfn(acc, v):
        if v > acc:
            return v
        return acc
    base = 0
    results = []
    def cb(w, v):
        nonlocal results
        results.append( (w, v) )
    def getval(v):
        return v % 10
    (folder, term) = events.buildFoldOverWindow(w, base, foldfn, cb, getval)
    rangestops = [5, 7, 8,2, 6]
    streams = [ range(ii*10, ii*10+v) for ii, v in enumerate(rangestops)]
    s = itertools.chain(*streams)
    for i in s:
        folder(i)
    term()
    for ii, v in enumerate(results):
        assert v[1] == rangestops[ii] -1
        assert v[0] == ii
