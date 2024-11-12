import utils

class Control:

    # do not modify this function
    def __init__(self):
        self.signals = {
            "RegDst": None, "ALUSrc": None, "MemtoReg": None, "RegWrite": None,
            "MemRead": None, "MemWrite": None, "Branch": None, "ALUOp": None
        }
        self.alu_signal = 0

    #FIXME
    def set_control_signals(self, opcode):
        """
        Sets main control signals based on the given opcode.

        Parameters:
            - opcode (int): The 6-bit opcode value extracted from the
              instruction.

        Functionality:
            - Based on the opcode, this method determines the appropriate
              values for various control signals, including RegDst, ALUSrc,
              MemtoReg, RegWrite, MemRead, MemWrite, Branch, and ALUOp (signal
              values should be integer type). These control signals influence
              the datapath for instruction execution. The resulting control
              signals are stored in the self.signals dictionary. If the value
              of a control signal is 'don't care', assign it as None.
              Assign example:
                  self.signals = {
                      "RegDst": None, "ALUSrc": 1, "MemtoReg": None, "RegWrite": 0,
                      "MemRead": 0, "MemWrite": 1, "Branch": 0, "ALUOp": 0b00
                  }

        Returns:
            None

        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """

    #FIXME
    def set_alu_signal(self, aluop, funct):
        """
        Determines the ALU operation based on ALUOp and funct code.

        Parameters:
            - aluop (int): The 2-bit aluop control signal value.
            - funct (int): The 6-bit function code from the instruction.

        Functionality:
            - This function analyzes the aluop and funct to determine the exact
              ALU operation signal. The determined 4-bit ALU operation code
              (int) is stored in self.alu_signal.

        Returns:
            None

        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """

    # do not modify this function
    # you can access to the signals dictionary using this function
    def get_signal(self, signal_name):
        return self.signals.get(signal_name)


    # you can access to the alu_signal variable using this function
    # do not modify this function
    def get_alu_signal(self):
        return self.alu_signal
