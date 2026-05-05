#!/usr/bin/env python3
from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str


class Argument(BaseModel):
    name: str
    type: str


class Function(BaseModel):
    name: str
    description: str
    arguments: list[Argument]
    returns: Argument