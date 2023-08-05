from .generics import _run_main, _start_main, _check_main
import asyncio
import sys

# Generics
def run(api_key, model_key, model_parameters):
    out = _run_main(
        api_key = api_key, 
        model_key = model_key, 
        model_parameters = model_parameters
    )
    return out

def start(api_key, model_key, model_parameters):
    out = _start_main(
        api_key = api_key, 
        model_key = model_key, 
        model_parameters = model_parameters
    )
    return out
    
def check(api_key, task_id):
    out_dict = _check_main(
        api_key = api_key,
        task_id = task_id
    )
    return out_dict