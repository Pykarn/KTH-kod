clear all
close all
%g(x) = x(pi-x)
N=20; % antal Fourierbasfunktioner
tN=100; % antal tidssteg
xN=100; % antal x-steg
T=4; %sluttid
dx=pi/xN;
dt=T/tN;
x=0:dx:pi;
t=0:dt:T;
u=zeros(length(x),length(t));
for k=0:N
    u=u+8/pi/(2*k+1)^3 * sin((2*k+1)*x') * exp(-(2*k+1)^2*t);
end
surf(x,t,u');
xlabel('x'),ylabel('t'),zlabel('u')



%fel




%Referenslösning tas fram med liten steglängd
M_ref = 800;
N_ref = 800;
dx_ref = pi/M_ref;
dt_ref = T/N_ref;
A_ref = diag(ones(M_ref-2,1),-1)+diag(-2*ones(M_ref-1,1))+diag(ones(M_ref-2,1),1);

x_ref = (dx_ref:dx_ref:pi-dx_ref)';
u_ref = zeros(M_ref-1, N_ref+1);

%Startdata g(x)
u_ref(:,1) = x_ref.*(pi-x_ref);

% Beräkna referenslösning med BE
for i = 1:N_ref
    u_ref(:,i+1) = (eye(M_ref-1)-dt_ref/dx_ref^2*A_ref)\u_ref(:,i);
end
% ==========================
%   Fel som funktion av dt
% ==========================

% Välj antal Fourierbaser
N = 20;

% Välj en tidpunkt för utvärdering
eval_time = 0.1;  

% Vektorer för olika tidssteg
dt_values = [0.01 0.02 0.05 0.1 0.2 0.5];   % exempel, kan ändras
Error_dt = zeros(length(dt_values),1);

% Referenslösning är redan beräknad: u_ref_interp vid eval_time
[~, t_ref_index] = min(abs((0:dt_ref:T) - eval_time));
u_ref_interp = interp1(x_ref, u_ref(:, t_ref_index), x);

for i = 1:length(dt_values)
    dt_test = dt_values(i);
    t_test = 0:dt_test:T;
    
    % Fourierapproximation vid valda tidssteg
    u_test = zeros(length(x), length(t_test));
    for k = 0:N
        u_test = u_test + 8/pi/(2*k+1)^3 * sin((2*k+1)*x') .* exp(-(2*k+1)^2 * t_test);
    end
    
    % Ta ut värdet vid tiden när vi vill mäta felet
    [~, t_index] = min(abs(t_test - eval_time));
    u_test_eval = u_test(:, t_index);
    
    % Beräkna maxnorm-felet mot referens
    Error_dt(i) = max(abs(u_test_eval - u_ref_interp'));
end

% Plot: fel som funktion av dt
figure
plot(dt_values, Error_dt, 'o-', 'LineWidth',1.5)
set(gca,'XScale','log')   % log-skala på x för tydligare trend
set(gca,'YScale','log')   % log-skala på y för tydligare trend
xlabel('Tidssteg dt')
ylabel('Max-fel vid t = 0.1')
title('Fel i Fourier-approximation som funktion av tidssteg')
grid on
