class Point1{
    private double x, y, fi, r;

    Point1 (double r, double fi){
	setPolar(r,fi);
    }

      public void setPolar(double r, double fi){
	  if (r<0 ||fi<0 || fi > 2*Math.PI)
	      throw new IllegalArgumentException("Wrong arg values");
	  this.r = r; this.fi = fi;
	  x = r*Math.cos(fi);
	  y = r*Math.sin(fi);
    }

    public void setCart(double x, double y){
        this.x = x; this.y=y;
        r = Math.sqrt(x*x + y*y);
        fi = Math.atan2(y,x); 
    } 

    public double getX() {return x;}
    public double getY() {return y;}
    public double getR() {return r;}
    public double getFi() {return fi;}
}
