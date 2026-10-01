class S{
    static S s = new S();
}

class Main{
    public static void main(String[] args){
	
	S s1 = S.s;
	S s2 = S.s; //new S();

	//Men om utvecklaren skriver s2=new S(); ?
	//Eller råkar skriv S.s = new S();
	System.out.println(s1==s2);
    }
}
