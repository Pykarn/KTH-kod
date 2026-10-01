s = tf('s');

% plant from Figure 3.1a
Gv = 2/(1+5*s);     % valve
Gt = 1/s;           % tank

%% 

Kp = 0.12; Ki = 0.01; Kd = 0.7;   % same Kp everywhere -- only add I and/or D
Tf = 1;   % derivative filter time constant -- a REAL controller always filters
          % the D term; an ideal Kd*s reacts to a step's instant jump with an
          % infinite spike, which isn't physical (and can't even be simulated)

D_term = Kd*s/(1+Tf*s);

F_P   = Kp;
F_PD  = Kp + D_term;
F_PI  = Kp + Ki/s;
F_PID = Kp + Ki/s + D_term;

names = {'P','PD','PI','PID'};
Fs    = {F_P, F_PD, F_PI, F_PID};
c     = {'#FF8800', '#800080', '#000080', '#808000'};

%% ---- Part 1: reference step (r = 1, v = 0) ----
% 
t = linspace(0, 80, 2000);

F_fig = figure('Color', 'w');
subplot(4,1,1); hold on; grid on;
xlabel('t [s]'); ylabel('u(t)'); 
title('Controller output (command to the valve)');
ylim([-0.2 1.1])
subplot(4,1,2); hold on; grid on;
xlabel('t [s]'); ylabel('e(t)'); title('Error');
ylim([-1 1])
subplot(4,1,3); hold on; grid on;
plot([t(1) t(end)], [1 1], 'k:', 'DisplayName', 'r(t)');
xlabel('t [s]'); ylabel('y(t)'); title('Response to a step');
ylim([0 2])
subplot(4,1,4); hold on; grid on;
xlabel('t [s]'); ylabel('x(t)'); title('Flow to tank');
ylim([-0.1 0.3])


% Fx_fig = figure(); hold on; grid on;
% xlabel('t [s]'); ylabel('x(t)'); title('Flow to tank'); ylim([-0.1 1])

for k = 1:4
    F = Fs{k};
    Gcl = 1 + (Gt*Gv*F); 
    Tyr = (Gt*Gv*F)/Gcl;    % r -> y
    Tur = F/Gcl;            % r -> u
    Ter = 1/Gcl;            % r -> e 
    Txr = Gv*Tur;           % r -> x
        
    y = step(Tyr, t);
    u = step(Tur, t);
    e = step(Ter, t);
    x = step(Txr, t);
    
    figure(F_fig)
    subplot(4,1,1); plot(t, u, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'southeast');
    subplot(4,1,2); plot(t, e, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'northeast');
    subplot(4,1,3); plot(t, y, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'northeast');
    subplot(4,1,4); plot(t, x, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'northeast');

    % figure(Fx_fig)
    % plot(t, u, 'Color', c{k}, 'LineWidth', 1.6, 'LineStyle', '--', ...
    %     'DisplayName', sprintf('%s -- u(t)',names{k}))
    % plot(t, x, 'Color', c{k}, 'LineWidth', 1.6, 'LineStyle', '-', ...
    %     'DisplayName', sprintf('%s -- x(t)',names{k}))
    % legend('show', 'Location', 'northeast');

    fprintf('%s -- reference step\n', names{k});
    pause;
end


%% ---- Part 2: disturbance step (r = 0, v = 1) ----

figure('Color', 'w');
subplot(4,1,1); hold on; grid on;
xlabel('t [s]'); ylabel('u(t)'); 
title('Controller output fighting the disturbance');
ylim([0 1])
subplot(4,1,2); hold on; grid on;
xlabel('t [s]'); ylabel('e(t)'); title('Error');
ylim([-2 6])
subplot(4,1,3); hold on; grid on;
plot([t(1) t(end)], [0 0], 'k:', 'DisplayName', 'r(t)');
xlabel('t [s]'); ylabel('y(t)'); title('Response to a disturbance step');
ylim([-6 2])
subplot(4,1,4); hold on; grid on;
xlabel('t [s]'); ylabel('x(t)'); title('Flow to tank');
ylim([0 1.8])



for k = 1:4
    F = Fs{k};
    Gcl = 1 + (Gt*Gv*F); 
    Tyv = -Gt/Gcl;          % v -> y
    Tuv = F*Gt/Gcl;         % v -> u
    Tev = Gt/Gcl;           % v -> e
    Txv = Gv*Tuv;           % r -> x

    y = step(Tyv, t);
    u = step(Tuv, t);
    e = step(Tev, t);
    x = step(Txv, t);


    subplot(4,1,1); plot(t, u, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'southeast');
    subplot(4,1,2); plot(t, e, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'northeast');
    subplot(4,1,3); plot(t, y, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'northeast');
    subplot(4,1,4); plot(t, x, 'Color', c{k}, 'LineWidth', 1.6, 'DisplayName', names{k});
    legend('show', 'Location', 'northeast');


    fprintf('%s -- disturbance step\n', names{k});
    pause;
end

%%
% 3.2
% b

Kp = 1;
% Kd = 1.7;
Kd = 3;
D_term = Kd*s;%/(1+Tf*s);
F_PD  = Kp + D_term;

Gcl = 1 + (Gt*Gv*F_PD); 
Tyr = (Gt*Gv*F_PD)/Gcl;    % r -> y

y = step(Tyr, t);
overshoot_pct = (max(y)-1)*100;

fprintf('overshoot (zero included) = %.2f %%\n', overshoot_pct);

figure('Color', 'w'); hold on; grid on;
plot(t, y, 'LineWidth', 1.8);
plot([t(1) t(end)], [1 1], 'k:');
plot([t(1) t(end)], [1.05 1.05], 'r--');
xlabel('t [s]'); ylabel('y(t)');
title(sprintf('PD step response, K_d = %.1f -- overshoot = %.1f%%', Kd, overshoot_pct));
legend('y(t)', 'final value', '5% overshoot limit', 'Location', 'southeast');
% xlim([0 25]);

%%
% Root locus
s = tf('s');

% Example 1: two real poles, no zero
G1 = 1/(s*(s+2));

% Example 2: same poles + one real zero pulling a branch in
G2 = (s+1)/(s*(s+2));

% Example 3: three real poles -- needs an actual breakaway point
G3 = 1/(s*(s+2)*(s+4));

Gs    = {G1, G2, G3};
names = {'Example 1: two poles, no zero', ...
         'Example 2: same poles + a real zero', ...
         'Example 3: three poles (breakaway)'};

for k = 1:3
    figure('Color', 'w');

    rlocus(Gs{k});
    grid on;
    title(names{k});
    set(findobj(gca, 'Type', 'Line'), 'LineWidth', 2);
    title(names{k});

    fprintf('%s -- press Enter to continue\n', names{k});
    pause;
end

%%
% Build up a root locus sketch one rule at a time, for each example:
% 1) poles (and zeros)   2) real-axis segments   3) asymptote centroid
% 4) asymptote angles    5) the actual locus, for comparison

poles_list = {[0 -2],        [0 -2],        [0 -2 -4]};
zeros_list = {[],            [-1],          []};
names      = {'Example 1: two poles, no zero', ...
              'Example 2: same poles + a real zero', ...
              'Example 3: three poles (breakaway)'};

xlims      = {[-4 2], [-4 2], [-8 3]};
ylims      = {[-4 4], [-1 1], [-6 6]};

%%
poles_list = {[0 -3+6i, -3-6i], [roots([1 3 5 0])']};
zeros_list = {[], [roots([0.075 1 1])']};
names      = {'System 1', ...
              'System 2'};

xlims      = {[-8 3], [-30 2]};
ylims      = {[-9 9], [-5 5]};

%%

for ex = 1:length(poles_list)
    p = poles_list{ex};
    z = zeros_list{ex};
    n = numel(p); m = numel(z);

    figure('Color', 'w'); hold on; grid on; axis equal;
    xlim(xlims{ex}); ylim(ylims{ex});
    xlabel('Re'); ylabel('Im'); title(names{ex});
    fprintf('\n=== %s ===\n', names{ex});

    % ---- Step 1: poles and zeros (plotted at their TRUE Re/Im location --
    plot(real(p), imag(p), 'kx', 'MarkerSize', 14, 'LineWidth', 2.5);
    text(xlims{ex}(1)+0.2, ylims{ex}(2)-0.4, 'x = poles', 'FontSize', 9);
    if ~isempty(z)
        plot(real(z), imag(z), 'ko', 'MarkerSize', 12, 'LineWidth', 2);
        text(xlims{ex}(1)+0.2, ylims{ex}(2)-0.9, 'o = zeros', 'FontSize', 9);
    end
    fprintf('Step 1: poles at %s', mat2str(p));
    if ~isempty(z), fprintf(',  zeros at %s', mat2str(z)); end
    fprintf('\n');
    pause;

    % ---- Step 2: real-axis segments that belong to the locus ----
    % Rule 3 only ever looks at REAL poles/zeros -- a complex-conjugate
    % pair always cancels its angle contribution, so it plays no part in
    % this count and must be filtered out here.
    p_real = real(p(abs(imag(p)) < 1e-9));
    z_real = real(z(abs(imag(z)) < 1e-9));
    allpts = sort([p_real z_real]);
    bounds = [xlims{ex}(1)-1, allpts, xlims{ex}(2)+1];
    for i = 1:length(bounds)-1
        test_pt = (bounds(i) + bounds(i+1)) / 2;
        count = sum(allpts > test_pt);
        if mod(count, 2) == 1
            plot([bounds(i) bounds(i+1)], [0 0], 'm-', 'LineWidth', 4, 'HandleVisibility', 'off');
        end
    end
    fprintf('Step 2: real-axis segments shaded (odd count of poles+zeros to the right)\n');
    pause;

    % ---- Step 3: asymptote centroid ----
    if n > m
        sigma_a = (sum(p) - sum(z)) / (n - m);
        plot(sigma_a, 0, 'b+', 'MarkerSize', 16, 'LineWidth', 2.5);
        text(sigma_a, 0.3, 'centroid', 'Color', 'b', 'FontSize', 9, 'HorizontalAlignment', 'center');
        fprintf('Step 3: asymptote centroid at sigma_a = %.3f\n', sigma_a);
    else
        fprintf('Step 3: n = m here, no asymptotes needed\n');
    end
    pause;

    % ---- Step 4: asymptote angles ----
    if n > m
        L = 6;
        for k = 0:(n-m-1)
            ang = (2*k+1)*180/(n-m);
            xe = sigma_a + L*cosd(ang);
            ye = L*sind(ang);
            plot([sigma_a xe], [0 ye], 'b--', 'LineWidth', 1.5, 'HandleVisibility', 'off');
            fprintf('   asymptote angle: %.1f deg\n', ang);
        end
    end
    pause;

    % ---- Step 5: breakaway / break-in points ----
    % P(s) + K*Q(s) = 0  =>  K = -P(s)/Q(s).  Breakaway/break-in points are
    % where dK/ds = 0, i.e. P'(s)Q(s) - P(s)Q'(s) = 0 (quotient rule,
    % multiplied through by Q(s)^2 so we only need polynomials).
    P = poly(p);           % P(s), from the poles
    Q = poly(z);           % Q(s), from the zeros (poly([]) = 1)
    Pp = polyder(P);
    Qp = polyder(Q);
    a = conv(Pp, Q);
    b = conv(P, Qp);
    L2 = max(length(a), length(b));
    a = [zeros(1, L2-length(a)) a];
    b = [zeros(1, L2-length(b)) b];
    dK = a - b;
 
    cands = roots(dK);
    cands = real(cands(abs(imag(cands)) < 1e-6));   % keep only real roots
 
    for c = cands'
        count = sum(allpts > c);
        if mod(count, 2) == 1        % must actually sit on the real-axis locus
            Kc = -polyval(P, c) / polyval(Q, c);
            plot(c, 0, 'gs', 'MarkerSize', 14, 'LineWidth', 2.5);
            text(c, -0.4, sprintf('K=%.2f', Kc), 'Color', [0 0.5 0], ...
                'HorizontalAlignment', 'center', 'FontSize', 8);
            fprintf('Step 5: breakaway/break-in at s = %.3f  (K = %.3f)\n', c, Kc);
        else
            fprintf('Step 5: dK/ds = 0 at s = %.3f, but that''s off the locus -- discarded\n', c);
        end
    end
    if isempty(cands)
        fprintf('Step 5: no real breakaway/break-in points here\n');
    end
    pause;
 
    % ---- Step 6: the actual locus, in a fresh figure for a clean comparison ----
    G = zpk(z, p, 1);
    figure('Color', 'w');
    rlocus(G);
    grid on;
    set(findobj(gca, 'Type', 'Line'), 'LineWidth', 2);
    title([names{ex} ' -- built-in check']);
    fprintf('Step 6: full locus drawn (new figure) -- compare to the sketch\n');
    pause;
end


%%















