_This project has been created as part of the 42 curriculum by msuizu_

## **--- Description ---**

call_me_maybe is a function calling LLMs project. Using a 500 millions parameters model like Qwen3-0.6B,\
the project must be sufficiently accurate with constrained decoding.

## **--- Instructions ---**

`make lint-strict` to check flake8 and mypy in strict

`make install` install dependencies

`make run` execute with flags

`make debug` enter in debug mode

`make clean` keep the project space clean

## **--- Resources ---**

[json package](https://www.w3schools.com/python/python_json.asp)

AI was used for creating efficient prompt, and\
the understanding of constrained decoding and uv.

## **--- Algorithm explanation ---**

the generation is splitted in two steps.

the first step is the function calling, the vocabulary is contrained with only functions keywords and a space, by encoding the name of each function defined with a leading space.
for each generation, the name's leading space is removed with lstrip, leaving with the keyword of the functions name. the generation is done when the space's token is the highest.

for the second step, a prompt is used for each argument needed in the function called. the start of the json is generated with the name of the argument, so the model can directly starts generate the argument. the end is known by ',' caracter (with other proper verification to ensure the end of generation), and the process is looped for the argument's count.

## **--- Design decisions ---**

each classes in `Arguments` file uses [pydantic](https://pydantic.dev/docs/validation/latest/get-started/).
`parsing` file returns data readed from json input file in dict and pydantic classes.
`selector` file contains the main functions for function calling and arguments selection.
`helper` contains additional functions for check or find.

## **--- Performance analysis ---**

the generation is done in 5 minutes with 42's pcs.
the accuracy aims nearly 100% with default input files.

## **--- Challenges faced ---**

they were several challenges faced:

> the excepted output was difficult to obtain especially for arguments selection.\
the key is to make the generation easier for the model by using a efficient prompt,\
and generating automatically already known paramaters like arguments name.

> the reliability of the json output file was not easy because they were edge cases like\
missing prompt or function definition, infinite loop in arguments generation.\
the solution was to limit generation size, and to ensure that the json is parsable no matter what happens,\
by keeping an eye on what's written.

## **--- Testing strategy ---**

the implementation was validated by testinf with of course default input files, but also with for exemple one missing function definition, or empty string. even if the model generates wrong output, the output json is correct.

## **--- Example usage ---**

with default paths: `uv run python -m src`

with custom paths: `uv run python -m src
  --functions_definition data/input/functions_definition.json
  --input data/input/function_calling_tests.json
  --output data/output/function_calls.json`

excepted output:\
`[
	{
        "prompt": "What is the sum of 2 and 3?",
        "name": "fn_add_numbers",
        "parameters": {
            "a": 2.0,
            "b": 3.0
        }
    }
]`