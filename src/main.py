import requests

def calcular_reserva(gastos_mensais, valor_poupado):
    if gastos_mensais <= 0:
        raise ValueError("Os gastos mensais devem ser maiores que zero.")
    if valor_poupado < 0:
        raise ValueError("O valor poupado não pode ser negativo.")
    return round(valor_poupado / gastos_mensais, 2)

def buscar_cotacao_dolar():
    """Consome a API pública AwesomeAPI para obter a cotação do Dólar."""
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            # Retorna o valor de compra (bid) do dólar convertido para float
            return float(dados["USDBRL"]["bid"])
        return None
    except Exception:
        return None

def exibir_interface():
    print("--- Calculador de Reserva de Emergência (v1.1.0) ---")
    try:
        gastos = float(input("Digite seu gasto mensal médio (R$): "))
        poupado = float(input("Quanto você tem guardado hoje (R$): "))
        
        meses = calcular_reserva(gastos, poupado)
        print(f"\nSua reserva atual cobre {meses} meses de custo de vida.")
        
        # Nova funcionalidade: Integração com API
        cotacao_usd = buscar_cotacao_dolar()
        if cotacao_usd:
            reserva_usd = round(poupado / cotacao_usd, 2)
            print(f"Sua reserva convertida em Dólar (USD): $ {reserva_usd} (Cotação atual: R$ {cotacao_usd:.2f})")
        else:
            print("[Aviso]: Não foi possível buscar a cotação do dólar em tempo real.")

    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    exibir_interface()