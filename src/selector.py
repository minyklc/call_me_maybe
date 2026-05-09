#!/usr/bin/env python3
from .helper import check_logits
import numpy as np
from .Arguments import Function


class Select():
    def __init__(self, llm, data, functions):
        self.llm = llm
        self.data = data
        self.funcs = functions


    def function(self, prompt, authorized) -> str:
        tokens = self.llm.encode(
            f"""You are a function selector. Given a user request, \
            you must select the appropriate function to call.
            Available functions: 
            {self.data}
            User request: {prompt.prompt}
            The correct function to call is: """
        ).cpu().detach().numpy()[0].tolist()

        func = str()
        while True:
            logits = self.llm.get_logits_from_input_ids(tokens)
            logits_np = check_logits(logits, authorized)
            token_id = int(np.argmax(logits_np))
            if self.llm.decode(token_id).isspace():
                break
            tokens.append(token_id)
            func += self.llm.decode(token_id).lstrip()
        return func


    def args(self, prompt, function: Function | None) -> str:
        if not function:
            return '{}'
        args_str = '{'
        function_str = f"{function.name}("
        for arg in function.arguments:
            if arg.type == "number":
                arg.type = "float"
            function_str += f"{arg.name}: {arg.type}"
            if arg != function.arguments[-1]:
                function_str += ", "
        if function.returns.type == "number":
            function.returns.type = "float"
        function_str += f") -> {function.returns.type}"
        # print(function_str)

        for arg in function.arguments:
            token = 0
            supp = str()
            if arg.type == 'float':
                supp = " in float"
            args_str += f'"{arg.name}":'
            tokens = self.llm.encode(
                f"""Given the user request: "{prompt.prompt}"
Call the function: {function_str}
Arguments{supp}: {args_str}"""
            ).cpu().detach().numpy()[0].tolist()
            # print(f"[{llm.decode(tokens)}]")

            while True:
                if token == 15:
                    if args_str.count('"') % 2 == 1:
                        tokens.append(self.llm.encode('"').cpu().detach().numpy()[0].tolist()[0])
                        args_str += self.llm.decode(tokens[-1])
                    if arg != function.arguments[-1]:
                        tokens.append(self.llm.encode(",").cpu().detach().numpy()[0].tolist()[0])
                        args_str += self.llm.decode(tokens[-1])
                    break
                logits = self.llm.get_logits_from_input_ids(tokens)
                token_id = int(np.argmax(logits))
                tokens.append(token_id)
                args_str += self.llm.decode(token_id)
                if ',' in self.llm.decode(token_id):
                    if args_str.count('"') % 2 == 0:
                        tokens.append(self.llm.encode(" ").cpu().detach().numpy()[0].tolist()[0])
                        args_str += self.llm.decode(tokens[-1])
                        break
                elif '}' in self.llm.decode(token_id):
                    if args_str.count('}') == args_str.count('{'):
                        break
                token += 1
                print(args_str)

        if args_str.count('"') % 2 == 1 and args_str.count('}') != args_str.count('{'):
            args_str += '"'
        if args_str.count('}') != args_str.count('{'):
            args_str += '}'
        return args_str
