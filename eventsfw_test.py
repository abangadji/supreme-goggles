import time

import eventsfw

def makeEnum():
    cnt = 0
    def enumerator(token):
        nonlocal cnt
        tmp = (cnt, token)
        cnt += 1
        return tmp
    return enumerator

def test_buildFiniteChain():
    inputs = ( chr(ii) for ii in range(ord('A'), ord('z')))
    chain = eventsfw.buildFiniteChain(inputs, [makeEnum()])
    eventsfw.startChain(chain)
    #time.sleep(0.1)
    eventsfw.stopChain(chain)
    new_cnt = 0
    cc = ord('A')
    for l in chain['RESULTS']:
        assert l[0] == new_cnt
        assert l[1] == chr(cc)
        new_cnt += 1
        cc += 1

def test_buildDecisionChain():
    countto = 10000
    inputs = range(countto)

    evenchain = eventsfw.buildMultiProcessSubchain([makeEnum()])
    oddchain = eventsfw.buildMultiProcessSubchain([makeEnum()])
    evens = eventsfw.chainOutput(evenchain)
    odds = eventsfw.chainOutput(oddchain)

    def decider(token, outcount):
        assert outcount == 2
        return token % 2, token
    split = eventsfw.buildDecisionChain(decider, [evenchain, oddchain])
    eventsfw.startChain(split)
    eventsfw.enqueue(inputs, split['HEAD'])
    #time.sleep(1.0)

    expect = 1
    expectcnt = 0
    for item in odds:
        print(item)
        cnt, val = item
        assert val % 2 == 1
        assert val == expect
        expect += 2
        assert cnt == expectcnt
        expectcnt += 1

    expect = 0
    expectcnt = 0
    for item in evens:
        print(item)
        cnt, val = item
        assert val % 2 == 0
        assert val == expect
        expect += 2
        assert cnt == expectcnt
        expectcnt += 1

    eventsfw.stopChain(split)
