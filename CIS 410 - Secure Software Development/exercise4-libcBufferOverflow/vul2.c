#include <stdio.h>
#include <string.h>

void proc_input(char* source) {
    unsigned char buf[80];
    strcpy(buf, source);
}

int main() {
    struct {
        int balance;
        int type;
        int interest;
        char note[174];
    } account;

    account.balance = 88888888;
    account.type = 1;
    account.interest = 1;
    strncpy(account.note, "AAA", 4);

    unsigned char buf[128]  = {'\0'};
    FILE *fp;

    fp = fopen("abc", "rb");
    fread(buf, 128, 1, fp);
    
    proc_input(buf);

    fclose(fp);
}
