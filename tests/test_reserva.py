import pytest
from src.main import calcular_reserva

def test_calculo_correto():
    # Caminho Feliz: R$ 6000 poupados / R$ 1000 gastos = 6 meses
    assert calcular_reserva(1000, 6000) == 6.0

def test_gasto_zero_deve_falhar():
    # Entrada Inválida: Não se divide por zero
    with pytest.raises(ValueError):
        calcular_reserva(0, 5000)

def test_valor_poupado_negativo():
    # Caso Limite: Valor negativo
    with pytest.raises(ValueError):
        calcular_reserva(2000, -100)
