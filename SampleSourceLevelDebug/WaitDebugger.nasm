BITS 64
DEFAULT REL

section .text
    global WaitDebugger

WaitDebugger:
    mov rax, 0F8AB709FD9C57EA1h

Loop:
    cmp rax, 0h
    pause

    jnz Loop

    ret