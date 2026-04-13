"""Interface de linha de comando (CLI) do MedControl."""

from typing import Optional

from src.storage import MedicationStorage

# ---------------------------------------------------------------------------
# Helpers de formatação
# ---------------------------------------------------------------------------

LINHA = "─" * 60
TITULO = "💊  MedControl — Controle de Medicamentos para Idosos  💊"


def _cabecalho() -> None:
    print(f"\n{LINHA}")
    print(f"  {TITULO}")
    print(LINHA)


def _menu_principal() -> None:
    print("\n  MENU PRINCIPAL")
    print("  1. Cadastrar novo medicamento")
    print("  2. Listar todos os medicamentos")
    print("  3. Ver detalhes de um medicamento")
    print("  4. Remover medicamento")
    print("  5. Atualizar observações")
    print("  0. Sair")
    print()


def _input_obrigatorio(prompt: str) -> str:
    """Solicita entrada não vazia ao usuário."""
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("  ⚠  Este campo é obrigatório. Tente novamente.")


def _input_horarios() -> list:
    """Coleta uma lista de horários do usuário."""
    print("  Informe os horários (ex: 08:00), um por linha.")
    print("  Pressione ENTER em branco para finalizar.\n")
    horarios = []
    while True:
        h = input("  Horário: ").strip()
        if not h:
            if horarios:
                break
            print("  ⚠  Informe ao menos um horário.")
        else:
            horarios.append(h)
    return horarios


def _input_id(prompt: str) -> Optional[int]:
    """Solicita um ID inteiro ao usuário."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("  ⚠  ID inválido. Digite apenas números.")
        return None


# ---------------------------------------------------------------------------
# Ações do menu
# ---------------------------------------------------------------------------

def _cadastrar(storage: MedicationStorage) -> None:
    print(f"\n{LINHA}")
    print("  CADASTRAR MEDICAMENTO")
    print(LINHA)
    name = _input_obrigatorio("  Nome do medicamento : ")
    dosage = _input_obrigatorio("  Dosagem (ex: 10mg)  : ")
    schedules = _input_horarios()
    notes = input("  Observações (opcional): ").strip()
    try:
        med = storage.add(name, dosage, schedules, notes)
        print(f"\n  ✅ Medicamento '{med.name}' cadastrado com ID #{med.id}.")
    except ValueError as e:
        print(f"\n  ❌ Erro: {e}")


def _listar(storage: MedicationStorage) -> None:
    print(f"\n{LINHA}")
    print("  MEDICAMENTOS CADASTRADOS")
    print(LINHA)
    meds = storage.list_all()
    if not meds:
        print("  Nenhum medicamento cadastrado ainda.")
        return
    for med in meds:
        horarios = ", ".join(med.schedules)
        print(f"  [{med.id:>3}]  {med.name:<25} | {med.dosage:<10} | Horários: {horarios}")
    print(f"\n  Total: {len(meds)} medicamento(s).")


def _detalhes(storage: MedicationStorage) -> None:
    print(f"\n{LINHA}")
    print("  DETALHES DO MEDICAMENTO")
    print(LINHA)
    med_id = _input_id("  ID do medicamento: ")
    if med_id is None:
        return
    med = storage.get_by_id(med_id)
    if med is None:
        print(f"  ❌ Nenhum medicamento com ID #{med_id} encontrado.")
        return
    print(f"\n  ID          : {med.id}")
    print(f"  Nome        : {med.name}")
    print(f"  Dosagem     : {med.dosage}")
    print(f"  Horários    : {', '.join(med.schedules)}")
    print(f"  Observações : {med.notes if med.notes else '—'}")


def _remover(storage: MedicationStorage) -> None:
    print(f"\n{LINHA}")
    print("  REMOVER MEDICAMENTO")
    print(LINHA)
    med_id = _input_id("  ID do medicamento a remover: ")
    if med_id is None:
        return
    confirmacao = input(f"  Confirma remoção do ID #{med_id}? (s/N): ").strip().lower()
    if confirmacao != "s":
        print("  ℹ  Operação cancelada.")
        return
    if storage.remove(med_id):
        print(f"  ✅ Medicamento #{med_id} removido com sucesso.")
    else:
        print(f"  ❌ Nenhum medicamento com ID #{med_id} encontrado.")


def _atualizar_obs(storage: MedicationStorage) -> None:
    print(f"\n{LINHA}")
    print("  ATUALIZAR OBSERVAÇÕES")
    print(LINHA)
    med_id = _input_id("  ID do medicamento: ")
    if med_id is None:
        return
    notes = input("  Nova observação: ").strip()
    if storage.update_notes(med_id, notes):
        print("  ✅ Observações atualizadas.")
    else:
        print(f"  ❌ Nenhum medicamento com ID #{med_id} encontrado.")


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

ACOES = {
    "1": _cadastrar,
    "2": _listar,
    "3": _detalhes,
    "4": _remover,
    "5": _atualizar_obs,
}


def run(storage: Optional[MedicationStorage] = None) -> None:
    """Ponto de entrada da CLI. Aceita storage externo para facilitar testes."""
    if storage is None:
        storage = MedicationStorage()

    _cabecalho()
    print("\n  Bem-vindo ao MedControl!")
    print("  Gerencie os medicamentos e horários de forma simples e segura.")

    while True:
        _menu_principal()
        escolha = input("  Escolha uma opção: ").strip()
        if escolha == "0":
            print("\n  Até logo! Cuide-se bem. 👋\n")
            break
        elif escolha in ACOES:
            ACOES[escolha](storage)
        else:
            print("  ⚠  Opção inválida. Digite um número entre 0 e 5.")
