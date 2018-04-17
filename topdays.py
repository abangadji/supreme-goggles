import csv

import util
import events

def main(path, n):

    maxNc, maxNr = events.makeHighestDaysMonitorReporter(n)
    minNc, minNr = events.makeLowestDaysMonitorReporter(n)
    with open(path, newline='') as ifil:
        #recs = util.recordsFromStream(ifil)
        recs = csv.DictReader(ifil)
        evs = events.to_event_stream(recs)
        popEvents = events.tallyPopulation(evs)
        events.consumePEvent(popEvents, maxNc, minNc)

    print("Top {} peak days".format(n))
    print("Usage Peak\tDate")
    for pop, day in maxNr():
        print("\t{}\t{}".format(pop, day))
    print("\nLow Peak\tDate")
    for pop, day in minNr():
        print("\t{}\t{}".format(pop, day))


if __name__ == '__main__':
    path = "data/sorted.csv"
    main(path, 20)
