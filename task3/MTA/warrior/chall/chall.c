y#include <stdio.h>
#include <stdlib.h>

struct weapon
{
    char *name;
    void (*attack_func)();
} *inventory[8];

void init()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

void secret_skill(){
    puts(">>> ULTIMATE SKILL ACTIVATED: SYSTEM SHELL!");
    system("/bin/sh");
}

void menu()
{
    puts("--- WARRIOR INVENTORY ---");
    puts("1. Forge new weapon");
    puts("2. Rename weapon");
    puts("3. Discard weapon");
    puts("4. Test weapon");
    puts("5. Exit");
    printf("> ");
}

void sword_attack()
{
    puts("Slash! Swish! [Physical Dmg]");
}

void bow_attack()
{
    puts("Twang! Thwack! [Ranged Dmg]");
}

void wand_attack()
{
    puts("Fwoosh! Boom! [Magic Dmg]");
}

void forge_weapon(int index)
{
    unsigned int type, size;

    inventory[index] = malloc(sizeof(struct weapon));

    puts("1. Iron Sword");
    puts("2. Hunter Bow");
    puts("3. Magic Wand");
    printf("> ");
    scanf("%u", &type);
    if (type==1)
        inventory[index]->attack_func = sword_attack;
    else if (type==2)
        inventory[index]->attack_func = bow_attack;
    else if (type==3)
        inventory[index]->attack_func = wand_attack;

    printf("Name length: ");
    scanf("%u", &size);
    getchar();
    inventory[index]->name = malloc(size);

    printf("Weapon Name: ");
    fgets(inventory[index]->name, size, stdin);
}

void rename_weapon(int index)
{
    unsigned int size;

    printf("New name length: ");
    scanf("%u", &size);
    getchar();
    
    inventory[index]->name = malloc(size);

    printf("New Weapon Name: ");
    fgets(inventory[index]->name, size, stdin);
}

void discard_weapon(int index)
{
    free(inventory[index]->name);
    free(inventory[index]);
}

void test_weapon(int index){
    inventory[index]->attack_func();
}

int main()
{
    int is_done = 0, option, index;

    init();

    while (!is_done)
    {
        menu();
        scanf("%d", &option);
        getchar();

        index = 8;
        printf("Slot Index: ");
        scanf("%d", &index);
        getchar();

        switch(option)
        {
        case 1:
            forge_weapon(index);
            break;
        case 2:
            rename_weapon(index);
            break;
        case 3:
            discard_weapon(index);
            break;
        case 4:
            test_weapon(index);
            break;
        case 5:
            is_done = 1;
            break;
        default:
            puts("Invalid choice!");
        }
    }
}