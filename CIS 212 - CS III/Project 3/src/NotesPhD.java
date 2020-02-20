
public class NotesPhD extends NotesGrad{
	
	int salary;
	int financialAid;
	
	@Override
	public int payTuition() {
		return -10000;
	}
	
	public void PhD(int age, int salary) {
		financialAid = age*1000;
		this.salary = salary;
	}
	
	public static void main(String[] args) {
		NotesStudents mary = new NotesGrad();
	}
	
	

}
