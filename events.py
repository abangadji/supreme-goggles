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

