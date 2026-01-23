# Knight
## knight academy
- This challenge has only one vunerable, bof and no pie, no canary


<img width="1196" height="621" alt="image" src="https://github.com/user-attachments/assets/183756cf-61f0-4c42-ae0c-9c364d07d429" />

- There is a function that print flag to output
- So i just need to ret2 that function by overwriting saved rip with bof

<img width="600" height="565" alt="image" src="https://github.com/user-attachments/assets/8ae71b3c-3846-43f2-b8fa-bda45632ce88" />

## jail 1
- This is a black box challenge, so i need to guess a lot
- The only hint is in the description

<img width="945" height="681" alt="image" src="https://github.com/user-attachments/assets/f5f8f1d8-6de3-4fc9-809c-0c1f70e177e5" />

- As we can see, the author love chars. So the challenge may relate to char
- So i will just input random words
- And after i enter Q(), the server give me some instruction about a function name Q and it argument

<img width="807" height="241" alt="image" src="https://github.com/user-attachments/assets/45c94f50-1e57-41af-8ba1-eeafc3215f8a" />

- Then ill just guess by input random argument in it. After i input random number in both argument it may print this

<img width="453" height="201" alt="image" src="https://github.com/user-attachments/assets/690c7295-7275-47a3-8127-630acf2220ff" />

- In this stage, i used AI to guess it usage. And from what gemini teach me, it is use to compare the position 'i' with the ascii of a char 'x' arguments
- If the value is right, it will return 1. If wrong, it may return -1 or 0
- At this stage, i used AI to write brute force each char of the flag
- The idea is pretty simple, ill guess each character at 0 index first. If it return 1, ill increase the index and guess from start and repeat to the end of the flag
##
