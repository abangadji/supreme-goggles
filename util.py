import io
import datetime
import csv

def destringify(field):
    return datetime.datetime.strptime(field, "%Y-%m-%d %H:%M:%S")

FIELDS = ['entry_time',
        'exit_time',
        ]
FIELD_PARSER = {
        'entry_time': destringify,
        "exit_time": destringify,
        }

def recordsFromStream(istrm, fields=FIELDS, parsers=FIELD_PARSER):
    reader = csv.DictReader(istrm)
    for raw in reader:
        tmp = {}
        for fld in fields:
            p = parsers[fld]
            tmp[fld] = p(raw[fld])
        yield tmp

def recordsfromfile(path, fields=FIELDS, parsers=FIELD_PARSER):
    with open(path, newline='') as ifil:
        return recordsFromStream(ifil, fields, parsers)

