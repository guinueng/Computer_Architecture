    .data # Data segment
prompt: .asciiz "The index for the Fibonacci sequence: " # Prompt for input
fib_result: .asciiz "Fibonacci number: " # Format for Fibonacci result
call_count: .asciiz "The number of fibonacci function calls: " # Format for call count
newline: .asciiz "\n" # Newline string

    .text # Code segment
    .globl main # Entry point

main:
    add $s0 $zero $zero # Set int cnt as 0.

    # Print "The index for the Fibonacci sequence: "
    li $v0, 4 # syscall for print_string
    la $a0, prompt # Load address of prompt
    syscall

    # Read integer input (n)
    li $v0, 5 # syscall for read_int
    syscall
    move $a0, $v0 # Move input (n) to $a0 for fibonacci call

    # Call fibonacci function
    jal fibonacci # Call fibonacci(n)

    # Print "Fibonacci number: "
    li $v0, 4 # syscall for print_string
    la $a0, fib_result # Load address of fib_result
    syscall

    # Print fibonacci number
    move $a0, $v0 # Move result to $a0 to print fibonacci number.
    li $v0, 4 # syscall for print_string
    syscall

    # Print "The number of fibonacci function calls: "
    la $a0, call_count # Load address of call_count
    syscall

    # Print number of fibonacci function calls
    move $a0, $s0
    syscall

    # Exit program
    li $v0, 10 # syscall for exit
    syscall

fibonacci:
    addi $sp, $sp, -8 # Allocate stack frame 8 bytes.
    sw $ra, 4($sp) # Store return address into stack frame.
    addi $s0, $s0, 1 # Make cnt = cnt + 1;
    li $t0, 1
    bne $a0, $t0, L1 # If n != 0 then move line L1.
    # n == 0 case.
    li $v0, 0 # Make return value 0.
    addi $sp, $sp, 8 # Destroy stack frame.
    jr $ra # Make return to previous pc.
L1: li $t0, 2
    bne $a0, $t1, L2 # If n!= 1, then move line L2.
    # n == 1 case.
    li $v0, 1 # Make return value 1.
    addi $sp, $sp, 8 # Destroy stack frame.
    jr $ra, # Make return to previous pc.
L2: # n > 1 case.
    addi $a0, $a0, -1 # n = n - 1.
    sw $a0, 0($sp) # Store argument into stack frame.
    jal fibonacci # Do recursive fibonacci(n-1).
    lw $a0, 0($sp)
    add $s1, $v0, $zero # Store result to register s1.
    addi $sp, $sp, -4 # Increase stack frame 4 byte more.
    sw $s1, 0($sp) # Backup register s1 value into stack.
    addi $a0, $a0, -1 # n = n - 1.
    sw $a0, 4($sp) # Store argument into stack frame.
    jal fibonacci # Do recursive fibonacci(n-1).
    lw $a0, 4($sp)
    add $s2, $v0, $zero # Store result to register s2.
    add $v0, $s1, $s2 # return value = fibonacci (n - 1) + fibonacci(n - 2)
    lw $ra, 8($sp) # Restore return address to $ra.
    addi $sp, $sp, 12 # Destroy stack frame.
    jr $ra # Return.
