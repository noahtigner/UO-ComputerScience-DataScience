import java.util.Arrays;
import java.util.List;

public class Main {
	
	public static void main(String[] args) {

		// Test add
		OccurenceSet<Integer> intSet = new OccurenceSet<Integer>();
		intSet.add(1);
		intSet.add(3);
		intSet.add(3);
		intSet.add(3);
		intSet.add(5);
		System.out.println(".add()... " + intSet.toString());
		
		// Test addAll
		List<Integer> nums1 = Arrays.asList(2, 7, 9);
		intSet.addAll(nums1);
		System.out.println(".addAll()... " + intSet.toString());
		
		// Test remove
		intSet.remove(5);
		System.out.println(".remove()... " + intSet.toString());
		
		// Test removeAll
		List<Integer> nums2 = Arrays.asList(1, 3);
		intSet.removeAll(nums2);
		System.out.println(".removeAll()... " + intSet.toString());
		
		// Test retainAll
		List<Integer> nums3 = Arrays.asList(2, 7);
		intSet.retainAll(nums3);
		System.out.println(".retainAll()... " + intSet.toString());
		
		// Test contains
		System.out.println(".contains(): " + intSet.contains(2));
		
		// Test containsAll
		System.out.println(".containsAll(): " + intSet.containsAll(nums3));
		
		// Test size
		System.out.println(".size(): " + intSet.size());
		
		// Test clear
		intSet.clear();
		System.out.println(".clear()...");
		
		// Test isEmpty
		System.out.println(".isEmpty(): " + intSet.isEmpty());
		
		// Test iterator
			// used in toArray
		
		// Test toArray
		intSet.addAll(nums3);
		
		System.out.println(".toArray(): " + intSet.toArray()
		+ ", length: " + intSet.toArray().length);
		
		// Test toArray(T[])
		Integer[] a = new Integer[intSet.size()];
		System.out.println(".toArray(T[]): " + intSet.toArray(a)
		+ ", length: " + intSet.toArray().length);
		
		// Test toString
		System.out.println(".toString(): " + intSet.toString());
		
		
		// Testing with Strings
		OccurenceSet<String> stringSet = new OccurenceSet<String>();
		
		stringSet.add("hello");
		stringSet.add("hello");
		stringSet.add("world");
		stringSet.add("world");
		stringSet.add("world");
		stringSet.add("here");
		System.out.println(".add()..." + stringSet);
	
	}
}
