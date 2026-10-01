%%

% Closed-loop characteristic equation: T*s^2 + s + K*kv = 0
Kvals = [0 0.01 0.02 0.03 0.04 0.05 0.1 0.2];

zeta = 0.707;               % damping ratio boundary to compare against Fig. 3.1c
theta = acos(zeta);
m=1
figure('Color', 'w'); hold on; grid on; axis equal;
plot([0 -m*cos(theta)], [0  m*sin(theta)], 'r--');
plot([0 -m*cos(theta)], [0 -m*sin(theta)], 'r--');
xlabel('Re'); ylabel('Im');
title('Closed-loop poles as K increases');
xlim([-0.3 0.3]); ylim([-0.4 0.4]);

for K = Kvals
    p = roots([5 1 2*K]);
    plot(real(p), imag(p), 'bx', 'MarkerSize', 10, 'LineWidth', 2);
    text(real(p(1)), imag(p(1))+0.03, sprintf('K=%.2g', K), 'FontSize', 8);
    fprintf('K = %-6.3g  poles at %s\n', K, mat2str(p, 3));
    pause;
end





%%