% analytisk lösning

epsilon = 1e-1;

u_exakt = @(r) log(r)./log(epsilon);

[x,y] = meshgrid(linspace(-1,1,300));
r = sqrt(x.^2 + y.^2);

u = u_exakt(r);
u(r < epsilon | r > 1) = NaN;  

surf(x,y,u)
