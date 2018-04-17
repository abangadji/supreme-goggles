import csv

import util
import events

def main(path, n):

    c, r = events.makeHighestDaysMonitorReporter(n)
    with open(path, newline='') as ifil:
        #recs = util.recordsFromStream(ifil)
        recs = csv.DictReader(ifil)
        evs = events.to_event_stream(recs)
        popEvents = events.tallyPopulation(evs)
        events.consumePEvent(popEvents, c)

    print("Top {} peak days".format(n))
    print("Usage Peak\tDate")
    for pop, day in r():
        print("\t{}\t{}".format(pop, day))


if __name__ == '__main__':
    path = "data/sorted.csv"
    main(path, 20)
