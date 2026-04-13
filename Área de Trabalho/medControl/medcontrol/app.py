import streamlit as st
import sys
import os

# Garante que o Python encontre a pasta 'src'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.Storage import MedicationStorage
from src.models import Medication

# Configurações da página
st.set_page_config(page_title="MedControl 💊", layout="centered")

# Inicializa o 'motor' com o nome CORRETO da classe
# Se o arquivo não existir, ele criará na pasta data/
storage = MedicationStorage()

st.title("💊 MedControl")
st.markdown("---")

menu = st.sidebar.selectbox("O que deseja fazer?", ["Listar Medicamentos", "Cadastrar Novo", "Remover"])

if menu == "Listar Medicamentos":
    st.header("📋 Lista de Remédios")
    medicamentos = storage.list_all()
    
    if not medicamentos:
        st.info("Nenhum medicamento cadastrado ainda.")
    else:
        for med in medicamentos:
            with st.expander(f"📌 {med.name} - {med.dosage}"):
                st.write(f"**Horários:** {', '.join(med.schedules)}")
                st.write(f"**Observações:** {med.notes if med.notes else 'Sem observações.'}")
                st.caption(f"ID: {med.id}")

elif menu == "Cadastrar Novo":
    st.header("📝 Novo Cadastro")
    
    with st.form("form_cadastro"):
        nome = st.text_input("Nome do Medicamento")
        dosagem = st.text_input("Dosagem (ex: 50mg, 1 comprimido)")
        horarios = st.text_input("Horários (separe por vírgula, ex: 08:00, 20:00)")
        notas = st.text_area("Observações Adicionais")
        
        enviado = st.form_submit_button("Salvar Medicamento")
        
        if enviado:
            if nome and dosagem and horarios:
                lista_horarios = [h.strip() for h in horarios.split(",")]
                try:
                    novo_med = storage.add(nome, dosagem, lista_horarios, notas)
                    st.success(f"✅ {nome} cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.error("Por favor, preencha o nome, dosagem e pelo menos um horário.")

elif menu == "Remover":
    st.header("🗑️ Remover Medicamento")
    medicamentos = storage.list_all()
    
    if medicamentos:
        opcoes = {f"{m.id} - {m.name}": m.id for m in medicamentos}
        escolha = st.selectbox("Selecione o medicamento para remover", list(opcoes.keys()))
        
        if st.button("Confirmar Exclusão", type="primary"):
            if storage.remove(opcoes[escolha]):
                st.success("Medicamento removido!")
                st.rerun()
    else:
        st.info("Nada para remover.")