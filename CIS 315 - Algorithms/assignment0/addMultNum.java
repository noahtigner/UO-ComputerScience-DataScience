import java.util.Scanner;

public class addMultNum {
	public static void main(String[] args){

        //Initialize scanner
        Scanner sc = new Scanner(System.in);  
        sc.nextLine();
        
        //Loop through input file or stream
        while(sc.hasNext()) {
        	String line = sc.nextLine(); 

            //Parse line into first and second ints
            String[] arr = line.split(" ", 2);
            int first = Integer.valueOf(arr[0]);
            int second = Integer.valueOf(arr[1]);

            //print(sum product)
            System.out.println(first + second + " " + first * second);
        }
        //Close Scanner
        sc.close();
	}
}