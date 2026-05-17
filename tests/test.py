import pytest
from src.main import buscar_cotacao_dolar

def test_integracao_api_awesomeapi():
    """Valida se a aplicação consegue se comunicar com a API e recebe um valor numérico válido."""
    cotacao = buscar_cotacao_dolar()
    
    # O teste passa se a API responder e o valor for um número maior que zero
    assert cotacao is not None
    assert isinstance(cotacao, float)
    assert cotacao > 0.0