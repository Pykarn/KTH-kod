
epsilon = 0.1;
N = 100;
h = (1 - epsilon)/N;

x = linspace(epsilon,1,N+1)';

D  = zeros(N-1,1);   
D1 = zeros(N-2,1);    

for i = 1:N-1
    D(i) = 1/(2*h^2)*(x(i+2)^2-x(i)^2);
end 

for i = 1:N-2
    D1(i) = -(x(i+2)^2 - x(i+1)^2)/(2*h^2);
end

A = diag(D) + diag(D1,1) + diag(D1,-1);


L = zeros(N-1,1);

L(1) = (x(2)^2 - x(1)^2)/(2*h^2);  % u0=1

u_inre = A \ L;


u = [1; u_inre; 0];


figure
plot(x,u,'LineWidth',3)
xlabel('r')
ylabel('u(r)')
title('FEM')



u_exact = @(r) log(r)/log(epsilon);
hold on
plot(x,u_exact(x),'--','LineWidth',3)
legend('FEM','Analytisk')
