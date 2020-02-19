import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;


public class ServerExtra {
	
	private static final int PORT = 42069;
	
	@SuppressWarnings("unchecked")
	public static void main(String[] args) {		
		System.out.println("running server!");
		
		ServerSocket serverSocket = null;
		Socket socket = null;
		ObjectOutputStream outputStream = null;
		ObjectInputStream inputStream = null;		
		List<Integer> in;
		List<Integer> out = new ArrayList<Integer>();
		
		try {
			serverSocket = new ServerSocket(PORT);
			
			System.out.println("server socket created");

			
			socket = serverSocket.accept();
			
			outputStream = new ObjectOutputStream(socket.getOutputStream());
			outputStream.flush();
			
			inputStream = new ObjectInputStream(socket.getInputStream());
			
			in = (List<Integer>) inputStream.readObject();		

			for(int i = 0; i < in.size(); i++) {
				if(isPrime(in.get(i))) {
					out.add(in.get(i));
					//System.out.println(in.get(i));
				}
			}
			
			outputStream.writeObject(out);
			in.clear();
			out.clear();
			outputStream.flush();
			
		} catch (IOException ex) {
			ex.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				if (serverSocket != null) {
					serverSocket.close();
				}
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
		
		//System.out.println("server finished");

	}
	public static boolean isPrime(int i) {
		if(i == 1) {
			return false;
		}
	    if(i > 2 && (i & 1) == 0) {
	    	return false;
	    }
	    for(int j = 3; j * j <= i; j += 2) {
	        if (i % j == 0) {
	            return false;
	        }
	    }
	    return true;
	}
}
