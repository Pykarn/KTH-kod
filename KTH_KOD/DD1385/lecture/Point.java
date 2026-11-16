class Point{
    double x, y, fi, r;

    Point (double r, double fi){
	this.fi=fi;
	this.r=r;
	x=fi*Math.cos(fi);
	y=fi*Math.sin(fi);
    }

}
