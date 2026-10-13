import java.awt.*;
abstract class A{


    abstract void abstrktMetod();
    
    void knkrtMethod(){
	System.out.println("A: konret metod");
    }
}

class B extends A{

    B(){

    }

     void abstrktMetod(){
	System.out.println("B: Konkretisering av abstktMetod i A");
    }

    void knkrtMethod(){
	System.out.println("metod i B");
    }
}

abstract class D extends A{

        void abstrktMetod(){
	    System.out.println("D: Konkrertisering av abstktMetod i A");
	} 
}

//klassen C ger felmeddelande varför?
class C extends A{
    C(){}
}

class Main{

    public static void main(String[] args){
	A a = new B();
	A c = new C();
	A d = new D(); //ger fel för att D är abstrakt
	a.knkrtMethod();
	c.knkrtMethod();
    }
}
