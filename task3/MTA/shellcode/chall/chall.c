#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);

    char *s;

    s = mmap(NULL, 256, PROT_READ | PROT_WRITE | PROT_EXEC,
             MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (s == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    printf("Enter your shellcode (max %d bytes):\n", 256);

    if (!fgets(s, 256, stdin)) {
        perror("fgets");
        exit(1);
    }

    void (*func)(void) = (void (*)())s;
    func();

    munmap(s, 256);
    return 0;
}
