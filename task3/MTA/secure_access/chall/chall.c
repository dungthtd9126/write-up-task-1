#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int secret_room() {
    char s[256];
    FILE *stream;

    stream = fopen("flag.txt", "r");
    if(!stream) {
        puts("Error: flag file is missing.");
        exit(1);
    }
    if(!fgets(s, sizeof(s), stream)) {
        puts("Error: unable to read the flag.");
        fclose(stream);
        exit(1);
    }
    fclose(stream);

    int l = strlen(s);
    if(l && s[l-1] == '\n')
        s[l-1] = 0;

    return printf("[+] FLAG: %s\n", s);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    char s[64];

    puts("=== Secure Access Console v1.0 ===");
    puts("System online.");
    puts("Provide input to proceed:");

    fgets(s, 80, stdin);  

    return 0;
}