import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="HBH Motor Tático - Análise de Jogos", layout="centered"
)

st.title("🎯 HBH Consultoria - Motor Tático de Decisão")
st.write(
    "Insira os dados essenciais da partida para validar a entrada nos mercados"
    " de Gols e Lay Correct Score."
)

# Formulário de Entrada Rápida
with st.form(key="formulario_partida"):
  st.subheader("📋 Dados da Partida")

  col1, col2 = st.columns(2)
  with col1:
    time_mandante = st.text_input("Time Mandante", "Mirassol")
    pos_mandante = st.number_input(
        "Posição do Mandante na Tabela", min_value=1, max_value=20, value=14
    )
    falha_def_mandante = st.number_input(
        "Jogos sem sofrer gols (Mandante em Casa %)",
        min_value=0,
        max_value=100,
        value=13,
    )

  with col2:
    time_visitante = st.text_input("Time Visitante", "Internacional")
    pos_visitante = st.number_input(
        "Posição do Visitante (Ex: Z4 >= 16)",
        min_value=1,
        max_value=20,
        value=16,
    )
    falha_def_visitante = st.number_input(
        "Jogos sem sofrer gols (Visitante Fora %)",
        min_value=0,
        max_value=100,
        value=13,
    )

  st.subheader("⚡ Padrões Táticos e Timing")
  falha_ataque_visitante = st.number_input(
      "Jogos sem marcar (Visitante Fora %)", min_value=0, max_value=100, value=33
  )
  eficiencia_16_mais = st.checkbox(
      "Mandante aumenta eficiência de gols a partir dos 16' do 1T?", value=True
  )

  # Botão de Execução
  botao_analisar = st.form_submit_button(
      label="🚀 Analisar Jogo e Dar Veredito"
  )

# Lógica do Motor de Decisão após o clique
if botao_analisar:
  st.divider()
  st.subheader(f"📊 Relatório de Veredito: {time_mandante} vs {time_visitante}")

  # 1. Checagem de Fator Motivacional (Z4)
  pressao_z4 = pos_visitante >= 16
  vantagem_mandante = pos_mandante < pos_visitante

  if pressao_z4 and vantagem_mandante:
    st.success(
        f"✅ **Fator Tático Ativado:** O visitante ({time_visitante}) está no"
        f" Z4 ({pos_visitante}º) e tem a obrigação de propor o jogo. O"
        f" mandante ({time_mandante}) tem o cenário ideal para bloco baixo e"
        " transição."
    )
  else:
    st.warning(
        "⚠️ **Cenário Neutro:** A tabela não indica urgência crítica do Z4 ou"
        " posições invertidas. Peso anímico reduzido."
    )

  # 2. Avaliação dos Mercados
  st.markdown("### 🎯 Veredito para os Mercados")

  # Regra Over Gols
  over_15_aprovado = falha_def_mandante <= 25 and falha_def_visitante <= 25
  over_25_aprovado = (
      over_15_aprovado and eficiencia_16_mais and pressao_z4
  )

  if over_15_aprovado:
    st.markdown(
        "✅ **Over 1.5 Gols:** **APROVADO** (Alta propensão de quebra de"
        " linhas defensivas mútua)."
    )
  else:
    st.markdown(
        "❌ **Over 1.5 Gols:** **REPROVADO** (Defesas sólidas nos contextos"
        " analíticos)."
    )

  if over_25_aprovado:
    st.markdown(
        "✅ **Over 2.5 Gols:** **APROVADO** (Exposição do visitante + conversão"
        " cronometrada do mandante)."
    )
  else:
    st.markdown(
        "⚠️ **Over 2.5 Gols:** **CAUTELA / CONDICIONAL** (Faltam gatilhos"
        " plenos de explosão de gols)."
    )

  # Regra Lay Correct Score
  if pressao_z4 and eficiencia_16_mais and falha_ataque_visitante >= 30:
    st.markdown(
        "✅ **Lay Correct Score (1x0 / 0x1):** **APROVADO!** O padrão aponta"
        " para alta volatilidade e grande probabilidade de alteração rápida do"
        " placar inicial devido à exposição do visitante."
    )
  else:
    st.markdown(
        "❌ **Lay Correct Score (1x0 / 0x1):** **REPROVADO** (Sem gatilho"
        " seguro de desestabilização precoce)."
    )
