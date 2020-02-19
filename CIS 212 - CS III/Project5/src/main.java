import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class main {
	
	public static void main(String[] args) {		
		
		try {
			
			matchedOutput(readFile("phonebook_test.txt"), "new");
			elapsedTime();
			
			System.out.println("Reversed matches with 'new':");
			for(int i = 0; i < reverse(readFile("Output.txt")).size(); i++) {
				System.out.println(reverse(readFile("Output.txt")).get(i).getFormatted());
			}
		} 
		catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	public static ArrayList<Entry> readFile(String path) {
		ArrayList <Entry> original = new ArrayList<>();
		
		try {
			File file = new File(path);
			Scanner scanner = new Scanner(file);
			
			String line = scanner.nextLine();
			while(scanner.hasNext()) {
				original.add(parseLine(line));
				line = scanner.nextLine();
			}
			scanner.close();
		}
		catch (FileNotFoundException e) {
			   e.printStackTrace();
		}
		return original;
	}
	
	public static Entry parseLine(String line) {
		
		String[] parts = line.split(" ");
		String PhoneNumber = parts[0];
		String names = "";
		names += parts[1];
		names += parts[2];
		String[] nameList = names.split(",");
		String LastName = nameList[0];
		String FirstName = nameList[1];
		return new Entry(PhoneNumber, LastName, FirstName);
	}
	
	public static void matchedOutput(ArrayList<Entry> original, String input) {
		Pattern pattern = Pattern.compile(input);
		ArrayList <String> matched = new ArrayList<>();
			
		for(int i = 0; i < original.size(); i++) {
			Matcher firstMatcher = pattern.matcher(original.get(i).getFirstName());
			Matcher lastMatcher = pattern.matcher(original.get(i).getLastName());
			
			if(firstMatcher.find()) {
				//System.out.println("First: " + original.get(i).getFirstName());
				matched.add(original.get(i).getFormatted());
			}
			else if(lastMatcher.find()) {
				matched.add(original.get(i).getFormatted());
			}
		}
		Path file = Paths.get("Output.txt"); 
		try {
			Files.write(file, matched, Charset.forName("UTF-8"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static ArrayList<Entry> reverse(ArrayList<Entry> original) {
		
		ArrayList<Entry> rev = new ArrayList<>();

		if(original.size() >= 1) {
			Entry moved = original.remove(0);
			rev.add(moved);
			reverse(original);
			original.addAll(rev);
		} 
		return original;
	}
	
	public static ArrayList<Entry> selectionSort(ArrayList<Entry> original) {
		
		ArrayList<Entry> sorted = new ArrayList<>(original);
		
		for(int i = 0; i < sorted.size() - 1; i++) {
			int min = i;
			for(int j = i + 1; j < sorted.size(); j++) {
				if(sorted.get(j).getLastName().compareTo(sorted.get(min).getLastName()) < 0) {
					min = j;
				}
			}
			Entry temp = sorted.get(i);
			sorted.set(i, sorted.get(min));
			sorted.set(min, temp);
		 }
		return sorted;
	}
	
	public static ArrayList<Entry> mergeSort(ArrayList<Entry> original) { //stackOverflowError
		
		if(original.size() <= 1) {
			return original;
		}
		return splitArray(original, 0, original.size());
	
	}
	public static ArrayList<Entry> splitArray(ArrayList<Entry> original, int start, int end) {
		ArrayList<Entry> split = new ArrayList<>(original);
		
		if(original.size() == 1) {
			return original;
		}
		else if(split.size() > 1) {
			ArrayList<Entry> half1 = splitArray(split, 0, split.size()/2);
			ArrayList<Entry> half2 = splitArray(split, split.size()/2, split.size());
			return merge(split, half1, half2);
		}	
		else {
			return original;
		}
	}
	public static ArrayList<Entry> merge(ArrayList<Entry> original, ArrayList<Entry> half1, ArrayList<Entry> half2) {
		ArrayList<Entry> merged = new ArrayList<>();
		int i = 0;
		int j = 0;
		int k = 0;
		
		while(i < half1.size() && j < half2.size()) {
			if(half1.get(i).getLastName().compareTo(half2.get(j).getLastName()) < 0) {
				merged.set(k, half1.get(i));
				i++;
				
			}
			else {
				merged.set(k, half2.get(i));
				j++;
			}
			k++;
		}
		return merged;
	}
	
	public static void elapsedTime() throws Exception {
		
		ArrayList<Entry> phonebook = readFile("phonebook_test.txt");
		
		long start = System.nanoTime();
		selectionSort(phonebook);
		long end = System.nanoTime();
		double duration = ((end-start)/1000000000.0);
		System.out.println("Selection Sort Time: " + duration);
		
		
		long s = System.nanoTime();
		//mergeSort(phonebook);
		long e = System.nanoTime();
		double d = ((e-s)/1000000000.0);
		System.out.println("Merge Sort Time: " + d);
		
	} 
	
	
	public static boolean test_file(ArrayList<Entry> original) {
		
		boolean sorted = true;
		for(int i = 0; i < original.size() - 1; i++) {
			if(original.get(i).getLastName().compareTo(original.get(i + 1).getLastName()) > 0) {
				sorted = false;
			}
		}
		return sorted;
	}
}
