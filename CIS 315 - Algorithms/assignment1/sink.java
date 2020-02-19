//import java.util.Scanner;

public class sink {
	public static void main(String[] args){

        int[][] arr = new int[5][5]; 

        arr[0][0] = 1;
        arr[0][1] = 1; 
        arr[0][4] = 1; 

        arr[1][1] = 1;
        arr[1][4] = 1;

        //arr[2][1] = 1;
        //arr[2][4] = 1;

        arr[3][1] = 1;
        arr[3][4] = 1;

        arr[4][1] = 1;
        arr[4][3] = 1;

        for(int i = 0; i < arr.length; i++) {
            for(int j = 0; j < arr[0].length; j++) {
                System.out.print(" " + arr[i][j]); 
            }
            System.out.print('\n'); 
        }



        int sink = hasSink(arr);
        if(sink != -1) {
            System.out.println("Vertex " + sink + " is a universal sink"); 
        }
        else {
            System.out.println("No universal sink"); 
        }
      
    }

    public static int hasSink(int[][] arr) {
        int i = 0;
        int j = 0;

        while(i < arr.length && j < arr.length) {
            if(arr[i][j] == 1) {
                i++;
            }
            else {
                j++;
            }
        }
        return i;
        /*
        if(isSink(arr, i)) {
            return i;
        }
        return -1;*/
    }

    public static boolean isSink(int[][] arr, int i) {
        
        for(int in = 0; in < arr.length; in++) {
            
            if(arr[i][in] == 1) {
                return false;
            }
            if(arr[in][i] != arr[i][i] && arr[in][i] == 0) {
                return false;
            }
        }
        return true;
    }
}