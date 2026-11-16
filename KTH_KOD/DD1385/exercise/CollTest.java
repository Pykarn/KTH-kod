import java.text.*;

class CollTest1 {
    
    public static void main(String[] u) {
	String s1 = "å", s2 = "ä", s3 = "ö";

	// Default Collator will compare swedish texts correctly
        // With appropriate parameter a Collator for another
        // language will be obtained.
	Collator coll = Collator.getInstance();
	
	System.out.println();
	System.out.println("           compareTo() coll.compare()\n");
	System.out.print(" ava  bob       ");
	System.out.print("ava".compareTo("bob") + "       ");
	System.out.println(coll.compare("ava","bob"));
	System.out.print(" " + s1 + " " + s2 + "             ");
	System.out.print(s1.compareTo(s2) + "       ");
	System.out.println(coll.compare(s1,s2));
	System.out.print(" " + s2 + " " + s3 + "           ");
	System.out.print(s2.compareTo(s3) + "       ");
	System.out.println(coll.compare(s2,s3));
	System.out.print(" " + s1 + " " + s3 + "           ");
	System.out.print(s1.compareTo(s3) + "       ");
	System.out.println(coll.compare(s1,s3));
	System.out.println();

	// ASCII-codes for some letters are printed
	for (char c : "abcxyzåäö".toCharArray())
	    System.out.println(" " + c + " " + (int)c);
	for (char c : "ABCXYZÅÄÖ".toCharArray())
	    System.out.println(" " + c + " " + (int)c);
    }
}	
