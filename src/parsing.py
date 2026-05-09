#!/usr/bin/env python3
import json
from .Arguments import Function, Argument, Prompt

def parsing(p_path: str, f_path: str):
    with open(p_path, 'r') as f:
        prompt_data = json.load(f)
    with open(f_path, 'r') as f:
        function_data = json.load(f)

    function_list = list()
    for function in function_data:
        function_list.append(
            Function(
                name=function['name'],
                description=function['description'],
                arguments=[Argument(
                    name=a,
                    type=function['parameters'][a]['type']) \
                                  for a in function['parameters']],
                returns=Argument(
                    name='returns',
                    type=function['returns']['type']
                )
            )
        )
    if not function_list:
        raise ValueError('must contains at least one definition')

    prompt_list = list()
    for prompt in prompt_data:
        prompt_list.append(Prompt(prompt=prompt['prompt']))
    if not prompt_list:
        raise ValueError('must contains at least one prompt')

    return prompt_list, function_list, function_data
    