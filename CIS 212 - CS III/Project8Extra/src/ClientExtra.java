import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.ThreadLocalRandom;


public class ClientExtra {
	
	private static final int PORT = 42069;
	
	@SuppressWarnings("unchecked")
	public static void main(String[] args) {
		
		Scanner input = new Scanner(System.in);
		
		List<Integer> out = new ArrayList<Integer>();
		List<Integer> in = new ArrayList<Integer>();
		int counter = 0;
		
		
		Socket socket = null;
		ObjectOutputStream outputStream = null;
		ObjectInputStream inputStream = null;	
		InetAddress address;
		
		try {
			address = InetAddress.getLocalHost();
			socket = new Socket(address, PORT);
			//System.out.println("socket created");
			
			outputStream = new ObjectOutputStream(socket.getOutputStream());
			outputStream.flush();

			
			
			inputStream = new ObjectInputStream(socket.getInputStream());

			
			System.out.println("Enter “!” to start and stop, “#” to quit");
			do { 

				try {
					String s = input.next();
					if(s.startsWith("!")) {
						counter++;

						if(counter % 2 != 0) {
							for(int i = 0; i < 5; i++) {
								int randomNumber = ThreadLocalRandom.current().nextInt(2, 100 + 1);
								out.add(randomNumber);
								
							}
							outputStream.writeObject(out);
							System.out.println("Send: " + out);
							
							in = (List<Integer>) inputStream.readObject();
							System.out.println("Receive: " + in);
						

						}
						else {
							System.out.println("Enter “!” to start and stop, “#” to quit");
							out.clear();
							outputStream.flush();
							in.clear();
							inputStream.reset();
						}
					}	
					else if(s.startsWith("#")) {
						System.out.println("Close");
						input.close();
						break;
					}			      
			    }
			    catch (Exception e) {
			    }
			}
			while (true);
				
		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (socket != null) {
					socket.close();
				}
				if (outputStream != null) {
					outputStream.close();
				}
				if (inputStream != null) {
					inputStream.close();
				}
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
		
		//System.out.println("client finished");

	}
}
