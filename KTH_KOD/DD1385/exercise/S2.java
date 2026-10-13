class S{
    

}

class Main{
    public static void main(String[] args){
	
	S s1=new S();
	S s2;
	
	if(s1!=null)
	    s2=new S();
	else
	    s2=s1;

	System.out.println(s1==s2);
    }
    //MEN DET ÄR INGEN HÅLLBAR LÖSNING, TÄNK OM DET ÄR FLERA UTVECKLARE SOM SKRIVER SINA EGNA KLASSER SOM SKA ANVÄNDA SIG AV klassen S. VI BEHÖVER FLYTTA ANSVARET ATT KONTROLLERA OM DET FINNS ETT OBJEKT TILL SJÄLVA KLASSEN S. 

}
