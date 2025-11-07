#!/usr/bin/env python3


from typing import Any


class Glob:
    def __init__(self):
        self.data = {}
       
    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key) -> Any:
        if " " in key:
            keys = key.split(" ")
            return [self.data[k] for k in keys]
        return self.data.get(key)

    def __repr__(self) -> str:
        return f"Glob({self.data})"
    
    def __str__(self) -> str:
        return str(self.data)