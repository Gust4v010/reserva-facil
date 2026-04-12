def calcular_reserva(gastos_mensais, valor_poupado):
    """Calcula quantos meses a reserva atual cobre."""
    if gastos_mensais <= 0:
        raise ValueError("Os gastos mensais devem ser maiores que zero.")
    if valor_poupado < 0:
        raise ValueError("O valor poupado não pode ser negativo.")
    
    meses = valor_poupado / gastos_mensais
    return round(meses, 2)

def exibir_interface():
    print("--- Calculador de Reserva de Emergência ---")
    try:
        gastos = float(input("Digite seu gasto mensal médio (R$): "))
        poupado = float(input("Quanto você tem guardado hoje (R$): "))
        
        meses = calcular_reserva(gastos, poupado)
        
        print(f"\nSua reserva atual cobre {meses} meses de custo de vida.")
        
        if meses < 6:
            print("Aviso: Especialistas recomendam pelo menos 6 meses de reserva.")
        else:
            print("Parabéns! Sua reserva está em um nível seguro.")
            
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception:
        print("Erro inesperado. Verifique os dados digitados.")

if __name__ == "__main__":
    exibir_interface()
