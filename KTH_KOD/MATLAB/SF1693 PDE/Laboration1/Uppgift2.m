% Uppgift 2 - Konvektion och diffusion

clear;

M = 1000;
N = 6;
P = ( 2*N +1 )^2;
k = 2*pi;

xvek = rand(M,1);
yvek = rand(M,1);

v1_vals = yvek;
v2_vals = 1 - xvek;

r = sqrt((xvek - 0.5).^2 + (yvek - 0.5).^2);
f_vals = double(r < 0.1);

% Bygger lista/matris med alla par n1, n2:
idx = 0;
n1n2list = zeros(P,2);
for n1 = -N:N
    for n2 = -N:N
        idx = idx+1;
        n1n2list(idx,:) = [n1,n2];
    end
end

% Bygger matris med varje fourierbasterm:
A = zeros(M,P);
for i = 1:P % Loopar genom hela n1n2listan
    n1 = n1n2list(i,1);
    n2 = n1n2list(i,2);
    A(:,i) = exp(1i*k*(n1*xvek + n2*yvek));
end

% Matlab gör MKM:
v1_Fkoeff = A \ v1_vals;
v2_Fkoeff = A \ v2_vals;
f_Fkoeff  = A \  f_vals;

n1vek = n1n2list(:,1);
n2vek = n1n2list(:,2);

% Kontinuerliga fourierfunktioner för lösning av PDE senare
v1_fourier = @(x,y) real( sum( v1_Fkoeff .* exp(1i*k*(n1vek*x + n2vek*y)) ) );
v2_fourier = @(x,y) real( sum( v2_Fkoeff .* exp(1i*k*(n1vek*x + n2vek*y)) ) );
f_fourier  = @(x,y) real( sum( f_Fkoeff  .* exp(1i*k*(n1vek*x + n2vek*y)) ) );

K = 10;            
deltas = 0.0005;        
rand_dist = 1e-5;   % tolerans för att träffa en kant
maxsteg = 10000;
count = 0;

u = zeros(K,K);

for k1 = 1:K
    for k2 = 1:K

        % Startpunkt
        x0 = k1/K;
        y0 = k2/K;

        x_kar = x0;
        y_kar = y0;
        u_kar = 0;

        for steg = 1:maxsteg
            
            % Euler framåt (bakåt) för karakteristikan
            x_kar = x_kar - deltas * v1_fourier(x_kar,y_kar);
            y_kar = y_kar - deltas * v2_fourier(x_kar,y_kar);

            % Kolla om vi träffat vänster eller nedre kant
            if (x_kar <= rand_dist) || (y_kar <= rand_dist)
                count = count+1;
                break;
            end

            % Euler framåt för u
            u_kar = u_kar + deltas * f_fourier(x_kar,y_kar);
        end

        u(k1,k2) = u_kar;

    end
end


% ---- Plot resultat ----
figure; contour(u',30);
title('Nivåkurvor av lösningen u');
axis equal; colorbar;

figure; mesh(u');
title('3D-plott av u, test1');
xlabel('x-index'); ylabel('y-index'); zlabel('u');
