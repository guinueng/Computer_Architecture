import utils

class RegisterFile:
    # do not modify this function
    def __init__(self, reg_file):
        self.registers = self.load_registers(reg_file)

    # do not modify this function
    def load_registers(self, filename):
        registers = {}
        with open(filename, 'r') as file:
            for line in file:
                reg, value = line.strip().split()
                registers[reg] = int(value, 16)
        return registers

    def read(self, reg_num):
        if(reg_num < 0 or reg_num > 32 or self.registers.get('$' + str(reg_num)) is None):
            utils.handle_invalid_register_access()
        return self.registers.get('$' + str(reg_num)) # Return target register's value.
        # Due to register number has ${num} notation, we need to concatenate $ sign in front of reg_num.
        # Similarly, I used get function to get register value in register tuple to make sure we fetch value safely,
        # due to if non exist key value inputted, it returns None.

        """
        This function reads the value stored in the specified register.

        Parameters:
            - reg_num (int): The register number to read the value from.

        Returns:
            - The value stored in the specified register in self.registers
              (int)
        """

    def write(self, reg_num, value):
        if(reg_num < 0 or reg_num > 32 or self.registers.get('$' + str(reg_num)) is None):
            utils.handle_invalid_register_access()
        self.registers['$' + str(reg_num)] = value # Update target register as given value.
        # But, if we want to modify or add value into tuples, we need to directly access tuple by using key.

        """
        This function writes a value to the specified register in
        self.registers.

        Parameters:
            - reg_num (int): The register number to write the value to.
            - value (int): The value to store in the specified register.

        Returns:
            None
        """

    # do not modify this function
    def dump_register(self):
        print ("-" * 35)
        print ("Current register states:")
        print ("-" * 35)
        for reg_num in range(10):
            print(f"${reg_num}: 0x{self.read(reg_num):08x}")
        print ("-" * 35)
