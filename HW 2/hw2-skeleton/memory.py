import utils

class Memory:
    # do not modify this function
    def __init__(self, inst_file, data_file):
        self.instruction_memory = self.load_instructions(inst_file)
        self.data_memory = self.load_data(data_file)


    # do not modify this function
    def load_instructions(self, inst_file):
        instruction_memory = {}
        with open(inst_file, 'r') as file:
            address = 0
            for line in file:
                line = line.split('#')[0].strip()  # Remove comments after '#'
                instruction_memory[address] = int(line, 16)  # Store as hexadecimal integer
                address += 4
        return instruction_memory

    # do not modify this function
    def load_data(self, data_file):
        data_memory = {}
        with open(data_file, 'r') as file:
            for line in file.read().strip().split("\n"):
                address, value = line.strip().split()
                data_memory[int(address)] = int(value, 16)  # Store as hexadecimal integer
        return data_memory

    def read_instruction(self, address):
        data = self.instruction_memory.get(address)
        if(data is None or address < 0 or address > 32): # If address is out of word size or does not exist data, regard it as invalid memory access.
            utils.handle_invalid_memory_access()
        return data # Return instruction memory value.

        """
        Read (fetch) an instruction form instruction_memory.

        Parameters:
            - address (int): The address to read the value from.

        Returns:
            - The instruction memory value (int) at the specified address.
        """

    def read_data(self, address):
        data = self.data_memory.get(address)
        if(data is None or address < 0 or address > 32): # If address is out of word size or does not exist data, regard it as invalid memory access.
            utils.handle_invalid_memory_access()
        return data # Return target data memory's value.

        """
        Read data from data_memory.

        Parameters:
            - address (int): The address to read the data from .

        Returns:
            - The data memory value (int) at the specified address.
        """

    def write_data(self, address, value):
        if(self.data_memory.get(address) is None or address < 0 or address > 32): # If address is out of word size or does not exist data, regard it as invalid memory access.
            utils.handle_invalid_memory_access()
        self.data_memory[address] = value # Update target data memory by given value.

        """
        Write data to data_memory.

        Parameters:
            - address (int): The address in data memory to write to.
            - value (int): The value to store at the specified address.

        Returns:
            None.
        """

    # do not modify this function
    def dump_data_memory(self):
        print ("-" * 35)
        print ("Current memory states:")
        print ("-" * 35)
        for address in range(0, 32, 4):
            print(f"Address {address:02}: 0x{self.read_data(address):08x}")
        print ("-" * 35)
