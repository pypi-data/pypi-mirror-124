"""
Defines decorators used to check that external dependencies can be resolved.
"""
import subprocess
import sys

from functools import wraps


def requires_ffmpeg(func):
    """
    Ensure ffmpeg is installed before running wrapped function.
    If ffmpeg is not installed, abort with a useful error message.
    """
    @wraps(func)
    def function_wrapper(*args, **kwargs):
        try:
            subprocess.call(["ffmpeg", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return func(*args, **kwargs)
        except FileNotFoundError:
            print('[ERROR] ffmpeg binary is missing from your operating system. Please install it and retry.')
            sys.exit(1)
    
    return function_wrapper
