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

def buildFoldOverWindow(windowingfn, base_val, leftfold, reportcb, extract_val):
    acc_val = base_val
    active_window = None
    def folder(event):
        nonlocal acc_val
        nonlocal active_window
        window = windowingfn(event)
        curval = extract_val(event)
        if active_window is None:
            active_window = window
        if window != active_window:
            reportcb(active_window, acc_val)
            acc_val = base_val
            active_window = window
        acc_val = leftfold(acc_val, curval)
    def endStream():
        nonlocal acc_val
        nonlocal active_window
        reportcb(active_window, acc_val)
    return folder, endStream

def nlargestPerWindow(n, extract_val, base_case, accum, windowid):
    hp = []
    prevwindow = None
    window_acc = base_case 
    def consumer(event):
        nonlocal prevwindow
        nonlocal window_acc
        nonlocal hp
        window = windowid(event)
        curval = extract_val(event)
        if prevwindow is None:
            prevwindow = window
        if window != prevwindow:
            newelt = (window_acc, prevwindow)
            if len(hp) == n and hp[0][0] < window_acc:
                heapq.heapreplace(hp, newelt)
            elif len(hp) < n:
                heapq.heappush(hp, newelt)
            prevwindow = window
            window_acc = base_case
        window_acc = accum(curval, window_acc)
    def reporter():
        nonlocal prevwindow
        nonlocal window_acc
        nonlocal hp
        # deal with storing day's day
        if len(hp) == n and hp[0][0] < window_acc:
            heapq.heapreplace(hp, (window_acc, prevwindow))
        elif len(hp) < n:
            heapq.heappush(hp, (window_acc, prevwindow))
        tmp = [heapq.heappop(hp) for ii in range(len(hp))]
        return tmp
    return consumer, reporter

def makeHighestDaysMonitorReporter(n):
    hp = []
    def folder(acc, v):
        if v > acc:
            return v
        return acc
    def extract_val(event):
        return event[-1]['pop']
    base_case = 0
    def w(event):
        return eventdate(event)
    def cb(w, acc):
        nonlocal hp
        if len(hp) == n and acc > hp[0][0]:
            heapq.heapreplace(hp, (acc, w))
        elif len(hp) < n:
            heapq.heappush(hp, (acc, w))
    proc, term =  buildFoldOverWindow(w, base_case, folder, cb, extract_val)
    def results():
        nonlocal hp
        term()
        tmp = [heapq.heappop(hp) for ii in range(len(hp))]
        return tmp
    return proc, results

def makeLowestDaysMonitorReporter(n):
    hp = []
    def folder(acc, v):
        if v < acc:
            return v
        return acc
    def extract_val(event):
        return -1 * event[-1]['pop']
    base_case = 0
    def w(event):
        return eventdate(event)
    def cb(w, acc):
        nonlocal hp
        if len(hp) == n and acc < hp[0][0]:
            heapq.heapreplace(hp, (acc, w))
        elif len(hp) < n:
            heapq.heappush(hp, (acc, w))
    proc, term =  buildFoldOverWindow(w, base_case, folder, cb, extract_val)
    def results():
        nonlocal hp
        term()
        tmp = [heapq.heappop(hp) for ii in range(len(hp))]
        return [(-1 * pop, date) for pop, date in tmp]
    return proc, results

def consumePEvent(popEvents, *eaters):
    for pevent in popEvents:
        for eater in eaters:
            eater(pevent)

