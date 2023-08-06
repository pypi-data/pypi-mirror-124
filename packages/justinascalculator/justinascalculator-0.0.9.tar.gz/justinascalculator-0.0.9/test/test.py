# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 11:06:56 2021

@author: Justinas
"""


import pytest
from calculator.Calculator import Calculator

def test_memory():
    calculator = Calculator()
    
    assert calculator.memory == 0

def test_set_memory():
    calculator = Calculator(10)
    
    assert calculator.memory == 10
    
def test_additon():
    calculator = Calculator()
    calculator.addition(15)
    
    assert calculator.memory == 15
    
def test_addition_2num():
    calculator = Calculator()
    calculator.addition(14,15)
    
    assert calculator.memory == 29    
    
def test_subtracton():
    calculator = Calculator()
    calculator.subtraction(8)
    
    assert calculator.memory == -8

def test_subtraction_2num():
    calculator = Calculator()
    calculator.subtraction(15,5)
    
    assert calculator.memory == 10

def test_divition():
    calculator = Calculator(8)
    calculator.division(2)
    
    assert calculator.memory == 4
  
def test_divition_2num():
    calculator = Calculator()
    calculator.division(16,8)
    
    assert calculator.memory == 2

def test_multiplication():
    calculator = Calculator(2)
    calculator.multiplication(5)
    
    assert calculator.memory == 10

def test_multiplication_2num():
    calculator = Calculator()
    calculator.multiplication(5,5)
    
    assert calculator.memory == 25
    
def test_power():
    calculator = Calculator(2)
    calculator.power(3)
    
    assert calculator.memory == 8
    
def test_power_2num():
    calculator = Calculator()
    calculator.power(3,2)
    
    assert calculator.memory == 8
    
def test_reset():
    calculator = Calculator(6)
    calculator.reset()
    
    assert calculator.memory == 0
    
def test_nth_root():
    calculator = Calculator(27)
    calculator.nth_root(3)
    
    assert calculator.memory == 3
    
def test_nth_root_2num():
    calculator = Calculator()
    calculator.nth_root(3,27)
    
    assert calculator.memory == 3