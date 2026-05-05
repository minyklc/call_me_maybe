#!/usr/bin/env python3
import json
from .Function import Function, Argument, Prompt

def parsing():
    with open('data/.input/function_calling_tests.json', 'r') as f:
        prompt_data = json.load(f)
    with open('data/.input/functions_definition.json', 'r') as f:
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

    prompt_list = list()
    for prompt in prompt_data:
        prompt_list.append(Prompt(prompt=prompt['prompt']))
    return prompt_list, function_list, function_data
    