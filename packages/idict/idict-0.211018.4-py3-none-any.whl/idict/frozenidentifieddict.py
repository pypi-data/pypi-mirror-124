#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
#
import operator
from functools import reduce
from random import Random
from typing import Dict, TypeVar, Union, Callable

from garoupa import ø40, Hosh
from ldict import FunctionSpace
from ldict.core.base import AbstractLazyDict, AbstractMutableLazyDict
from ldict.frozenlazydict import FrozenLazyDict
from ldict.parameter.abslet import AbstractLet

from idict.appearance import decolorize, ldict2txt
from idict.core.identification import key2id, blobs_hashes_hoshes

VT = TypeVar("VT")


class FrozenIdentifiedDict(AbstractLazyDict):
    """Immutable lazy universally identified dict for serializable (picklable) pairs str->value

    Usage:

    >>> from idict.frozenidentifieddict import FrozenIdentifiedDict as idict
    >>> print(idict())
    {
        "id": "0000000000000000000000000000000000000000",
        "ids": {}
    }
    >>> d = idict(x=5, y=3)
    >>> print(d)
    {
        "x": 5,
        "y": 3,
        "id": "Xt_6cc13095bc5b4c671270fbe8ec313568a8b35",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "XB_1cba4912b6826191bcc15ebde8f1b960282cd"
        }
    }
    >>> d["y"]
    3
    >>> print(idict(x=123123, y=88))
    {
        "x": 123123,
        "y": 88,
        "id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "ids": {
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> print(idict(y=88, x=123123))
    {
        "y": 88,
        "x": 123123,
        "id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "ids": {
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e"
        }
    }
    >>> d = idict(x=123123, y=88)
    >>> d2 = d >> (lambda x: {"z": x**2})
    >>> d2.hosh == d2.identity * d2.ids["z"] * d2.ids["x"] * d2.ids["y"]
    True
    >>> e = d2 >> (lambda x,y: {"w": x/y})
    >>> print(e)
    {
        "w": "→(x y)",
        "z": "→(x)",
        "x": 123123,
        "y": 88,
        "id": "96PdbhpKgueRWa.LSQWcSSbr.ZMZsuLzkF84sOwe",
        "ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "z": ".JXmafqx65TZ-laengA5qxtk1fUJBi6bgQpYHIM8",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> a = d >> (lambda x: {"z": x**2}) >> (lambda x, y: {"w": x/y})
    >>> b = d >> (lambda x, y: {"w": x/y}) >> (lambda x: {"z": x**2})
    >>> dic = d.asdict  # Converting to dict
    >>> dic
    {'x': 123123, 'y': 88, 'id': 'dR_5b58200b12d6f162541e09c570838ef5a429e', 'ids': {'x': '4W_3331a1c01e3e27831cf08b7bde9b865db7b2e', 'y': '9X_c8cb257a04eba75c381df365a1e7f7e2dc660'}}
    >>> d2 = idict(dic)  # Reconstructing from a dict
    >>> print(d2)
    {
        "x": 123123,
        "y": 88,
        "id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "ids": {
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> d == d2
    True
    >>> from idict import Ø
    >>> d = idict() >> {"x": "more content"}
    >>> print(d)
    {
        "x": "more content",
        "id": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff",
        "ids": {
            "x": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff"
        }
    }
    """
    hosh: Hosh

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, id=None, ids=None, rnd=None, identity=ø40, _cloned=None, **kwargs):
        self.rnd = rnd
        self.identity = identity
        data = _dictionary or {}
        data.update(kwargs)

        # Freeze mutable *dicts.
        for k, v in data.items():
            if isinstance(v, AbstractMutableLazyDict):
                data[k] = v.frozen

        if _cloned:
            self.blobs = _cloned["blobs"]
            self.hashes = _cloned["hashes"]
            self.hoshes = _cloned["hoshes"]
            self.hosh = _cloned["hosh"]
        else:
            if "id" in data:
                if id:  # pragma: no cover
                    raise Exception(f"Conflicting 'id' values: {id} and {data['id']}")
                id = data.pop("id")
            if "ids" in data:
                if ids:  # pragma: no cover
                    raise Exception(f"Conflicting 'ids' values: {ids} and {data['ids']}")
                ids = data.pop("ids")

            if id:
                if ids is None:  # pragma: no cover
                    raise Exception(f"'id' {id} given, but 'ids' is missing.")
                self.blobs = {}
                self.hashes = {}
                self.hoshes = {k: identity * v for k, v in ids.items()}
            else:
                self.blobs, self.hashes, self.hoshes = blobs_hashes_hoshes(data, identity, ids or {}).values()
            self.hosh = reduce(operator.mul, [identity] + list(self.hoshes.values()))

        if id is None:
            id = self.hosh.id
            try:
                ids = {k: v.id for k, v in self.hoshes.items()}
            except:
                print(self.hoshes)
                raise Exception()

        # Store as an immutable lazy dict.
        self.frozen = FrozenLazyDict(data, id=id, ids=ids, rnd=rnd)
        self.data = self.frozen.data
        self.id = self.hosh.id

    def __getitem__(self, item):
        return self.frozen[item]

    def __setitem__(self, key: str, value):
        self.frozen[key] = value

    def __delitem__(self, key):
        del self.frozen[key]

    def __getattr__(self, item):
        return getattr(self.frozen, item)

    def __repr__(self):
        return repr(self.frozen)

    __str__ = __repr__

    def evaluate(self):
        """
        >>> from idict.frozenidentifieddict import FrozenIdentifiedDict as idict
        >>> f = lambda x: {"y": x+2}
        >>> d = idict(x=3)
        >>> a = d >> f
        >>> print(a)
        {
            "y": "→(x)",
            "x": 3,
            "id": "tFkvrmyHlXSnstVFIFktJjD7K91yW4AU0sYuSnwe",
            "ids": {
                "y": "BZz1P5xA5r0gfAqOtHySEb.m0HTxW4AU0sYuSnwe",
                "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
            }
        }
        >>> a.evaluate()
        >>> print(a)
        {
            "y": 5,
            "x": 3,
            "id": "tFkvrmyHlXSnstVFIFktJjD7K91yW4AU0sYuSnwe",
            "ids": {
                "y": "BZz1P5xA5r0gfAqOtHySEb.m0HTxW4AU0sYuSnwe",
                "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
            }
        }
        """
        self.frozen.evaluate()

    @property
    def asdict(self):
        """
        >>> from idict.frozenidentifieddict import FrozenIdentifiedDict as idict
        >>> d = idict(x=3, y=5)
        >>> d.id
        'Xt_a63010fa2b5b4c671270fbe8ec313568a8b35'
        >>> e = idict(x=7, y=8, d=d)
        >>> e.asdict
        {'x': 7, 'y': 8, 'd': {'x': 3, 'y': 5, 'id': 'Xt_a63010fa2b5b4c671270fbe8ec313568a8b35', 'ids': {'x': 'WB_e55a47230d67db81bcc1aecde8f1b950282cd', 'y': '0U_e2a86ff72e226d5365aea336044f7b4270977'}}, 'id': 'AN_650bae25143e28c5489bfbc806f5fb55c6fdc', 'ids': {'x': 'lX_9e55978592eeb1caf8778e34d26f5fd4cc8c8', 'y': '6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde', 'd': '8s_1ccd1655bae1d9e91270e5eddc31351eb8b35'}}
        >>> d.hosh ** key2id("d", d.identity.digits) == e.hoshes["d"]
        True
        """
        return self.frozen.asdic

    def __rrshift__(self, left: Union[Random, Dict, Callable, FunctionSpace]):
        if isinstance(left, Random):
            return self.clone(rnd=left)
        if isinstance(left, Dict) and not isinstance(left, AbstractLazyDict):
            return FrozenIdentifiedDict(left) >> self
        if callable(left):
            return FunctionSpace(left, self)
        return NotImplemented

    def __rshift__(self, other: Union[Dict, AbstractLazyDict, Callable, AbstractLet, FunctionSpace, Random]):
        from idict import iEmpty
        from idict.core.rshift import application, ihandle_dict
        if isinstance(other, iEmpty):
            return self
        if isinstance(other, Random):
            return self.clone(rnd=other)
        if isinstance(other, FunctionSpace):
            return reduce(operator.rshift, (self,) + other.functions)
        if isinstance(other, AbstractLet):
            return application(self, other, other.f, other.asdict.encode())
        if callable(other):
            return application(self, other, other, self.identity)
        if isinstance(other, Dict):
            return ihandle_dict(self, other)
        return NotImplemented

    def clone(self, data=None, rnd=None, _cloned=None):
        cloned_internals = _cloned or dict(blobs=self.blobs, hashes=self.hashes, hoshes=self.hoshes, hosh=self.hosh)
        return FrozenIdentifiedDict(
            data or self.data, rnd=rnd or self.rnd, identity=self.identity, _cloned=cloned_internals
        )

    def __hash__(self):
        return hash(self.hosh)

    def show(self, colored=True):
        r"""
        >>> from idict.frozenidentifieddict import FrozenIdentifiedDict as idict
        >>> idict(x=134124, y= 56).show(colored=False)
        {
            "x": 134124,
            "y": 56,
            "id": "dq_d85091ef315b9ce0d5eb1a5aabb6e6434a97f",
            "ids": {
                "x": "gZ_37ee5e71c9cd4c9bde421cdb917e5c56f7ebe",
                "y": "Zs_c473399e77e6c2d2f69914891a488a3732bb0"
            }
        }
        """
        return print(self.all if colored else decolorize(self.all))

    def __repr__(self, all=False):
        return ldict2txt(self, all)

    @property
    def all(self):
        r"""
        Usage:

        >>> from idict.frozenidentifieddict import FrozenIdentifiedDict as idict
        >>> from idict.appearance import decolorize
        >>> out = idict(x=134124, y= 56).all
        >>> decolorize(out)
        '{\n    "x": 134124,\n    "y": 56,\n    "id": "dq_d85091ef315b9ce0d5eb1a5aabb6e6434a97f",\n    "ids": {\n        "x": "gZ_37ee5e71c9cd4c9bde421cdb917e5c56f7ebe",\n        "y": "Zs_c473399e77e6c2d2f69914891a488a3732bb0"\n    }\n}'
        """
        return self.__repr__(all=True)

    def __eq__(self, other):
        if isinstance(other, Dict):
            if "id" in other:
                return self.id == other["id"]
            if list(self.keys())[:-2] != list(other.keys()):
                return False
        from idict.core.idict_ import Idict
        if isinstance(other, (FrozenIdentifiedDict, Idict)):
            return self.hosh == other.hosh
        if isinstance(other, AbstractLazyDict):
            if self.keys() != other.keys():
                return False
            other.evaluate()
            return self.data == other.data
        if isinstance(other, Dict):
            data = self.data.copy()
            del data["id"]
            del data["ids"]
            return data == other
        raise TypeError(f"Cannot compare {type(self)} and {type(other)}")  # pragma: no cover
