# -*- coding: utf-8 -*-
from typing import Union

class Calculator:
    
    
    def __init__(self, memory: Union[int, float] = 0) -> None:
        
        """
        
        Constructor to initialize a calculator and set it's memory. Default is 0.
        
        """
        self.__error_not_a_number = "Incorrect data type of parameter. Please enter a float or an integer."
        
        if not isinstance(memory, (int, float)):
            raise ValueError(self.__error_not_a_number)
            
        self.memory = memory
        
    def addition(self, number1: Union[int, float] = None, number2: Union[int, float] = None):
        
        """
        
        Method to add numbers. If entered only 1 parameter, add it up to the memory. If 2 parameters are entered, they are summed and overwrites memory.
        :param number1: float or int
        :param number2: float or int
        
        """
        
        self.__error_not_a_number1 = "Incorrect data type of first parameter. Please enter a float or an integer."
        self.__error_not_a_number2 = "Incorrect data type of second. Please enter a float or an integer."
        
        if isinstance(number1, (int, float)):
            if number2 is None:
                self.memory += number1
            elif isinstance(number2, (int, float)):
                self.memory = number1 + number2
            else:
                raise ValueError(self.__error_not_a_number2)
        else:
            raise ValueError(self.__error_not_a_number1)
                
        return self.memory
    
    def subtraction(self, number1: Union[int, float] = None, number2: Union[int, float] = None):
        
        """
        
        Method to subtract numbers. If entered only 1 parameter, subtract it from memory. If 2 parameters are entered, second parameter is subtracted from first and overwrites memory.
        :param number1: float or int
        :param number2: float or int
        
        """
        
        self.__error_not_a_number1 = "Incorrect data type of first parameter. Please enter a float or an integer."
        self.__error_not_a_number2 = "Incorrect data type of second. Please enter a float or an integer."
        
        if isinstance(number1, (int, float)):
            if number2 is None:
                self.memory -= number1
            elif isinstance(number2, (int, float)):
                self.memory = number1 - number2
            else:
                raise ValueError(self.__error_not_a_number2)
        else:
            raise ValueError(self.__error_not_a_number1)
      
        return self.memory
    
    def division(self, number1: Union[int, float] = None, number2: Union[int, float] = None):
        
        """
        
        Method to divide numbers. If entered only 1 parameter, divide it from memory. If 2 parameters are entered, second parameter is divided from first and overwrites memory.
        :param number1: float or int
        :param number2: float or int
       
        """
        
        self.__error_not_a_number1 = "Incorrect data type of first parameter. Please enter a float or an integer."
        self.__error_not_a_number2 = "Incorrect data type of second. Please enter a float or an integer."
        
        if isinstance(number1, (int, float)):
            if number2 is None:
                self.memory /= number1
            elif isinstance(number2, (int, float)):
                self.memory = number1 / number2
            else:
                raise ValueError(self.__error_not_a_number2)
        else:
            raise ValueError(self.__error_not_a_number1)
        
        return self.memory
    
    def multiplication(self, number1: Union[int, float] = None, number2: Union[int, float] = None):
        
        """
        
        Method to multiply numbers. If entered only 1 parameter, multiply it with memory. If 2 parameters are entered, both parameters are multiplied and overwrites memory.
        :param number1: float or int
        :param number2: float or int
        
        """
       
        self.__error_not_a_number1 = "Incorrect data type of first parameter. Please enter a float or an integer."
        self.__error_not_a_number2 = "Incorrect data type of second. Please enter a float or an integer."
        
        if isinstance(number1, (int, float)):
            if number2 is None:
                self.memory *= number1
            elif isinstance(number2, (int, float)):
                self.memory = number1 * number2
            else:
                raise ValueError(self.__error_not_a_number2)
        else:
            raise ValueError(self.__error_not_a_number1)
        
        return self.memory
    
    def nth_root(self, degree: Union[int, float] = None, number: Union[int, float] = None):
        
        """
        
        Method to take nth_root numbers. If entered only 1 parameter, it takes the root from memory of entered degree. If 2 parameters are entered, it takes the root from second parameter by degree of first and overwrites memory.
        :param number1: float or int
        :param number2: float or int
        
        """      
        
        self.__error_not_a_number1 = "Incorrect data type of first parameter. Please enter a float or an integer."
        self.__error_not_a_number2 = "Incorrect data type of second. Please enter a float or an integer."
        
        if isinstance(degree, (int, float)):
            if number is None:
                self.memory = self.memory**(1/degree)
            elif isinstance(number, (int, float)):
                self.memory = number**(1/degree)
            else:
                raise ValueError(self.__error_not_a_number2)
        else:
            raise ValueError(self.__error_not_a_number1)
        
        return self.memory
    
    
    
    def power(self, number1: Union[int, float] = None, number2: Union[int, float] = None):
        
        """ 
        
        Method to raise power of numbers. If entered only 1 parameter, raises power of memory. If 2 parameters are entered, raises power of second parameter by first parameter, and overwrites memory.
        :param number1: float or int
        :param number2: float or int
        
        """
        
        self.__error_not_a_number1 = "Incorrect data type of first parameter. Please enter a float or an integer."
        self.__error_not_a_number2 = "Incorrect data type of second. Please enter a float or an integer."
        
        if isinstance(number1, (int, float)):
            if number2 is None:
                self.memory **= number1
            elif isinstance(number2, (int, float)):
                self.memory = number2 ** number1
            else:
                raise ValueError(self.__error_not_a_number2)
        else:
            raise ValueError(self.__error_not_a_number1)
        
        return self.memory
    
    def reset(self):
        
        """
        
        Method to reset calculator memory to 0
        
        """
        
        self.memory = 0
        
        return self.memory
    