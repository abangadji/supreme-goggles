import io
import heapq

def to_event_stream(records):
    hp = []
    for rec in records:
        # process input stream
        i = rec['entry_time']
        o = rec['exit_time']
        if len(hp) > 0:
            if hp[0] <= i:
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

def makeHighestDaysMonitorReporter(n):
    hp = []
    curday = None
    curmax = 0
    def consumer(event):
        nonlocal curday
        nonlocal curmax
        nonlocal hp
        epop = event[-1]['pop']
        dd = event[1].date()
        if curday is None:
            curday = dd
        if curday != dd:
            # deal with storing day's day
            newelt = (curmax, dd)
            if len(hp) == n and hp[0][0] < curmax:
                heapq.heapreplace(hp, newelt)
            elif len(hp) < n:
                heapq.heappush(hp, newelt)
            curday = dd
            curmax = 0
        else:
            if epop > curmax:
                curmax = epop
    def reporter():
        nonlocal curday
        nonlocal curmax
        nonlocal hp
        if len(hp) == n and hp[0][0] < curmax:
            heapq.heapreplace(hp, (curmax, curday))
        elif len(hp) < n:
            heapq.heappush(hp, (curmax, curday))
        return hp
    return consumer, reporter

def consumePEvent(popEvents, eat):
    for pevent in popEvents:
        eat(pevent)

