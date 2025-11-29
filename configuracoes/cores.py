import random
import matplotlib.colors as mcolors
from dados.fichas import fichas 

def cores_partido(base = fichas("2024")):
    # Gerar cores aleatórias para os partidos
    cores = {}
    for partido in base['sg_partido'].unique():
        if partido == 'PSDB':
            cores[partido] = 'blue'
        elif partido == 'PT':
            cores[partido] = 'red'
        else:
            # Gera uma cor RGB aleatória (excluindo tons muito claros para melhor visibilidade)
            rgb = [random.random() for _ in range(3)]  # 0.8 para evitar cores muito claras
            cores[partido] = mcolors.rgb2hex(rgb)  # Converte RGB para formato hexadecimal
    return cores

cores = cores_partido()