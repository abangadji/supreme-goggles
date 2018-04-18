import io
import heapq

def to_event_stream(records):
    hp = []
    for rec in records:
        # process input stream
        i = rec['entry_time']
        o = rec['exit_time']
        while len(hp) > 0 and hp[0] <= i:
            yield ("exit", heapq.heappop(hp))
        yield ("entry", i)
        heapq.heappush(hp, o)
        
    for _ in range(len(hp)):
        yield ("exit", heapq.heappop(hp))

def tallyPopulation(events):
    pop = 0
    for event in events:
        if event[0] == "entry":
            pop +=1
        elif event[0] == 'exit':
            pop -= 1
        yield (event[0], event[1], {"pop": pop})

def eventdate(event):
    return event[1].split(maxsplit=1)[0]

def tallyDailyIntegral(events):
    prevevent = None
    area = 0
    for event in events:
        if prevevent is None:
            prevevent = event
        if prevevent != event:
            if eventdate(prevevent) != eventdate(event):
                yield (area, eventdate(prevevent))
                area = 0
            prevpop = prevevent[2]['pop']
            td = event[1] - prevevent[1]
            tmparea = prevpop * td.total_seconds()
            area += temparea
    yield (area, prevevent[1].date())

def makeCounter():
    count = 0
    def consumer(event):
        nonlocal count 
        count == 1
    def reporter():
        nonlocal count
        return count
    return consumer, reporter

def makeHighestDaysMonitorReporter(n):
    hp = []
    prevday = None
    curmax = 0
    def consumer(event):
        nonlocal prevday
        nonlocal curmax
        nonlocal hp
        epop = event[-1]['pop']
        #curday = event[1].date()
        curday = eventdate(event)
        if prevday is None:
            prevday = curday
        if curday != prevday:
            # deal with storing day's day
            newelt = (curmax, prevday)
            if len(hp) == n and hp[0][0] < curmax:
                heapq.heapreplace(hp, newelt)
            elif len(hp) < n:
                heapq.heappush(hp, newelt)
            prevday = curday
            curmax = 0
        else:
            if epop > curmax:
                curmax = epop
    def reporter():
        nonlocal prevday
        nonlocal curmax
        nonlocal hp
        # deal with storing day's day
        if len(hp) == n and hp[0][0] < curmax:
            heapq.heapreplace(hp, (curmax, prevday))
        elif len(hp) < n:
            heapq.heappush(hp, (curmax, prevday))
        tmp = [heapq.heappop(hp) for ii in range(len(hp))]
        return tmp
    return consumer, reporter

def makeLowestDaysMonitorReporter(n):
    hp = []
    prevday = None
    curmax = 0
    def consumer(event):
        nonlocal prevday
        nonlocal curmax
        nonlocal hp
        epop = event[-1]['pop']
        #curday = event[1].date()
        curday = event[1].split(maxsplit=1)[0]
        if prevday is None:
            prevday = curday
        if curday != prevday:
            # deal with storing day's day
            newelt = (curmax * -1, prevday)
            if len(hp) == n and hp[0][0] < newelt[0]:
                heapq.heapreplace(hp, newelt)
                #heapq._heapreplace_max(hp, newelt)
            elif len(hp) < n:
                heapq.heappush(hp, newelt)
            prevday = curday
            curmax = 0
        else:
            if epop > curmax:
                curmax = epop
    def reporter():
        nonlocal prevday
        nonlocal curmax
        nonlocal hp
        # deal with storing day's day
        newelt = (curmax * -1, prevday)
        if len(hp) == n and hp[0][0] < newelt[0]:
            heapq.heapreplace(hp, newelt)
        elif len(hp) < n:
            heapq.heappush(hp, newelt)
        tmp = [heapq.heappop(hp) for ii in range(len(hp))]
        return [(-1 * pop, date) for pop, date in tmp]
    return consumer, reporter

def consumePEvent(popEvents, *eaters):
    for pevent in popEvents:
        for eater in eaters:
            eater(pevent)

