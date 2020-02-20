import java.util.ArrayList;

public class Arrays {
	public static void main(String[] args ) {

		int[] array = {1, 2, 3, 4};
		for(int i = 0; i < array.length; i++) {
			System.out.println(array[i]); 
		}
		
		// ArrayList
		// length, size can change
		//listarray = new ArrayList<>();
		//listarray.add(3);
		//listarray.add(index, var);
		
		ArrayList <int[]> list = new ArrayList<>();
		
		System.out.println(list.size()); //have size not length
		foo(1, 0.5);
		
	}
	//method that mus return an int
	public static int foo(int length, double density) {
		
		return 0; // place holder return statement
	}
}

