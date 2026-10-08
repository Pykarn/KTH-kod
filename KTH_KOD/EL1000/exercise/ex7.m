%%

%%%%%%%%%%--------3.21--------%%%%%%%%%%
%%
% a

s = tf('s');

P = (s^2+s+1)*(s+0.2);
Q = 0.2;

G_ = Q/P;

figure
rl_p = rlocusplot(G_); 
rl_p.Responses.MarkerSize = 10;  
rl_p.Responses.LineWidth = 3;  

%%
%--------3.4a--------%
figure
for Kp = 0:0.5:7
    F = Kp;
    Gc = feedback(F*G_, 1);
    sp = stepplot(Gc,50);
    sp.Responses.LineWidth = 3;
    sp.Title.String = sprintf('$K_P$ = %0.2f',Kp);
    sp.Title.Interpreter = 'latex';
    sp.Title.FontSize = 15;
    grid; ylim([0 2]);
    pause(0.001)
end

%%
% b

P = s*((s^2+s+1)*(s+0.2) + 0.2);
Q = 0.2;

G = Q/P;

figure
rl_p = rlocusplot(G); 
rl_p.Responses.MarkerSize = 10;  
rl_p.Responses.LineWidth = 3;  

%%
%--------3.4b--------%
figure
KP = 1; 
for KI = 0:0.05:2
    F = KP + KI / s;
    Gc = feedback(F*G_, 1);
    sp = stepplot(Gc,50);
    sp.Responses.LineWidth = 3;
    sp.Title.String = sprintf('$K_I$ = %0.2f',KI);
    sp.Title.Interpreter = 'latex';
    sp.Title.FontSize = 15;
    grid; ylim([-1 3])
    set(findall(gcf,'type','line'),'linewidth',3);
    pause(0.01)
end

%%
% c

P = (0.1*s+1)*(s*(s^2+s+1)*(s+0.2) + 0.2*(s+1));
Q = 0.2*s^2;

G = Q/P;

figure
rl_p = rlocusplot(G); 
rl_p.Responses.MarkerSize = 10;  
rl_p.Responses.LineWidth = 3;  
rl_p.YLimits = {[-6 6]};
rl_p.XLimits = {[-12 2]};

%%
zero(G)
%%
%--------3.4c--------%
figure
KP = 1; KI = 1; T = 0.1; 
% for KD = 0:0.1:3
for KD = 1:1:70
    FP = KP;
    FI = KI / s;
    FD = KD * s / ( s*T + 1 );
    F = FP + FI + FD;
    Gc = feedback(F*G_, 1);
    sp = stepplot(Gc,50);
    sp.Responses.LineWidth = 3;
    sp.Title.String = sprintf('$K_D$ = %0.2f',KD);
    sp.Title.Interpreter = 'latex';
    sp.Title.FontSize = 15;
    grid; ylim([-1 3])
    set(findall(gcf,'type','line'),'linewidth',3);
    % pause(0.01)
    pause(0.0001)
end


%%
%%%%%%%%%%--------3.22--------%%%%%%%%%%

%%
% a

figure('Position', [0 50 1100 650]);
for Kp = 1:0.1:10
    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
    F = Kp;
    np = nyquistplot(F*G);
    np.Title.Interpreter = ("latex");
    np.Title.String = sprintf("Nyquist $K_P=%0.1f$", Kp);
    np.Responses.MarkerSize = 10;
    np.Responses.LineWidth = 3;
    axis([-3 11 -7 7])
    pause(0.1)
end
%%

fig = figure('Position', [0 50 1100 650]);

for Kp = 5.5:0.1:6.5
    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
    F = Kp;
    Gcl = feedback( F*G, 1 );
    
    t = tiledlayout(fig, 2, 2);

    ax1 = nexttile;
    np = nyquistplot(ax1, F*G);
    np.Title.Interpreter = ("latex");
    np.Title.String = sprintf("Nyquist $K_P=%0.2f$", Kp);
    np.Responses.MarkerSize = 10;
    np.Responses.LineWidth = 3;
    axis(ax1, [-3 11 -7 7])

    ax2 = nexttile;
    sp = stepplot(ax2, Gcl, 30);
    sp.Title.Interpreter = ("latex");
    sp.Title.String = sprintf("Step $K_P=%0.2f$", Kp);
    sp.Responses.LineWidth = 3;
    axis(ax2, [0 30 0 2])

    ax3 = nexttile([1 2]);
    pzp = pzplot(ax3, Gcl); xlim([-1.5 0.5]);
    pzp.Title.Interpreter = ("latex");
    pzp.Title.String = sprintf("Pole-Zero map $K_P=%0.2f$", Kp);
    pzp.Responses.MarkerSize = 10;  
    pzp.Responses.LineWidth = 3;  

    pause(0.01)
end

%%
% b
figure('Position', [0 50 1100 650]);
KP = 1; 
for KI = 0:0.05:2
    F = KP + KI / s;
    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );

    np = nyquistplot(F*G);
    np.Title.Interpreter = ("latex");
    np.Title.String = sprintf("Nyquist $K_I=%0.1f$", KI);
    np.Responses.MarkerSize = 10;
    np.Responses.LineWidth = 3;
    axis([-3 1 -2 2])
    pause(0.1)
end
%%

fig = figure('Position', [0 50 1100 650]);

KP = 1; 
for KI = 1:0.05:1.5
    F = KP + KI / s;
    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
    Gcl = feedback( F*G, 1 );
    
    t = tiledlayout(fig, 2, 2);

    ax1 = nexttile;
    np = nyquistplot(ax1, F*G);
    np.Title.Interpreter = ("latex");
    np.Title.String = sprintf("Nyquist $K_I=%0.1f$", KI);
    np.Responses.MarkerSize = 10;
    np.Responses.LineWidth = 3;
    axis(ax1, [-3 1 -2 2])

    ax2 = nexttile;
    sp = stepplot(ax2, Gcl, 30);
    sp.Title.Interpreter = ("latex");
    sp.Title.String = sprintf("Step $K_I=%0.1f$", KI);
    sp.Responses.LineWidth = 3;
    axis(ax2, [0 30 0 2])

    ax3 = nexttile([1 2]);
    pzp = pzplot(ax3, Gcl); 
    pzp.Title.Interpreter = ("latex");
    pzp.Title.String = sprintf("Pole-Zero map $K_I=%0.1f$", KI);
    pzp.Responses.MarkerSize = 10;  
    pzp.Responses.LineWidth = 3;  
    axis(ax3, [-2 0.5 -1 1]);

    pause(0.01)
end

%%
% c

figure('Position', [0 50 1100 650]);
KP = 1; KI = 1; T = 0.1; 
for KD = 0:0.1:3
    FP = KP;
    FI = KI / s;
    FD = KD * s / ( s*T + 1 );
    F = FP + FI + FD;

    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );

    np = nyquistplot(F*G);
    np.Title.Interpreter = ("latex");
    np.Title.String = sprintf("Nyquist $K_D=%0.1f$", KD);
    np.Responses.MarkerSize = 10;
    np.Responses.LineWidth = 3;
    axis([-2 1 -2 2])
    pause(0.1)
end
%%

fig = figure('Position', [0 50 1100 650]);

KP = 1; KI = 1; T = 0.1; 
for KD = 65.5:0.2:67
    FP = KP;
    FI = KI / s;
    FD = KD * s / ( s*T + 1 );
    F = FP + FI + FD;

    G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
    Gcl = feedback( F*G, 1 );
    
    t = tiledlayout(fig, 2, 2);

    ax1 = nexttile;
    np = nyquistplot(ax1, F*G);
    np.Title.Interpreter = ("latex");
    np.Title.String = sprintf("Nyquist $K_D=%0.1f$", KD);
    np.Responses.MarkerSize = 10;
    np.Responses.LineWidth = 3;
    % axis(ax1, [-3 11 -7 7])

    ax2 = nexttile;
    sp = stepplot(ax2, Gcl, 30);
    sp.Title.Interpreter = ("latex");
    sp.Title.String = sprintf("Step $K_D=%0.1f$", KD);
    sp.Responses.LineWidth = 3;
    axis([0 20 -0.2 2])

    ax3 = nexttile([1 2]);
    pzp = pzplot(ax3, Gcl); %xlim([-1.5 1]);
    pzp.Title.Interpreter = ("latex");
    pzp.Title.String = sprintf("Pole-Zero map $K_D=%0.1f$", KD);
    pzp.Responses.MarkerSize = 10;  
    pzp.Responses.LineWidth = 3;  

    pause(0.01)
end



%%
fig = figure;
KD = 67;
FP = KP;
FI = KI / s;
FD = KD * s / ( s*T + 1 );
F = FP + FI + FD;

G = 0.2 / ( ( s^2 + s + 1 ) * ( s + 0.2 ) );
Gcl = feedback( F*G, 1 );

t = tiledlayout(fig, 2, 2);

ax1 = nexttile;
np = nyquistplot(ax1, F*G);
np.Title.Interpreter = ("latex");
np.Title.String = sprintf("Nyquist $K_D=%0.1f$", KD);
np.Responses.MarkerSize = 10;
np.Responses.LineWidth = 3;
% axis(ax1, [-3 11 -7 7])

ax2 = nexttile;
sp = stepplot(ax2, Gcl, 30);
sp.Title.Interpreter = ("latex");
sp.Title.String = sprintf("Step $K_D=%0.1f$", KD);
sp.Responses.LineWidth = 3;
% axis([-3 11 -7 7])

ax3 = nexttile([1 2]);
pzp = pzplot(ax3, Gcl); %xlim([-1.5 1]);
pzp.Title.Interpreter = ("latex");
pzp.Title.String = sprintf("Pole-Zero map $K_D=%0.1f$", KD);
pzp.Responses.MarkerSize = 10;  
pzp.Responses.LineWidth = 3;  


%%
%%%%%%%%%%--------3.23--------%%%%%%%%%%


%%
% a
s = tf('s');
G = 0.4/((s^2+s+1)*(s+0.2));
F = 1;

[GM,PM,Wcg,Wcp] = margin(F*G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("GM = %.2f, $\\omega_{gc} = %.2f$. " + ...
                    "PM = %.2f, $\\omega_{pc} = %.2f$", GM, Wcg, PM, Wcp);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, F*G, opts);
bd.showCharacteristic('AllStabilityMargins')
bd.Responses.LineWidth = 3;

ax2 = nexttile([2 1]);
Gcl = feedback(F*G, 1);
sp = stepplot(ax2, Gcl, 30);
sp.Title.Interpreter = ("latex");
sp.Title.String = sprintf("Step $K_P=%0.1f$", F);
sp.Responses.LineWidth = 3;

%%
% b
s = tf('s');
G = 0.4/((s^2+s+1)*(s+0.2));
F = 2.5;

[GM,PM,Wcg,Wcp] = margin(F*G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("GM = %.2f, $\\omega_{gc} = %.2f$. " + ...
                    "PM = %.2f, $\\omega_{pc} = %.2f$", GM, Wcg, PM, Wcp);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, F*G, opts);
bd.showCharacteristic('AllStabilityMargins')
bd.Responses.LineWidth = 3;

ax2 = nexttile([2 1]);
Gcl = feedback(F*G, 1);
sp = stepplot(ax2, Gcl, 30);
sp.Title.Interpreter = ("latex");
sp.Title.String = sprintf("Step $K_P=%0.1f$", F);
sp.Responses.LineWidth = 3;

%%
% c
s = tf('s');
G = 0.4/((s^2+s+1)*(s+0.2));
F = 3.1;

[GM,PM,Wcg,Wcp] = margin(F*G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("GM = %.2f, $\\omega_{gc} = %.2f$. " + ...
                    "PM = %.2f, $\\omega_{pc} = %.2f$", GM, Wcg, PM, Wcp);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, F*G, opts);
bd.showCharacteristic('AllStabilityMargins')
bd.Responses.LineWidth = 3;

ax2 = nexttile([2 1]);
Gcl = feedback(F*G, 1);
sp = stepplot(ax2, Gcl, 30);
sp.Title.Interpreter = ("latex");
sp.Title.String = sprintf("Step $K_P=%0.1f$", F);
sp.Responses.LineWidth = 3;


%%
%%%%%%%%%%--------4.5--------%%%%%%%%%%

%%
% a

s = tf( 's' );

%%
%GA

GA = 1 / ( s^2 + 2*s + 1 );
G = GA;
fb = bandwidth(G);
[gpeak, wpeak] = getPeakGain(G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("$\\omega_{B} = %.2f$. " + ...
                    "$\\omega_{r} = %.2f$. " + ...
                    "$M_{p} = %.2f$", fb, wpeak, gpeak);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

figure
bd = bodeplot(GA, opts);
bd.showCharacteristic('AllStabilityMargins')
bd.Responses.LineWidth = 3;


%%
fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, G, opts);
bd.showCharacteristic('AllStabilityMargins')
bd.Responses.LineWidth = 3;


ax2 = nexttile([2 1]);
Gcl = feedback(G, 1);
sp = stepplot(ax2, Gcl);
sp.Responses.LineWidth = 3;
sp.Characteristics.PeakResponse.Visible = 'on';
sp.Characteristics.RiseTime.Visible = 'on';

tr = stepinfo(G).RiseTime;
Mp = stepinfo(G).Overshoot;

sp.Title.FontWeight = "normal";
sp.Title.Interpreter = "latex";
sp.Title.String = sprintf("$T_r=%.2f. M_p=%.2f$", tr, Mp);

%%
%GB

GB = 1 / ( s^2 + 0.4*s + 1 );
G = GB;
fb = bandwidth(G);
[gpeak, wpeak] = getPeakGain(G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("$\\omega_{B} = %.2f$. " + ...
                    "$\\omega_{r} = %.2f$. " + ...
                    "$M_{p} = %.2f$", fb, wpeak, gpeak);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

figure
bd = bodeplot(GA, opts);
bd.showCharacteristic('AllStabilityMargins')

%%
fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, G, opts);
bd.showCharacteristic('AllStabilityMargins')

ax2 = nexttile([2 1]);
Gcl = feedback(G, 1);
sp = stepplot(ax2, Gcl);
sp.Responses.LineWidth = 3;
sp.Characteristics.PeakResponse.Visible = 'on';
sp.Characteristics.RiseTime.Visible = 'on';

tr = stepinfo(G).RiseTime;
Mp = stepinfo(G).Overshoot;

sp.Title.FontWeight = "normal";
sp.Title.Interpreter = "latex";
sp.Title.String = sprintf("$T_r=%.2f. M_p=%.2f$", tr, Mp);


%%
%GC

GC = 1 / ( s^2 + 5*s + 1 );
G = GC;
fb = bandwidth(G);
[gpeak, wpeak] = getPeakGain(G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("$\\omega_{B} = %.2f$. " + ...
                    "$\\omega_{r} = %.2f$. " + ...
                    "$M_{p} = %.2f$", fb, wpeak, gpeak);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

figure
bd = bodeplot(GA, opts);
bd.showCharacteristic('AllStabilityMargins')

%%
fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, G, opts);
bd.showCharacteristic('AllStabilityMargins')

ax2 = nexttile([2 1]);
Gcl = feedback(G, 1);
sp = stepplot(ax2, Gcl);
sp.Responses.LineWidth = 3;
sp.Characteristics.PeakResponse.Visible = 'on';
sp.Characteristics.RiseTime.Visible = 'on';

tr = stepinfo(G).RiseTime;
Mp = stepinfo(G).Overshoot;

sp.Title.FontWeight = "normal";
sp.Title.Interpreter = "latex";
sp.Title.String = sprintf("$T_r=%.2f. M_p=%.2f$", tr, Mp);

%%
%GD

GD = 1 / ( s^2 + s + 1 );
G = GD;
fb = bandwidth(G);
[gpeak, wpeak] = getPeakGain(G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("$\\omega_{B} = %.2f$. " + ...
                    "$\\omega_{r} = %.2f$. " + ...
                    "$M_{p} = %.2f$", fb, wpeak, gpeak);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

figure
bd = bodeplot(GA, opts);
bd.showCharacteristic('AllStabilityMargins')

%%
fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, G, opts);
bd.showCharacteristic('AllStabilityMargins')

ax2 = nexttile([2 1]);
Gcl = feedback(G, 1);
sp = stepplot(ax2, Gcl);
sp.Responses.LineWidth = 3;
sp.Characteristics.PeakResponse.Visible = 'on';
sp.Characteristics.RiseTime.Visible = 'on';

tr = stepinfo(G).RiseTime;
Mp = stepinfo(G).Overshoot;

sp.Title.FontWeight = "normal";
sp.Title.Interpreter = "latex";
sp.Title.String = sprintf("$T_r=%.2f. M_p=%.2f$", tr, Mp);

%%
%GE

GE = 4 / ( s^2 + 2*s + 4 );
G = GE;
fb = bandwidth(G);
[gpeak, wpeak] = getPeakGain(G);

opts = bodeoptions('cstprefs');
opts.MagUnits = "abs";
opts.Title.Interpreter = "latex";
opts.Title.String = sprintf("$\\omega_{B} = %.2f$. " + ...
                    "$\\omega_{r} = %.2f$. " + ...
                    "$M_{p} = %.2f$", fb, wpeak, gpeak);
opts.Title.FontSize = 12;
opts.Title.FontWeight = "bold";

figure
bd = bodeplot(GA, opts);
bd.showCharacteristic('AllStabilityMargins')

%%
fig = figure('Position', [0 50 1100 650]);
t = tiledlayout(fig, 2, 2);

ax1 = nexttile([2 1]);
bd = bodeplot(ax1, G, opts);
bd.showCharacteristic('AllStabilityMargins')

ax2 = nexttile([2 1]);
Gcl = feedback(G, 1);
sp = stepplot(ax2, Gcl);
sp.Responses.LineWidth = 3;
sp.Characteristics.PeakResponse.Visible = 'on';
sp.Characteristics.RiseTime.Visible = 'on';

tr = stepinfo(G).RiseTime;
Mp = stepinfo(G).Overshoot;

sp.Title.FontWeight = "normal";
sp.Title.Interpreter = "latex";
sp.Title.String = sprintf("$T_r=%.2f. M_p=%.2f$", tr, Mp);

%%
