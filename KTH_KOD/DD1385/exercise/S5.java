class S{
    static S s = new S();
    private S(){}
	

}

class Main{
    public static void main(String[] args){
	
	S s1=S.s;
	S s2=S.s;
	System.out.println(s1==s2);
    }
    //MEN DET ÄR INGEN HÅLLBAR LÖSNING, TÄNK OM DET ÄR FLERA UTVECKLARE SOM SKRIVER SINA EGNA KLASSER SOM SKA ANVÄNDA SIG AV klassen S. VI BEHÖVER FLYTTA ANSVARET ATT KONTROLLERA OM DET FINNS ETT OBJEKT TILL SJÄLVA KLASSEN S. 

}
