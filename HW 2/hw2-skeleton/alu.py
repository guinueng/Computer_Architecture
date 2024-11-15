import math
import utils

class ALU:
    # do not modify this function
    def __init__(self):
        pass

    def operate(self, operation, operand1, operand2): # operation gives 4bit signal from ALU Control
        # We need to extract A invert, B invert and operation information from given 4bit operation code.
        Ainvert = (operation & 0x8) >> 3 # Can get get first 1 bit of signal as A value invert signal by utilizing bitwise and operation and bitwise shifting.
        Binvert = (operation & 0x4) >> 2 # Can get get second 1 bit of signal as B value invert signal by utilizing bitwise and operation and bitwise shifting.
        Operation = operation & 0x3 # Can get last 2 bit of signal as operation alu performs by utilizing bitwise and operation.
        
        A = operand1 # Initialize A and B value as given operands.
        B = operand2

        if(((A & 0x80000000) >> 31) == 0b1): # In python, all integer to hex value is treated as unsigned one.
            A = (-1) * (operand1 ^ 0xffffffff) + 1 # So if we want to use negative hex number as negative integer, we need to convert as manually.
            # In two's complement, finding corresponding opposite sign number equals negate target number + 1.
            # Negating target number is utilizing not operation, so by utilizing XOR operation w/ 0xfffffff which corresponds 0b11111111111111111111111111111111,
            # we can get negated value. Then, add 1 to keep two's complement property.
            # This property has been found in professor's lecture note.
            # Reference : https://docs.python.org/3.9/reference/expressions.html?highlight=xor
        if(((B & 0x80000000) >> 31) == 0b1): # Same property as above but treating B.
            B = (-1) * (operand2 ^ 0xffffffff) + 1

        A = (operand1 & 0x7ffffffff) # Delete sign bit of A.
        B = (operand2 & 0x7ffffffff) # Delete sign bit of B.

        if(Ainvert == 1): # Negating A based on ALUControl signal.
            A *= -1
        if(Binvert == 1): # Negating B based on ALUControl signal.
            B *= -1

        calc_result = A + B # Calculate A + B for add operation and slt operation.

        if(calc_result == 0): # Check whether calculated value is 0 or not.
            Zero = 1 # By calc result, trigger Zero signal or not.
        else:
            Zero = 0

        if(calc_result < 0): # Python support hex(neg number) as '-0x(unsigned hex)'.
            calc_result = 0xffffffff + calc_result + 1 # Thus, we need to manually convert neg number into 32-bit hex notation.
            # To convert it, we add 0xffffffff(-1) and calculated result(negative number), so we can get negative number.
            # But, since we used -1 hex value to calculate negative form of calculated result, we need to add 1 to sure that value is correct.
        if(A < 0): # Same operation should occur in A and B.
            A = 0xffffffff + A + 1
        if(B < 0):
            B = 0xffffffff + B + 1

        if(Operation == 0b00): # And gate
            return {"result": A & B, "zero": Zero} # In python there exist bitwise and/or operation by using &/|. And and and or operation returns and|or operated value.
        elif (Operation == 0b01): # OR gate
            return {"result": A | B, "zero": Zero} # Reference : https://docs.python.org/3.9/library/stdtypes.html?highlight=bitwise
        elif(Operation == 0b10): # Add operation returns calc result.
            return {"result": calc_result, "zero": Zero}
        elif(Operation == 0b11): # Set on less than operation
            if(((calc_result & (0x80000000)) >> 31) == 0b1): # If calculated value's MSB is 1 which denotes sign bit is 1, it is negative number.
                return {"result": 1, "zero": Zero} # If two subtracted value is negative, we can consider A value is smaller than B value, thus return 1.
            else: # Else, we can regard A value is same or bigger than B, so we would return value 0.
                return {"result": 0, "zero": Zero}

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
        """
