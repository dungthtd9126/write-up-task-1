#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_USERS 5
#define MAX_NAME 32
#define MAX_FILE 256

char usernames[MAX_USERS][MAX_NAME];
char passwords[MAX_USERS][MAX_NAME];
char files[MAX_USERS][MAX_FILE];
bool logged[MAX_USERS];

int user_count = 0;
int current = -1;

void register_user() {
    if (user_count >= MAX_USERS) { puts("User limit!"); return; }

    char user[MAX_NAME], pass[MAX_NAME];
    printf("Username: "); fgets(user, sizeof(user), stdin);
    user[strcspn(user, "\n")] = 0;

    printf("Password: "); fgets(pass, sizeof(pass), stdin);
    pass[strcspn(pass, "\n")] = 0;

    for (int i = 0; i < user_count; i++) {
        if (!strcmp(usernames[i], user)) {
            puts("User exists!");
            return;
        }
    }

    strcpy(usernames[user_count], user);
    strcpy(passwords[user_count], pass);
    files[user_count][0] = 0;
    logged[user_count] = false;
    user_count++;

    puts("Registered!");
}

void login() {
    char user[MAX_NAME], pass[MAX_NAME];
    printf("Username: "); fgets(user, sizeof(user), stdin);
    user[strcspn(user, "\n")] = 0;

    printf("Password: "); fgets(pass, sizeof(pass), stdin);
    pass[strcspn(pass, "\n")] = 0;

    for (int i = 0; i < user_count; i++) {
        if (!strcmp(usernames[i], user) && !strcmp(passwords[i], pass)) {
            logged[i] = true;
            current = i;
            puts("Login OK!");
            return;
        }
    }
    puts("Invalid!");
}

void write_file() {
    if (current < 0 || !logged[current]) {
        puts("Not logged in!");
        return;
    }

    printf("Content: ");
    fgets(files[current], MAX_FILE, stdin);
    files[current][strcspn(files[current], "\n")] = 0;

    puts("Saved!");
}

void read_file() {
    if (current < 0 || !logged[current]) {
        puts("Not logged in!");
        return;
    }

    if (strlen(files[current]) == 0) {
        puts("Empty!");
        return;
    }

    char buf[MAX_FILE];
    memcpy(buf, files[current], MAX_FILE);

    printf(buf);     
    printf("\n");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);

    char cmd[32];
    puts("=== Mini File Manager ===");

    while (1) {
        printf("> ");
        if (!fgets(cmd, sizeof(cmd), stdin)) break;
        cmd[strcspn(cmd, "\n")] = 0;

        if (!strcmp(cmd, "REGISTER")) register_user();
        else if (!strcmp(cmd, "LOGIN")) login();
        else if (!strcmp(cmd, "WRITE")) write_file();
        else if (!strcmp(cmd, "READ")) read_file();
        else if (!strcmp(cmd, "EXIT")) break;
        else puts("Unknown!");
    }

    return 0;
}
