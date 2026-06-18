import os
import requests
from supabase import create_client, Client, ClientOptions

# Credenciais do Supabase inseridas diretamente para a apresentação
URL_SUPABASE = "https://lxkdyjyfqxhqvxoyzejg.supabase.co"
CHAVE_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx4a2R5anlmcXhocXZ4b3l6ZWpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODExNjkxMTYsImV4cCI6MjA5Njc0NTExNn0.g49C6haZMdyadzTG06v905An6G3OtCaiymAXX64O494"

def conectar_banco() -> Client:
    """Estabelece conexão com o banco de dados no Supabase de forma síncrona."""
    if not URL_SUPABASE or not CHAVE_SUPABASE:
        return None
    try:
        # Configuração síncrona obrigatória para evitar erros de loop no terminal local
        return create_client(
            URL_SUPABASE,
            CHAVE_SUPABASE,
            options=ClientOptions(postgrest_client_timeout=10, gotrue_client_timeout=10)
        )
    except Exception:
        return None

def calcular_reserva(gastos_mensais, valor_poupado):
    """Calcula quantos meses a reserva atual cobre."""
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
            return round(float(dados["USDBRL"]["bid"]), 2)
    except Exception:
        return None
    return None

def salvar_simulacao(db: Client, valor_poupado, meses_cobertos, cotacao_dolar):
    """C - CREATE: Salva o registro da simulação na nuvem (Supabase)."""
    if not db:
        print("[Aviso] Banco de dados não conectado. Dados não salvos na nuvem.")
        return False
    try:
        dados = {
            "valor_poupado": valor_poupado,
            "meses_cobertos": meses_cobertos,
            "cotacao_dolar": cotacao_dolar
        }
        db.table("Tb_simulacao").insert(dados).execute()
        print("✅ Simulação salva com sucesso na nuvem!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return False

def listar_historico(db: Client):
    """R - READ: Consulta e exibe o histórico salvo na tabela."""
    if not db:
        print("[Erro] Sem conexão com a nuvem para listar o histórico.")
        return
    try:
        resposta = db.table("Tb_simulacao").select("*").execute()
        historico = resposta.data
        
        print("\n--- HISTÓRICO DE SIMULAÇÕES (SUPABASE) ---")
        if not historico:
            print("Nenhum registro encontrado.")
        for item in historico:
            print(f"ID: {item['id']} | Poupança: R$ {item['valor_poupado']} | Cobertura: {item['meses_cobertos']} meses | Dólar: R$ {item['cotacao_dolar']}")
        print("------------------------------------------")
    except Exception as e:
        print(f"❌ Erro ao consultar histórico: {e}")

def exibir_interface():
    db = conectar_banco()
    
    while True:
        print("\n--- RESERVAFÁCIL: CALCULADORA FINANCEIRA ---")
        print("1. Calcular Nova Reserva de Emergência")
        print("2. Ver Histórico de Simulações (Banco de Dados)")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            try:
                gastos = float(input("Digite o seu gasto mensal médio (R$): "))
                poupado = float(input("Quanto você tem guardado hoje (R$): "))
                
                meses = calcular_reserva(gastos, poupado)
                cotacao = buscar_cotacao_dolar()
                
                print(f"\nSua reserva atual cobre {meses} meses de custo de vida.")
                if cotacao:
                    convertido = round(poupado / cotacao, 2)
                    print(f"Sua reserva convertida em Dólar (USD): $ {convertido} (Cotação: R$ {cotacao})")
                
                if meses < 6:
                    print("⚠️ Alerta: Especialistas recomendam pelo menos 6 meses de reserva.")
                
                salvar = input("Deseja salvar essa simulação no banco de dados? (s/n): ")
                if salvar.lower() == 's':
                    salvar_simulacao(db, poupado, meses, cotacao if cotacao else 0.0)
                    
            except ValueError as e:
                print(f"❌ Entrada inválida: {e}")
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                
        elif opcao == "2":
            listar_historico(db)
            
        elif opcao == "3":
            print("Saindo... Cuide bem do seu patrimônio!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    exibir_interface()
