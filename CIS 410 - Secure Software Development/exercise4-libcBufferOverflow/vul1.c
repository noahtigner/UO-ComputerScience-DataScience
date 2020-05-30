#include <stdio.h>
#include <string.h>

void proc_input(char* source) {
  unsigned char buf[80]; //note to use unsigned char


  strcpy(buf, source);

//  printf("vul: %d\n", strlen(buf));

//int i;
//printf("\n dst-buf[0-79]=\n"); for (i=0; i<80;i++){printf("%02x ",buf[i]);}
//printf("\n dst-buf[88-99]=\n"); for (i=88; i<100;i++){printf("%02x ",buf[i]);}
//printf("\n before return, it will cause buffer overflow...\n");
//printf("\n dst-buf[120-127]=\n"); for (i=120; i<128;i++){printf("%02x ",buf[i]);}

}

int main() {
  unsigned char pwd[9] = "Pa55w0rd";
  unsigned char buf[128] = {'\0'};
  FILE *fp;

  fp = fopen("abc", "rb");
  fread(buf, 128, 1, fp);

//int i;
//printf("\n src-buf[0-127]=\n"); for (i=0; i<128;i++){printf("%02x ",buf[i]);}

  proc_input(buf);

  fclose(fp);
}