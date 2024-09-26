.data # Data segment
prompt: .asciiz "The index for the Fibonacci sequence: " # Prompt for input
fib_result: .asciiz "Fibonacci number: " # Format for Fibonacci result
call_count: .asciiz "The number of fibonacci function calls: " # Format for call count
newline: .asciiz "\n" # Newline string
.text # Code segment
.globl main # Entry point
add $s0 $zero $zero # Set int cnt as 0.
main:
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
    # Exit program
    li $v0, 10 # syscall for exit
    syscall
fibonacci:
    addi $sp $sp -8 # Allocate stack frame 8 bytes.
    sw $ra 4($sp) # Store return address into stack frame.
    sw $a0 0($sp) # Store argument into stack frame.
    addi $s0 $s0 1 # Make cnt = cnt + 1;
    bne $a0 $zero L1 # If n != 0 then move line L1.
    # n == 0 case.
    li $v0 $zero # Make return value 0.
    addi $sp $sp 8 # Destroy stack frame.
    jr $ra # Make return to previous pc.
L1: li $t0 1
    bne $a0 $t1 L2 # If n!= 1, then move line L2.
    # n == 1 case.
    li $v0 1 # Make return value 1.
    addi $sp $sp 8 # Destroy stack frame.
    jr $ra # Make return to previous pc.
L2:
