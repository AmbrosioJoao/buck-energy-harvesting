clc; clear; close all;

%% 1. DEFINIÇÃO DOS PARÂMETROS (Circuito Ideal)
Vin = 30;         % Tensão de Entrada (Antigo E)
D = 0.60;         % Duty Cycle (60%)
L = 1e-3;         % Indutor 1mH
R = 94;           % Carga
fsw = 50e3;       % Frequência de chaveamento
Ts = 1/fsw;       % Período de chaveamento

%% 2. CÁLCULOS TEÓRICOS
Ton = D * Ts;
Toff = (1-D) * Ts;

% Tensão de Saída Ideal
Vo = Vin * D;

% Corrente Média na carga
I_avg = Vo / R;

% Cálculo do Ripple de Corrente (Delta IL)
Delta_IL = ((Vin - Vo) * Ton) / L;

% Correntes Mínima e Máxima
Il_min = I_avg - (Delta_IL / 2); % Il(0)
Il_max = I_avg + (Delta_IL / 2); % Il_max

%% 3. PREPARAÇÃO DOS VETORES
% --- Vetores para Tensão no Indutor (vL) ---
time_vL = [0, Ton, Ton, Ts];
% Nível Alto: Vin - Vo | Nível Baixo: -Vo
data_vL = [Vin-Vo, Vin-Vo, -Vo, -Vo];

% --- Vetores para Corrente no Indutor (iL) ---
time_iL = [0, Ton, Ts];
data_iL = [Il_min, Il_max, Il_min];

%% 4. GERAÇÃO DO GRÁFICO
figure('Color', 'w', 'Position', [100, 100, 700, 600]);

% --- SUBPLOT 1: Tensão no Indutor (vL) ---
subplot(2,1,1);
plot(time_vL*1e6, data_vL, 'b-', 'LineWidth', 2.5); hold on;
yline(0, 'k-'); % Linha do zero

% Decoração
title('Tensão no Indutor (v_L)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Tensão (V)');
xlim([0 Ts*1e6]);
ylim([-Vo*1.4, (Vin-Vo)*1.4]); % Margem visual um pouco maior

% Labels Personalizados (Vin em vez de E)
text(Ton*1e6/2, (Vin-Vo)+2, 'V_{in} - V_o', 'HorizontalAlignment', 'center', 'FontSize', 11, 'FontWeight', 'bold');
text(Ton*1e6 + Toff*1e6/2, -Vo-2, '-V_o', 'HorizontalAlignment', 'center', 'FontSize', 11, 'FontWeight', 'bold');

% Eixos Personalizados
set(gca, 'XTick', [0, Ton*1e6, Ts*1e6]);
set(gca, 'XTickLabel', {'0', 't_{on}', 'T_s'});
set(gca, 'YTick', [-Vo, 0, Vin-Vo]);
set(gca, 'YTickLabel', {'-V_o', '0', 'V_{in} - V_o'});
grid on;

% --- SUBPLOT 2: Corrente no Indutor (iL) ---
subplot(2,1,2);
plot(time_iL*1e6, data_iL, 'r-', 'LineWidth', 2.5); hold on;

% Decoração
title('Corrente no Indutor (i_L)', 'FontSize', 12, 'FontWeight', 'bold');
xlabel('Tempo (\mus)', 'FontSize', 11);
ylabel('Corrente (A)');
xlim([0 Ts*1e6]);
ylim([0, Il_max*1.3]); 

% Textos dos Pontos
text(0, Il_min, sprintf(' i_{L}(0) = %.3f A', Il_min), 'VerticalAlignment', 'top', 'FontSize', 10);
text(Ton*1e6, Il_max, sprintf(' I_{L_{max}} = %.3f A', Il_max), 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'center', 'FontSize', 10);

set(gca, 'XTick', [0, Ton*1e6, Ts*1e6]);
set(gca, 'XTickLabel', {'0', 't_{on}', 'T_s'});
grid on;

% --- CAIXA DE TEXTO COM OS VALORES (O Quadrado solicitado) ---
% Posição [x y largura altura] relativa à janela
dim = [0.15 0.55 0.2 0.1]; 
str = {['V_{in} = ' num2str(Vin) ' V'], ['V_o = ' num2str(Vo) ' V'], ['Duty = ' num2str(D*100) '%']};
annotation('textbox', dim, 'String', str, 'FitBoxToText', 'on', ...
           'BackgroundColor', 'white', 'EdgeColor', 'black', 'LineWidth', 1, ...
           'FontSize', 11, 'FontWeight', 'bold');