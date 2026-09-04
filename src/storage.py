"""Módulo de persistência de dados em arquivo JSON."""

import json
import os
from typing import List, Optional

from src.models import Medication

DEFAULT_DATA_FILE = "data/medications.json"


class MedicationStorage:
    """Gerencia o armazenamento e recuperação de medicamentos em JSON."""

    def __init__(self, filepath: str = DEFAULT_DATA_FILE):
        self.filepath = filepath
        self._ensure_data_dir()
        self._medications: List[Medication] = self._load()
        # Garante que o contador nunca volte atrás após remoções
        self._id_counter: int = max(
            (med.id for med in self._medications), default=0
        )

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def _ensure_data_dir(self) -> None:
        """Garante que o diretório de dados existe."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def _load(self) -> List[Medication]:
        """Carrega os dados do arquivo JSON."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
                return [Medication.from_dict(item) for item in raw]
            except (json.JSONDecodeError, KeyError):
                return []

    def _save(self) -> None:
        """Persiste os dados no arquivo JSON."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(
                [med.to_dict() for med in self._medications],
                f,
                ensure_ascii=False,
                indent=2,
            )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def _next_id(self) -> int:
        """Gera o próximo ID único, nunca reutilizando IDs de itens removidos."""
        self._id_counter += 1
        return self._id_counter

    def add(
        self,
        name: str,
        dosage: str,
        schedules: List[str],
        notes: str = "",
        para_que_serve: str = "",
        contraindicacoes: str = "",
    ) -> Medication:
        """Adiciona um novo medicamento."""
        if not name or not name.strip():
            raise ValueError("O nome do medicamento não pode ser vazio.")
        if not dosage or not dosage.strip():
            raise ValueError("A dosagem não pode ser vazia.")
        if not schedules:
            raise ValueError("Informe ao menos um horário.")

        med = Medication(
            id=self._next_id(),
            name=name.strip(),
            dosage=dosage.strip(),
            schedules=[s.strip() for s in schedules if s.strip()],
            notes=notes.strip(),
            para_que_serve=para_que_serve.strip(),
            contraindicacoes=contraindicacoes.strip(),
        )
        self._medications.append(med)
        self._save()
        return med

    def list_all(self) -> List[Medication]:
        """Retorna todos os medicamentos cadastrados."""
        return list(self._medications)

    def get_by_id(self, medication_id: int) -> Optional[Medication]:
        """Busca um medicamento pelo ID."""
        for med in self._medications:
            if med.id == medication_id:
                return med
        return None

    def remove(self, medication_id: int) -> bool:
        """Remove um medicamento pelo ID. Retorna True se removido."""
        original_count = len(self._medications)
        self._medications = [m for m in self._medications if m.id != medication_id]
        if len(self._medications) < original_count:
            self._save()
            return True
        return False

    def update_notes(self, medication_id: int, notes: str) -> bool:
        """Atualiza as observações de um medicamento."""
        med = self.get_by_id(medication_id)
        if med is None:
            return False
        med.notes = notes.strip()
        self._save()
        return True

    def count(self) -> int:
        """Retorna a quantidade de medicamentos cadastrados."""
        return len(self._medications)