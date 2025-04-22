# Dashboard de Performance - Omoda

Este dashboard foi desenvolvido para análise de performance de campanhas de marketing digital da Omoda, utilizando dados reais de leads e relatórios do Google Ads.

## Funcionalidades

- Visão geral com métricas principais (total de leads, gasto em anúncios, CPL médio)
- Gráfico de evolução diária de leads
- Ranking de campanhas por custo-benefício
- Tabela interativa com filtros por campanha e período

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone este repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Certifique-se de que os arquivos CSV estão na mesma pasta do script:
   - `Relatório da campanha.csv`
   - `leads-omoda-recreio.csv`

2. Execute o dashboard:
```bash
streamlit run app.py
```

3. O dashboard será aberto automaticamente no seu navegador padrão.

## Estrutura dos Dados

### Relatório da campanha.csv
Contém dados de performance das campanhas do Google Ads, incluindo:
- Nome da campanha
- Impressões
- Interações
- Taxa de interação
- Custo
- Conversões
- Custo por conversão

### leads-omoda-recreio.csv
Contém dados de leads gerados, incluindo:
- Data de criação
- Informações do cliente
- Origem do lead
- Tipo de lead

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request 