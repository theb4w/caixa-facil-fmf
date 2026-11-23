# -*- coding: utf-8 -*-
"""
Caixa Fácil Vila Buriti — Gestão Financeira e Previsão Acessível.
Centro Universitário Martha Falcão Wyden | Tópicos de Big Data em Python
Docente: Prof. Ranyere Lima
Equipe: Paulo Allan da Silva Alves, Andrew Willians Carvalho de Lima e Lucas Serrão dos Santos Sousa
"""

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from logic import (
    PERFIS_CONFIG,
    calcular_indicadores_mensais,
    calcular_projecao_linear,
    carregar_base_mensal_padrao,
    converter_venda_diaria_para_porte,
    diagnosticar_sebrae,
    formatar_brl,
    treinar_motor_big_data,
)
from styles import (
    configurar_matplotlib,
    injetar_estilos,
    render_alerta_reserva,
    render_cabecalho,
    render_card_guia,
    render_hero_card,
    render_semaforo_card,
)

# ------------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Caixa Fácil Vila Buriti — Gestão Financeira",
    page_icon=":material/storefront:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

configurar_matplotlib()
injetar_estilos()
render_cabecalho()

# ------------------------------------------------------------------------------
# 2. ESTADO DA SESSÃO
# ------------------------------------------------------------------------------
COLUNAS_BASE = ["Meses", "Receita_Bruta", "Custo_Mercadorias", "Despesas_Fixas", "Qtd_Vendas"]

if "df_base_editavel" not in st.session_state:
    st.session_state["df_base_editavel"] = carregar_base_mensal_padrao()[COLUNAS_BASE].copy()

if "lancamentos_dia" not in st.session_state:
    st.session_state["lancamentos_dia"] = []

if "avaliacoes_reacao" not in st.session_state:
    st.session_state["avaliacoes_reacao"] = []

# ------------------------------------------------------------------------------
# 3. BARRA LATERAL (IMPORTAÇÃO E EXPORTAÇÃO DE PLANILHAS)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("#### :material/table_view: Planilhas (.csv)")
    st.caption("Importe seus números mensais ou salve uma cópia atualizada no celular ou computador.")

    arquivo_csv = st.file_uploader(
        "Importar planilha mensal (.csv)",
        type=["csv"],
        help="Colunas esperadas: Meses, Receita_Bruta, Custo_Mercadorias, Despesas_Fixas, Qtd_Vendas",
    )

    if arquivo_csv is not None:
        try:
            df_lido = pd.read_csv(arquivo_csv)
            if set(COLUNAS_BASE).issubset(set(df_lido.columns)):
                st.session_state["df_base_editavel"] = df_lido[COLUNAS_BASE].copy()
                st.success("Planilha carregada com sucesso.")
            else:
                st.error("O arquivo deve conter as colunas: Meses, Receita_Bruta, Custo_Mercadorias, Despesas_Fixas e Qtd_Vendas.")
        except Exception as exc:
            st.error(f"Não foi possível ler o CSV: {exc}")

    st.divider()

    csv_modelo = carregar_base_mensal_padrao()[COLUNAS_BASE].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar planilha modelo (.csv)",
        icon=":material/download:",
        data=csv_modelo,
        file_name="modelo_caixa_vila_buriti.csv",
        mime="text/csv",
        width="stretch",
    )

    csv_atual = st.session_state["df_base_editavel"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar meus dados atuais (.csv)",
        icon=":material/save:",
        data=csv_atual,
        file_name="meu_caixa_vila_buriti.csv",
        mime="text/csv",
        width="stretch",
    )

    st.divider()
    st.caption(
        "Privacidade local: os números preenchidos ficam apenas na sua sessão atual e não são "
        "enviados para bancos de dados externos."
    )

# ------------------------------------------------------------------------------
# 4. PARÂMETROS RÁPIDOS DO COMÉRCIO (VISÍVEIS NO CELULAR E NO COMPUTADOR)
# ------------------------------------------------------------------------------
with st.container(border=True):
    c_cfg1, c_cfg2, c_cfg3 = st.columns([1.0, 1.15, 1.15])
    with c_cfg1:
        perfil_negocio = st.selectbox(
            "Perfil do comércio",
            options=["Misto", "Mercadinho", "Lanchonete"],
            index=0,
            help="Define as faixas de referência do SEBRAE para compras de mercadoria e margem.",
        )
    with c_cfg2:
        pro_labore_mensal = st.number_input(
            "Pró-labore mensal fixo (R$)",
            min_value=0.0,
            max_value=25000.0,
            value=2200.0,
            step=100.0,
            help="Retirada fixa mensal para despesas pessoais da família (separação PF/PJ).",
        )
    with c_cfg3:
        pct_reserva_pico = st.slider(
            "Meta de reserva nos meses fortes (%)",
            min_value=5,
            max_value=40,
            value=20,
            step=5,
            help="Percentual do lucro de junho, novembro e dezembro guardado para atravessar fevereiro.",
        )

# ------------------------------------------------------------------------------
# 5. MOTOR DE MACHINE LEARNING (10.950 REGISTROS — CACHEADO)
# ------------------------------------------------------------------------------
df_grande, lr_multi, rf_model, metricas_ml, perfis_cfg = treinar_motor_big_data()

# ------------------------------------------------------------------------------
# 6. NAVEGAÇÃO PRINCIPAL (4 ABAS COM ÍCONES MATERIAL)
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/account_balance_wallet: Meu Caixa",
    ":material/calendar_month: Sazonalidade e Reserva",
    ":material/trending_up: Previsão de Vendas",
    ":material/menu_book: Guia Prático",
])

# ==============================================================================
# ABA 1: MEU CAIXA, DIAGNÓSTICO SEBRAE E FECHAMENTO DO DIA
# ==============================================================================
with tab1:
    df_calc = calcular_indicadores_mensais(st.session_state["df_base_editavel"])

    receita_anual = float(df_calc["Receita_Bruta"].sum())
    cmv_anual = float(df_calc["Custo_Mercadorias"].sum())
    fixas_anual = float(df_calc["Despesas_Fixas"].sum())
    saldo_anual = float(df_calc["Saldo_Liquido"].sum())
    margem_ponderada = (saldo_anual / receita_anual * 100.0) if receita_anual > 0 else 0.0
    cmv_pct_anual = (cmv_anual / receita_anual * 100.0) if receita_anual > 0 else 0.0
    saldo_medio_mensal = float(df_calc["Saldo_Liquido"].mean())

    render_hero_card(
        receita_anual=receita_anual,
        cmv_anual=cmv_anual,
        fixas_anual=fixas_anual,
        saldo_anual=saldo_anual,
        margem_pct=margem_ponderada,
        pro_labore_mensal=pro_labore_mensal,
        saldo_medio_mensal=saldo_medio_mensal,
        formatar_brl=formatar_brl,
    )

    diag = diagnosticar_sebrae(
        cmv_pct=cmv_pct_anual,
        margem_pct=margem_ponderada,
        saldo_medio=saldo_medio_mensal,
        pro_labore=pro_labore_mensal,
        perfil=perfil_negocio,
    )

    c_d1, c_d2 = st.columns(2)
    with c_d1:
        render_semaforo_card(
            titulo="Custo de Mercadorias (CMV)",
            valor_destaque=f"{cmv_pct_anual:.1f}% das vendas",
            referencia=diag["cmv"]["referencia"],
            status=diag["cmv"]["status"],
            badge_texto=diag["cmv"]["badge"],
            recomendacao=diag["cmv"]["recomendacao"],
        )
    with c_d2:
        render_semaforo_card(
            titulo="Separação PF/PJ e Margem Líquida",
            valor_destaque=f"{margem_ponderada:.1f}% de margem real",
            referencia=diag["pf_pj"]["referencia"],
            status=diag["pf_pj"]["status"],
            badge_texto=diag["pf_pj"]["badge"],
            recomendacao=diag["pf_pj"]["recomendacao"],
        )

    # Fechamento diário de balcão (4 colunas)
    with st.container(border=True):
        st.markdown("#### :material/point_of_sale: Fechamento Rápido do Dia")
        st.caption(
            "Anote ao encerrar o expediente os 4 números essenciais do balcão para saber quanto "
            "sobrou livre hoje e somar ao mês correspondente."
        )

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            venda_dia = st.number_input("Total vendido hoje (R$)", min_value=0.0, value=580.0, step=10.0, format="%.2f")
        with f2:
            qtd_dia = st.number_input("Qtd. de vendas", min_value=1, value=20, step=1)
        with f3:
            cmv_dia = st.number_input("Compras de mercadoria (R$)", min_value=0.0, value=320.0, step=10.0, format="%.2f")
        with f4:
            fixa_dia = st.number_input("Contas fixas pagas (R$)", min_value=0.0, value=140.0, step=10.0, format="%.2f")

        lucro_hoje = venda_dia - (cmv_dia + fixa_dia)
        ticket_hoje = venda_dia / qtd_dia if qtd_dia > 0 else 0.0

        a1, a2, a3 = st.columns([2.2, 1.1, 1.3])
        with a1:
            if lucro_hoje >= 0:
                st.success(f"Resultado do dia: sobrou **{formatar_brl(lucro_hoje)}** livre (ticket médio: {formatar_brl(ticket_hoje)}).")
            else:
                st.error(f"Resultado do dia: saldo negativo de **{formatar_brl(lucro_hoje)}** (saídas maiores que as vendas).")
        with a2:
            meses_lista = list(st.session_state["df_base_editavel"]["Meses"].astype(str))
            mes_destino = st.selectbox("Somar ao mês", options=meses_lista, index=0, label_visibility="collapsed")
        with a3:
            if st.button("Somar no mês", icon=":material/add_circle:", width="stretch", type="primary"):
                df_tmp = st.session_state["df_base_editavel"].copy()
                mask = df_tmp["Meses"].astype(str) == mes_destino
                if mask.any():
                    idx = df_tmp.index[mask][0]
                    df_tmp.at[idx, "Receita_Bruta"] = float(df_tmp.at[idx, "Receita_Bruta"]) + venda_dia
                    df_tmp.at[idx, "Custo_Mercadorias"] = float(df_tmp.at[idx, "Custo_Mercadorias"]) + cmv_dia
                    df_tmp.at[idx, "Despesas_Fixas"] = float(df_tmp.at[idx, "Despesas_Fixas"]) + fixa_dia
                    df_tmp.at[idx, "Qtd_Vendas"] = int(df_tmp.at[idx, "Qtd_Vendas"]) + int(qtd_dia)
                    st.session_state["df_base_editavel"] = df_tmp
                    st.session_state["lancamentos_dia"].append({
                        "Horario": datetime.now().strftime("%H:%M"),
                        "Mes": mes_destino,
                        "Vendas": venda_dia,
                        "Mercadorias": cmv_dia,
                        "Fixas": fixa_dia,
                        "Lucro": lucro_hoje,
                    })
                    st.rerun()

        if st.session_state["lancamentos_dia"]:
            with st.expander(f"Lançamentos adicionados hoje ({len(st.session_state['lancamentos_dia'])})"):
                df_hist = pd.DataFrame(st.session_state["lancamentos_dia"])
                st.dataframe(
                    df_hist.style.format({
                        "Vendas": formatar_brl,
                        "Mercadorias": formatar_brl,
                        "Fixas": formatar_brl,
                        "Lucro": formatar_brl,
                    }),
                    width="stretch",
                    hide_index=True,
                )

    # Tabela mensal editável
    t_head1, t_head2, t_head3 = st.columns([2.6, 1.2, 1.2])
    with t_head1:
        st.markdown("#### :material/edit_calendar: Planilha Mensal do Comércio")
        st.caption("Clique em qualquer célula para editar os valores reais do seu negócio.")
    with t_head2:
        if st.button("Restaurar simulado", icon=":material/refresh:", width="stretch"):
            st.session_state["df_base_editavel"] = carregar_base_mensal_padrao()[COLUNAS_BASE].copy()
            st.session_state["lancamentos_dia"] = []
            st.rerun()
    with t_head3:
        csv_export = st.session_state["df_base_editavel"].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar meus dados",
            icon=":material/download:",
            data=csv_export,
            file_name="meu_caixa_vila_buriti.csv",
            mime="text/csv",
            width="stretch",
        )

    df_editado = st.data_editor(
        st.session_state["df_base_editavel"],
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Meses": st.column_config.TextColumn("Mês"),
            "Receita_Bruta": st.column_config.NumberColumn("Vendas (R$)", format="R$ %.2f", min_value=0.0),
            "Custo_Mercadorias": st.column_config.NumberColumn("Mercadorias / CMV (R$)", format="R$ %.2f", min_value=0.0),
            "Despesas_Fixas": st.column_config.NumberColumn("Contas fixas (R$)", format="R$ %.2f", min_value=0.0),
            "Qtd_Vendas": st.column_config.NumberColumn("Qtd. vendas", format="%d", min_value=1),
        },
    )

    if not df_editado.equals(st.session_state["df_base_editavel"]):
        st.session_state["df_base_editavel"] = df_editado.copy()
        st.rerun()

    with st.expander("Ver demonstrativo contábil completo", icon=":material/receipt_long:"):
        st.dataframe(
            df_calc.style.format({
                "Receita_Bruta": formatar_brl,
                "Custo_Mercadorias": formatar_brl,
                "Despesas_Fixas": formatar_brl,
                "Despesas_Totais": formatar_brl,
                "Saldo_Liquido": formatar_brl,
                "CMV_%": "{:.2f}%".format,
                "Margem_Liquida_%": "{:.2f}%".format,
                "Ticket_Medio": formatar_brl,
            }),
            width="stretch",
            hide_index=True,
        )

# ==============================================================================
# ABA 2: SAZONALIDADE E RESERVA (IBGE / PMC)
# ==============================================================================
with tab2:
    df_calc = calcular_indicadores_mensais(st.session_state["df_base_editavel"])

    idx_min = df_calc["Saldo_Liquido"].idxmin()
    idx_max = df_calc["Saldo_Liquido"].idxmax()
    mes_vale = str(df_calc.loc[idx_min, "Meses"])
    saldo_vale = float(df_calc.loc[idx_min, "Saldo_Liquido"])
    mes_pico = str(df_calc.loc[idx_max, "Meses"])
    saldo_pico = float(df_calc.loc[idx_max, "Saldo_Liquido"])

    saldos_fortes = df_calc[df_calc["Meses"].isin(["Jun", "Nov", "Dez"])]["Saldo_Liquido"].sum()
    reserva_estimada = float(max(0.0, saldos_fortes) * (pct_reserva_pico / 100.0))

    m1, m2, m3 = st.columns(3)
    m1.metric(f"Mês mais fraco ({mes_vale})", formatar_brl(saldo_vale), "Retração típica de início de ano")
    m2.metric(f"Mês mais forte ({mes_pico})", formatar_brl(saldo_pico), "Pico de fim de ano e 13º salário")
    m3.metric(
        f"Reserva formada ({pct_reserva_pico}% de Jun/Nov/Dez)",
        formatar_brl(reserva_estimada),
        "Fundo próprio sem empréstimo",
    )

    render_alerta_reserva(
        mes_vale=mes_vale,
        saldo_vale=saldo_vale,
        pro_labore=pro_labore_mensal,
        reserva_estimada=reserva_estimada,
        pct_reserva=pct_reserva_pico,
        formatar_brl=formatar_brl,
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 7.2), gridspec_kw={"hspace": 0.44})
    x_pos = np.arange(len(df_calc["Meses"]))
    larg = 0.36

    b_rec = ax1.bar(x_pos - larg / 2, df_calc["Receita_Bruta"], width=larg, color="#1F2937", label="Vendas brutas (R$)")
    b_desp = ax1.bar(x_pos + larg / 2, df_calc["Despesas_Totais"], width=larg, color="#9CA3AF", label="Saídas totais (R$)")
    ax1.set_title("Vendas Brutas vs. Saídas Totais por Mês", fontweight="bold", loc="left", pad=10)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(df_calc["Meses"])
    ax1.set_ylabel("Valor (R$)")
    ax1.set_ylim(0, max(1.0, float(df_calc["Receita_Bruta"].max())) * 1.18)
    ax1.legend(loc="upper left", frameon=False, ncol=2)

    for barra in b_rec:
        h = barra.get_height()
        ax1.annotate(f"{h/1000:.1f}k", (barra.get_x() + barra.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                     fontsize=7.8, color="#1F2937", fontweight="600")
    for barra in b_desp:
        h = barra.get_height()
        ax1.annotate(f"{h/1000:.1f}k", (barra.get_x() + barra.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                     fontsize=7.8, color="#6B7280")

    ax2.plot(x_pos, df_calc["Saldo_Liquido"], marker="o", linewidth=2.2, markersize=5.5,
             color="#B45309", label="Lucro líquido mensal")
    ax2.axhline(pro_labore_mensal, color="#374151", linestyle="--", linewidth=1.2,
                label=f"Pró-labore fixo ({formatar_brl(pro_labore_mensal)})")

    pos_min = list(df_calc.index).index(idx_min)
    pos_max = list(df_calc.index).index(idx_max)
    ax2.scatter([pos_min], [saldo_vale], color="#991B1B", s=85, zorder=5, label=f"Vale ({mes_vale})")
    ax2.scatter([pos_max], [saldo_pico], color="#166534", s=85, zorder=5, label=f"Pico ({mes_pico})")

    for i, val in enumerate(df_calc["Saldo_Liquido"]):
        offset_y = -15 if i == pos_min else 9
        cor = "#991B1B" if i == pos_min else ("#166534" if i == pos_max else "#374151")
        ax2.annotate(formatar_brl(float(val)), (i, float(val)), xytext=(0, offset_y),
                     textcoords="offset points", ha="center", va="center",
                     fontsize=7.8, fontweight="600", color=cor)

    ax2.set_title("Evolução do Lucro Líquido vs. Meta de Pró-Labore", fontweight="bold", loc="left", pad=10)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(df_calc["Meses"])
    ax2.set_ylabel("Lucro (R$)")
    y_min = min(float(df_calc["Saldo_Liquido"].min()), pro_labore_mensal)
    y_max = max(float(df_calc["Saldo_Liquido"].max()), pro_labore_mensal)
    ax2.set_ylim(y_min * 0.72, y_max * 1.18)
    ax2.legend(loc="upper left", frameon=False, ncol=4)

    st.pyplot(fig)
    plt.close(fig)

    if len(df_calc) >= 3:
        with st.expander("Ver projeção linear introdutória (visão acadêmica)", icon=":material/science:"):
            df_proj, inc_simples, r2_simples = calcular_projecao_linear(df_calc)
            st.caption(
                f"Tendência linear média: +{formatar_brl(inc_simples)}/mês (R² = {r2_simples:.4f}). "
                "Como ajusta uma reta contínua, a Regressão Linear Simples não desconta sozinha "
                "a retração sazonal de janeiro e fevereiro — por isso utilizamos o Random Forest na aba seguinte."
            )
            st.dataframe(
                df_proj.style.format({"Receita_Linear_Projetada": formatar_brl}),
                width="stretch",
                hide_index=True,
            )

# ==============================================================================
# ABA 3: PREVISÃO DE VENDAS DIÁRIAS (RANDOM FOREST)
# ==============================================================================
with tab3:
    st.markdown("#### :material/insights: Planejamento de Estoque e Previsão de Movimento")
    st.caption(
        "Informe o perfil do seu comércio, o dia que deseja planejar e quanto você costuma vender "
        "num dia normal para estimar o movimento esperado e o limite seguro de compras."
    )

    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
    }
    nomes_dias = {
        0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
        3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo",
    }

    with st.container(border=True):
        s1, s2, s3 = st.columns(3)
        with s1:
            perfil_sim = st.selectbox("Perfil do comércio", ["Mercadinho", "Lanchonete", "Misto"], index=2, key="sim_perfil")
        with s2:
            mes_sim = st.selectbox("Mês", list(nomes_meses.keys()), format_func=lambda m: nomes_meses[m], index=11)
        with s3:
            dia_sim = st.selectbox("Dia da semana", list(nomes_dias.keys()), format_func=lambda d: nomes_dias[d], index=4)

        s4, s5 = st.columns(2)
        with s4:
            pag_sim = st.selectbox(
                "Semana de pagamento (Distrito Industrial I)",
                options=[1, 0],
                format_func=lambda v: "Sim — dias 1 a 10 ou 15 a 22" if v == 1 else "Não — demais dias do mês",
                index=0,
            )
        with s5:
            base_perfil = float(PERFIS_CONFIG[perfil_sim]["receita_dia_base"])
            venda_normal_dia = st.number_input(
                "Quanto você vende num dia normal? (R$)",
                min_value=150.0,
                max_value=2500.0,
                value=base_perfil,
                step=20.0,
                format="%.2f",
            )

    porte_sim, fora_faixa = converter_venda_diaria_para_porte(venda_normal_dia, perfil_sim)
    if fora_faixa:
        st.caption(
            f"Nota: a venda informada foi ajustada para a faixa calibrada do modelo ({porte_sim:.2f}x a base do perfil {perfil_sim})."
        )

    entrada = pd.DataFrame([{
        "Mes_Num": mes_sim,
        "Dia_Semana": dia_sim,
        "Semana_Pagamento": pag_sim,
        "Fator_Porte": porte_sim,
        "Perfil_Mercadinho": 1 if perfil_sim == "Mercadinho" else 0,
        "Perfil_Misto": 1 if perfil_sim == "Misto" else 0,
    }])

    pred_rf = float(rf_model.predict(entrada)[0])
    pred_lr = float(lr_multi.predict(entrada)[0])

    cfg = perfis_cfg[perfil_sim]
    teto_cmv = pred_rf * cfg["cmv_medio"]
    fixo_dia_est = cfg["fixo_dia"] * porte_sim
    lucro_dia_est = pred_rf - (teto_cmv + fixo_dia_est)

    p1, p2, p3 = st.columns(3)
    p1.metric("Previsão de vendas no dia", formatar_brl(pred_rf), f"{nomes_dias[dia_sim]} em {nomes_meses[mes_sim]}")
    p2.metric(f"Limite seguro de compras ({cfg['cmv_medio']*100:.0f}%)", formatar_brl(teto_cmv), "Teto recomendado para estoque")
    p3.metric("Lucro estimado no dia", formatar_brl(lucro_dia_est), f"Após custo fixo médio ({formatar_brl(fixo_dia_est)})")

    st.markdown("##### Movimento médio por dia da semana (base calibrada de 10.950 registros)")
    fig_sem, ax_s = plt.subplots(figsize=(10.5, 3.8))
    ordem_dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    tab_sem = df_grande.groupby(["Dia_Semana", "Perfil"])["Receita_Bruta"].mean().unstack()
    tab_sem.index = ordem_dias
    cores = {"Mercadinho": "#1F2937", "Misto": "#B45309", "Lanchonete": "#6B7280"}
    for col_nome in tab_sem.columns:
        ax_s.plot(tab_sem.index, tab_sem[col_nome], marker="o", linewidth=2.0, markersize=5,
                  label=col_nome, color=cores[col_nome])
    ax_s.set_ylabel("Venda média diária (R$)")
    ax_s.legend(title="Perfil", frameon=False, ncol=3, loc="upper left")
    st.pyplot(fig_sem)
    plt.close(fig_sem)

    with st.expander("Auditoria científica dos modelos (banca · 10.950 registros)", icon=":material/science:"):
        st.caption(
            f"Comparativo da simulação atual — Random Forest: {formatar_brl(pred_rf)} vs. "
            f"Regressão Linear Múltipla: {formatar_brl(pred_lr)} (diferença: {formatar_brl(pred_rf - pred_lr)})."
        )
        st.dataframe(
            metricas_ml.style.format({"MAE": formatar_brl, "RMSE": formatar_brl, "R2": "{:.4f}"}),
            width="stretch",
            hide_index=True,
        )
        st.caption(
            "Validação estratificada 80%/20% (2.190 registros de teste): o Random Forest reduz o "
            "Erro Médio Absoluto (MAE) em 30,4% (de R$ 62,51 para R$ 43,51) e eleva o R² para 0,8570 "
            "ao capturar interações não lineares entre sazonalidade IBGE, sextas/sábados e janelas salariais."
        )

# ==============================================================================
# ABA 4: GUIA PRÁTICO E AVALIAÇÃO DE REAÇÃO
# ==============================================================================
with tab4:
    st.markdown("#### :material/checklist: Trilha Prática de Gestão a Custo Zero")
    st.caption("Três hábitos simples para organizar o caixa do comércio sem depender de softwares pagos.")

    g1, g2, g3 = st.columns(3)
    with g1:
        render_card_guia(
            numero="01",
            titulo="Separação PF/PJ e Pró-Labore",
            texto=(
                "Defina uma retirada fixa mensal ou quinzenal para a família e evite retirar dinheiro "
                "avulso da gaveta. Segundo o SEBRAE, cerca de 60% dos pequenos negócios misturam "
                "contas pessoais e empresariais."
            ),
        )
    with g2:
        render_card_guia(
            numero="02",
            titulo="Anotação Diária em 4 Colunas",
            texto=(
                "No fim do expediente, registre em caderno ou na aba Meu Caixa apenas quatro números: "
                "total vendido, quantidade de vendas, compras de mercadoria e contas fixas pagas."
            ),
        )
    with g3:
        render_card_guia(
            numero="03",
            titulo="Reserva Sazonal Programada",
            texto=(
                "Guarde entre 15% e 20% do lucro líquido nos meses fortes (junho e dezembro) em conta "
                "separada para atravessar a queda de vendas de janeiro e fevereiro sem empréstimos."
            ),
        )

    st.divider()

    with st.container(border=True):
        st.markdown("#### :material/rate_review: Avaliação de Reação (Oficina Comunitária)")
        st.caption(
            "Instrumento anônimo da Seção 3.1.1 do relatório de extensão para coletar a percepção "
            "dos comerciantes após a demonstração (escala de 1 = Discordo totalmente a 5 = Concordo totalmente)."
        )

        with st.form("form_avaliacao_reacao", clear_on_submit=True):
            q1 = st.slider("1. Os gráficos ajudaram a enxergar a diferença entre dinheiro bruto e lucro real?", 1, 5, 5)
            q2 = st.slider("2. A explicação sobre a queda em fevereiro e o pico em dezembro reflete sua rotina?", 1, 5, 5)
            q3 = st.slider("3. O modelo de anotação diária em 4 colunas é viável na correria do balcão?", 1, 5, 4)
            q4 = st.slider("4. Separar um pró-labore fixo e guardar reserva ajuda a organizar as contas?", 1, 5, 5)
            q5 = st.text_area(
                "5. Que outra dificuldade do dia a dia você gostaria que esta ferramenta ajudasse a controlar?",
                placeholder="Ex.: controle de fiado, vencimento de produtos, separar Pix pessoal do Pix da loja...",
            )
            enviado = st.form_submit_button("Registrar resposta", icon=":material/send:", type="primary")

        if enviado:
            st.session_state["avaliacoes_reacao"].append({
                "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Q1_Clareza_Lucro": q1,
                "Q2_Aderencia_Sazonal": q2,
                "Q3_Viabilidade_4_Colunas": q3,
                "Q4_Impacto_PF_PJ": q4,
                "Q5_Sugestao_Aberta": q5.strip(),
            })
            st.success("Avaliação registrada na sessão.")

        if st.session_state["avaliacoes_reacao"]:
            df_aval = pd.DataFrame(st.session_state["avaliacoes_reacao"])
            st.download_button(
                label=f"Exportar avaliações coletadas ({len(df_aval)}) (.csv)",
                icon=":material/download:",
                data=df_aval.to_csv(index=False).encode("utf-8"),
                file_name="avaliacao_reacao_vila_buriti.csv",
                mime="text/csv",
            )
