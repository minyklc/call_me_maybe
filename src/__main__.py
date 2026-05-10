#!/usr/bin/env python3
import sys
from .parsing import parsing
from .selector import Select
from llm_sdk import Small_LLM_Model  # type: ignore
from .helper import find_func, make_path, create_correct
from .helper import check_path, write_output


def main() -> None:
    try:
        args = sys.argv
        args.pop(0)
        p_path, f_path, o_path = check_path(args)
        prompt_list, function_list, function_data = parsing(p_path, f_path)
        make_path()
    except FileNotFoundError as n:
        return print(n)
    except OSError as o:
        return print(o)
    except Exception as e:
        return print('unexpected error:', e)

    result = list()
    llm = Small_LLM_Model()
    t_list = create_correct(llm, function_list)
    select = Select(llm, function_data, function_list)

    for prompt in prompt_list:
        print(prompt.prompt)
        func = select.function(prompt, t_list)
        if not func:
            func = "function not found"
        print(func)
        function = find_func(function_list, func)
        args_str = select.args(prompt, function)
        name = ""
        if function:
            name = function.name
        # print(args_str)

        try:
            f_args = eval(args_str)
        except Exception:
            f_args = args_str
        print(f_args)
        result.append({
            "prompt": prompt.prompt,
            "name": name,
            "parameters": f_args,
        })
        print()

    write_output(o_path, result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('unexpected error:', e)
