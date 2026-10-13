import java.awt.*;
class Brade{}
class Ruta{}

abstract class Schackpjas{
    private Color farg;
    Image bild;
    Brade brade;
    private Ruta ruta;
    
    Schackpjas(Color f, Image bild, Brade b, Ruta r){
	this.bild=bild;
	this.brade=brade;
	this.ruta=r;
    }
    
    abstract boolean dragOk(Ruta r1, Ruta r2);
}


class Bonde extends Schackpjas{
    Bonde(){
	super(Color.black,null,null,null);
	
    }
    
    boolean dragOk(Ruta r1, Ruta r2){
	System.out.println("bonden förflyttar sig");
	return true;
    }
}

class Dam extends Schackpjas{
    Dam(){
	super(Color.black,null,null,null);
    }
    
    boolean dragOk(Ruta r1, Ruta r2){return true;}
}

class Torn extends Schackpjas{
    Torn(){
	super(Color.black,null,null,null);
    }
    boolean dragOk(Ruta r1, Ruta r2){return true;}
}

class Springare extends Schackpjas{
    
    Springare(){
	super(Color.black,null,null,null);
    }
    
    boolean dragOk(Ruta r1, Ruta r2){
	System.out.println("springaren springer");
	return true;
    }
}


class Main{

    public static void main(String[] args){
	Schackpjas s= new Bonde();
	Schackpjas c= new Springare();
	s.dragOk(new Ruta(), new Ruta());
	c.dragOk(new Ruta(), new Ruta());
    }
}
