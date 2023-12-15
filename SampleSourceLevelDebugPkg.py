import gdb
import re
import logging

rax = gdb.Value(int(gdb.parse_and_eval('$rax')))
rip = gdb.Value(int(gdb.parse_and_eval('$rip')))

rip = rip & (~0xFFF)

def get_program_path():
    program_info = gdb.execute("info program", to_string = True)
    pattern = r"[`']([^`']*)[`']"

    match = re.search(pattern, program_info)

    if match:
        program_path = match.group(1)
        program_path = program_path.replace("\\", "/")
        print("program_path:" + program_path)
        
    return "D:/repo/native/edk2/SampleSourceLevelDebugPkg/Build/NOOPT_CLANGDWARF/X64/SampleSourceLevelDebug.debug"

logging.basicConfig(filename='test_example.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

if rax == 0xF8AB709FD9C57EA1:
    while rip > 0:
        data = int.from_bytes(gdb.selected_inferior().read_memory(rip, 4)) >> 16
        if data == 0x4D5A:
            break
        rip -= 0x1000

    if rip != 0:
        rip += 0x240
        logger.debug(gdb.execute("info program", to_string = True))
        gdb.execute("add-symbol-file " + get_program_path() + " " + hex(rip))
        gdb.execute("set $rax = 0x0")