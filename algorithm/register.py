# -*- coding: utf-8 -*-

class AlgRegister(object):
    _algs = {}

    @classmethod
    def has_alg(cls, alg):
        k = alg.__name__.lower()
        return k in cls._algs

    @classmethod
    def add(cls, alg):
        k = alg.__name__.lower()
        cls._algs[k] = alg

    @classmethod
    def delete(cls, alg):
        k = alg.__name__.lower()
        del cls._algs[k]

    @classmethod
    def iter(cls):
        yield cls._algs

    @classmethod
    def keys(cls):
        return cls._algs.keys()

    @classmethod
    def algcls(cls, algnm):
        return cls._algs[algnm]
