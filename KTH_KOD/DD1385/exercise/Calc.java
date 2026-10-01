class Calc{
    public int add(int a, int b){
	return a+b;
    }
    
    public double div(int a, int b)throws ArithmeticException {
	return ((double)a)/b;
    }
    
    public static void main(String[] args){
	Calc c =new Calc();
	System.out.println(c.add(2,3));
	System.out.println(c.div(6,5));
	
    }

}
