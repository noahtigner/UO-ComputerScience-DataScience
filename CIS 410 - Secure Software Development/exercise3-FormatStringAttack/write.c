#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 1024

int main(int argc, char * argv[]){
  char buf[BUF_SIZE];

  static int balance = 0x0012d687; 


  strncpy(buf, argv[1], BUF_SIZE);

  printf("Safe: ");
  printf("%s", buf);
  printf("\n");

  printf("Vulnerable: ");
  printf(buf);      
  printf("\n");

  printf("*** balance @ %p = %d 0x%08x\n", &balance,balance,balance);

  exit(0);

}