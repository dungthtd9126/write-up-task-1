#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void win() {
    system("/bin/sh");
}

int main(int argc, char **argv, char **envp) {
    setvbuf(stdout, NULL, _IONBF, 0);
    
    char s[259];
    char tmp;
    int len;
    unsigned long i;

    gets(s);

    len = strlen(s);

    for (i = 0; i < len / 2; i++) {
        tmp = s[len - 1 - i];
        s[len - 1 - i] = s[i];
        s[i] = tmp;
    }

    puts("Reversed string:");
    puts(s);

    return 0;
}


