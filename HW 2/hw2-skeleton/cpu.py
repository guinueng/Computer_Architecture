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
        utils.print_instruction_fetch(self.pc, instruction) # Print fetching instruction mem addr.

        # Need to Implement Instruction : lw, sw , beq, add, sub, and, or, slt, nor, addi
        # R type instruction (opcode is fixed w/ 0, funct code will be written here) : add (0x20), sub (0x22), and (0x24), or (0x25), slt (0x2a), nor (0x27)
        # I type instruction (opcode) : lw (0x23), sw (0x2b), beq (0x4), addi (0x8)

        # 2. Instruction Decode Step.
        # First, we need to extract opcode part.
        opcode = (instruction & 0xfc000000) >> 26 # Get 6 bit opcode and other necessary information as bitwise and operation and make remain only 6 bit as shift operation.
        self.control.set_control_signals(opcode) # By decoded result, we need to set Control signal.
        rs = (instruction & 0x03e00000) >> 21 # Decode necessary value(rs, rt value for both R, I type, rd, shamt, funct value for R type and sign_ex_num for I type.)
        # Get 5 bit rs register as bitwise and operation and make remain only 5 bit as shift operation.
        rt = (instruction & 0x001f0000) >> 16
        # Get 5 bit rt register as bitwise and operation and make remain only 5 bit as shift operation.
        rd = (instruction & 0x0000f800) >> 11
        # Get 5 bit rd register as bitwise and operation and make remain only 5 bit as shift operation for R type instruction execution purpose.
        sign_ex_num = (instruction & 0x0000ffff)
        # Get 16 bit immediate value as bitwise and operation for I type instruction.
        shamt = (instruction & 0x000007c0) >> 6
        # Get 5 bit shift amount value as bitwise and operation and make remain only 5 bit as shift operation.
        funct = (instruction & 0x0000003f)
        # Get 5 bit function code for R type instruction as bitwise and operation.

        rs_value = self.register_file.read(rs) # Read rs register value.
        rt_value = self.register_file.read(rt) # Read rt register value for purpose.

        self.control.set_alu_signal(self.control.get_signal("ALUOp"), funct)
        # Set alu signal based on ALUOp signal from Control and additionally consider function code if R type instuction.

        # 3. Execution step.
        if(self.control.get_signal("ALUSrc") == 0): # Choose second input value of ALU by signal of ALUSrc by utilizing mux.
            B = rt_value # If ALUSrc value is 0, select rt register value.
        else: # If ALUSrc value is 1, select sign extended immediate value.
            B = sign_ex_num
        result = self.alu.operate(self.control.get_alu_signal(), rs_value, B) # Execute ALU by signal from ALU Control, rs register value, and selected value from mux.
        
        if(self.control.get_alu_signal() == 0b0010): # Checking overflow of during add calculation on ALU.
            if(rs_value > 0 and B > 0 and ((result[0] & 0x80000000) >> 31) == 1): # Overflow occurred by pos + pos num = neg case.
                utils.handle_overflow()
            if(rs_value < 0 and B < 0 and ((result[0] & 0x80000000) >> 31) == 0): # Overflow occurred by neg + neg num = pos case.
                utils.handle_overflow()
        if(self.control.get_alu_signal() == 0b0110): # Checking overflow of during sub calculation on ALU.
            if(rs_value > 0 and B < 0 and ((result[0] & 0x80000000) >> 31) == 1): # Overflow occurred by pos - neg num = neg case.
                utils.handle_overflow()
            if(rs_value < 0 and B > 0 and ((result[0] & 0x80000000) >> 31) == 1): # Overflow occurred by neg - pos num = pos case.
                utils.handle_overflow()

        # 3-1. Branch Addr calc step for some I type instruction case. (beq inst. case.)
        # Shift left 2 to get target branch address.
        # Python has << operator to shift number left by desire times.
        # Reference : https://docs.python.org/3.9/reference/expressions.html?highlight=shift%20left
        target_branch_addr = sign_ex_num << 2

        # 4. Data Memory Fetch Step.
        if(self.control.get_signal("MemRead") == 1): # If MemRead sig == 1, we need to read data memory based on calculated effective address by alu.
            mem_read_data = self.memory.read_data(result[0])

        if(self.control.get_signal("MemWrite") == 1): # If MemWrite == 1, we need to write data into data memory based on calculated effective address by alu.
            self.memory.write_data(result[0], rt_value)

        if(self.control.get_signal("MemtoReg") == 1): # Select reg write data by using MemtoReg signal as utilizing mux.
            reg_w_data = mem_read_data # If MemtoReg value is 1, set register write value as read value from data memory.
        else: # If MemtoReg signal is 0, set reg write data as calculated result of ALU.
            reg_w_data = result[0]

        # 5. Register Write Back step.
        if(self.control.get_signal("RegWrite") == 1): # If RegWrite signal is 1, we write reg write data into target register.
            # And target register is selected by mux getting RegDst signal.
            if(self.control.get_signal("RegDst") == 0): # If RegDst is 0, we choose Inst[20-16] which is rt case.
                self.register_file.write(rt, reg_w_data)
            else: # If RegDst is 1, we choose Inst[15-11] which is rd case.
                self.register_file.write(rd, reg_w_data)

        # 6. Update PC value at the end of cycle.
        if(self.control.get_signal("Branch") == 1 and result[1] == 1): # If branch signal is occured as 1,
            # and branch condition which is zero (only considering beq on this hw case) has occured,
            self.pc += (4 + target_branch_addr) # Need to update pc value by target branch destination.
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
