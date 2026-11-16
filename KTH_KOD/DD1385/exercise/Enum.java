enum Snowwhite{
    
    TheOnly;
    
    boolean married=false;
    String occupation;
    int age;

    void incrAge(){
	age++;
    }
    
    public String toString(){
	return "Snowwhite "+age;
    }
    
}

enum Dwarf{
    Blick(131), Flick(112),Glick(142), Snick(115),Plick(108),Whick(120),Quee(99);

    int age;

    Dwarf(int age){
	this.age=age;

    }

    public String toString(){
	return super.toString()+" "+age+" ";
    }
    
}


class Main2{
    public static void main(String[] args){
	System.out.println("All dwarfs");
	Dwarf db=Dwarf.Blick;
	for(Dwarf d: Dwarf.values())
	    System.out.println(d+"  ");

	System.out.println("  ");
	
    }
}


class Main1{
    public static void main(String[] args){
	enum Day {Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday};
	
	Day idag = Day.Thursday;
	
	System.out.println(idag);
	for (Day d: Day.values()){
		System.out.println(d);
	}
	
    }
}


