import java.util.*;
class Person{
    int age;
    String name;
    
    Person(int age,String name){
	this.age=age;
	this.name=name;
    }
    
    public String toString(){
	return name+" "+age;
    }

    public static void main(String[] args){
	ArrayList<Person> al = new ArrayList<Person>();
	al.add(new Person(24,"Kalle"));
	al.add(new Person(20,"Eva"));
	al.add(new Person(10,"Pelle"));
	al.add(new Person(34,"Karin"));

	System.out.println("Sorterad efter namnsordning:");
	Collections.sort(al ,new CollName());
	for( Person p:al)
	    System.out.println(p);
	
	System.out.println("Sorterad efter alder:");
	Collections.sort(al, new CollAge());
	for( Person p:al)
	    System.out.println(p);
    }

}

class CollAge implements Comparator<Person>{
    
    public  int compare(Person el1, Person el2){
	if (el1.age > el2.age)
	    return 1;
	else if (el1.age < el2.age)
	    return -1;
	else
	    return 0;
    }
}

class CollName implements Comparator<Person>{
    //Comparable
    public int compare(Person el1, Person el2){
	return (el1.name).compareTo(el2.name);
    }
}

