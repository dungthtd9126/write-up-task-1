# Knight
## Knight Squad Academy 
- This challenge has only one vunerable, bof and no pie, no canary


<img width="1196" height="621" alt="image" src="https://github.com/user-attachments/assets/183756cf-61f0-4c42-ae0c-9c364d07d429" />

- There is a function that print flag to output
- So i just need to ret2 that function by overwriting saved rip with bof

<img width="600" height="565" alt="image" src="https://github.com/user-attachments/assets/8ae71b3c-3846-43f2-b8fa-bda45632ce88" />

## Knight Squad Academy Jail
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
- Each character that is correct, ill stored in a variable. After i get '}', ill exit the loop and print out the full flag
## Knight Squad Academy Jail 2
- This challenge is also simple too, ill have to guess again
- But this time, the server won't ouput error to us so we cant know if we used right function
- But luckily, the hint is pretty obvious
<img width="831" height="603" alt="image" src="https://github.com/user-attachments/assets/32765f76-d235-44c1-97be-6ca4683d208f" />

- Only a knight can help me, so if i used knight function alone, it will output error ( error is a word that output everytime i used wrong function or not enough argument). But with other function, it just say dont exist
- The server is pretty lag at the moment im writing this so i may not give enough images
- So the core idea of this challenge is: knight(string argument)
- And this function will check how many char that i guess correctly, then it will output that as first number
- The second number is index at place i guess wrong, for me, it doesnt matter much because my method dont need second number
- Note that if the string argument must be the same length as the flag
- So i will have to guess the flag length first. If my string not fit in size, it may return "too long" or "too short"
- After succesfully guess the flag length, ill brute force each char of the flag, from "KCTF{" to "}"
- First, ill input string full of "!" char to check if the flag has that char.
- If not, then ill use that as default for padding the string argument long enough for the length check bypass
- In this stage, i used gemini to write script for me so im done here, the rest is the server speed and time
