% % G3(s) = (10s^2 + 200s + 2000) / ((s+10)(s^2+10s+100))
% num = [10 200 2000];
% den = conv([1 2], [1 10 100]);

% % G4(s) = 200 / ((s^2+10s+100)(s+2))
% num = 200;
% den = conv([1 2], [1 10 100]);       % (s^2+10s+100)(s+2)

% % zeros
% num = [2 -1];
% den = conv([1 2], [1 1]);

t = linspace(0, 3, 1000);

[r, p] = residue(num, conv(den, [1 0]));   % partial fractions of Y(s) = G(s)/s

figure('Color', 'w'); hold on; grid on;
plot([t(1) t(end)], [0 0], 'k:');
xlabel('t [s]'); ylabel('y(t)');
title('step response');
xlim([t(1) t(end)]);
ylim([-10 10]);
% ylim([-3 3]);

total = zeros(size(t));
used  = false(size(p));

for k = 1:length(p)
    if used(k), continue; end

    if abs(imag(p(k))) < 1e-6
        mode = real(r(k)) * exp(p(k)*t);
        lbl  = sprintf('pole at %.1f', real(p(k)));
        used(k) = true;
    else
        j2 = find(abs(p - conj(p(k))) < 1e-6 & ~used, 1);
        mode = 2*real(r(k) * exp(p(k)*t));
        lbl  = sprintf('poles at %.1f %+.1fi', real(p(k)), imag(p(k)));
        used(k) = true; used(j2) = true;
    end

    total = total + mode;
    plot(t, mode, 'LineWidth', 1.5, 'DisplayName', lbl);
    fprintf('%s\n', lbl);
    legend('show', 'Location', 'southeast');
    pause;
end

plot(t, total, 'b', 'LineWidth', 2.5, 'DisplayName', 'step response');
legend('show', 'Location', 'southeast');

