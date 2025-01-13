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
        tag = (address & 0xffffff00) >> 8 # Extract tag bits.
        cache_index = (address & 0xe0) >> 5 # Extract cache index bits.
        block_offset = (address & 0x1c) >> 2 # Extract block offset.
        
        hit = False # Denotes write hit or miss.
        fetched_way = 0 # Assign fetched way to find what position did we fetched way.
        blocks = self.sets[cache_index].blocks # Bring target cache index's set of blocks.
        data = 0 # Assign data to store read value later.

        for block in blocks: # Loop ways to find position we want to fetch.
            if(block.tag == tag): # If target way has same tag bits case.
                if(block.valid == 1): # If block is valid,
                    data = block.data[block_offset] # bring data into block's data set. Choose data on block by block offset.
                    hit = True # Change hit true.
                    break # Stop looping due to we did our goals.

            fetched_way += 1 # Check what position did we fetched way.

        if(not hit): # All block is valid but target data block is not exist or remaining block's valid bit is 0 in cache. Read miss case and need to utilize LRU.
            target_block = self.sets[cache_index].blocks[self.sets[cache_index].history[0]] # Assign target block based on LRU.

            target_addr = target_block.tag << 3 # Calculate target block's tag
            target_addr = (target_addr + cache_index) << 5 # Since cache index is same, we need to calculate target address based on current cache's tag bit and cache index.

            if (target_block.dirty == 1): # Check dirty bit and if dirty bit is 1, we need to pursue write back operation before overwriting current block.
                self.ram.block_write(target_addr, target_block.data) # Write block data into memory.

            target_block.data = self.ram.block_read(((address) >> 5) << 5) # Update target block's data into current target address's block data.
            fetched_way = self.sets[cache_index].history[0] # Save fetched way position to update LRU later.
            
            # Update block's valid bit, dirty bit, tag and update return data.
            target_block.valid = 1
            target_block.dirty = 0
            target_block.tag = tag
            data = target_block.data[block_offset]
            
        find = False # Denotes found target fetched_way on LRU.
        for i in range (0, 4):
            if (self.sets[cache_index].history[i] == fetched_way or find == True): # If we found target LRU value first or found target LRU value before,
                find = True # change found state True.
                if(i != 3): # Then, if it is not last of array, store next value in current LRU position.
                    self.sets[cache_index].history[i] = self.sets[cache_index].history[i + 1]
                else: # If position is on last of LRU array, update value as fetched way position above.
                    self.sets[cache_index].history[i] = fetched_way

        return data # Returns target address's value.

    # Stores data in the cache at the specified address
    def write(self, address, data):
        tag = (address & 0xffffff00) >> 8 # Extract tag bits.
        cache_index = (address & 0xe0) >> 5 # Extract cache index bits.
        block_offset = (address & 0x1c) >> 2 # Extract block offset.
        
        hit = False # Denotes write hit or miss.
        fetched_way = 0 # Assign fetched way to find what position did we fetched way.
        blocks = self.sets[cache_index].blocks # Bring target cache index's set of blocks.

        for block in blocks: # Loop ways to find position we want to fetch.
            if(block.tag == tag): # If target way has same tag bits case.
                if(block.valid == 1): # If valid bit is 1, write data on target block.
                    block.data[block_offset] = data
                    
                    # And set block's valid bit 1, dirty bit 1, hit true.
                    block.valid = 1
                    block.dirty = 1
                    hit = True
                    break # Stop looping due to we did out goal.

            fetched_way += 1 # Check what position did we fetched way.
                    
        if(not hit): # All block is valid but target data block is not exist or remaining block's valid bit is 0 in cache. Write miss case and need to utilize LRU.
            target_block = self.sets[cache_index].blocks[self.sets[cache_index].history[0]] # Assign target block based on LRU.

            target_addr = target_block.tag << 3 # Calculate target block's tag
            target_addr = (target_addr + cache_index) << 5 # Since cache index is same, we need to calculate target address based on current cache's tag bit and cache index.

            if (target_block.dirty == 1): # Check dirty bit and if dirty bit is 1, we need to pursue write back operation before overwriting current block.
                self.ram.block_write(target_addr, target_block.data) # Write block data into memory.
                target_block.data = self.ram.block_read(((tag << 3) + cache_index) << 5) # Update block data into target memory's block.

            # Update block's valid bit, dirty bit, tag and data we want to write.
            target_block.valid = 1
            target_block.dirty = 1
            target_block.tag = tag
            target_block.data[block_offset] = data

            # Save fetched way position to update LRU later.
            fetched_way = self.sets[cache_index].history[0]

        # Denotes found target fetched_way on LRU.
        find = False
        for i in range (0, 4):
            if(self.sets[cache_index].history[i] == fetched_way or find == True): # If we found target LRU value first or found target LRU value before,
                find = True # change found state True.
                if(i != 3): # Then, if it is not last of array, store next value in current LRU position.
                    self.sets[cache_index].history[i] = self.sets[cache_index].history[i + 1]
                else: # If position is on last of LRU array, update value as fetched way position above.
                    self.sets[cache_index].history[i] = fetched_way

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
