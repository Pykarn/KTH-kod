abstract class Fordon{
        abstract void kör();
}

class Båt extends Fordon{
     void kör(){
	System.out.println("Metoden kör i Båt anropats");
    }	
}

class Bil extends Fordon{
    
    private void tuta(){
	System.out.println("Metoden tuta i Bil anropas");
    }

    void tutTest(){
	tuta();
    }

    void kör(){
	System.out.println("Metoden kör i Bil anropats");
    }	
}

class Lastbil extends Bil{

    private void tuta(){
	System.out.println("Metoden tuta i LastBil anropas");
    }


    
    void kör(){
	System.out.println("Metoden kör i Lastbil anropats");
    }
}

class Main{

     static void anropaKör(Fordon fp){
        fp.kör();
    }

    /*    static void anropaTuta(Bil fp){
        fp.tuta();
	}*/

     static void main(String[] args){
	 Fordon båt = new Båt();
	Fordon bil = new Bil();
	Bil lastB = new Lastbil();
	anropaKör(båt);
	anropaKör(bil);
	anropaKör(lastB);
	//Betrakta nedan skillnad mellan Statisk bindning och dynamisk bindning
	lastB.tutTest();
	lastB.kör();
	
    }
}
