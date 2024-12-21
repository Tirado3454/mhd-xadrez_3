import streamlit as st
import pandas as pd
from fpdf import FPDF

# Banco de frases organizado por categorias (baseado no documento fornecido)
frases_por_titulo = {
    "Método Científico e a Evolução da Ciência": [
        "O método científico é uma abordagem sistemática para entender o mundo natural.",
        "A ciência evolui com base em observações, hipóteses, experimentos e análises.",
        "Cada descoberta científica é construída sobre os ombros de conhecimentos prévios.",
        "O método científico promove a busca pela verdade com base em evidências.",
    ],
    "Sem Método Científico e Fatores Insólitos": [
        "Sem o método científico, nossas explicações para fenômenos naturais seriam baseadas em mitos e superstições.",
        "A humanidade viveria à mercê de crenças infundadas e dogmas inquestionáveis.",
        "A saúde estaria limitada a práticas mágicas e remédios sem eficácia comprovada.",
        "Doenças seriam vistas como maldições ou punições divinas, e não como processos biológicos tratáveis.",
    ],
    "Como Proceder na Ciência": [
        "O cientista deve buscar a verdade com base em evidências, e não em preferências pessoais.",
        "É fundamental manter a mente aberta, mas sempre exigindo provas antes de aceitar novas ideias.",
        "O método científico é a bússola que guia o cientista no caminho da racionalidade.",
        "O cientista deve estar disposto a mudar de opinião diante de novos dados confiáveis.",
    ],
    "Pensadores e Transformações nos Métodos Científicos": [
        "O conhecimento é poder. (Francis Bacon)",
        "A dúvida é o princípio da sabedoria. (Aristóteles)",
        "A matemática é a linguagem na qual Deus escreveu o universo. (Galileu Galilei)",
        "A simplicidade é a sofisticação máxima. (Leonardo da Vinci)",
    ],
}

# Título do programa
st.title("Banco de Frases para Aulas")
st.markdown("### Selecione frases organizadas por categorias para sua aula.")

# Armazenar seleções
selecoes = {}

# Exibir categorias e frases
for titulo, frases in frases_por_titulo.items():
    with st.expander(f"Categoria: {titulo}"):
        selecoes[titulo] = []
        for frase in frases:
            if st.checkbox(frase, key=f"{titulo}_{frase}"):
                selecoes[titulo].append(frase)

# Botão para organizar e exportar frases
st.markdown("### Revisar e Exportar Frases Selecionadas")
if st.button("Organizar e Exportar"):
    frases_selecionadas = [
        {"Categoria": titulo, "Frase": frase}
        for titulo, frases_categoria in selecoes.items()
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
