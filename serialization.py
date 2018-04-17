import datetime

FIELDS = ['entry_time',
        'exit_time',
        ]

def destringify(field):
    return datetime.datetime.strptime(field, "%Y-%m-%d %H:%M:%S")

def test_destringify():
    input = "2012-12-01 07:26:00"
    result = destringify(input)
    assert result.year == 2012
    assert result.month == 12
    assert result.day == 1
    assert result.hour == 7
    assert result.minute == 26
    assert result.second == 0
