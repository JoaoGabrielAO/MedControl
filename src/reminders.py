"""
Módulo de lembretes/notificações de horários de medicamentos.

A ideia é simples: pegamos o horário atual e comparamos com os horários
cadastrados do medicamento. Dependendo da diferença de minutos, dizemos
se está ATRASADO, PRÓXIMO ou EM DIA.
"""

from datetime import datetime


# Se o horário já passou há até 60 minutos, consideramos "atrasado"
MINUTOS_TOLERANCIA_ATRASO = 60

# Se faltam até 30 minutos para o horário, consideramos "próximo"
MINUTOS_TOLERANCIA_PROXIMO = 30


def converter_horario_em_minutos(horario_texto):
    """
    Recebe um horário como texto, por exemplo "08:30",
    e devolve quantos minutos isso representa desde a meia-noite.

    Exemplo: "08:30" -> 8*60 + 30 = 510

    Se o texto não for um horário válido, devolve None.
    """
    horario_texto = horario_texto.strip()

    # Tentamos separar em hora e minuto usando o ":"
    partes = horario_texto.split(":")

    if len(partes) != 2:
        return None

    try:
        hora = int(partes[0])
        minuto = int(partes[1])
    except ValueError:
        return None

    if hora < 0 or hora > 23:
        return None
    if minuto < 0 or minuto > 59:
        return None

    return hora * 60 + minuto


def calcular_diferenca_em_minutos(minutos_horario, minutos_agora):
    """
    Calcula quantos minutos faltam (ou já passaram) entre o horário
    cadastrado e o horário atual.

    Se o resultado for negativo, quer dizer que o horário já passou.
    Se for positivo, quer dizer que o horário ainda vai acontecer.

    Também tratamos a virada do dia (ex: agora é 23:50 e o remédio é 00:10).
    """
    diferenca = minutos_horario - minutos_agora

    # Se a diferença for muito grande num sentido, é porque estamos
    # perto da virada da meia-noite. Ajustamos para o caminho mais curto.
    if diferenca > 12 * 60:
        diferenca = diferenca - 24 * 60
    elif diferenca < -12 * 60:
        diferenca = diferenca + 24 * 60

    return diferenca


def verificar_status_do_horario(horario_texto, agora=None):
    """
    Verifica se um horário está ATRASADO, PROXIMO ou EM_DIA.

    Devolve um texto simples: "atrasado", "proximo", "em_dia" ou None
    (se o horário for inválido).
    """
    minutos_horario = converter_horario_em_minutos(horario_texto)

    if minutos_horario is None:
        return None

    if agora is None:
        agora = datetime.now()

    minutos_agora = agora.hour * 60 + agora.minute

    diferenca = calcular_diferenca_em_minutos(minutos_horario, minutos_agora)

    if diferenca < 0 and diferenca >= -MINUTOS_TOLERANCIA_ATRASO:
        return "atrasado"
    elif diferenca >= 0 and diferenca <= MINUTOS_TOLERANCIA_PROXIMO:
        return "proximo"
    else:
        return "em_dia"


def verificar_status_geral(lista_de_horarios, agora=None):
    """
    Recebe uma lista de horários (ex: ["08:00", "20:00"]) e devolve
    o status mais urgente entre todos eles.

    Prioridade: atrasado é mais importante que proximo, que é mais
    importante que em_dia.
    """
    tem_atrasado = False
    tem_proximo = False

    for horario in lista_de_horarios:
        status = verificar_status_do_horario(horario, agora=agora)

        if status == "atrasado":
            tem_atrasado = True
        elif status == "proximo":
            tem_proximo = True

    if tem_atrasado:
        return "atrasado"
    elif tem_proximo:
        return "proximo"
    else:
        return "em_dia"


def pegar_emoji_do_status(status):
    """Devolve um emoji para representar o status na tela."""
    if status == "atrasado":
        return "🔴"
    elif status == "proximo":
        return "🟡"
    else:
        return "🟢"


def pegar_texto_do_status(status):
    """Devolve um texto amigável para representar o status na tela."""
    if status == "atrasado":
        return "Atrasado"
    elif status == "proximo":
        return "Próximo horário"
    else:
        return "Em dia"