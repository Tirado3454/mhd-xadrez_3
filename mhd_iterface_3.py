import streamlit as st
import pandas as pd
import chess
import chess.svg

# ConfiguraÃ§Ã£o inicial da interface
st.set_page_config(page_title="Modelo HipotÃ©tico-Dedutivo no Xadrez", layout="centered")
st.markdown("""<h1 style='font-size:32px; display: flex; align-items: center;'>
<img src='data:image/png;base64,<insira_o_base64_gerado_da_logo_aqui>' style='height:50px; margin-right:10px;'> Modelo HipotÃ©tico-Dedutivo no Xadrez
</h1>""", unsafe_allow_html=True)
st.write("Configure e salve posiÃ§Ãµes personalizadas no tabuleiro.")

# InicializaÃ§Ã£o da tabela de dados
if "mhd_data" not in st.session_state:
    st.session_state.mhd_data = pd.DataFrame(columns=["Etapa", "DescriÃ§Ã£o", "FEN"])

# InicializaÃ§Ã£o do tabuleiro
if "current_board" not in st.session_state:
    st.session_state.current_board = chess.Board()

# Perguntas norteadoras para cada etapa do MHD
perguntas = {
    "Base TeÃ³rica": "Qual Ã© a base de conhecimento ou estratÃ©gia que serÃ¡ usada como referÃªncia?",
    "HipÃ³tese": "O que vocÃª espera alcanÃ§ar com uma jogada ou sequÃªncia de jogadas?",
    "ConsequÃªncias": "Quais reaÃ§Ãµes ou respostas vocÃª espera do adversÃ¡rio?",
    "Experimento": "Qual jogada ou sequÃªncia serÃ¡ aplicada para testar sua hipÃ³tese?",
    "ObservaÃ§Ãµes": "O que aconteceu apÃ³s a jogada? O resultado foi o esperado?",
    "AvaliaÃ§Ã£o": "A hipÃ³tese inicial foi confirmada, ajustada ou refutada? Por quÃª?"
}

# FunÃ§Ã£o para renderizar o tabuleiro com estilo customizado
def render_tabuleiro_customizado(board):
    return chess.svg.board(
        board=board, 
        size=320,  # Reduzindo o tamanho do tabuleiro (20% menor)
        style="""
            .square.light { fill: #ffffff; }  /* Casas claras em branco */
            .square.dark { fill: #8FBC8F; }  /* Casas escuras em verde */
        """
    )

# ConfiguraÃ§Ã£o do tabuleiro com FEN
st.markdown("### ConfiguraÃ§Ã£o do Tabuleiro")
fen_input = st.text_input(
    "Insira a notaÃ§Ã£o FEN para configurar o tabuleiro:", 
    value=st.session_state.current_board.fen()
)

if st.button("Atualizar Tabuleiro com FEN"):
    try:
        st.session_state.current_board.set_fen(fen_input)
        st.success("Tabuleiro atualizado com sucesso!")
    except ValueError:
        st.error("NotaÃ§Ã£o FEN invÃ¡lida. Por favor, insira uma notaÃ§Ã£o correta.")

# FormulÃ¡rio para entrada dos dados
st.markdown("### Adicionar Nova Etapa")
with st.form("mhd_form"):
    etapa = st.selectbox("Selecione a Etapa", list(perguntas.keys()))
    st.markdown(f"**Dica:** {perguntas[etapa]}")  # Atualiza a dica dinamicamente com base na seleÃ§Ã£o
    descricao = st.text_area("Descreva a etapa:", height=100)

    # Visualizar tabuleiro configurado
    st.markdown("### Tabuleiro Atual")
    st.image(render_tabuleiro_customizado(st.session_state.current_board), use_container_width=True)

    submitted = st.form_submit_button("Adicionar Etapa")
    if submitted:
        if descricao.strip():
            nova_entrada = pd.DataFrame({
                "Etapa": [etapa],
                "DescriÃ§Ã£o": [descricao],
                "FEN": [st.session_state.current_board.fen()]
            })
            st.session_state.mhd_data = pd.concat([st.session_state.mhd_data, nova_entrada], ignore_index=True)
            st.success(f"Etapa '{etapa}' adicionada com sucesso!")
        else:
            st.error("A descriÃ§Ã£o nÃ£o pode estar vazia!")

# ExibiÃ§Ã£o da tabela dinÃ¢mica
st.subheader("Tabela do Modelo HipotÃ©tico-Dedutivo")
if not st.session_state.mhd_data.empty:
    for index, row in st.session_state.mhd_data.iterrows():
        st.markdown(f"**Etapa:** {row['Etapa']}")
        st.markdown(f"**DescriÃ§Ã£o:** {row['DescriÃ§Ã£o']}")
        st.image(render_tabuleiro_customizado(chess.Board(row['FEN'])), use_column_width=True)
else:
    st.info("Nenhuma etapa adicionada ainda.")

# Exportar a tabela para CSV
st.markdown("### ExportaÃ§Ã£o de Dados")
if not st.session_state.mhd_data.empty:
    csv_data = st.session_state.mhd_data.to_csv(index=False)
    st.download_button(
        label="Baixar Tabela como CSV",
        data=csv_data,
        file_name="mhd_xadrez.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhum dado disponÃ­vel para exportaÃ§Ã£o.")

