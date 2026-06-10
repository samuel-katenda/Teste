import requests
import time
import datetime
from cryptography.fernet import Fernet

# 1. Configuração de Segurança (Sua marca registrada)
chave = Fernet.generate_key()
cipher = Fernet(chave)
print(f"--- 🛡️ CHAVE DE SESSÃO GERADA: {chave.decode()[:10]}... ---")

def obter_preco_bitcoin():
    # API pública da Binance - Sem necessidade de login para consulta
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        return float(dados['price'])
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

def salvar_log_criptografado(preco):
    data = datetime.datetime.now().strftime("%H:%M:%S")
    mensagem = f"[{data}] Bitcoin: ${preco:.2f}"
    
    # Criptografando a informação antes de salvar no disco
    token = cipher.encrypt(mensagem.encode())
    
    with open("btc_logs_protegidos.bin", "ab") as f:
        f.write(token + b"\n")
    return mensagem

# 2. Loop de Monitoramento (Lógica de Sentinela)
print("--- 🚀 MONITORANDO BITCOIN EM TEMPO REAL ---")
preco_anterior = 0

try:
    while True:
        preco_atual = obter_preco_bitcoin()
        
        if preco_atual:
            status = salvar_log_criptografado(preco_atual)
            
            # Lógica de Alerta: Só avisa se o preço mudar significativamente
            if preco_atual > preco_anterior:
                print(f"📈 {status} (Subindo!)")
            elif preco_atual < preco_anterior:
                print(f"📉 {status} (Caindo!)")
            
            preco_anterior = preco_atual
            
        # Espera 10 segundos para a próxima verificação (Não sobrecarregar a API)
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\n--- 🛑 Monitoramento encerrado pelo usuário. ---")