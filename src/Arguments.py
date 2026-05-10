#!/usr/bin/env python3
from pydantic import BaseModel, Field


class Prompt(BaseModel):
    prompt: str = Field(min_length=1)


class Argument(BaseModel):
    name: str = Field(min_length=1)
    type: str = Field(min_length=1)


class Function(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    arguments: list[Argument]
    returns: Argument
