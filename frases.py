import streamlit as st
import pandas as pd
from fpdf import FPDF

# Banco de frases extraído do documento enviado
frases_por_titulo = {
    "Método Científico e a Evolução da Ciência": [
        "O método científico é uma abordagem sistemática para entender o mundo natural.",
        "A ciência evolui com base em observações, hipóteses, experimentos e análises.",
        "Cada descoberta científica é construída sobre os ombros de conhecimentos prévios.",
        "O método científico promove a busca pela verdade com base em evidências.",
        "Hipóteses científicas devem ser testáveis e sujeitas a refutação.",
        "A experimentação é o coração do método científico, permitindo a validação de hipóteses.",
        "O método científico evoluiu ao longo da história, desde a filosofia grega até a ciência moderna.",
        "Observações precisas são a base para formular questões científicas relevantes.",
        "A ciência é um processo cumulativo que se adapta e se corrige ao longo do tempo.",
        "Teorias científicas não são verdades absolutas, mas explicações baseadas em evidências robustas.",
        "A ciência moderna foi moldada pela Revolução Científica nos séculos XVI e XVII.",
        "Galileu Galilei é considerado um dos pioneiros na aplicação do método científico.",
        "O avanço da tecnologia ampliou significativamente as fronteiras da ciência.",
        "A repetibilidade é um princípio fundamental para validar experimentos científicos.",
        "O método científico permite transformar curiosidade em conhecimento estruturado.",
        "A ciência é impulsionada por perguntas, mas cresce a partir das respostas.",
        "Grandes descobertas frequentemente surgem da observação de fenômenos inesperados.",
        "A ciência é uma ferramenta poderosa para resolver problemas globais, como mudanças climáticas e pandemias.",
        "A evolução da ciência depende da colaboração entre pesquisadores de diferentes áreas.",
        "O método científico promove um pensamento crítico e cético, essencial para o progresso humano.",
        "Cientistas devem estar dispostos a revisar suas ideias à luz de novas evidências.",
        "A ética desempenha um papel fundamental na aplicação responsável do conhecimento científico.",
        "A ciência moderna se tornou interdisciplinar, unindo biologia, química, física e mais.",
        "A evolução da ciência é marcada por revoluções paradigmáticas, como descrito por Thomas Kuhn.",
        "A comunicação científica é vital para a disseminação e aplicação do conhecimento.",
        "Grandes invenções, como o telescópio e o microscópio, revolucionaram o método científico.",
        "O método científico é aplicável em diversas áreas, desde ciências naturais até ciências sociais.",
        "Einstein destacou que a imaginação é tão importante quanto o conhecimento na ciência.",
        "A ciência continua a evoluir, questionando as fronteiras do desconhecido.",
        "O método científico é um farol para a humanidade, guiando-nos em direção à compreensão e ao progresso."
    ],
    "Sem Método Científico e Fatores Insólitos": [
        "Sem o método científico, nossas explicações para fenômenos naturais seriam baseadas em mitos e superstições.",
        "A humanidade viveria à mercê de crenças infundadas e dogmas inquestionáveis.",
        "A saúde estaria limitada a práticas mágicas e remédios sem eficácia comprovada.",
        "Doenças seriam vistas como maldições ou punições divinas, e não como processos biológicos tratáveis.",
        "A navegação dependeria de presságios e sinais celestiais, em vez de mapas precisos e instrumentos como o GPS.",
        "A exploração espacial nunca teria saído do papel, sendo considerada um sonho impossível ou sagrado.",
        "A eletricidade seria um mistério incompreensível, talvez atribuída a forças sobrenaturais.",
        "O desenvolvimento da tecnologia seria substituído por objetos rituais e mágicos.",
        "Decisões políticas poderiam ser tomadas com base em augúrios ou adivinhações, e não em dados e análises.",
        "A agricultura dependeria de rituais para invocar boas colheitas, e não de técnicas científicas comprovadas.",
        "Fenômenos como relâmpagos e eclipses seriam temidos como sinais divinos ou castigos.",
        "A longevidade humana seria limitada pela falta de vacinas e tratamentos baseados em evidências.",
        "A comunicação à distância seria inexistente, sem a invenção do rádio, telefone ou internet.",
        "A química seria vista como alquimia, com práticas sem fundamentos e resultados imprevisíveis.",
        "A física seria substituída por crenças místicas sobre o funcionamento do universo.",
        "Catástrofes naturais, como terremotos, seriam interpretadas como ira divina e não como fenômenos geológicos.",
        "Sem o método científico, teorias absurdas e conspirações governariam o pensamento popular.",
        "Os avanços na alimentação, como o controle da fome, seriam inexistentes sem a ciência alimentar.",
        "A medicina seria dominada por práticas sem base, como sangrias e amuletos.",
        "As viagens aéreas seriam impossíveis, já que o entendimento da física e da engenharia não existiria.",
        "A economia dependeria de adivinhações e horóscopos, em vez de estatísticas e previsões.",
        "Não haveria proteção contra pandemias, com curas sendo buscadas em práticas esotéricas.",
        "A ciência forense seria inexistente, e julgamentos dependeriam de testemunhos ou confissões forçadas.",
        "A arqueologia seria vista como um trabalho de exploração espiritual e não de estudo histórico.",
        "Sem ciência, os limites do conhecimento seriam definidos pelo medo e pelo misticismo.",
        "As relações humanas seriam moldadas por tabus e tradições, em vez de estudos sobre comportamento e psicologia.",
        "O progresso científico seria substituído por práticas repetitivas e sem inovação.",
        "A busca pelo conhecimento seria vista como desrespeito às tradições, freando qualquer avanço.",
        "O conceito de bem-estar seria reduzido a práticas intuitivas e conselhos de 'curandeiros'.",
        "A humanidade estaria presa a ciclos de ignorância, limitada por explicações que nada fariam para melhorar nossa condição."
    ],
    "Como Proceder na Ciência": [
        "O cientista deve buscar a verdade com base em evidências, e não em preferências pessoais.",
        "É fundamental manter a mente aberta, mas sempre exigindo provas antes de aceitar novas ideias.",
        "O método científico é a bússola que guia o cientista no caminho da racionalidade.",
        "O cientista deve estar disposto a mudar de opinião diante de novos dados confiáveis.",
        "A dúvida é um motor do progresso científico, mas o ceticismo deve ser construtivo.",
        "Evitar preconceitos é essencial para interpretar dados de forma imparcial.",
        "Hipóteses devem ser testáveis e sujeitas a refutação, não dogmas imutáveis.",
        "A ética científica deve prevalecer sobre pressões externas, como política ou interesses financeiros.",
        "O cientista deve sempre buscar replicar experimentos para validar conclusões.",
        "A ciência avança quando se faz perguntas, não quando se aceita respostas sem questionamento.",
        "É importante separar crenças pessoais da análise objetiva dos fatos.",
        "Transparência nos métodos e resultados é vital para garantir a credibilidade científica.",
        "A curiosidade deve ser aliada à disciplina para que a investigação não se desvie.",
        "O cientista deve reconhecer a possibilidade de erro e trabalhar para minimizá-lo.",
        "Publicar resultados negativos é tão importante quanto relatar sucessos.",
        "Colaborações científicas devem ser baseadas na busca do conhecimento, não na competição.",
        "A ciência não é sobre certezas, mas sobre probabilidades baseadas em dados sólidos.",
        "Pressões sociais e culturais não devem ditar o rumo das investigações científicas.",
        "O cientista deve evitar atalhos que comprometam a precisão ou a integridade dos resultados.",
        "Hipóteses devem ser testadas contra os fatos, e não os fatos ajustados às hipóteses.",
        "A ciência deve estar aberta ao escrutínio público e à revisão por pares.",
        "O cientista deve lembrar que a ausência de evidência não é evidência de ausência.",
        "Argumentos de autoridade não substituem a necessidade de provas concretas.",
        "O cientista deve distinguir entre correlação e causalidade ao interpretar dados.",
        "Decisões científicas devem ser baseadas em lógica e não em emoções ou intuições.",
        "Ética e responsabilidade são fundamentais no uso e aplicação do conhecimento científico.",
        "O cientista deve evitar viés de confirmação, buscando dados que refutem suas próprias hipóteses.",
        "A humildade é essencial: nenhuma teoria está acima de revisão ou substituição.",
        "A ciência deve priorizar o bem coletivo e não interesses individuais ou de grupos.",
        "A busca pelo conhecimento deve ser guiada pela honestidade intelectual e pela integridade."
    ],
    "Pensadores e Transformações nos Métodos Científicos": [
        "O conhecimento é poder. (Francis Bacon)",
        "A dúvida é o princípio da sabedoria. (Aristóteles)",
        "A matemática é a linguagem na qual Deus escreveu o universo. (Galileu Galilei)",
        "A simplicidade é a sofisticação máxima. (Leonardo da Vinci)",
        "A experiência nunca erra; apenas nossos julgamentos falham ao esperar que ela produza resultados fora do possível. (Leonardo da Vinci)",
        "O todo é maior do que a soma das suas partes. (Aristóteles)",
        "Se vi mais longe, foi porque me apoiei nos ombros de gigantes. (Isaac Newton)",
        "Não é a mais forte das espécies que sobrevive, nem a mais inteligente, mas a que melhor se adapta às mudanças. (Charles Darwin)",
        "A imaginação é mais importante que o conhecimento. (Albert Einstein)",
        "A ciência nada mais é do que o refinamento do pensamento cotidiano. (Albert Einstein)",
        "Penso, logo existo. (René Descartes)",
        "A hipótese deve ser testada, não aceita cegamente. (Isaac Newton)",
        "O método é a base de todo progresso genuíno no conhecimento. (René Descartes)",
        "Não devemos apenas aceitar aquilo que vemos, mas buscar as causas por trás dos fenômenos. (Platão)",
        "A astronomia é escrita para os matemáticos. (Nicolau Copérnico)"
    ]
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
