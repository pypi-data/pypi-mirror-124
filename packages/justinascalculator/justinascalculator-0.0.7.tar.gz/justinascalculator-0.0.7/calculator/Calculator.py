# -*- coding: utf-8 -*-

class Calculator:
    
    def __init__(self):
        
        """
        
        Initialise Calculator object
        Sets calculators memory into 0
        
        """
        
        self.memory = 0
    
    def addition(self, number):
        
        """
        
        Method to add a number in memory to a number in parameter.
        :param num: float or int
        
        """
        
        calculator.memory += number
    
    def subtraction(self, nubmer):
        
        """
        
        Method to subtract a number in memory from a number in parameter.
        :param num: float or int
        
        """
        
        calculator.memory -= number
    
    def division(self, number):
        
        """
        
        Method to divide a number in memory from a number in parameter.
        :param num: float or int
       
        """
        
        calculator.memory /= number
    
    def multiplication(self, number):
        
        """
        
        Method to multiply a number in memory with a number in parameter.
        :param num: float or int
        
        """
       
        calculator.memory *= number
    
    def nth_root(self, root):
        
        """
        
        Method to take parameter degree root from a number in memory.
        :param num: float or int
        
        """        
        calculator.memory = calculator.memory**(1/root)
    
    def reset(self):
        
        """
        
        Method to reset calculator memory to 0
        
        """
        
        calculator.memory = 0
    
    def power(self, number):
        
        """ 
        
        Methot to raise a number in memory by power with a number in parameters 
        
        """
        
        calculator.memory **= number
                