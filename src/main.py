import os
import requests
from supabase import create_client, Client, ClientOptions

# Busca as credenciais das variáveis de ambiente salvas no terminal
URL_SUPABASE = os.getenv("SUPABASE_URL")
CHAVE_SUPABASE = os.getenv("SUPABASE_KEY")

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
            return float(dados["USDBRL"]["bid"])
        return None
    except Exception:
        return None

def salvar_simulacao(db: Client, gastos: float, poupado: float, meses: float, valor_usd: float):
    """Insere os dados da simulação na tabela do Supabase."""
    if not db:
        print("[Aviso] Banco de dados não conectado. Dados não salvos na nuvem.")
        return
    try:
        dados = {
            "gastos_mensais": gastos,
            "valor_poupado": poupado,
            "meses_cobertos": meses,
            "valor_usd": valor_usd
        }
        db.table("simulacoes").insert(dados).execute()
        print("✅ Simulação salva com sucesso no Supabase!")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")

def listar_historico(db: Client):
    """Busca e exibe os registros armazenados no banco de dados."""
    if not db:
        print("❌ Banco de dados não conectado.")
        return
    try:
        resposta = db.table("simulacoes").select("*").order("created_at", descending=True).execute()
        registros = resposta.data
        
        print("\n================ HISTÓRICO DE SIMULAÇÕES ================")
        if not registros:
            print("Nenhum registro encontrado.")
        for reg in registros:
            # Garante tratamento caso valor_usd venha nulo do banco antigo
            v_usd = reg.get('valor_usd') or 0.0
            print(f"Gasto: R$ {reg['gastos_mensais']:.2f} | Guardado: R$ {reg['valor_poupado']:.2f} | Autonomia: {reg['meses_cobertos']} meses | Em USD: $ {v_usd:.2f}")
        print("=========================================================")
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")

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
                gastos = float(input("Digite seu gasto mensal médio (R$): "))
                poupado = float(input("Quanto você tem guardado hoje (R$): "))
                
                meses = calcular_reserva(gastos, poupado)
                print(f"\nSua reserva atual cobre {meses} meses de custo de vida.")
                
                cotacao_usd = buscar_cotacao_dolar()
                reserva_usd = 0.0
                if cotacao_usd:
                    reserva_usd = round(poupado / cotacao_usd, 2)
                    print(f"Sua reserva convertida em Dólar (USD): $ {reserva_usd} (Cotação: R$ {cotacao_usd:.2f})")
                
                if meses < 6:
                    print("⚠️ Alerta: Especialistas recomendam pelo menos 6 meses de reserva.")
                else:
                    print("🛡️ Parabéns! Sua reserva está em um nível seguro.")
                
                salvar = input("\Deseja salvar essa simulação no banco de dados? (s/n): ")
                if salvar.lower() == 's':
                    salvar_simulacao(db, gastos, poupado, meses, reserva_usd)
                    
            except ValueError as e:
                print(f"❌ Erro: {e}")
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
