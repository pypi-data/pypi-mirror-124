#cython: language_level=3, annotation_typing=False, c_string_encoding=utf-8, binding=True
# THIS FILE IS GENERATED - DO NOT EDIT #

from typing import Any
from collections.abc import Generator
import cython  # type: ignore
from cython import (declare as decl, address as addr, sizeof, typeof, struct, cfunc, ccall, nogil, no_gc, inline,
                    union, typedef, cast, char, short, int as cint, bint, short, double, long, longdouble,
                    longdoublecomplex, longlong, complex, float as cfloat)

from pyrsistent import (
    pset, 
    pmap, 
    pvector, 
    s, v, m
)
from Aspidites.woma import *
from Aspidites._vendor import (
    take,
    drop,
    takelast,
    droplast,
    consume,
    nth,         
    first_true,  
    iterate,     
    padnone,     
    ncycles,     
    repeatfunc,  
    grouper,     
    group_by,    
    roundrobin,  
    partition,   
    splitat,     
    splitby,     
    powerset,    
    pairwise,    
    iter_suppress,
    flatten,     
    accumulate,  
    reduce,      
    filterfalse, 
    zip_longest,
    call,   
    apply,  
    flip,   
    curry,  
    zipwith,
    foldl,  
    foldr,  
    unfold,
    Capture,
    Strict,
    OneOf,
    AllOf,
    NoneOf,
    Not,
    Each,
    EachItem,
    Some,
    Between,
    Length,
    Contains,
    Regex,
    Check,
    InstanceOf,
    SubclassOf,
    Arguments,
    Returns,
    Transformed,
    At,
    Object,
    match as __match,
    _,
)
from Aspidites.monads import Maybe, Surely
from Aspidites.math import Undefined, SafeDiv, SafeExp, SafeMod, SafeFloorDiv, SafeUnaryAdd, SafeUnarySub, SafeFactorial
from Aspidites._vendor.contracts import contract, new_contract
from Aspidites._vendor.RestrictedPython import safe_builtins
safe_builtins['print'] = print
from Aspidites._vendor.RestrictedPython import compile_restricted as compile
safe_builtins['compile'] = compile
# DECLARATIONS TO ALLOW CONTRACTS TO TYPE CHECK #
procedure: None
coroutine: Generator
number: Any
globals().update(dict(__builtins__=safe_builtins))  # add all imports to globals


@contract()
def add(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x+y


@contract()
def sub(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return x-y


@contract()
def div(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return Maybe(SafeDiv, x, y)()


@contract()
def exp(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return Maybe(SafeExp, x, y, )()


@contract()
def mod(x : 'number' = 0, y : 'number' = 0) -> 'number':
    return Maybe(SafeMod, x, y, )()


