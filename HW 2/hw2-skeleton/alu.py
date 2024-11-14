import math
import utils

class ALU:
    # do not modify this function
    def __init__(self):
        pass

    #FIXME
    def operate(self, operation, operand1, operand2):
        Ainvert = operation // 8
        Binvert = operation // 4
        Operation = operation % 4
        A = operand1
        B = operand2
        if(Ainvert == 1): # Negating A
            A *= -1
        if(Binvert == 1): # Negating B
            B *= -1

        if(A + B == 0): # Check whether value is 0 or not.
            Zero = 1
        else:
            Zero = 0

        if(Operation == 0): # And gate
            return {"result": A & B, "zero": Zero} # In python there exist bitwise and/or operation by using &/|.
        elif (Operation == 1): # OR gate
            return {"result": A | B, "zero": Zero} # Reference : https://docs.python.org/3.9/library/stdtypes.html?highlight=bitwise
        elif(Operation == 2): # Add operation
            return {"result": A + B, "zero": Zero}
        elif(Operation == 3):
            return {"result": A + B, "zero": Zero}


        """
        Perform ALU operation based on the operation code.

        Parameters:
            - operation (int): The 4-bit ALU control signal that determines
              the operation to be performed.
            - operand1 (int): The first operand (32-bit data) for the ALU
              operation.
            - operand2 (int): The second operand (32-bit data) for the ALU
              operation.

        Functionality:
            - This function performs ALU operations based on the operation
              argument and the operand1 and operand2 arguments. It returns the
              result of the operation along with a zero flag.


        Returns:
            - A tuple (result, zero), where:
                - result (int): Result of the ALU operation.
                - zero (int): A flag indicating if the result is zero (1 if
                              zero, otherwise 0).

        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """
