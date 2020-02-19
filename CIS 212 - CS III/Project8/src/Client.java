import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class Client {
	
	private static final int PORT = 42069;
	
	@SuppressWarnings("unchecked")
	public static void main(String[] args) {
		
		Scanner input = new Scanner(System.in);
		int i;
		List<Integer> out = new ArrayList<Integer>();
		List<Integer> in = new ArrayList<Integer>();
		  
		do { 
			System.out.println("Enter an integer (“!” to send):");
			try {
				String s = input.next();
				if(s.startsWith("!")) {
					System.out.println("Send: " + out);
					input.close();
					break;
				}		
		        i = Integer.parseInt(s);
		        out.add(i);
		    }
		    catch (Exception e) {
		    }
		}
		while (true);
		
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

			outputStream.writeObject(out);
			
			inputStream = new ObjectInputStream(socket.getInputStream());
			in = (List<Integer>) inputStream.readObject();
			
			System.out.println("Receive: " + in);
			
		} catch (UnknownHostException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
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
