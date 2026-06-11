import os
from supabase import create_client, Client

# As credenciais devem ser puxadas de variáveis de ambiente por segurança
URL_SUPABASE = os.getenv("SUPABASE_URL")
CHAVE_SUPABASE = os.getenv("SUPABASE_KEY")

def conectar_banco() -> Client:
    """Estabelece conexão com o banco de dados PostgreSQL no Supabase."""
    if not URL_SUPABASE or not CHAVE_SUPABASE:
        # Retorna None caso localmente não esteja configurado, evitando quebrar o app
        return None
    return create_client(URL_SUPABASE, CHAVE_SUPABASE)

def salvar_simulacao(db: Client, gastos: float, poupado: float, meses: float):
    """Insere os dados da simulação na tabela do banco de dados na nuvem."""
    if db:
        dados = {
            "gastos_mensais": gastos,
            "valor_poupado": poupado,
            "meses_cobertos": meses
        }
        db.table("simulacoes").insert(dados).execute()

def listar_historico(db: Client):
    """Busca e exibe os registros armazenados no banco de dados."""
    if not db:
        print("Banco de dados não conectado.")
        return
    
    resposta = db.table("simulacoes").select("*").execute()
    registros = resposta.data
    
    print("\n--- Histórico de Simulações Salvas ---")
    for reg in registros:
        print(f"ID: {reg['id']} | Gastos: R${reg['gastos_mensais']} | Guardado: R${reg['valor_poupado']} | Autonomia: {reg['meses_cobertos']} meses")
