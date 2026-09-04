"""
Testes do módulo de lembretes (src/reminders.py).

Aqui testamos as funções que calculam se um horário está
atrasado, próximo ou em dia.
"""

from datetime import datetime

from src.reminders import (
    converter_horario_em_minutos,
    verificar_status_do_horario,
    verificar_status_geral,
)


# ---------------------------------------------------------------------------
# Testes da função que converte horário em minutos
# ---------------------------------------------------------------------------

def test_converter_horario_valido():
    """Um horário válido deve ser convertido corretamente para minutos."""
    resultado = converter_horario_em_minutos("08:30")
    assert resultado == 510  # 8*60 + 30


def test_converter_horario_invalido_retorna_none():
    """Um texto que não é um horário deve retornar None."""
    resultado = converter_horario_em_minutos("isso nao e horario")
    assert resultado is None


def test_converter_horario_vazio_retorna_none():
    """Uma string vazia deve retornar None."""
    resultado = converter_horario_em_minutos("")
    assert resultado is None


# ---------------------------------------------------------------------------
# Testes da função que verifica o status de um horário
# ---------------------------------------------------------------------------

def test_horario_em_dia():
    """Um horário bem distante do momento atual deve estar 'em_dia'."""
    agora = datetime(2024, 1, 1, 8, 0)
    status = verificar_status_do_horario("20:00", agora=agora)
    assert status == "em_dia"


def test_horario_proximo():
    """Um horário 15 minutos no futuro deve estar 'proximo'."""
    agora = datetime(2024, 1, 1, 8, 0)
    status = verificar_status_do_horario("08:15", agora=agora)
    assert status == "proximo"


def test_horario_atrasado():
    """Um horário que já passou há 20 minutos deve estar 'atrasado'."""
    agora = datetime(2024, 1, 1, 8, 20)
    status = verificar_status_do_horario("08:00", agora=agora)
    assert status == "atrasado"


def test_horario_muito_atrasado_volta_a_em_dia():
    """Depois de passar 1 hora do horário, consideramos que não é mais 'atrasado'."""
    agora = datetime(2024, 1, 1, 9, 5)  # 1h05 depois das 08:00
    status = verificar_status_do_horario("08:00", agora=agora)
    assert status == "em_dia"


def test_horario_invalido_retorna_none():
    """Um horário mal formatado deve retornar None, sem quebrar o programa."""
    status = verificar_status_do_horario("horario_qualquer", agora=datetime(2024, 1, 1, 8, 0))
    assert status is None


def test_virada_do_dia():
    """Perto da meia-noite, a conta deve continuar funcionando certinho."""
    agora = datetime(2024, 1, 1, 23, 50)
    status = verificar_status_do_horario("00:10", agora=agora)
    assert status == "proximo"


# ---------------------------------------------------------------------------
# Testes da função que verifica o status geral (vários horários)
# ---------------------------------------------------------------------------

def test_status_geral_prioriza_atrasado():
    """Se um dos horários estiver atrasado, o status geral deve ser 'atrasado'."""
    agora = datetime(2024, 1, 1, 8, 20)
    status = verificar_status_geral(["08:00", "20:00"], agora=agora)
    assert status == "atrasado"


def test_status_geral_sem_atrasado_mas_com_proximo():
    """Se não houver atrasado mas houver próximo, o status geral deve ser 'proximo'."""
    agora = datetime(2024, 1, 1, 8, 0)
    status = verificar_status_geral(["08:15", "20:00"], agora=agora)
    assert status == "proximo"


def test_status_geral_lista_vazia():
    """Uma lista vazia de horários não deve dar erro, deve retornar 'em_dia'."""
    status = verificar_status_geral([], agora=datetime(2024, 1, 1, 8, 0))
    assert status == "em_dia"


def test_status_geral_com_horario_invalido_no_meio():
    """Um horário inválido dentro da lista não deve travar o cálculo dos outros."""
    agora = datetime(2024, 1, 1, 8, 0)
    status = verificar_status_geral(["horario_ruim", "08:15"], agora=agora)
    assert status == "proximo"