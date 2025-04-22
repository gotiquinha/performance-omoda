import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Performance - Omoda",
    page_icon="🚗",
    layout="wide"
)

# Função para formatar valores monetários
def format_currency(value):
    if pd.isna(value):
        return "R$ 0,00"
    try:
        value = float(value)
        # Separa parte inteira e decimal
        integer_part = int(value)
        decimal_part = int(round((value - integer_part) * 100))
        
        # Formata parte inteira com pontos como separadores de milhar
        str_integer = str(integer_part)
        formatted_integer = ""
        for i in range(len(str_integer)-1, -1, -3):
            if i < 3:
                formatted_integer = str_integer[0:i+1] + formatted_integer
            else:
                formatted_integer = "." + str_integer[i-2:i+1] + formatted_integer
        
        # Remove ponto inicial se houver
        if formatted_integer.startswith("."):
            formatted_integer = formatted_integer[1:]
            
        return f"R$ {formatted_integer},{decimal_part:02d}"
    except:
        return "R$ 0,00"

# Função para formatar percentuais
def format_percentage(value):
    if pd.isna(value):
        return "0,00%"
    try:
        value = float(str(value).replace('%', '').replace(',', '.'))
        integer_part = int(value)
        decimal_part = int((value - integer_part) * 100)
        return f"{integer_part},{decimal_part:02d}%"
    except:
        return "0,00%"

# Função para formatar números decimais
def format_decimal(value):
    if pd.isna(value):
        return "0,00"
    try:
        value = float(value)
        # Separa parte inteira e decimal
        integer_part = int(value)
        decimal_part = int(round((value - integer_part) * 100))
        
        # Formata parte inteira com pontos como separadores de milhar
        str_integer = str(integer_part)
        formatted_integer = ""
        for i in range(len(str_integer)-1, -1, -3):
            if i < 3:
                formatted_integer = str_integer[0:i+1] + formatted_integer
            else:
                formatted_integer = "." + str_integer[i-2:i+1] + formatted_integer
        
        # Remove ponto inicial se houver
        if formatted_integer.startswith("."):
            formatted_integer = formatted_integer[1:]
            
        return f"{formatted_integer},{decimal_part:02d}"
    except:
        return "0,00"

# Função para formatar números inteiros
def format_integer(value):
    if pd.isna(value):
        return "0"
    try:
        # Remove caracteres especiais e converte para inteiro
        clean_value = str(value).replace('\xa0', '').replace(' ', '').replace('.', '')
        num = int(clean_value)
        
        # Formata com pontos como separadores de milhar
        str_num = str(num)
        formatted = ""
        for i in range(len(str_num)-1, -1, -3):
            if i < 3:
                formatted = str_num[0:i+1] + formatted
            else:
                formatted = "." + str_num[i-2:i+1] + formatted
        
        # Remove ponto inicial se houver
        if formatted.startswith("."):
            formatted = formatted[1:]
            
        return formatted
    except:
        return "0"

# Função para limpar strings numéricas
def clean_numeric_string(value):
    if pd.isna(value):
        return '0'
    # Remove R$, espaços, caracteres especiais e troca vírgula por ponto
    return str(value).replace('R$', '').replace('\xa0', '').replace(' ', '').replace('.', '').replace(',', '.')

# Função para carregar e processar os dados
@st.cache_data
def load_data():
    # Carregar dados do Google Ads
    ads_data = pd.read_csv('Relatório da campanha.csv', skiprows=2)
    
    # Carregar dados de leads
    leads_recreio = pd.read_csv('leads-omoda-recreio.csv', sep=';')
    leads_curitiba = pd.read_csv('leads-omoda-curitiba.csv', sep=';')
    
    # Adicionar coluna de origem
    leads_recreio['origem'] = 'Recreio'
    leads_curitiba['origem'] = 'Curitiba'
    
    # Combinar dados de leads
    leads_data = pd.concat([leads_recreio, leads_curitiba], ignore_index=True)
    
    # Converter data
    leads_data['criado_em'] = pd.to_datetime(leads_data['criado_em'], format='%d/%m/%Y %H:%M:%S')
    
    # Remover dados de teste
    leads_data = leads_data[~leads_data['nome_cliente'].str.contains('teste', case=False, na=False)]
    leads_data = leads_data[~leads_data['email_cliente'].str.contains('teste', case=False, na=False)]
    
    # Tratar dados do relatório
    ads_data['Custo'] = ads_data['Custo'].apply(clean_numeric_string).astype(float)
    ads_data['Custo/conv.'] = ads_data['Custo/conv.'].apply(clean_numeric_string).astype(float)
    ads_data['Conversões'] = ads_data['Conversões'].apply(clean_numeric_string).astype(float)
    
    # Remover linhas sem nome de campanha ou com 'Total'
    ads_data = ads_data[
        ads_data['Campanha'].notna() & 
        (ads_data['Campanha'] != 'None') & 
        ~ads_data['Campanha'].str.contains('Total', na=False)
    ]
    
    return ads_data, leads_data

# Carregar dados
ads_data, leads_data = load_data()

# Título do dashboard
st.title("📊 Dashboard de Performance - Omoda")

# Explicação do dashboard
st.markdown("""
Este dashboard apresenta as principais métricas de performance das campanhas de marketing digital da Omoda.
Os dados de campanhas são provenientes do Google Ads.
Utilize os filtros e gráficos interativos para analisar o desempenho das campanhas e tomar decisões baseadas em dados.
""")

# Métricas principais
st.subheader("📈 Métricas Principais")
st.markdown("""
Estas métricas representam o desempenho geral das campanhas:
- **Total de Leads**: Número total de contatos qualificados gerados através dos formulários
- **Total Gasto em Anúncios (Google)**: Investimento total em campanhas do Google Ads
- **CPL Médio (Google)**: Custo por Lead no Google Ads (investimento necessário para gerar cada lead)
""")

col1, col2, col3 = st.columns(3)

with col1:
    total_leads = len(leads_data)
    st.metric("Total de Leads Qualificados", 
             f"{total_leads:,}".replace(",", "."),
             help="Número total de leads que preencheram formulários nos sites da Omoda e Jaecoo")

with col2:
    total_gasto = ads_data['Custo'].sum()
    st.metric("Total Gasto em Anúncios (Google)", format_currency(total_gasto))

with col3:
    cpl_medio = total_gasto / total_leads if total_leads > 0 else 0
    st.metric("CPL Médio (Google)", format_currency(cpl_medio))

# Análise de Modelos por Região
st.subheader("🚗 Modelos Mais Procurados por Região")
st.markdown("""
Esta análise mostra a distribuição de interesse entre os modelos Omoda e Jaecoo em cada região:
""")

# Função para identificar o modelo específico
def get_modelo_from_versao(versao):
    if pd.isna(versao):
        return "Não especificado"
    versao = versao.lower()
    if 'omoda e5' in versao or 'omoda' in versao:
        return 'Omoda E5'
    elif 'jaecoo j7' in versao or 'jaecoo' in versao:
        return 'Jaecoo J7'
    return "Não especificado"

leads_data['modelo_principal'] = leads_data['versao'].apply(get_modelo_from_versao)

# Criar gráfico de modelos por região
modelos_regiao = leads_data.groupby(['origem', 'modelo_principal']).size().reset_index(name='quantidade')
modelos_regiao = modelos_regiao[modelos_regiao['modelo_principal'] != "Não especificado"]

fig_modelos = px.bar(
    modelos_regiao,
    x='origem',
    y='quantidade',
    color='modelo_principal',
    title='Interesse por Modelo em Cada Região',
    labels={
        'origem': 'Região',
        'quantidade': 'Número de Leads',
        'modelo_principal': 'Modelo do Veículo'
    },
    barmode='group',
    color_discrete_map={
        'Omoda E5': '#1f77b4',
        'Jaecoo J7': '#ff7f0e'
    }
)

fig_modelos.update_layout(
    xaxis_title="Região",
    yaxis_title="Número de Leads",
    legend_title="Modelo do Veículo"
)

st.plotly_chart(fig_modelos, use_container_width=True)

# Gráfico de leads por dia
st.subheader("📊 Evolução Diária de Leads")
st.markdown("""
Este gráfico mostra a evolução do número de leads ao longo do tempo, permitindo identificar:
- Tendências de crescimento ou queda
- Picos de performance
- Sazonalidade na geração de leads
""")

# Agrupar leads por dia
leads_por_dia = leads_data.groupby(leads_data['criado_em'].dt.date).size().reset_index(name='leads')

# Criar gráfico
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=leads_por_dia['criado_em'],
    y=leads_por_dia['leads'],
    name='Leads',
    line=dict(color='#1f77b4')
))

fig.update_layout(
    title='Evolução Diária de Leads',
    xaxis_title='Data',
    yaxis_title='Quantidade de Leads',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Ranking das campanhas
st.subheader("🏆 Ranking de Campanhas por Custo-Benefício")
st.markdown("""
Este ranking mostra o custo por conversão de cada campanha no Google Ads, permitindo identificar:
- Campanhas mais eficientes (menor custo por conversão)
- Oportunidades de otimização
- Distribuição do investimento entre campanhas do Google
""")

# Calcular métricas por campanha
campanhas_metrics = ads_data[ads_data['Campanha'].str.contains('Total', na=False) == False].copy()
campanhas_metrics['Custo/Conversão'] = campanhas_metrics['Custo/conv.']
campanhas_metrics = campanhas_metrics.sort_values('Custo/Conversão')

# Criar gráfico de barras
fig_campanhas = px.bar(
    campanhas_metrics,
    x='Campanha',
    y='Custo/Conversão',
    title='Custo por Conversão por Campanha (Google)',
    labels={'Custo/Conversão': 'Custo por Conversão (R$)', 'Campanha': 'Campanha do Google Ads'}
)

fig_campanhas.update_layout(
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(fig_campanhas, use_container_width=True)

# Tabela interativa
st.subheader("📋 Dados Detalhados por Campanha (Google)")
st.markdown("""
Esta tabela apresenta os dados detalhados das campanhas do Google Ads:
- **Impressões**: Número de vezes que o anúncio foi exibido no Google
- **Interações**: Número de cliques ou engajamentos com os anúncios
- **Taxa de interação**: Percentual de pessoas que interagiram com o anúncio
- **Custo**: Investimento total na campanha do Google Ads
- **Conversões**: Número de leads gerados através dos anúncios
- **Custo/conv.**: Custo por conversão (investimento por lead)

*Fonte: Relatório de Campanhas do Google Ads*
""")

# Filtros
col1, col2 = st.columns(2)

with col1:
    campanha_selecionada = st.selectbox(
        "Selecione a Campanha",
        ['Todas'] + list(ads_data['Campanha'].unique())
    )

with col2:
    data_inicio = st.date_input(
        "Data Inicial",
        value=leads_data['criado_em'].min().date()
    )
    data_fim = st.date_input(
        "Data Final",
        value=leads_data['criado_em'].max().date()
    )

# Filtrar dados
if campanha_selecionada != 'Todas':
    dados_filtrados = ads_data[ads_data['Campanha'] == campanha_selecionada]
else:
    dados_filtrados = ads_data

# Exibir tabela
dados_formatados = dados_filtrados.copy()
dados_formatados['Impressões'] = dados_formatados['Impressões'].apply(format_integer)
dados_formatados['Interações'] = dados_formatados['Interações'].apply(format_integer)
dados_formatados['Taxa de interação'] = dados_formatados['Taxa de interação'].apply(format_percentage)
dados_formatados['Custo'] = dados_formatados['Custo'].apply(format_currency)
dados_formatados['Conversões'] = dados_formatados['Conversões'].apply(format_decimal)
dados_formatados['Custo/conv.'] = dados_formatados['Custo/conv.'].apply(format_currency)

st.dataframe(
    dados_formatados[[
        'Campanha',
        'Impressões',
        'Interações',
        'Taxa de interação',
        'Custo',
        'Conversões',
        'Custo/conv.'
    ]],
    use_container_width=True
)

# Rodapé
st.markdown("---")
st.markdown("Dashboard desenvolvido para análise de performance de campanhas Omoda") 