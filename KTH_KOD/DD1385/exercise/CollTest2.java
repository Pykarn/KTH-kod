import java.text.*;
import java.util.*;

class CollTest2 {
    public static void main(String[] u) {
	
	ArrayList<String> alist = new ArrayList<String>();
	alist.add("åra"); alist.add("öga"); 
	alist.add("bob"); alist.add("ägg"); alist.add("ava");

	System.out.println("\nOsorterat");
	for (String s: alist)
	    System.out.println(s);

	Collections.sort(alist);
	System.out.println("\nSorterat med standard compareTo");
	for (String s: alist)
	    System.out.println(s);

	// Default Collator will compare swedish texts correctly
        // With appropriate parameter a Collator for another
        // language will be obtained.
	Collator coll = Collator.getInstance();

	Collections.sort(alist, coll);
	System.out.println("\nSorterat med Collator för svenska");
	for (String s: alist)
	    System.out.println(s);

	
    }
}	
