#!/usr/bin/env python3
from .Arguments import Function
import os
import json


def find_func(functions: list, func: str) -> Function | None:
    for f in functions:
        if f.name == func:
            return f
    return


def check_logits(logits: list, correct: list, banned: bool = False):
    if banned is False:
        for i in range(len(logits)):
            if i not in correct:
                logits[i] = float('-inf')
    else:
        for i in range(len(logits)):
            if i in correct:
                logits[i] = float('-inf')
    return logits


def make_path():
    path = 'data/output/function_calls.json'
    piece_of_path = path.split('/')
    piece_of_path.pop()
    path_dir = "/".join(piece_of_path)

    os.makedirs(path_dir, exist_ok=True)


def create_correct(llm, f_list):
    tmp = [llm.encode(" "+f.name).cpu().detach().numpy()[0].tolist()
        for f in f_list]
    tmp.append(llm.encode(' ').cpu().detach().numpy()[0].tolist())
    t_list = list()
    for tok in tmp:
        for t in tok:
            t_list.append(t)
    return t_list


def check_path(args: list):
    p_path = 'data/input/function_calling_tests.json'
    f_path = 'data/input/functions_definition.json'
    o_path = 'data/output/function_calling_results.json'

    if args:
        for i in range(len(args)):
            if args[i] == "--functions_definition":
               f_path = args[i + 1]
            elif args[i] == "--input":
                p_path = args[i + 1]
            elif args[i] == "--output":
                o_path = args[i + 1]
    
    return p_path, f_path, o_path


def write_output(o_path: str, result: list):
    with open(o_path, 'w') as o:
        o.write(json.dumps(result, indent=4))
