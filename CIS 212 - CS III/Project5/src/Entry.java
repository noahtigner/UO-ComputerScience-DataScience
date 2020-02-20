
public class Entry {
	private String PhoneNumber;
	private String LastName;
	private String FirstName;
	
	public Entry(String PhoneNumber, String LastName, String FirstName) {
		this.PhoneNumber = PhoneNumber;
		this.LastName = LastName;
		this.FirstName = FirstName;
	}
	
	public String getPhoneNumber() {
		return this.PhoneNumber;
	}
	
	public String getLastName() {
		return this.LastName;
	}
	
	public String getFirstName() {
		return this.FirstName;
	}
	
	public String getFormatted() {
		return this.PhoneNumber + " " + this.LastName + ", " + this.FirstName;
	}
	

}
