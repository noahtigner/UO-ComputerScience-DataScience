#include <stdio.h>
#include <string.h>

void proc_input(char* source) {
  unsigned char buf[160];
  int balance = 0;

  strcpy(buf, source);

  printf("balance: %d\n", balance);
}

int main() {
  unsigned char buf[256] = {'\0'};
  FILE *fp;

  fp = fopen("abc", "rb");
  fread(buf, 256, 1, fp);
  buf[255]='\0';

  proc_input(buf);

  fclose(fp);
}
