%% CONTROL SYSTEMS — Solutions in MATLAB
% Exercises: 3.21, 3.22, 3.23, 4.5
% Plant used in 3.21–3.23:  G(s) = 0.2 / [ (s^2 + 4 s + 1) (s + 0.2) ]
% Unless otherwise stated, use unity negative feedback.

clear; close all; clc;
s = tf('s');

G = 0.2 / ((s^2 + s + 1) * (s + 0.2));

%% 3.21  (Root locus with P / PI / PID)
% 3.21(a) Proportional control: C(s) = Kp
%   – Root locus of the closed-loop characteristic equation vs Kp > 0.
%   – As Kp increases, the complex-conjugate poles move toward the jw-axis,
%     damping decreases (faster but more oscillatory step response).
%   – There is a finite stabilizing range for Kp > 0; too large Kp destabilizes.

figure('Name','3.21(a) Root locus — P control');
rlocus(G); grid on;
title('3.21(a) Root locus of L(s)=K_p G(s)');
% Choose a few Kp to illustrate closed-loop responses:
Kp_list = [0.5, 1, 2.5];
figure('Name','3.21(a) Step responses for selected Kp');
hold on; grid on;
for Kp = Kp_list
    Tcl = feedback(Kp*G, 1);
    step(Tcl, 20);
end
legend(arrayfun(@(k)sprintf('K_p=%.2f',k), Kp_list,'uni',0),'Location','best');
title('3.21(a) Step response — effect of increasing K_p');

% 3.21(b) PI control with fixed Kp=1:  C(s) = Kp + Ki/s  (vary Ki>0)
%   – The integrator removes steady-state error to a step (type increases).
%   – Small Ki ⇒ slow integral action (long settling time, small overshoot).
%   – Large Ki ⇒ aggressive integral action (reduced error but larger overshoot,
%     reduced stability margins). There exists a stabilizing range of Ki>0.

P=s*(s^3+1.2*s^2+1.2*s+0.4);
Q=0.2;
rlocus(Q/P)

% 3.21(c) PID control with Kp=1, Ki=1, derivative with first-order roll-off T=0.1:
%   C(s) = Kp + Ki/s + Kd * [ s / (1 + T s) ]
%   – Increasing Kd generally increases damping and reduces overshoot.
%   – Too large Kd excites high-frequency dynamics (noise amplification)
%     and may eventually destabilize.
P=(0.1*s+1)*(s*(s^2+s+1)*(s+2)+0.2*(s+1));
Q=2*s^2;
rlocus(Q/P)

%% 3.22  (Nyquist with P / PI / PID)
% 3.22(a) Proportional control: explore Nyquist of Kp*G(s).
%   – Stability from Nyquist: with Kp>0, the (-1,0) encirclement count changes
%     as Kp grows; compare to the root-locus results in 3.21(a).
G = 0.2 / ((s^2 + s + 1) * (s + 0.2));
Kp_vals = [1,3,6,7];  % examine how encirclements change
figure('Name','3.22(a) Nyquist — P control');
for Kp = Kp_vals
    nyquist(Kp*G); hold on;
end
grid on; axis equal; title('3.22(a) Nyquist of K_p G(s) for several K_p');
legend(arrayfun(@(k)sprintf('K_p=%.1f',k), Kp_vals,'uni',0),'Location','best');

margin(G)


Ki_list=[1,1.5];
% 3.22(b) PI control with Kp=1, vary Ki>0; compare with 3.21(b).
figure('Name','3.22(b) Nyquist — PI (Kp=1, vary Ki)');
for Ki = Ki_list
    nyquist((1+ Ki/s)*G); hold on;
end
title('3.22(b) Nyquist of (K_p + K_i/s) G(s)');


%FUNCTION TO DETERMINE Ki

% Critical Ki for (1 + Ki/s)*G(s) crossing -1 in Nyquist
% Method: solve Im{ Ki(jw) } = 0 where
% Ki(jw) = j*w * ( -1/G(jw) - 1 ). Then Ki* = Re{ Ki(jw*) }.
% This is equivalent to (1 + Ki/(jw)) * G(jw) = -1.

Gj      = @(w) squeeze(freqresp(G, w));  % G(jw) --> frequency response in terms of w (we change s by jw)
Ki_of_w = @(w) 1j*w .* ( -1./Gj(w) - 1 ); % complex Ki(jw) --> (1+Ki/jw)*G=-1  --> Ki=jw(-1/G - 1)
ImKi    = @(w) imag(Ki_of_w(w));   % Im{Ki(jw)} --> we obtain the imaginary part of Ki

% 1) scan frequencies and detect ALL sign changes of Im{Ki(jw)}
W  = logspace(-3, 2, 4000);
Y  = arrayfun(ImKi, W);
chg = find(sign(Y(1:end-1)).*sign(Y(2:end)) < 0);   % indices of sign changes

Ki_cands = [];
w_cands  = [];

% 2) refine each sign-change interval with fzero
for k = chg(:).'
    wL = W(k); wR = W(k+1);
    % guard against pathological tiny intervals
    if ~isfinite(Y(k)) || ~isfinite(Y(k+1)), continue; end
    wstar = fzero(ImKi, [wL, wR]);
    Kistar = real(Ki_of_w(wstar));
    if isfinite(Kistar)
        Ki_cands(end+1,1) = Kistar; %#ok<AGROW>
        w_cands(end+1,1)  = wstar;  %#ok<AGROW>
    end
end

% 3) keep real positive Ki and sort ascending
mask = (Ki_cands > 0);
Ki_cands = Ki_cands(mask);
w_cands  = w_cands(mask);
[Ki_cands, order] = sort(Ki_cands, 'ascend');
w_cands = w_cands(order);

% 4) pick the first (smallest) as the critical one
if isempty(Ki_cands)
    error('No positive real Ki candidates found in the scanned band.');
end
Ki_crit = Ki_cands(1);
w_crit  = w_cands(1);

fprintf('Candidates Ki (ascending):\n');
disp(table(Ki_cands, w_cands));
fprintf('=> Critical Ki = %.6f at ω = %.6f rad/s\n', Ki_crit, w_crit);

% 5) verify: Nyquist passes through -1 and a pair of poles at ±jω
Lcrit = (1 + Ki_crit/s)*G;
figure; nyquist(Lcrit); grid on; title('Nyquist at Ki = Ki_{crit}');
Tcrit = feedback(Lcrit, 1);
disp('Closed-loop poles at Ki_crit:');
disp(pole(Tcrit));
labels = arrayfun(@(k) sprintf('K_i=%.2f',k), Ki_list, 'UniformOutput', false);
legend(labels,'Location','best');





% 3.22(c) PID with Kp=1, Ki=1, T=0.1; vary Kd>0.


Kd_list=[30,40,66,100];
figure('Name','3.22(c) Nyquist — PID (vary Kd)');
for Kd = Kd_list
    nyquist((1 + 1/s + Kd*s/(1+0.1*s))*G); hold on;
end
grid on; title('3.22(c) Nyquist of PID·G(s) for several K_d');
legend(arrayfun(@(k)sprintf('K_d=%.2f',k), Kd_list,'uni',0),'Location','best');


% Function to determine Kd
% L(s) = (Kp + Ki/s + Kd * s/(1+T s)) * G(s). Find Kd s.t. Nyquist crosses -1.
% Method: Kd(jw) = ((1+j*w*T)/(j*w)) * ( -1/G(jw) - Kp - Ki/(j*w) ).
% Pick all roots where Im{Kd(jw)}=0, keep real positive Re{Kd}, choose smallest.

% --- Plant and fixed PID parts
G  = 0.2/((s^2 + s + 1)*(s + 0.2));
Kp = 1; Ki = 1; T = 0.1;

% --- Frequency-domain helpers
Gj     = @(w) squeeze(freqresp(G, w));                          % G(jw)
Kd_of  = @(w) (1 + 1j*w*T)./(1j*w) .* ( -1./Gj(w) - Kp - Ki./(1j*w) );
ImKd   = @(w) imag( Kd_of(w) );

% --- Scan frequencies and detect ALL sign changes of Im{Kd(jw)}
W   = logspace(-3, 2, 4000);
Y   = arrayfun(ImKd, W);
chg = find(sign(Y(1:end-1)).*sign(Y(2:end)) < 0);              % intervals with sign change

% --- Refine each interval with fzero, collect candidates
Kd_cands = [];  w_cands = [];
for k = chg(:).'
    wL = W(k); wR = W(k+1);
    if ~isfinite(Y(k)) || ~isfinite(Y(k+1)), continue; end     % safety
    wstar  = fzero(ImKd, [wL, wR]);                            % solve Im{Kd}=0
    Kdstar = real( Kd_of(wstar) );                             % Kd should be real at w*
    if isfinite(Kdstar), Kd_cands(end+1,1) = Kdstar; w_cands(end+1,1) = wstar; end %#ok<AGROW>
end

% --- Keep real positive Kd and choose the smallest (first crossing as Kd increases)
mask = (Kd_cands > 0);
Kd_cands = Kd_cands(mask);  w_cands = w_cands(mask);
[Kd_cands, ord] = sort(Kd_cands, 'ascend');  w_cands = w_cands(ord);

if isempty(Kd_cands)
    error('No positive real Kd candidates found in the scanned band.');
end

Kd_crit = Kd_cands(1);
w_crit  = w_cands(1);
fprintf('Critical Kd ≈ %.6f at ω* ≈ %.6f rad/s\n', Kd_crit, w_crit);

% --- Quick visual verification (optional)
C     = @(Kd) (Kp + Ki/s + Kd*(s/(1+T*s)));
Lcrit = C(Kd_crit)*G;
figure; nyquist(Lcrit); grid on; title('Nyquist at K_d = K_{d,crit} (passes through -1)');
Tcl   = feedback(Lcrit, 1);
disp('Closed-loop poles at Kd_crit:');
disp(pole(Tcl));


%% 3.23  (Bode plot, margins, and step responses for different Kp)
% 3.23(a) With Kp = 1:
%   – Make a Bode plot of the open loop L(s)=Kp*G(s).
%   – Determine gain crossover ω_c, phase margin φ_m, and gain margin A_m.
%   – Simulate the closed-loop step response and comment on speed/overshoot.
G = 0.4 / ((s^2 + s + 1) * (s + 0.2));
Kp = 1; L = Kp*G;
figure('Name','3.23(a) Bode — Kp=1'); margin(L); grid on;
[GM, PM, Wcg, Wcp] = margin(L);
fprintf('3.23(a) Kp=1:  Gain margin = %.3g (at ω=%.3g rad/s), Phase margin = %.2f deg (at ω=%.3g rad/s)\n',...
    GM, Wcg, PM, Wcp);
Tcl = feedback(L, 1);
figure('Name','3.23(a) Step — Kp=1'); step(Tcl, 30); grid on;
title('3.23(a) Closed-loop step response (K_p=1)');

% 3.23(b) Increase Kp and study margins/step changes.
% The solution explores e.g., Kp=2.5 and Kp=3.1:
for Kp = [2.5]
    L = Kp*G;
    figure('Name',sprintf('3.23(b) Bode — Kp=%.2f',Kp)); margin(L); grid on;
    [GM, PM, Wcg, Wcp] = margin(L);
    fprintf('3.23(b) Kp=%.2f:  Gain margin = %.3g (ω=%.3g), Phase margin = %.2f deg (ω=%.3g)\n',...
        Kp, GM, Wcg, PM, Wcp);
    Tcl = feedback(L, 1);
    figure('Name',sprintf('3.23(b) Step — Kp=%.2f',Kp));
    step(Tcl, 30); grid on;
    title(sprintf('3.23(b) Closed-loop step response (K_p=%.2f)',Kp));
end
% Qualitative notes (as in the solution):
%   – Increasing Kp raises the open-loop magnitude, so ω_c moves to the right.
%   – Phase margin decreases; the step gets faster but more oscillatory.
%   – If Kp is pushed too far, the closed loop becomes unstable.


%% 4.5  (Amplitude Bode curves: DC gain, bandwidth, resonance)
% Problem statement: consider transfer functions G_A(s), G_B(s), G_C(s), G_D(s), G_E(s)
% as defined in Problem 2.26. The solution asks to:
%   – Study the amplitude (|G(jω)|) curves,
%   – Find the static gain (DC gain) and the bandwidth,
%   – In cases with a resonance peak, find its height and the resonance frequency.
%
% >>> IMPORTANT <<<
% Enter the five transfer functions exactly as in your Problem 2.26.
% Below are placeholders; replace them with the *actual* definitions from 2.26.

%% 4.5 — Bode + métricas con margin()
s = tf('s');

% --- Define tus sistemas (ejemplos/placeholder) ---
GA = 1/(s^2+2*s+1);                 
GB = 1/(s^2+0.4*s+1);             
GC = 1/(s^2+5*s+1);  
GD = 1/(s^2 + s +1);   
GE = 4/(s^2+2*s+4); 

Gs    = {GA,   GB,   GC,   GD,   GE};
names = {'G_A','G_B','G_C','G_D','G_E'};

% --- Results table ---
fprintf('\n%-5s | %-8s %-10s %-10s | %-8s %-10s | %-8s %-10s\n', ...
    'Sys','GM[dB]','PM[deg]','Wcg[rad/s]','Wcp[rad/s]','DCgain','BW[-3dB]','Mpeak','w_peak');
fprintf('%s\n', repmat('-',1,86));

for i = 1:numel(Gs)
    G = Gs{i};

    % 1) Bode with Margin
    figure('Name',['Bode w/ margins - ' names{i}]);
    margin(G); grid on; title(['Bode & margins — ' names{i}]);

    % 2) Margins: GM/PM and freq
    [GMlin, PMdeg, Wcg, Wcp] = margin(G);
    GMdB = 20*log10(GMlin); 
    
    % 3) DC Gain |G(j0)|
    DC = dcgain(G); 

    % 4) Initial BW, asumming there is not BW
    BW = NaN;
    try
        BW = bandwidth(G);   % Easy calculation
    catch
        % fallback: In case bandwidth doesnt work
        w = logspace(-3, 3, 20000);
        [mag,~] = bode(G,w); mag = squeeze(mag);
        ref = max(abs(DC), eps);         % eps is a very low number
        target = ref/sqrt(2);
        k = find(mag <= target, 1, 'first');
        if ~isempty(k), BW = w(k); end
    end

    % 5) Resonance peak
    w = logspace(-3, 3, 20000);
    [mag,~] = bode(G,w); mag = squeeze(mag);
    [Mpeak, kpk] = max(mag);
    wpk = w(kpk);

    % 6) Print data
    fprintf('%-5s | %8.3g %10.3g %10.3g | %8.3g %10.3g | %8.3g %10.3g\n', ...
        names{i}, GMdB, PMdeg, Wcg, Wcp, DC, BW, Mpeak, wpk);
end

% Qualitative relationships to observe (part (b)):
%   – Larger bandwidth generally implies faster rise time and smaller settling time.
%   – A pronounced resonance peak (M_p > 1) correlates with low damping and larger overshoot.
%   – Increasing damping reduces the peak and overshoot, but also narrows bandwidth
%     (slower response). These trade-offs are visible directly in the amplitude curves.
