import psutil
import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

console = Console()

def gerar_painel(net_antes, tempo_antes):
    # Coleta de dados básicos
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent
    
    # Coleta de dados da Rede (para calcular a velocidade)
    net_agora = psutil.net_io_counters()
    tempo_agora = time.time()
    
    # Calcula a diferença de tempo e de dados baixados/enviados
    tempo_decorrido = tempo_agora - tempo_antes
    if tempo_decorrido == 0: tempo_decorrido = 1 # Evita erro no cálculo
    
    down_mbs = ((net_agora.bytes_recv - net_antes.bytes_recv) / 1024 / 1024) / tempo_decorrido
    up_mbs = ((net_agora.bytes_sent - net_antes.bytes_sent) / 1024 / 1024) / tempo_decorrido

    # Define as cores de alerta
    cor_cpu = "green" if cpu < 50 else "yellow" if cpu < 80 else "red"
    cor_ram = "green" if ram < 50 else "yellow" if ram < 80 else "red"

    # Monta o visual do painel do ULTRAMASTERPC
    layout = f"[bold cyan]ULTRAMASTER MONITOR[/]\n\n"
    layout += f"[{cor_cpu}]CPU:      {cpu}% [/]\n"
    layout += f"[{cor_ram}]RAM:      {ram}% [/]\n"
    layout += f"[green]HD/SSD:   {disco}% [/]\n"
    layout += f"[blue]Download: {down_mbs:.2f} MB/s[/]\n"
    layout += f"[magenta]Upload:   {up_mbs:.2f} MB/s[/]\n"
    
    return Panel(layout, border_style="bright_blue", expand=False), net_agora, tempo_agora

# Prepara as variáveis para a primeira leitura da rede
net_atual = psutil.net_io_counters()
tempo_atual = time.time()
painel, net_atual, tempo_atual = gerar_painel(net_atual, tempo_atual)

# Roda a atualização na tela a cada meio segundo
with Live(painel, refresh_per_second=4) as live:
    while True:
        time.sleep(0.5)
        painel, net_atual, tempo_atual = gerar_painel(net_atual, tempo_atual)
        live.update(painel)