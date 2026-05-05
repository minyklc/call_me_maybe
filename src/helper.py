#!/usr/bin/env python3
from .Function import Function
import numpy as np


def find_func(functions: list, func: str) -> Function | None:
    for f in functions:
        if f.name == func:
            return f
    return None


def give_args(function: Function):
    res = str()
    for a in function.arguments:
        res += f" {a.name} ({a.type})"
        if a != function.arguments[-1]:
            res += ","
    return res

def check_logits(logits: list, correct: list, banned: bool = False):
    if banned is False:
        for i in range(len(logits)):
            if i not in correct:
                # print(lo, correct)
                logits[i] = float('-inf')
            # else:
            #     print(int(logits[i]))
    else:
        for i in range(len(logits)):
            if i in correct:
                logits[i] = float('-inf')
    return logits

def find_index(function: list, name: str):
    for i in range(len(function)):
        if function[i]['name'] == name:
            return i
    return -1