import gdb
import re
import logging

def get_program_path():
    return "D:/repo/native/edk2/SampleSourceLevelDebugPkg/Build/NOOPT_CLANGDWARF/X64/SampleSourceLevelDebug.debug"

gdb.execute("target remote 127.0.0.1:8864")

rax = gdb.Value(int(gdb.parse_and_eval('$rax')))
rip = gdb.Value(int(gdb.parse_and_eval('$rip')))

rip = rip & (~0xFFF)

if rax == 0xF8AB709FD9C57EA1:
    while rip > 0:
        data = int.from_bytes(gdb.selected_inferior().read_memory(rip, 4)) >> 16
        if data == 0x4D5A:
            break
        rip -= 0x1000

    if rip != 0:
        rip += 0x240
        gdb.execute("add-symbol-file " + get_program_path() + " " + hex(rip))
        gdb.execute("set $rax = 0x0")