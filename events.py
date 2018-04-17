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
        curday = event[1].split(maxsplit=1)[0]
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

def consumePEvent(popEvents, eat):
    for pevent in popEvents:
        eat(pevent)

