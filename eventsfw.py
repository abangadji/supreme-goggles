import multiprocessing as mp
import threading as th

POISON_PILL = "<POISON!>"

def multipleStep(processes, qin, qout):
    token = qin.get()
    while token != POISON_PILL:
        result = token
        for process in processes:
            result = process(result)
        qout.put(result)
        token = qin.get()
    qout.put(POISON_PILL)
    #qout.close()
    #qout.join_thread()

def singleProcess(process, qin, qout):
    token = qin.get()
    while token != POISON_PILL:
        result = process(token)
        qout.put(result)
        token = qin.get()
    qout.put(POISON_PILL)

def decision(decide, qin, qouts):
    token = qin.get()
    while token != POISON_PILL:
        q, tprime = decide(token, len(qouts))
        qouts[q].put(tprime)
        token = qin.get()
    for qout in qouts:
        qout.put(POISON_PILL)
    return

def fork(qin, qouts):
    token = qin.get()
    while token != POISON_PILL:
        for qout in qouts:
            qout.put(token)
        token = qin.get()
    for qout in qouts:
        qout.put(POISON_PILL)
    return

def enqueue(data, qout):
    for item in data:
        qout.put(item)
    qout.put(POISON_PILL)

def poison(*qouts):
    for qout in qouts: 
        qout.put(POISON_PILL)

def startChain(chain):
    for p in chain['STEPS']:
        p.start()
        subchains = chain.get('CHAINS')
        if subchains:
            for sc in subchains:
                startChain(sc)

def stopChain(chain):
    head = chain.get("HEAD")
    if head:
        poison(head)
    #for q in chain['QUEUES']:
    #    q.close()
    #    q.join_thread()
    for p in chain['STEPS']:
        p.join()
        subchains = chain.get('CHAINS')
        if subchains:
            for sc in subchains:
                stopChain(sc)

def chainOutput(chain):
    tail = chain.get('TAIL')
    if tail:
        return output(tail)
    return output(chain['QUEUES'][-1])

def output(qin):
    token = qin.get()
    while token != POISON_PILL:
        yield token
        token = qin.get()
    
def buildFiniteChain(initems, steps):
    q1 = mp.Queue()
    q2 = mp.Queue()

    p1 = mp.Process(target=enqueue, args=(initems, q1))
    p2 = mp.Process(target=multipleStep, args=(steps, q1, q2))

    chain = {
            "TYPE": "FINITE",
            "STEPS": [p1, p2],
            "QUEUES": [q1, q2],
            "RESULTS": output(q2),
            }
    return chain

def buildDecisionChain(decider, subchains):
    q = mp.Queue()
    chain = {
            "TYPE": "",
            "STEPS": [],
            "HEAD": q,
            "QUEUES": [q],
            "CHAINS": subchains,
            }
    qin = chain['QUEUES'][0]
    qouts = [sc['QUEUES'][0] for sc in subchains]
    if decider is None:
        chain['TYPE'] = "FORK"
        p = mp.Process(target=fork, args=(qin, qouts))
    else:
        chain['TYPE'] = "SWITCH"
        p = mp.Process(target=decision, args=(decider, qin, qouts))
    chain['STEPS'].append(p)
    return chain

def buildMultiProcessSubchain(*stepsets):
    q = mp.Queue()
    chain = {
            "TYPE": "LINEAR",
            "STEPS": [],
            "HEAD": q,
            "QUEUES": [q],
            "TAIL": None,
            }
    for stepset in stepsets:
        q1 = chain['QUEUES'][-1]
        chain['QUEUES'].append(mp.Queue())
        q2 = chain['QUEUES'][-1]
        pname = ":".join([fn.__name__ for fn in stepset])
        p = mp.Process(target=multipleStep, args=(stepset, q1, q2), name=pname)
        chain['STEPS'].append(p)
    chain['TAIL'] = chain['QUEUES'][-1]
    return chain
