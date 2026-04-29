N=1e2;
h=1/N;
x=(h:h:1-h)';
A=1/h*(2*diag(ones(length(x),1))-diag(ones(length(x)-1,1),-1)-diag(ones(length(x)-1,1),1));
L=h*randn(length(x),1);

xiexact=A\L;
plot([0;x;1],[0;xiexact;0]);
xlabel('x'),title('losning')

xi=randn(length(x),1);  %Initialisering av xi
delta=0.4*h;    %Uppfyller stabilitetsvillkoret
figure
while norm(xi-xiexact)>1e-2
    plot([0;x;1],[0;xi-xiexact;0]);
    xlabel('x'), title(['fel'])
    pause
    xi=xi-delta*(A*xi-L);
end
