# Caixa Fácil Vila Buriti — MVP

**Projeto de Extensão Universitária** — Centro Universitário Martha Falcão Wyden  
**Disciplina:** Tópicos de Big Data em Python | **Docente:** Prof. Ranyere Lima  
**Equipe:** Paulo Allan da Silva Alves, Andrew Willians Carvalho de Lima e Lucas Serrão dos Santos Sousa  

> **Aviso Metodológico & Ético:** Todos os dados pré-carregados nesta ferramenta são **100% fictícios e simulados** para fins didáticos de extensão comunitária, calibrados pelas referências públicas do IBGE (Pesquisa Mensal de Comércio — PMC) e do SEBRAE, não representando dados contábeis reais dos comerciantes da Vila Buriti.

---

## 🏛️ Visão Geral e Propósito

O **Caixa Fácil Vila Buriti** é uma aplicação web interativa desenvolvida em Python e Streamlit projetada para levar inteligência financeira e previsibilidade de caixa aos pequenos comerciantes locais (mercadinhos, lanchonetes e bazares). 

Combinando usabilidade visual ágil inspirada em **Nubank PJ**, **Mercado Pago**, **Conta Azul** e **Kyte**, o MVP traduz indicadores contábeis complexos em respostas claras: *Quanto sobrou de verdade? Meu pró-labore está coberto? Para onde foi cada R$ 100 faturado? Quanto devo guardar para o mês mais fraco do ano?*

---

## 🧩 Arquitetura Modular do Projeto

O sistema adota uma estrutura limpa e desacoplada em módulos especializados:

```text
Caixa Fácil MVP/
├── app.py                             # Ponto de entrada Streamlit e orquestração da interface
├── logic.py                           # Regras contábeis, métricas e motor de ML (10.950 registros)
├── styles.py                          # Camada visual (UI/UX), CSS responsivo, Hero Card e badges
├── .streamlit/
│   └── config.toml                    # Configuração de tema oficial (Superfície #F6F8FA, Ocre #D98218)
├── data/
│   └── modelo_caixa_vila_buriti.csv   # Base de exemplo pré-calibrada para download e upload
├── requirements.txt                   # Dependências do projeto (streamlit, pandas, scikit-learn, etc.)
└── README.md                          # Documentação completa e guia de execução
```

### Detalhamento dos Componentes:
- **`app.py`**: Gerencia o estado de sessão, as 4 abas de navegação (Visão Geral, Diagnóstico, Previsão Inteligente e Guia de Bolso), upload/download de dados CSV e controles interativos de simulação.
- **`logic.py`**: Centraliza os cálculos financeiros derivados (Margem Líquida, CMV%, Despesas Totais), simulações de cenários (reajuste de preços, corte de custos, meta de pró-labore) e o treinamento supervisionado dos modelos de Big Data (**Regressão Linear** e **Random Forest** treinados com 10.950 dias simulados para generalização por perfil de negócio).
- **`styles.py`**: Garante a identidade visual do projeto (**Ardósia `#1E293B` + Ocre `#D98218`**) com superfícies limpas (`#F6F8FA`), cards com raio de 14px, estilização customizada de gráficos Matplotlib, equações financeiras em 3 partes, barra de decomposição de R$ 100 e badges semânticos (`● Saudável`, `● Atenção`, `● Alerta`).
- **`.streamlit/config.toml`**: Aplica o tema visual nativo consistente com a marca em todos os elementos Streamlit.
- **`data/modelo_caixa_vila_buriti.csv`**: Planilha padronizada de 12 meses para testes rápidos de importação.

---

## ✨ Destaques de UI/UX e Usabilidade

1. **Hero Card Consolidado (Estilo Nubank PJ / Mercado Pago)**:
   - Apresenta o **Lucro Real Livre Acumulado** em tipografia ampla com pílula de margem consolidada.
   - Equação financeira transparente: `Entrou (Vendas)` − `Saiu (Mercadorias + Fixas)` = `Sobrou Livre/Mês` comparado diretamente com o **Pró-Labore Desejado**.
   - Barra horizontal segmentada: *"Para onde foi cada R$ 100 que entrou no caixa?"* dividindo visualmente Mercadorias, Contas Fixas e Sobra Líquida.

2. **Diagnóstico Semafórico (Estilo Conta Azul / Kyte)**:
   - Cards com borda semântica colorida e pílulas de status (`● Saudável`, `● Atenção`, `● Alerta`).
   - Métricas comparadas com referências oficiais do SEBRAE e seção direta **"O que fazer:"** com recomendações práticas em 1 frase.

3. **Simulador de Proteção contra o Vale Sazonal**:
   - Calcula o déficit financeiro no mês de menor movimento e avalia se a reserva preventiva acumulada (poupança programada nos meses de pico de Junho, Novembro e Dezembro) é suficiente para cobrir o sustento da família sem recorrer a empréstimos bancários.

4. **100% Responsivo e Mobile-Friendly**:
   - Layout otimizado com regras CSS `@media (max-width: 768px)` para operar perfeitamente na tela de smartphones e tablets no balcão do comércio.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.10 ou superior instalado.

### Passo a Passo

```powershell
# 1. Criar ambiente virtual
python -m venv .venv

# 2. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar a aplicação
streamlit run app.py
```

Acesse no navegador: `http://localhost:8501`

---

## ☁️ Como Publicar no Streamlit Community Cloud

1. Crie um repositório público no GitHub (ex.: `caixa-facil-vila-buriti`) e envie todos os arquivos do projeto (`app.py`, `logic.py`, `styles.py`, `requirements.txt`, `.streamlit/config.toml`, `data/`).
2. Acesse [share.streamlit.io](https://share.streamlit.io), faça login com sua conta GitHub e clique em **Create app**.
3. Selecione o repositório, branch `main` e defina `app.py` como arquivo principal (*Main file path*).
4. Clique em **Deploy!**. Após a inicialização, utilize o link público gerado (ex.: `https://caixa-facil-vila-buriti.streamlit.app`) para gerar o QR Code da apresentação acadêmica.
