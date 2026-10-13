interface EttInterface{

    public int m1(int i);
    public int m2(int j);
    
       
}


class Minklass{
    EttInterface eao;
    
    Minklass(EttInterface eao){
	this.eao=eao;
	
    }

    void enMetod(){
	System.out.println(this.eao.m1(12));
	System.out.println(this.eao.m2(12));
    }

    public static void main(String[] args){
	EttInterface eao=new Mockobjekt();
	Minklass mk=new Minklass(eao);
	mk.enMetod();
    }


}

class Mockobjekt implements EttInterface{

    public int m1(int i){
	return 10+i;
    }


    public int m2(int i){
	return 10-i;
    }
    
}
