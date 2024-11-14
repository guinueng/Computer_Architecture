import utils

class Control:

    # do not modify this function
    def __init__(self):
        self.signals = {
            "RegDst": None, "ALUSrc": None, "MemtoReg": None, "RegWrite": None,
            "MemRead": None, "MemWrite": None, "Branch": None, "ALUOp": None
        }
        self.alu_signal = 0

    def set_control_signals(self, opcode):
        if(opcode == 0): # R type instruction case.
            self.signals = {
                      "RegDst": 1, "ALUSrc": 0, "MemtoReg": 0, "RegWrite": 1,
                      "MemRead": 0, "MemWrite": 0, "Branch": 0, "ALUOp": 0b10
                  }
        elif(opcode == 0x23): # lw instruction case.
            self.signals = {
                      "RegDst": 0, "ALUSrc": 1, "MemtoReg": 1, "RegWrite": 1,
                      "MemRead": 1, "MemWrite": 0, "Branch": 0, "ALUOp": 0b00
                  }
        elif(opcode == 0x2b): # sw instruction case.
            self.signals = {
                      "RegDst": None, "ALUSrc": 1, "MemtoReg": None, "RegWrite": 0,
                      "MemRead": 0, "MemWrite": 1, "Branch": 0, "ALUOp": 0b00
                  }
        elif(opcode == 0x4): # beq instruction case.
            self.signals = {
                      "RegDst": None, "ALUSrc": 0, "MemtoReg": None, "RegWrite": 0,
                      "MemRead": 0, "MemWrite": 0, "Branch": 1, "ALUOp": 0b01
                  }
        elif(opcode == 0x8): # addi instruction case.
            self.signals = {
                      "RegDst": 0, "ALUSrc": 1, "MemtoReg": None, "RegWrite": 1,
                      "MemRead": 0, "MemWrite": 0, "Branch": 0, "ALUOp": 0b00
                  }
        else:
            utils.handle_invalid_opcode() # If invalid opcode given, handle it by using utils function.

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
        """

        # R type instruction (opcode is fixed w/ 0, funct code will be written here) : add (0x20), sub (0x22), and (0x24), or (0x25), slt (0x2a), nor (0x27)
        # I type instruction (opcode) : lw (0x23), sw (0x2b), beq (0x4), addi (0x8)
    def set_alu_signal(self, aluop, funct):
        if(aluop == 0b10): # ALUOP R-type instruction case.
            if(funct == 0x20): # FUNCT add case.
                self.alu_signal = 0b0010
            elif(funct == 0x22): # Sub case.
                self.alu_signal = 0b0110
            elif(funct == 0x24): # And case.
                self.alu_signal = 0b0000
            elif(funct == 0x25): # Or case.
                self.alu_signal = 0b0001
            elif(funct == 0x2a): # Slt case.
                self.alu_signal = 0b0111
            elif(funct == 0x27): # Nor case.
                self.alu_signal = 0b1100
            else:  # If invalid funct given, handle it by using utils function.
                utils.handle_invalid_funct()
        elif(aluop == 0b00): # ALUOP 00 case. (lw, sw, addi)
            self.alu_signal = 0b0010
        elif(aluop == 0b01): # ALUOp 01 case. (beq)
            self.alu_signal = 0b0110

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
        """

    # do not modify this function
    # you can access to the signals dictionary using this function
    def get_signal(self, signal_name):
        return self.signals.get(signal_name)


    # you can access to the alu_signal variable using this function
    # do not modify this function
    def get_alu_signal(self):
        return self.alu_signal
