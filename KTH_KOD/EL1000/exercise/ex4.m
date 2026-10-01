%%
% Install Control System Toolbox

s = tf( 's' );

%%
% 2.6

% Define system an get Step Response
% Right click characteristics & properties
% Fix overshoot percentage in the plot (w properties - options)


GA = 1 / ( s^2 + 2*s + 1 );
step(GA); grid
pole(GA)

%%

GA = 1 / ( s^2 + 2*s + 1 );
GB = 1 / ( s^2 + 0.4*s + 1 );
GC = 1 / ( s^2 + 5*s + 1 );
GD = 1 / ( s^2 + s + 1 );
GE = 4 / ( s^2 + 2*s + 4 );

systems = {GA, GB, GC, GD, GE};
names = {'GA', 'GB', 'GC', 'GD', 'GE'};

titles = {'$G(s) = \frac{1}{s^2+2s+1}$', ...
          '$G(s) = \frac{1}{s^2+0.4s+1}$', ...
          '$G(s) = \frac{1}{s^2+5s+1}$', ...
          '$G(s) = \frac{1}{s^2+s+1}$', ...
          '$G(s) = \frac{1}{s^2+2s+4}$'};

%%

for i=1:length(systems)
    G = systems{i};

    figure()
    sp = stepplot(G, 30);
    sp.Title.Interpreter = "latex";
    sp.Title.String = titles{i};
    sp.Title.FontSize = 20;
    sp.Responses.LineWidth = 3;
    sp.Characteristics.RiseTime.Visible = 'on';
    sp.Characteristics.SettlingTime.Visible = 'on';
    sp.Characteristics.SettlingTime.Threshold = 0.05;
    sp.Characteristics.PeakResponse.Visible = 'on';
    
    info = stepinfo(G);
    Tr = info.RiseTime;
    M = info.Overshoot;
    Ts = info.SettlingTime;

    annotation('textbox', [0.5, 0.2, 0.35, 0.06], ...
               'String',{sprintf('$T_r = %.2f, T_s = %.2f, M = %.0f \\%%$', Tr, Ts, M)}, ...
               'Interpreter','latex', ...
               'HorizontalAlignment', 'center', ...
               'EdgeColor', 'none', ...
               'FontSize', 12);

    G
    pole(G)
    exportgraphics(gcf, sprintf('%s.png', names{i}), 'Resolution', 300);
end
%%
%2.7


figure
for alpha=-10:10
    G = ( alpha*s + 1 ) / ( s^2 + 2*s + 1 ); 
    step(G,10); grid; ylim([-4 4]); 
    set(findall(gcf,'type','line'),'linewidth',3);
    title(sprintf('Step response $\\alpha$ = %d, $G(s) = \\frac{\\alpha s + 1}{s^2+2s+1}$', alpha), ...
    'interpreter', 'latex');
    pause(1);
end

%%

figure('Position', [0 30 900 600])
for alpha=-10:10
    G = ( alpha*s + 1 ) / ( s^2 + 2*s + 1 ); 
    sgtitle(sprintf('$\\alpha$ = %d, $G(s) = \\frac{\\alpha s + 1}{s^2+2s+1}$', alpha), ...
                     'interpreter','latex'); 
    subplot(1,2,1); step(G,10); 
    set(findall(gcf,'type','line'),'linewidth',3);
    grid; ylim([-4 4]);
    subplot(1,2,2); pzp = pzplot(G); xlim([-1.5 1.5]);
    pzp.Responses.MarkerSize = 10;  
    pzp.Responses.LineWidth = 3;  
    pause(1);
end

%%

figure()

% alpha = -10;
% alpha = 0;
alpha = 10;

title(sprintf('Step response $\\alpha$ = %d, $G(s) = \\frac{\\alpha s + 1}{s^2+2s+1}$', alpha), ...
               'interpreter','latex'); 
G = ( alpha*s + 1 ) / ( s^2 + 2*s + 1 ); 
step(G,10); grid; ylim([-4 4]); 
set(findall(gcf,'type','line'),'linewidth',3, 'color', '#800080');
hold on;
den = s^2 + 2*s + 1;
% step(num, 10); set(findall(gcf,'type','line'),'linewidth',3, 'color', '#FF8800');
step(den, 10); set(findall(gcf,'type','line'),'linewidth',3, 'color', '#000080');
grid; ylim([-4 4]);
l = legend('$G(s)$', 'poles');
l.Interpreter = latex;

%%
% 3.4

G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
F = 1;
Gc = feedback( F * G, 1 );
step( Gc, 30 ); grid

KP = 1; KI = 1;
F = KP + KI / s;
Gc = feedback( F * G, 1 );
step( Gc, 50 ); grid

KP = 1; KI = 1; T = 0.1; KD = 1;
FP = KP;
FI = KI / s;
FD = KD * s / ( s*T + 1 );
F = FP + FI + FD;
Gc = feedback(F*G,1);
step(Gc,50); grid

%%


G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) )
F = 1;
Gc_ = (F*G)/(1+F*G)
Gc = feedback( F * G, 1 )
Gc__ = minreal(Gc_)

%%
figure
for Kp = 1:0.1:10
    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
    F = Kp;
    Gc = feedback( F * G, 1 );
    step( Gc, 50 ); grid; ylim([0 2])
    set(findall(gcf,'type','line'),'linewidth',3);
    pause(0.1)
end

%%

figure
for Kp = 6:0.1:10
    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
    F = Kp;
    Gc = feedback( F * G, 1 );
    % step( Gc, 50 ); grid; ylim([0 2])
    % set(findall(gcf,'type','line'),'linewidth',3);

    sgtitle(sprintf('$K_P$ = %0.2f',Kp),'interpreter','latex'); 
    subplot(1,2,1); step(Gc,50); set(findall(gcf,'type','line'),'linewidth',3);
    grid; ylim([0 2]);
    subplot(1,2,2); pzp = pzplot(Gc); xlim([-1.5 1]);
    pzp.Responses.MarkerSize = 10;  
    pzp.Responses.LineWidth = 3;  


    pause(0.1)
end

%%
figure
KP = 1; 
for KI = 0:0.05:2
    F = KP + KI / s;
    Gc = feedback( F * G, 1 );
    step( Gc, 50 ); grid; ylim([0 2])
    set(findall(gcf,'type','line'),'linewidth',3);
    pause(1)
end

%%
figure
KP = 1; KI = 1; T = 0.1; 
for KD = 0:0.1:3
    FP = KP;
    FI = KI / s;
    FD = KD * s / ( s*T + 1 );
    F = FP + FI + FD;
    Gc = feedback(F*G,1);
    step(Gc,50); grid; ylim([0 2])
    set(findall(gcf,'type','line'),'linewidth',3);
    pause(0.1)
end

%%
figure
% Kp = 1; 
Kp = 2;
% Kp = 5; 
% Kp = 10; 
G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
F = Kp;
Gc = feedback( F * G, 1 );
step( Gc, 50 ); grid; %ylim([0 2])
set(findall(gcf,'type','line'),'linewidth',3);

%%
figure
KP = 1; 
% KI = 0.5; 
% KI = 1; 
KI = 2; 
F = KP + KI / s;
Gc = feedback( F * G, 1 );
step( Gc, 50 ); grid; %ylim([0 2])
set(findall(gcf,'type','line'),'linewidth',3);

%%
figure
KP = 1; KI = 1; T = 0.1; 
% KD = 0.5;
% KD = 2;
KD = 3;
FP = KP;
FI = KI / s;
FD = KD * s / ( s*T + 1 );
F = FP + FI + FD;
Gc = feedback(F*G,1);
step(Gc,50); grid; ylim([0 2])
set(findall(gcf,'type','line'),'linewidth',3);



