class Calc2{
    public int sub(int a, int b){
	return a-b;
    }
    
    public int mul(int a, int b){
	return a*b;
    }
    
    public static void main(String[] args){
	Calc2 c =new Calc2();
	System.out.println(c.sub(2,3));
	System.out.println(c.mul(6,5));	
    }

}
