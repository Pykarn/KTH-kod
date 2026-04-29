

%−∇⋅(c∇u)+au=f

c = 1;
a = 0;
f = @circlef;

% @circlef approximerar dirac delta funktion:
%   f är 1/(area av triangel), i triangeln som innehåller (0,0)
%   f är 0, annars


numberOfPDE = 1;
model = createpde(numberOfPDE);
%model är en "container" som beskriver PDE:n som vi jobbar med
%den har data för geometri, villkor, koefficienter

g = @circleg;
%lägger till geometrin g (som i detta fall är en cirkel) till model
geometryFromEdges(model,g);


figure;
pdegplot(model,'EdgeLabels','on');
axis equal
title('Geometry With Edge Labels Displayed');

%lägger till randvillkor till model
applyBoundaryCondition(model,'dirichlet','Edge',(1:4),'u',0);

%använder randvillkor och geometri från model och använder koefficienter
%från a och c, samt funktionen f enligt detta format:
%  −∇⋅(c∇u)+au=f
[u,p,e,t] = adaptmesh(g,model,c,a,f,'tripick','circlepick','maxt',2000,'par',1e-3);
% tripick: circlepick beskriver hur vi ritar våra trianglar
% maxt: 2000 beskriver hur många trianglar vi vill ha
% par: 1e-3 beskriver att om felet för noden (jag tror att det är noden, kan ha fel) 
% av en triangel är större än 1e-3 då ökar man antalet trianglar i det
% området så att det blir en "finare" lösning. Om felet är mindre än 1e-3
% då låter man det vara kvar. Därför blir det fler trianglar i mitten.
% Testa olika värden på par och maxt. Tex om du ökar par måste du också öka
% maxt osv




%plottar mesh
figure;
pdemesh(p,e,t);
axis equal
title("Mesh")

x = p(1,:)'; %alla x koordinater för alla meshpoints (noder)
y = p(2,:)'; %alla y koordinater för alla meshpoints (noder)

r = sqrt(x.^2 + y.^2);
r(r==0) = 1e-10;

uu = -log(r)/2/pi; %analytisk lösning för alla meshpoints (noder)

%plottar felet
figure;
pdeplot(p,e,t,'XYData',abs(u-uu),'ZData',abs(u-uu),'Mesh','off');
title("Plot the error values")

%plottar lösning u
figure;
pdeplot(p,e,t,'XYData',u,'ZData',u,'Mesh','off');
title("FEM solution on the finest mesh")