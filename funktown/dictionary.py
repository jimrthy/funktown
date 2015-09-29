import collections

from .lookuptree import LookupTree


class ImmutableDict(collections.Mapping):
import hashlib

from .lookuptree import LookupTree


def hash2(x):
    # Can't just use the hash object directly:
    # LookupTree relies on this being numeric
    h = hashlib.sha512(str(x))
    return long(h.hexdigest(), 16)


class ImmutableDict(object):
    '''An immutable dictionary class. Access, insertion, and removal
    are guaranteed to have O(log(n)) performance. Constructor takes same
    arguments as builtin dict'''

    def __init__(self, initdict=None, **kwargs):
        if initdict is None:
            initdict = {}
        else:
            # Don't want to overwrite what the caller sent
            initdict = initdict.copy()
        initdict.update(kwargs)
        hashlist = [(hash2(key), (key, initdict[key])) for key in initdict]
        fixed_up = dict(hashlist)
        #import pdb; pdb.set_trace()
        self.tree = LookupTree(fixed_up)
        self._length = len(initdict)

    def assoc(self, key, value):
        '''Returns a new ImmutableDict instance with value associated with key.
        The implicit parameter is not modified.'''
        copydict = ImmutableDict()
        copydict.tree = self.tree.assoc(hash2(key), (key, value))
        copydict._length = self._length + 1
        return copydict

    def update(self, other=None, **kwargs):
        '''Takes the same arguments as the update method in the builtin dict
        class. However, this version returns a new ImmutableDict instead of
        modifying in-place.'''
        copydict = ImmutableDict()
        if other:
            vallist = [(hash2(key), (key, other[key])) for key in other]
        else: vallist = []
        if kwargs:
            vallist += [(hash2(key), (key, kwargs[key])) for key in kwargs]
        copydict.tree = self.tree.multi_assoc(vallist)
        copydict._length = iter_length(copydict.tree)
        return copydict

    def remove(self, key):
        '''Returns a new ImmutableDict with the given key removed.'''
        copydict = ImmutableDict()
        copydict.tree = self.tree.remove(hash2(key))
        copydict._length = self._length - 1
        return copydict

    def get(self, key, default=None):
        '''Same as get method in builtin dict.'''
        try:
            return self[key]
        except KeyError: return default

    def __len__(self):
        return self._length

    def __getitem__(self, key):
        try:
            return self.tree[hash2(key)][1]
        except KeyError: raise KeyError(key)

    def __iter__(self):
        for key,val in self.tree:
            yield key

    def keys(self):
        '''Same as keys method in dict builtin.'''
        return [key for (key,val) in self.tree]

    def values(self):
        '''Same as values method in dict builtin.'''
        return [val for (key,val) in self.tree]

    def items(self):
        '''Same as items method in dict builtin.'''
        return [item for item in self.tree]

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return 'ImmutableDict('+str(self)+')'

    def __contains__(self, key):
        try:
            self.tree[hash2(key)]
            return True
        except KeyError: return False

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, collections.Mapping):
            return False

        if len(self) != len(other):
            return False

        for key in self:
            if self[key] != other[key]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

def iter_length(iterable):
    try:
        return len(iterable)
    except:
        i = 0
        for x in iterable:
            i+=1
        return i
