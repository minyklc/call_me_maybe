#!/usr/bin/env python3
# import json
from llm_sdk import Small_LLM_Model
import numpy as np
from .helper import find_func, give_args, check_logits, find_index
# import json
from .parsing import parsing


def main():
    try:
        prompt_list, function_list, function_data = parsing()
    except FileNotFoundError as n:
        return print(n)
    except Exception as e:
        return print(e)

    # print(function_list, prompt_list, function_data)

    llm = Small_LLM_Model()
    tmp = [llm.encode(" "+f.name).cpu().detach().numpy()[0].tolist()
        for f in function_list]
    tmp.append(llm.encode(' ').cpu().detach().numpy()[0].tolist())
    f_token_name = list()
    for tok in tmp:
        for t in tok:
            f_token_name.append(t)
            # print(llm.decode(t))
    # print(f_token_name)

    banned = []
    tmp = [llm.encode(b).cpu().detach().numpy()[0].tolist()
        for b in banned]
    tmp.append(llm.encode(' ').cpu().detach().numpy()[0].tolist())
    banned_token = list()
    for tok in tmp:
        for t in tok:
            banned_token.append(t)

    # print(function_data[0]['parameters'])

    for prompt in prompt_list:
        print(prompt.prompt)
        tokens = llm.encode(
            f"""You are a function selector. Given a user request, \
            you must select the appropriate function to call.
            Available functions: 
            {function_data}
            User request: {prompt.prompt}
            The correct function to call is: """
        ).cpu().detach().numpy()[0].tolist()

        func = str()
        while True:
            logits = llm.get_logits_from_input_ids(tokens)
            logits_np = check_logits(logits, f_token_name)
            token_id = int(np.argmax(logits_np))
            # print(f"[{llm.decode(token_id)}]")
            if llm.decode(token_id).isspace():
                break
            tokens.append(token_id)
            func += llm.decode(token_id).lstrip()
        print(func)

        function = find_func(function_list, func)
        if function:
            args = '{'
            for arg in function.arguments:
                args += f'"{arg.name}":'
                tokens = llm.encode(
                    f"""Given this user request: "{prompt.prompt}"
                        Call the function: {function.name}
                        Arguments needed: {function_data[find_index(
                        function_data, function.name)]['parameters']}
                        Arguments: {args}"""
                ).cpu().detach().numpy()[0].tolist()
                # print(f"[{llm.decode(tokens)}]")

                while True:
                    logits = llm.get_logits_from_input_ids(tokens)
                    logits_np = check_logits(logits, banned_token, banned=True)
                    token_id = int(np.argmax(logits_np))
                    tokens.append(token_id)
                    args += llm.decode(token_id)
                    if ',' in llm.decode(token_id):
                        if args.count('"') % 2 == 0:
                            tokens.append(llm.encode(" ").cpu().detach().numpy()[0].tolist()[0])
                            args += llm.decode(tokens[-1])
                            break
                    elif '}' in llm.decode(token_id):
                        if args.count('}') == args.count('{'):
                            break
                    # print(f"[{llm.decode(tokens)}]")
                    # print(f"[{args}]")
            print(args, '\n')
                            
            # tokens = llm.encode(
            #     f"""Given this user request: "{prompt.prompt}"
            #         Call the function: {function.name}
            #         Arguments needed: {function_data[find_index(
            #         function_data, function.name)]['parameters']}
            #         Arguments in json: """
            # ).cpu().detach().numpy()[0].tolist()
            # arg = str()
            # while True:
            #     logits = llm.get_logits_from_input_ids(tokens)
            #     logits_np = check_logits(logits, banned_token, banned=True)
            #     token_id = int(np.argmax(logits_np))
            #     if '}' in llm.decode(token_id):
            #         break
            #     tokens.append(token_id)
            #     arg += llm.decode(token_id)
            #     # print(arg)
            # arg += llm.decode(token_id)
            # print(arg, '\n')


if __name__ == "__main__":
    main()