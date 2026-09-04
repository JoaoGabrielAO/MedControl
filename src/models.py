"""Modelos de dados da aplicação MedControl."""

from dataclasses import dataclass
from typing import List


@dataclass
class Medication:
    """Representa um medicamento cadastrado."""

    id: int
    name: str
    dosage: str
    schedules: List[str]
    notes: str = ""
    para_que_serve: str = ""
    contraindicacoes: str = ""

    def to_dict(self) -> dict:
        """Converte o medicamento para dicionário (serialização JSON)."""
        return {
            "id": self.id,
            "name": self.name,
            "dosage": self.dosage,
            "schedules": self.schedules,
            "notes": self.notes,
            "para_que_serve": self.para_que_serve,
            "contraindicacoes": self.contraindicacoes,
        }

    @staticmethod
    def from_dict(data: dict) -> "Medication":
        """Cria um objeto Medication a partir de um dicionário."""
        return Medication(
            id=data["id"],
            name=data["name"],
            dosage=data["dosage"],
            schedules=data["schedules"],
            notes=data.get("notes", ""),
            para_que_serve=data.get("para_que_serve", ""),
            contraindicacoes=data.get("contraindicacoes", ""),
        )