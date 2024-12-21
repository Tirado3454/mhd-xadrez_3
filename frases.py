import streamlit as st
import pandas as pd
from fpdf import FPDF

# Banco de frases organizado por categorias
frases = {
    "Método Científico": [
        "O conhecimento é poder. (Francis Bacon)",
        "A dúvida é o princípio da sabedoria. (Aristóteles)",
        "A ciência nada mais é do que o refinamento do pensamento cotidiano. (Albert Einstein)",
    ],
    "História da Ciência": [
        "A matemática é a linguagem na qual Deus escreveu o universo. (Galileu Galilei)",
        "A experiência nunca erra; apenas nossos julgamentos falham ao esperar que ela produza resultados fora do possível. (Leonardo da Vinci)",
    ],
    "Pensadores": [
        "Se vi mais longe, foi porque me apoiei nos ombros de gigantes. (Isaac Newton)",
        "A imaginação é mais importante que o conhecimento. (Albert Einstein)",
        "Não é a mais forte das espécies que sobrevive, mas a que melhor se adapta às mudanças. (Charles Darwin)",
    ],
}

# Título da aplicação
st.title("Banco de Frases para Planos de Aula")
st.markdown("### Escolha as frases que deseja incluir em sua aula:")

# Armazenar seleções
selecoes = {}

# Interface para seleção de frases
for categoria, lista_frases in frases.items():
    st.markdown(f"#### {categoria}")
    selecoes[categoria] = []
    for frase in lista_frases:
        if st.checkbox(frase, key=f"{categoria}_{frase}"):
            selecoes[categoria].append(frase)

# Botão para organizar e exportar frases
st.markdown("### Exportar Frases Selecionadas")

if st.button("Organizar e Exportar"):
    # Criar DataFrame para frases selecionadas
    frases_selecionadas = [
        {"Categoria": categoria, "Frase": frase}
        for categoria, frases_categoria in selecoes.items()
        for frase in frases_categoria
    ]
    if frases_selecionadas:
        # Exibir as frases selecionadas
        st.markdown("### Frases Selecionadas:")
        for item in frases_selecionadas:
            st.markdown(f"- **{item['Categoria']}:** {item['Frase']}")
        
        # Exportar para CSV
        df = pd.DataFrame(frases_selecionadas)
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar como CSV",
            data=csv_data,
            file_name="frases_selecionadas.csv",
            mime="text/csv",
        )
        
        # Exportar para PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Frases Selecionadas para Aula", ln=True, align="C")
        pdf.ln(10)
        for item in frases_selecionadas:
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(200, 10, txt=f"Categoria: {item['Categoria']}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, item["Frase"])
            pdf.ln(5)
        pdf_output = pdf.output(dest="S").encode("latin1")
        st.download_button(
            label="Baixar como PDF",
            data=pdf_output,
            file_name="frases_selecionadas.pdf",
            mime="application/pdf",
        )
    else:
        st.warning("Nenhuma frase foi selecionada.")
