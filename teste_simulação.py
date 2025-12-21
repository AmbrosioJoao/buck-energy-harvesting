import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURAÇÃO (AGORA 24 HORAS) ---
horas = np.linspace(0, 24, 1000)
target_vo = 18.0
bateria_nivel = 40.0              # Começa o dia com 40%
min_bateria = 25.0                # LIMITE MÍNIMO (Proteção UVLO)
consumo_sensor = 0.4              # Consumo do sensor

# --- 2. GERANDO O SOL (Igual ao anterior) ---
vin_solar = np.zeros_like(horas)
mask_dia = (horas >= 6) & (horas <= 18)
vin_solar[mask_dia] = 35 * np.sin((horas[mask_dia] - 6) * np.pi / 12)

# Adicionando Nuvens
np.random.seed(42)
nuvens = np.random.normal(0, 5, 1000)
mask_nuvens = (np.random.rand(1000) > 0.8) & mask_dia
vin_solar[mask_nuvens] -= abs(nuvens[mask_nuvens])
vin_solar[vin_solar < 0] = 0 

# --- 3. SIMULANDO COM PROTEÇÃO DE BATERIA ---
vo_sensor = []
nivel_bateria_plot = []

for v in vin_solar:
    # 1. Calcular o saldo de energia do momento
    if v > 20: 
        # Tem sol: Buck alimenta sensor + Carrega bateria
        producao = 1.8 # Taxa de carga (Aumentei um pouco para garantir a noite)
        saldo = producao - consumo_sensor
    else:
        # Sem sol: Bateria tem que bancar tudo
        saldo = -consumo_sensor

    # 2. Lógica de Proteção (UVLO)
    # Se a bateria estiver no mínimo E o saldo for negativo (gastando)...
    if bateria_nivel <= min_bateria and saldo < 0:
        # CORTA A ENERGIA!
        output = 0            # Sensor desliga
        bateria_nivel = min_bateria # Bateria trava em 25% (não desce mais)
    else:
        # FUNCIONAMENTO NORMAL
        bateria_nivel += saldo
        output = target_vo    # Sensor recebe 18V
    
    # Travas de segurança (0 a 100%)
    if bateria_nivel > 100: bateria_nivel = 100
    # O limite inferior já foi tratado acima, mas por segurança:
    if bateria_nivel < min_bateria: bateria_nivel = min_bateria
    
    vo_sensor.append(output)
    nivel_bateria_plot.append(bateria_nivel)

vo_sensor = np.array(vo_sensor)

# --- 4. PLOTAGEM ---
fig, ax1 = plt.subplots(figsize=(12, 7), facecolor='white')

# Eixo Esquerdo (Tensões)
ax1.set_xlabel('Hora do Dia (0h - 24h)', fontsize=12)
ax1.set_ylabel('Tensão (V)', color='tab:blue', fontsize=12)
ln1 = ax1.plot(horas, vin_solar, color='orange', alpha=0.6, label='Painel Solar (Entrada)', linewidth=1)
ax1.fill_between(horas, vin_solar, color='orange', alpha=0.1)

ln2 = ax1.plot(horas, vo_sensor, color='green', linewidth=3, label='Sensor (Saída)')
ax1.set_ylim(-2, 40)
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Eixo Direito (Bateria)
ax2 = ax1.twinx() 
ax2.set_ylabel('Carga da Bateria (%)', color='purple', fontsize=12)
# Linha de limite mínimo (Vermelha pontilhada)
ax2.axhline(min_bateria, color='red', linestyle=':', alpha=0.5, label='Mínimo Seguro (25%)')
ln3 = ax2.plot(horas, nivel_bateria_plot, color='purple', linestyle='--', alpha=0.8, label='Nível da Bateria')
ax2.set_ylim(0, 110)
ax2.tick_params(axis='y', labelcolor='purple')

# Legendas juntas
lines = ln1 + ln2 + ln3
labs = [l.get_label() for l in lines]
ax1.legend(lines, labs, loc='upper left')

plt.title('Sistema com Proteção de Bateria (UVLO 25%)', fontsize=14, fontweight='bold')
plt.grid(True, linestyle=':', alpha=0.6)

# Anotação Visual
plt.annotate('Proteção contra\nDescarga Profunda', xy=(23, 25), xytext=(20, 10),
             arrowprops=dict(facecolor='red', arrowstyle='->'), color='red')

plt.tight_layout()
plt.show()