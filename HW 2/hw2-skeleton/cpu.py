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

    def run_cycle(self):
        # 1. Instruction Fetch Step.
        instruction = self.memory.read_instruction(self.pc) # Fetch instruction on inst. mem. based on current program counter value(which is current address).
        utils.print_instruction_fetch(self.pc, instruction)
        # print("Instruction on decimal : ", instruction)

        # Need to Implement Instruction : lw, sw , beq, add, sub, and, or, slt, nor, addi
        # R type instruction (opcode is fixed w/ 0, funct code will be written here) : add (0x20), sub (0x22), and (0x24), or (0x25), slt (0x2a), nor (0x27)
        # I type instruction (opcode) : lw (0x23), sw (0x2b), beq (0x4), addi (0x8)

        # 2. Instruction Decode Step.
        # First, we need to extract opcode part.
        opcode = int(instruction / int(2 ** 26))
        instruction %= (2 ** 26)
        # print("opcode for decimal : ", opcode)
        # print("opcode for hex : ", hex(opcode))

        self.control.set_control_signals(opcode) # By decoded result, we need to set Control signal.

        rs = int(instruction // (2 ** 21)) # Decode necessary value(rs, rt value for both R, I type, rd, shamt, funct value for R type and sign_ex_num for I type.)
        instruction %= (2 ** 21)
        rt = int(instruction / (2 ** 16))
        instruction %= (2 ** 16)
        rd = int(instruction / (2** 11))
        sign_ex_num = instruction
        instruction %= 2 ** 11
        shamt = int(instruction // (2 ** 6))
        funct = int(instruction % (2 ** 6))
        # print("R Instruction on decimal: ", opcode, rs, rt, rd, shamt, funct)
        # print("R Instruction on hex: ", hex(opcode), hex(rs), hex(rt), hex(rd), hex(shamt), hex(funct))
        # print("I Instruction on decimal: ", opcode, rs, rt, sign_ex_num)
        # print("I Instruction on hex: ", hex(opcode), hex(rs), hex(rt), hex(sign_ex_num))

        rs_value = self.register_file.read(rs)
        rt_value = self.register_file.read(rt)

        self.control.set_alu_signal(self.control.get_signal("ALUOp"), funct)

        # 3. Execution step.
        if(self.control.get_signal("ALUSrc") == 0):
            B = rt_value
        else:
            B = sign_ex_num
        result = self.alu.operate(self.control.get_alu_signal(), rs_value, B)

        # 3-1. Branch Addr calc step.
        # Shift left 2 to get target branch address.
        # Python has << operator to shift number left by desire times.
        # Reference : https://docs.python.org/3.9/reference/expressions.html?highlight=shift%20left
        target_branch_addr = sign_ex_num << 2

        # 4. Data Memory Fetch Step.
        if(self.control.get_signal("MemRead") == 1): # If MemRead sig == 1, we need to read data memory.
            mem_read_data = self.memory.read_data(result.get("result"))

        if(self.control.get_signal("MemWrite") == 1): # If MemWrite == 1, we need to write data into data memory.
            self.memory.write_data(result.get("result"), rt_value)

        if(self.control.get_signal("MemtoReg") == 1): # Select reg write data by using MemtoReg signal.
            reg_w_data = mem_read_data
        else:
            reg_w_data = result.get("result")

        # 5. Register Write Back step.
        if(self.control.get_signal("RegWrite") == 1):
            if(self.control.get_signal("RegDst") == 0): # If RegDst is Inst[20-16] which is rt case.
                self.register_file.write(rt, reg_w_data)
            else: # If RegDst is Inst[15-11] which is rd case.
                self.register_file.write(rd, reg_w_data)

        # 6. Update PC value at the end of cycle.
        if(self.control.get_signal("Branch") == 1 and result.get("zero") == 1): # If branch is occured,
            self.pc += (4 + target_branch_addr) # Need to update pc value by branch destination.
        else:
            self.pc += 4 # Else, update PC value by adding 4.

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
