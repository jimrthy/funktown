#!/usr/bin/env python

import uuid

import funktown

from funktown.lookuptree import LookupTree
from funktown import ImmutableDict, ImmutableVector, ImmutableList

def treetest():
    t1 = LookupTree({0:0, 32:32, 4:4})
    assert t1.get(0) == 0
    t2 = t1.assoc(36, 36)
    assert t1.get(36) is None
    assert t2.get(36) == 36
    t3 = t2.assoc(36, 35)
    assert t3.get(36) == 35
    t4 = t2.multi_assoc([(15,15), (14,14)])
    assert t4.get(15) == 15
    assert t4.get(14) == 14

def vectortest():
    v1 = ImmutableVector([0,1,2])
    v2 = v1.conj(3)
    v3 = v1.pop()
    assert len(v1) == 3
    assert len(v2) == 4
    assert len(v3) == 2
    assert v2[3] == 3
    assert v2 == [0, 1, 2, 3]
    v4 = v1 + v2
    assert v4 == [0,1,2,0,1,2,3]
    assert v4[0:4] == [0,1,2,0]
    assert 2 in v4
    assert ImmutableVector() == []

def dicttest():
    d1 = ImmutableDict(hello="world")
    d2 = d1.assoc("goodbye", "moon")
    d3 = d2.remove("hello")
    assert d1["hello"] == "world"
    assert d2["goodbye"] == "moon"
    assert d1.get("goodbye") is None
    assert d3.get("hello") is None
    assert d2 == {"hello":"world", "goodbye":"moon"}
    d4 = d2.update(ImmutableDict({"a":"b", "c":"d"}))
    assert len(d4) == 4
    assert d4['a'] == 'b'
    assert d4['c'] == 'd'
    d5 = d1.update(hola="mundo")
    assert d5['hola'] == 'mundo'
    assert 'hola' in d5
    assert ImmutableDict() == {}
    assert ImmutableDict().get(1, 2) == 2

def dict_creation_test():
    d1 = {"a": 1, "b": 2, "c": 3, 4: 'd'}
    initial_length = len(d1)
    i_d = ImmutableDict(d1, d=4)
    assert len(d1) == initial_length
    assert len(i_d) == initial_length + 1

def dict_collision_test():
    l = [uuid.uuid4() for _ in range(10000)]
    d = {str(uid):uid for uid in l}
    #import pdb; pdb.set_trace()
    i_d = ImmutableDict(d)
    assert len(i_d.keys()) == len(d.keys())
    for k in l:
        assert i_d[str(k)]

def listtest():
    l1 = ImmutableList([2, 3])
    assert l1.conj(1) == [1, 2, 3]
    assert len(l1) == 2
    assert l1.conj(1) == ImmutableList(1, l1)
    l3 = ImmutableList()
    assert len(l3) == 0
    assert l3 == ImmutableList([])

def typetest():
    l = ImmutableList()
    v = ImmutableVector()
    d = ImmutableDict()

    assert l != None
    assert v != 3
    assert d != 'a'

    assert l == v
    assert d == v
    assert d != l

if __name__ == "__main__":
    treetest()
    vectortest()
    dicttest()
    dict_creation_test()
    dict_collision_test()
    listtest()
    typetest()
    print("All tests passed")
