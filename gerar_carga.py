# Script para gerar perfil de consumo IoT para LTspice
# O objetivo é simular pulsos de transmissão LoRa/LR-FHSS

filename = "perfil_carga.txt"

# --- PARÂMETROS ---
# Correntes
i_sleep = "5u"     # 5 microamperes (modo Sleep profundo)
i_tx = "40m"       # 40 miliamperes (Pico de transmissão)

# Tempos (ACELERADOS para demonstração visual rápida)
# Na vida real seria 900s, aqui usamos 100ms para a simulação rodar em segundos
t_sleep = 0.1      
t_tx = 0.05        # 50ms de transmissão

ciclos = 4         # Quantos "disparos" queremos ver no gráfico

with open(filename, "w") as f:
    tempo = 0
    f.write(f"0 {i_sleep}\n") # Começa dormindo
    
    for i in range(ciclos):
        # 1. Dormindo
        tempo += t_sleep
        f.write(f"{tempo} {i_sleep}\n")
        
        # 2. Acorda bruscamente (sobe corrente)
        f.write(f"{tempo + 0.0001} {i_tx}\n")
        
        # 3. Transmitindo
        tempo += t_tx
        f.write(f"{tempo} {i_tx}\n")
        
        # 4. Volta a dormir (desce corrente)
        f.write(f"{tempo + 0.0001} {i_sleep}\n")

print(f"Arquivo {filename} criado com sucesso!")