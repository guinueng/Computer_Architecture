class Cache:
    def __init__(self, ram):
        self.associativity = 4 # 4-way set associative cache
        self.n_sets = 8        # 8 line caches
        self.block_size = 8   # 1 block = 8 words
        self.ram = ram
        self.sets = [Set(self.block_size, self.associativity) for _ in range(self.n_sets)]

    # Unlike Homework 2, we will not test each function individually in this
    # assignment. Therefore, if you do not want to use the skeleton code, you
    # are allowed to write the code from scratch. Additionally, you are free to
    # modify the parameters, return types, or other aspects

    # Retrieves data from the cache using the given address
    def read(self, address):
        """
        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """
        pass

    # Stores data in the cache at the specified ad- dress
    def write(self, address, data):
        """
        /*************************************************/
        /********************* FIXME *********************/
        /*************************************************/
        """
        pass

    def dump(self):
        print("Cache content:")

        empty = " " * self.block_size * 4
        print(f"|index| v |  tag   |  {empty}way0{empty}   | v |  tag   |  {empty}way1{empty}   | v |  tag   |  {empty}way2{empty}   | v |  tag   |  {empty}way3{empty}   |")

        idx = 0
        for set in self.sets:
            pline = f"| {idx:03b} |"
            for b in set.blocks:
                data = 0
                data_str = ""
                for word_data in b.data:
                    data_str += f"{word_data:08x}."
                data_str = data_str[:-1]

                pline += f" {b.valid} | {b.tag:06x} | {data_str} |"
            print(pline)
            idx += 1
        print("")

class Block:
    def __init__(self, block_size):
        self.valid = 0
        self.dirty = 0
        self.tag = 0
        self.data = [0x00000000] * block_size

class Set:
    def __init__(self, block_size, associativity):
        self.blocks = [Block(block_size) for i in range(associativity)]
        self.history = list(range(associativity)) # Access history for LRU replacement
