import csv
import datetime

from util import destringify

"""
(head -1 data/trans.csv && tail +2 data/trans.csv | sort -t',' -k1,2 -s ) > data/sorted.csv
"""

datapath = "data/sorted.csv"

def main():
    total_records = 0
    records_with_errors = []
    last_entry = None
    longest_without_entry = datetime.timedelta()
    longest_sans_at = 0
    all_accending = True
    longest_stay = datetime.timedelta()
    longest_stay_at = 0
    multday_stays = 0
    with open(datapath, r'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total_records += 1
            idt = None
            odt = None
            try:
                idt = destringify(row["entry_time"])
                if last_entry:
                    if idt >= last_entry:
                        temp = idt - last_entry
                        if temp > longest_without_entry:
                            longest_without_entry = temp
                            longest_sans_at = total_records
                    else:
                        all_accending = False
                        #records_with_errors.append(
                        #    ("non-accending entry", total_records,
                        #        row.get("entry_time")))
                last_entry = idt
            except ValueError:
                records_with_errors.append(
                    ("bad entry_time", total_records, row.get("entry_time")))
            try:
                odt = destringify(row["exit_time"])
            except ValueError:
                records_with_errors.append(
                    ("bad exit_time", total_records, row.get("exit_time")))
            if idt and odt:
                stay = odt - idt
                if stay > longest_stay:
                    longest_stay = stay
                    longest_stay_at = total_records
                if stay.days >= 1:
                    multday_stays += 1

    print("records:", total_records)
    print("all entries in accending order:", all_accending)
    print("longest stretch without entries:", longest_without_entry, "see record:", longest_sans_at)
    print("number of stays longer than 24hr:", multday_stays)
    print("longest stay:", longest_stay, "at record:", longest_stay_at)
    if len(records_with_errors) > 0:
        print("error reports:")
        for rec in records_with_errors:
            print(rec)
    else:
        print("all records have parsable datetimes for entry and exit")

if __name__ == '__main__':
    main()
