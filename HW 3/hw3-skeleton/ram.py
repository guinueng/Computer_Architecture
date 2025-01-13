class RAM:

    def __init__(self):
        self.mem = {}

        self.mem_addr_start = 0x10000000
        self.mem_addr_end = 0x10000700
        cnt = 0
        for word_addr in range(self.mem_addr_start, self.mem_addr_end, 4):
            self.mem[word_addr] = 0x00000000

    # Unlike Homework 2, we will not test each function individually in this
    # assignment. Therefore, if you do not want to use the skeleton code, you
    # are allowed to write the code from scratch. Additionally, you are free to
    # modify the parameters, return types, or other aspects

    #  Retrieves a 32-byte block of data from the main memory
    def block_read(self, address):
        """
        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """
        pass


    # #rites a 32-byte block of data from the cache back to the main memory
    def block_write(self, address, block_data):
        """
        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """
        pass


    def mdump(self, start, stop):
        print("-------------------------------------")
        for b in range(start, stop+1, 0x20):
            line = f"{b:08x}...{(b + 0x1c):08x}| "
            for i in range(b, b + 0x20, 4):
                line += f"{self.mem[i]:08x}."
            line = line[:-1]
            line +=" |"
            print(line)
        print("")


    def dump(self):
        print(f"memory [0x{self.mem_addr_start:08x}..0x{self.mem_addr_end:08x}] :")
        self.mdump(self.mem_addr_start, self.mem_addr_end-4)
        print("")
