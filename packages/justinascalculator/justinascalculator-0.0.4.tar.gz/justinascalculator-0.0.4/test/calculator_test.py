from calculator import calculator
from numpy import sqrt
import pytest


def test_memory():
    calculator = calculator()
    assert calculator.memory == 0

def test_set_memory():
    calculator = calculator()
    calculator.memory = 1
    with pytest.raises(ValueError):
        calculator.memory = 'test'
    assert calculator.memory == 1

def test_reset():
    calculator = calculator()
    calculator.reset()
    assert calculator.memory == 0

def test_addition():
    calculator = calculator(10)
    with pytest.raises(ValueError):
        calculator.addition('test')
    calculator.addition(10)
    assert calculator.memory == 20

def test_subtraction():
    calculator = calculator(10)
    with pytest.raises(ValueError):
        calculator.subtraction('test')
    calculator.subtraction(10)
    assert calculator.memory == 0

def test_multiplication():
    calculator = calculator(10)
    with pytest.raises(ValueError):
        calculator.multiplication('test')
    calculator.multiplication(10)
    assert calculator.memory == 100

def test_division():
    calculator = calculator(100)
    with pytest.raises(ValueError):
        calculator.division('test')
    with pytest.raises(ZeroDivisionError):
        calculator.division(0)
    calculator.division(10)
    assert calculator.memory == 10

def nth_root():
    calculator = calculator(-9)
    with pytest.raises(ValueError):
        calculator.nth_root()
    calculator = calculator(9)
    calculator.nth_root(2)
    assert calculator.memory == sqrt(9)
