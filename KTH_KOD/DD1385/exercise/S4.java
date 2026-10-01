class S{
    private static S s = new S();

    public static S getS(){
	return s;
    }
}

class Main{
    public static void main(String[] args){

	S s1 = S.getS();
	S s2 = S.getS(); 

	//Men om utvecklaren skriver s2=new S(); ?
	//Eller råkar skriv S.s = new S();
	System.out.println(s1==s2);
    }
}
