import sys
import os

from basic_functions.basic_functions import add, subtract, multiply 

def test_add():
    assert add(5,8) == 13

def test_subtract():
    assert subtract(5,8) == -3

def test_multiply():
    assert multiply(5,8) == 40

