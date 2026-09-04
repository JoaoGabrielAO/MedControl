"""
Testes automatizados do MedControl — cobrindo caminho feliz,
entrada inválida e casos limite.
"""

import pytest

from src.models import Medication
from src.storage import MedicationStorage


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def storage(tmp_path):
    """Cria um MedicationStorage temporário para cada teste."""
    filepath = str(tmp_path / "test_medications.json")
    return MedicationStorage(filepath=filepath)


# ===========================================================================
# 1. CAMINHO FELIZ — operações normais devem funcionar corretamente
# ===========================================================================

class TestCaminhoFeliz:
    """Testa o fluxo principal e esperado da aplicação."""

    def test_adicionar_medicamento_retorna_objeto_correto(self, storage):
        """Ao adicionar um medicamento válido, deve retornar um objeto Medication."""
        med = storage.add(
            name="Atenolol",
            dosage="25mg",
            schedules=["08:00", "20:00"],
            notes="Tomar com água",
        )

        assert isinstance(med, Medication)
        assert med.id == 1
        assert med.name == "Atenolol"
        assert med.dosage == "25mg"
        assert med.schedules == ["08:00", "20:00"]
        assert med.notes == "Tomar com água"

    def test_listar_todos_retorna_lista_com_medicamentos(self, storage):
        """Após adicionar medicamentos, list_all deve retorná-los todos."""
        storage.add("Losartana", "50mg", ["08:00"])
        storage.add("Metformina", "500mg", ["12:00", "19:00"])

        todos = storage.list_all()

        assert len(todos) == 2
        nomes = [m.name for m in todos]
        assert "Losartana" in nomes
        assert "Metformina" in nomes

    def test_remover_medicamento_existente_retorna_true(self, storage):
        """Remover um medicamento existente deve retornar True e reduzir a lista."""
        med = storage.add("Omeprazol", "20mg", ["07:30"])
        resultado = storage.remove(med.id)

        assert resultado is True
        assert storage.count() == 0

    def test_get_by_id_retorna_medicamento_correto(self, storage):
        """get_by_id deve retornar o medicamento pelo seu identificador."""
        med = storage.add("Sinvastatina", "20mg", ["22:00"])
        encontrado = storage.get_by_id(med.id)

        assert encontrado is not None
        assert encontrado.name == "Sinvastatina"

    def test_atualizar_observacoes(self, storage):
        """update_notes deve persistir a nova observação no medicamento."""
        med = storage.add("Aspirina", "100mg", ["13:00"])
        storage.update_notes(med.id, "Tomar após o almoço")

        atualizado = storage.get_by_id(med.id)
        assert atualizado.notes == "Tomar após o almoço"

    def test_persistencia_entre_instancias(self, tmp_path):
        """Dados salvos por uma instância devem ser lidos por outra instância."""
        filepath = str(tmp_path / "persist.json")
        s1 = MedicationStorage(filepath=filepath)
        s1.add("Captopril", "12.5mg", ["08:00", "14:00", "20:00"])

        s2 = MedicationStorage(filepath=filepath)
        assert s2.count() == 1
        assert s2.list_all()[0].name == "Captopril"

    def test_ids_sao_unicos_e_crescentes(self, storage):
        """Cada medicamento adicionado deve receber um ID único e crescente."""
        m1 = storage.add("Med A", "10mg", ["08:00"])
        m2 = storage.add("Med B", "20mg", ["12:00"])
        m3 = storage.add("Med C", "30mg", ["18:00"])

        assert m1.id < m2.id < m3.id
        assert len({m1.id, m2.id, m3.id}) == 3

    def test_serialization_to_dict(self):
        """to_dict deve produzir dicionário com todas as chaves corretas."""
        med = Medication(id=1, name="Vitamina D", dosage="2000UI",
                         schedules=["09:00"], notes="Com refeição")
        d = med.to_dict()

        assert d["id"] == 1
        assert d["name"] == "Vitamina D"
        assert d["dosage"] == "2000UI"
        assert d["schedules"] == ["09:00"]
        assert d["notes"] == "Com refeição"

    def test_from_dict_recria_objeto(self):
        """from_dict deve recriar um objeto Medication idêntico ao original."""
        data = {
            "id": 5,
            "name": "Ferro",
            "dosage": "40mg",
            "schedules": ["08:00"],
            "notes": "",
        }
        med = Medication.from_dict(data)

        assert med.id == 5
        assert med.name == "Ferro"


# ===========================================================================
# 2. ENTRADA INVÁLIDA — a aplicação deve lançar erros ou rejeitar dados ruins
# ===========================================================================

class TestEntradaInvalida:
    """Testa que entradas inválidas são tratadas corretamente."""

    def test_nome_vazio_levanta_value_error(self, storage):
        """Adicionar medicamento com nome vazio deve lançar ValueError."""
        with pytest.raises(ValueError, match="nome do medicamento não pode ser vazio"):
            storage.add(name="", dosage="10mg", schedules=["08:00"])

    def test_nome_apenas_espacos_levanta_value_error(self, storage):
        """Nome composto apenas por espaços deve ser rejeitado."""
        with pytest.raises(ValueError):
            storage.add(name="   ", dosage="10mg", schedules=["08:00"])

    def test_dosagem_vazia_levanta_value_error(self, storage):
        """Dosagem vazia deve lançar ValueError."""
        with pytest.raises(ValueError, match="dosagem não pode ser vazia"):
            storage.add(name="Paracetamol", dosage="", schedules=["08:00"])

    def test_lista_de_horarios_vazia_levanta_value_error(self, storage):
        """Lista de horários vazia deve lançar ValueError."""
        with pytest.raises(ValueError, match="ao menos um horário"):
            storage.add(name="Dipirona", dosage="500mg", schedules=[])

    def test_remover_id_inexistente_retorna_false(self, storage):
        """Tentar remover ID que não existe deve retornar False sem erros."""
        resultado = storage.remove(9999)
        assert resultado is False

    def test_get_by_id_inexistente_retorna_none(self, storage):
        """Buscar ID inexistente deve retornar None."""
        resultado = storage.get_by_id(9999)
        assert resultado is None

    def test_update_notes_id_inexistente_retorna_false(self, storage):
        """Atualizar observações de ID inexistente deve retornar False."""
        resultado = storage.update_notes(9999, "alguma obs")
        assert resultado is False


# ===========================================================================
# 3. CASOS LIMITE — comportamentos em fronteiras e situações extremas
# ===========================================================================

class TestCasosLimite:
    """Testa comportamentos em condições de borda."""

    def test_listar_sem_medicamentos_retorna_lista_vazia(self, storage):
        """list_all em storage vazio deve retornar lista vazia, não erro."""
        resultado = storage.list_all()
        assert resultado == []

    def test_count_inicia_em_zero(self, storage):
        """count() num storage vazio deve ser 0."""
        assert storage.count() == 0

    def test_adicionar_muitos_medicamentos(self, storage):
        """Deve ser possível adicionar 50 medicamentos sem erros."""
        for i in range(1, 51):
            storage.add(f"Med {i}", f"{i}mg", ["08:00"])
        assert storage.count() == 50

    def test_id_nao_reutilizado_apos_remocao(self, storage):
        """Após remover um medicamento, o próximo ID deve ser maior, não reutilizado."""
        m1 = storage.add("Alpha", "5mg", ["08:00"])
        m2 = storage.add("Beta", "10mg", ["12:00"])
        storage.remove(m2.id)
        m3 = storage.add("Gamma", "15mg", ["18:00"])

        assert m3.id > m1.id
        assert m3.id != m2.id

    def test_horario_unico_aceito(self, storage):
        """Medicamento com apenas um horário deve ser aceito normalmente."""
        med = storage.add("Levotiroxina", "50mcg", ["06:30"])
        assert len(med.schedules) == 1
        assert med.schedules[0] == "06:30"

    def test_muitos_horarios_aceitos(self, storage):
        """Medicamento com múltiplos horários (6x ao dia) deve ser aceito."""
        schedules = ["06:00", "08:00", "10:00", "12:00", "16:00", "20:00"]
        med = storage.add("Antibiotico", "250mg", schedules)
        assert len(med.schedules) == 6

    def test_notes_opcional_padrao_vazio(self, storage):
        """O campo notes deve ter string vazia como padrão."""
        med = storage.add("Cálcio", "600mg", ["13:00"])
        assert med.notes == ""

    def test_from_dict_sem_notes_usa_padrao(self):
        """from_dict sem campo 'notes' deve usar string vazia como padrão."""
        data = {"id": 1, "name": "X", "dosage": "1mg", "schedules": ["08:00"]}
        med = Medication.from_dict(data)
        assert med.notes == ""

    def test_nome_e_dosagem_sao_stripados(self, storage):
        """Espaços extras em nome/dosagem devem ser removidos automaticamente."""
        med = storage.add("  Ácido Fólico  ", "  400mcg  ", ["08:00"])
        assert med.name == "Ácido Fólico"
        assert med.dosage == "400mcg"

    def test_horarios_vazios_na_lista_sao_ignorados(self, storage):
        """Horários em branco dentro da lista devem ser ignorados."""
        med = storage.add("Magnésio", "300mg", ["08:00", "", "  ", "22:00"])
        assert "" not in med.schedules
        assert len(med.schedules) == 2


# ---------------------------------------------------------------------------
# Testes do informativo do remédio (para que serve / contraindicações)
# ---------------------------------------------------------------------------

class TestInformativoRemedio:
    """Testa os campos opcionais de informativo do remédio."""

    def test_cadastro_com_informativo_completo(self, storage):
        """Deve salvar corretamente os campos de informativo quando informados."""
        med = storage.add(
            "Dipirona",
            "500mg",
            ["08:00"],
            notes="",
            para_que_serve="Dor e febre",
            contraindicacoes="Alergia a dipirona",
        )
        assert med.para_que_serve == "Dor e febre"
        assert med.contraindicacoes == "Alergia a dipirona"

    def test_cadastro_sem_informativo_usa_padrao_vazio(self, storage):
        """Se o usuário não preencher o informativo, deve ficar vazio (não obrigatório)."""
        med = storage.add("Paracetamol", "750mg", ["12:00"])
        assert med.para_que_serve == ""
        assert med.contraindicacoes == ""

    def test_informativo_persiste_apos_salvar_e_recarregar(self, storage):
        """O informativo deve ser salvo e recuperado corretamente do arquivo."""
        storage.add(
            "Ibuprofeno",
            "400mg",
            ["09:00"],
            para_que_serve="Inflamação",
            contraindicacoes="Problemas gástricos",
        )
        medicamentos = storage.list_all()
        encontrado = medicamentos[0]
        assert encontrado.para_que_serve == "Inflamação"
        assert encontrado.contraindicacoes == "Problemas gástricos"