import java.util.Scanner;
import java.util.Random;
import java.util.ArrayList;

public class Project2 {
	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		
		while(true) {
			System.out.println("Enter the integer array length: ");
			int length = input.nextInt();
			System.out.println("Enter a double-precision array density: ");
			double density = input.nextDouble();
			if(length > 0 & (density < 1.0 & density > 0.0)) {
				
				long Time1 = System.nanoTime();
				sparseArray(length, density);
				long Time2 = System.nanoTime();
				System.out.printf("create dense array of length: %d, time: %d\n", length, ((Time2 - Time1)/1000000));
				
				long Time3 = System.nanoTime();
				denseArray(length, density);
				long Time4 = System.nanoTime();
				System.out.printf("create sparse array of length: %d, time: %d\n", length, ((Time4 - Time3)/1000000));
				
				long Time5 = System.nanoTime();
				denseToSparse(denseArray(length, density));
				long Time6 = System.nanoTime();
				System.out.printf("convert a dense array to a sparse array of length: %d, time: %d\n", length, ((Time6 - Time5)/1000000));
				
				long Time7 = System.nanoTime();
				sparseToDense(sparseArray(length, density), length);
				long Time8 = System.nanoTime();
				System.out.printf("convert a sparse array to a dense array of length: %d, time: %d\n", length, ((Time8 - Time7)/1000000));
				
				long Time9 = System.nanoTime();
				denseMax(denseArray(length, density));
				long Time10 = System.nanoTime();
				System.out.printf("time to find the max in a dense array: %d\n", ((Time10 - Time9)/1000000));

				long Time11 = System.nanoTime();
				sparseMax(sparseArray(length, density));
				long Time12 = System.nanoTime();
				System.out.printf("time to find the max in a sparse array: %d\n", ((Time12 - Time11)/1000000));
			
				input.close();
				break;
			}
		}
	}
	
	public static int[] denseArray(int length, double density) {
		Random random = new Random();
		int[] denseArray = new int[length];
		for(int i = 0; i < length; i++) {
			double randomDouble = random.nextDouble();
			if(randomDouble <= density) { // might need to be <
				denseArray[i] = random.nextInt(1000000);
			}
		}
		return denseArray;
	}
	
	public static ArrayList <int[]> sparseArray(int length, double density) {
		Random random = new Random();
		ArrayList <int[]> sparseArray = new ArrayList<>();
		for(int i = 0; i < length; i++) {
			double randomDouble = random.nextDouble();
			if(randomDouble <= density) {
				int randomInt = random.nextInt(1000000);
				int[] newArray = {i, randomInt};
				sparseArray.add(newArray);
			}
		}
		return sparseArray;
	}

	public static ArrayList <int[]> denseToSparse(int[] denseArray) {
		Random random = new Random();
		ArrayList <int[]> sparseArray = new ArrayList<>();
		for(int i = 0; i < denseArray.length; i++) {
			if(denseArray[i] != 0) {
				int randomInt = random.nextInt(1000000);
				int[] newArray = {i, randomInt};
				sparseArray.add(newArray);
			}
		}
		return sparseArray;
	}
	
	public static int[] sparseToDense(ArrayList <int[]> sparseArray, int length) {
		int[] denseArray = new int[length];
		for(int i = 0; i < sparseArray.size(); i++) {
			if(sparseArray.get(i)[1] != 0) {
				denseArray[sparseArray.get(i)[0]] = sparseArray.get(i)[1];
			}
		}
		return denseArray;
	}
	
	public static void denseMax(int[] denseArray) {
		int max = 0;
		int index = 0;
		for(int i = 0; i < denseArray.length; i++) {
			if(denseArray[i] > max) {
				max = denseArray[i];
				index = i;
			}	
		}
		System.out.printf("find max (dense): %d, at: %d \n", max, index);
	}
	
	public static void sparseMax(ArrayList <int[]> sparseArray) {
		int max = 0;
		int index = 0;
		for(int i = 0; i < sparseArray.size(); i++) {
			if(sparseArray.get(i)[1] > max) {
				max = sparseArray.get(i)[1];
				index = sparseArray.get(i)[0];
			}
		}
		System.out.printf("find max sparse: %d, at: %d \n", max, index);
	}
	
}

// Converting a sparse array to a dense takes longer than going the other way
// For both large and small array lengths, sparse arrays are much quicker to create
// For extremely large array lengths (>10,000,000), sparse arrays are slightly slower to construct
// Density has a huge effect on which type of array is faster. 
// A higher density means that the sparse array will be much faster than the dense
// A higher density greatly increase the time it takes to find the max in a sparse array


