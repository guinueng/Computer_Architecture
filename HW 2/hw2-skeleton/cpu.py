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
