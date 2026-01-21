# Easy
## secure access
- This challenge is pretty simple

<img width="596" height="348" alt="image" src="https://github.com/user-attachments/assets/8d390238-9dac-4b79-96c7-af5e258ba675" />

<img width="805" height="252" alt="image" src="https://github.com/user-attachments/assets/955f0dd1-d23d-4a97-9d7a-e7da7b4285f8" />

- We can see that we there are bof that we can overwrite saved rip
- So we only need to overwrite it to win function in challenge

## shellcode
- Another easy challenge, i only need to send my payload and it will execute my shellcode which is the most basic technique in bof
# Medium
## Warrior
- This is a heap based challenge, we have uaf in here and we can abuse it to overwrite function ptr with the purpose of ret2win
- First, we can see that pie is off and there is win function

<img width="1248" height="312" alt="image" src="https://github.com/user-attachments/assets/f070b23b-9374-4938-a3f6-c8a94bca34b7" />

<img width="920" height="274" alt="image" src="https://github.com/user-attachments/assets/43ede921-69c5-4d1c-9d1e-0f538066cfae" />

- Next we can see that in option 1, it will create 2 chunks: the first chunk is used to store function ptr and name ptr

<img width="699" height="743" alt="image" src="https://github.com/user-attachments/assets/29fb5b43-6fe8-4074-a5ac-a52f71dece5c" />

<img width="1232" height="999" alt="image" src="https://github.com/user-attachments/assets/e8eb8fd8-1a4e-40e8-9f6a-aef998e78c21" />

- So our target is to overwrite that function ptr to win ptr when we call test weapon

<img width="619" height="317" alt="image" src="https://github.com/user-attachments/assets/a32420e6-91a5-4980-a3e4-a049dffa02d9" />

- As we can see, when discard weapon, it only free chunks but not delete it ptr
- That enables me to uaf
- My progress is:
        - First, forge weapon at 0
        - Then free it --> forge again at index 1
        --> After that step, i will have uaf as index 0 and 1 have the same ptr because of the mechanism of tcache bin. It will reuse freed chunks when it can
- The next step is free index 0 again
- And then the chunk which contain func ptr with size of 0x20 will go to tcache bin
- Then i just need to create another chunk with the same size to reuse that chunk by rename function

<img width="646" height="378" alt="image" src="https://github.com/user-attachments/assets/82d0521f-1ddc-4a3b-8f68-5b42bd6e0020" />

- So we have succesfully get access to overwrite the function ptr by reuse the chunk storing func ptr from bins
- The next step is just overwrite the func ptr with win func and call it by test_weapon func
- And we can call it at index 0 or 1 because the ptr wasn't deleted and they have the same ptr. Just call test_weapon with either idx then win
## file_manager
- This challenge is a bit time-consuming because ill have to guess its libc version which affects my payload a lot and the event doesn't give me libc
- The main idea of this challenge is using fmt str to leak libc --> fmtstr changing saved rbp to stack pivot by rbp
- After that ill stack pivot to my input in bss section easily because PIE is off
- Finally, ill put my rop chain with useful gadgets in that pivot address to execute execve('/bin/sh') because my input is stored in low bss address so i prefer to not use system()

<img width="610" height="512" alt="image" src="https://github.com/user-attachments/assets/a7a45218-95fa-4eca-b725-f8f7ade07875" />

<img width="938" height="996" alt="image" src="https://github.com/user-attachments/assets/258cc173-3e8e-4682-85d8-191088ef060e" />


- As we can see, the only obvius bug is fmt str in read files and our input will store in files section
- There is also a write files which we can write a amount of byte that is the same with the section size
- And PIE is off, thats mean i can just stack pivot to this section and rop chain to get shell
- Note that we need to register and login first, then we just need to abuse read and write function to fmtstr to control our program run to our rop chain by stack pivot
