# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 17:41:01 2021

@author: Justinas
"""

class calculator:
    
    memory = 0
    
    def addition(self, number):
       
        calculator.memory += number
    
    def subtraction(self, nubmer):
        
        calculator.memory -= number
    
    def division(self, number):
        
        calculator.memory /= number
    
    def multiplication(self, number):
       
        calculator.memory *= number
    
    def nth_root(self, root):
        
        calculator.memory = calculator.memory**(1/root)
    
    def reset(self):
        
        calculator.memory = 0