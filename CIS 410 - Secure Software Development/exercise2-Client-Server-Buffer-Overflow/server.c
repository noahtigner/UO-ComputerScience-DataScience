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
#define hostAddress "184.171.124.101" //hard-coded server address
#define PORT 5010 //hard-coded port number for server to communicate with clients

void proc_buf(char* p);

void handle_conn(int fd);

int main(int argc, char *argv[]) {

 int listenfd = 0, connfd = 0;
 struct sockaddr_in serv_addr; // Address of server
 listenfd = socket(AF_INET, SOCK_STREAM, 0); // Create a file descriptor for

 // Prepare the socket address and port
 memset(&serv_addr, '0', sizeof(serv_addr));
 serv_addr.sin_family = AF_INET;
 serv_addr.sin_addr.s_addr = inet_addr(hostAddress);
 serv_addr.sin_port = htons(PORT);
 bind(listenfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)); //Bind

 // Listen to connection requests from clients
 listen(listenfd, 10);
 printf("server is ready...\n");
 while(1) {

    // Accept the incoming connection request
    connfd = accept(listenfd, (struct sockaddr *)NULL, NULL);

    // Handle the connection
    handle_conn(connfd);
  }
}

void proc_buf(char* p) {
 while(*p) {
 *p = toupper(*p);
 p++;
 }
 return;
}


void handle_conn(int fd) {
 printf("handle_conn\n");
 unsigned char *p, *q;

 struct {
 unsigned nbytes; // Number of bytes that will be received from client
 void (*fp) (char*); // Function pointer
 } s;

 s.fp = proc_buf; // Set s.fp to function proc_buf
 read(fd, &(s.nbytes), sizeof(s)); // Step 1
 write(fd, "okay", 4+1); // Step 2

 size_t npages = s.nbytes/4096; // Pages to be received next
 npages += s.nbytes ? 1 : 0;
 
 p =( mmap ( NULL, npages * 4096,PROT_READ | PROT_WRITE | PROT_EXEC,
 MAP_PRIVATE | MAP_ANONYMOUS,-1, 0 )); // Step 3

 q = p;
 while (s.nbytes > 0) {
 unsigned nread = read (fd, q, s.nbytes); // Step 4
 s.nbytes -= nread;
 q += nread;
 }

 printf ("receive data address is in range: %p-%p\n", p, q); // Address of received data
 s.fp (p); // Step 5: change data received at p to uppercase
 write(fd, p, strlen(p)+1); // Step 6: send uppercase data at p to client
 munmap(p, npages*4096);
 close(fd);

} 
