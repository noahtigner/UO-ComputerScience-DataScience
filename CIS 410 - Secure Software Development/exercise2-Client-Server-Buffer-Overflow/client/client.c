#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>
#include <sys/mman.h>
//#include <windows.h>
#include <ctype.h>
#include <unistd.h>
#define PORT 5010  //hard-coded sever port number 
#define hostAddress  "184.171.124.101" //hard-coded server IP address 

int main(int argc, char *argv[]) { 
  unsigned char *str = argv[1]; // message to send to server which converts it to upper case

  int sockfd = 0,n = 0;
  unsigned char recv_buf[1024];
  struct sockaddr_in serv_addr;
 
  memset(recv_buf, '0' ,sizeof(recv_buf));
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {

      printf("\n Error : Could not create socket \n");
      return 1;
    }
 
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(PORT); // set server port number
  serv_addr.sin_addr.s_addr = inet_addr(hostAddress); // set server address
 
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
         return 1;
    }

  struct {
         unsigned nbytes; 
         unsigned payload_addr;
  }v;
   
  v.nbytes = 4096; // Set size of data to be sent as 4096 bytes
  write (sockfd, &v, sizeof (v.nbytes)); // Send v to server 

  read(sockfd, recv_buf, sizeof (recv_buf) - 1); // Receive a message ("Okay") from client
  puts(recv_buf); // Print the received message

  unsigned char payload_buf [4096];
  memset(payload_buf, 0, sizeof(payload_buf)); 
  strcpy(payload_buf, str); // Copy the string to payload_buf 
  write (sockfd, payload_buf, 4096); // Send payload_buf to server
  
  read (sockfd, recv_buf, sizeof (recv_buf) - 1); // Receive the converted string
  puts (recv_buf); // Print the converted string }

}
