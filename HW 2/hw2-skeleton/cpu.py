from alu import ALU
from control import Control
from memory import Memory
from register_file import RegisterFile
import utils

import sys

class CPU:
    # do not modify this function
    def __init__(self, inst_file, data_file, reg_file):
        self.pc = 0
        self.alu = ALU()
        self.control = Control()
        self.memory = Memory(inst_file, data_file)
        self.register_file = RegisterFile(reg_file)


    #FIXME
    def run_cycle(self):
        # 1. Instruction Fetch Step.
        instruction = self.memory.read_instruction(self.pc) # Fetch instruction on inst. mem. based on current program counter value(which is current address).
        utils.print_instruction_fetch(self.pc, instruction)
        print("Instruction on decimal : ", instruction)

        # Need to Implement Instruction : lw, sw , beq, add, sub, and, or, slt, nor, addi
        # R type instruction (opcode is fixed w/ 0, funct code will be written here) : add (0x20), sub (0x22), and (0x24), or (0x25), slt (0x2a), nor (0x27)
        # I type instruction (opcode) : lw (0x23), sw (0x2b), beq (0x4), addi (8)

        # 2. Instruction Decode Step.
        # First, we need to extract opcode part.
        opcode = int(instruction / int(2 ** 26))
        instruction %= (2 ** 26)
        print("opcode for decimal : ", opcode)
        print("opcode for hex : ", hex(opcode))

        self.control.set_control_signals(opcode) # By decoded result, we need to set Control signal.

        rs = int(instruction / int(2 ** 21)) # Decode necessary value(rs, rt value for both R, I type, rd, shamt, funct value for R type and sign_ex_num for I type.)
        instruction %= (2 ** 21)
        rt = int(instruction / int(2 ** 16))
        instruction %= (2 ** 16)
        rd = int(instruction / int(2** 11))
        sign_ex_num = int(instruction)
        instruction %= int(2 ** 11)
        shamt = int(instruction / int(2 ** 6))
        funct = int(instruction % int(2 ** 6))
        print("R Instruction on decimal: ", opcode, rs, rt, rd, shamt, funct)
        print("R Instruction on hex: ", hex(opcode), hex(rs), hex(rt), hex(rd), hex(shamt), hex(funct))
        print("I Instruction on decimal: ", opcode, rs, rt, sign_ex_num)
        print("I Instruction on hex: ", hex(opcode), hex(rs), hex(rt), hex(sign_ex_num))

        if(opcode == 0): # R inst. case.
            
            # 3. Exec Step.
        else:




        self.pc += 4 # Update PC value at the end of cycle.

        """
        Implement the cycle steps by using the self.pc, self.alu, self.control,
        self.memory, and self.register_file objects.

        Functionality:
            1. Instruction Fetch
            2. Instruction Decode
               - During this step, set control signals by using
                 set_control_signals and set_alu_signal functions
            3. Execute
            4. Memory Access
            5. Register Write-back
            Also, update the PC for the next instruction

        Returns:
            None

        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """

    # do not modify this function
    def run(self):
        print (f"[*] Initial states")
        self.register_file.dump_register()
        self.memory.dump_data_memory()

        cycle_num = 1
        while self.pc in self.memory.instruction_memory:
            print (f"\n[*] Current cycle: {cycle_num}")
            self.run_cycle()
            self.register_file.dump_register()
            self.memory.dump_data_memory()

            cycle_num += 1
