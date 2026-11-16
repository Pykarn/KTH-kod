class Point{
    private double x, y, fi, r;

    private Point (double r, double fi){
	if(r<0 || fi<0||fi>2*Math.PI)
	    throw new IllegalArgumentException("Wrong arg values");
	this.fi=fi;
	this.r=r;
	x=fi*Math.cos(fi);
	y=fi*Math.sin(fi);
    }

      public static Point createPolar(double r, double fi){
	  if (r<0 ||fi<0 || fi > 2*Math.PI)
	      throw new IllegalArgumentException("Wrong arg values");
	  return new Point(r,fi);
    }

    public static Point cretaeCart(double x, double y){
        this.x = x; this.y=y;
        r = Math.sqrt(x*x + y*y);
        fi = Math.atan2(y,x);
	return new Point(r,fi);
    } 

    public double getX() {return x;}
    public double getY() {return y;}
    public double getR() {return r;}
    public double getFi() {return fi;}
}
