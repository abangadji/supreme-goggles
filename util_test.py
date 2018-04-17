import io
import util

def test_destringify():
    input = "2012-12-01 07:26:00"
    result = util.destringify(input)
    assert result.year == 2012
    assert result.month == 12
    assert result.day == 1
    assert result.hour == 7
    assert result.minute == 26
    assert result.second == 0

def test_records_from_stream():
    test_data = """entry_time,exit_time
2012-12-01 05:48:00,2012-12-01 11:02:00
2012-12-01 06:57:00,2012-12-01 09:52:00
"""
    expected = [
            {"entry_time": util.destringify("2012-12-01 05:48:00"),
                "exit_time": util.destringify("2012-12-01 11:02:00"),
                },
            {"entry_time": util.destringify("2012-12-01 06:57:00"),
                "exit_time": util.destringify("2012-12-01 09:52:00"),
                },
            ]

    ifil = io.StringIO(test_data)
    recordgen = util.recordsFromStream(ifil)
    for ii, rec in enumerate(recordgen):
        assert rec == expected[ii]
