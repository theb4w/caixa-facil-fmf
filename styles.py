# -*- coding: utf-8 -*-
"""
Componentes visuais e estilos — Caixa Fácil Vila Buriti.
Referências de interface: Stripe Dashboard, Mercury e Wise Business.
Princípios: bordas finas uniformes (1px), superfícies limpas, zero neon,
zero pílulas, zero emojis (apenas ícones SVG/Material) e tipografia tabular.
"""

from typing import Callable
import matplotlib.pyplot as plt
import streamlit as st

# Ícones SVG minimalistas (estilo Lucide, 16px, traço limpo)
_SVG_ICONS = {
    "store": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/>'
        '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>'
        '<path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/>'
        '<path d="M2 7h20"/>'
        '<path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>'
        '</svg>'
    ),
    "info": (
        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>'
        '</svg>'
    ),
    "check": (
        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>'
        '</svg>'
    ),
    "alert": (
        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
        '<path d="M12 9v4"/><path d="M12 17h.01"/>'
        '</svg>'
    ),
    "x_circle": (
        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>'
        '</svg>'
    ),
}

_STATUS_MAP = {
    "saudavel": {"color": "#166534", "icon": _SVG_ICONS["check"]},
    "atencao": {"color": "#92400E", "icon": _SVG_ICONS["alert"]},
    "alerta": {"color": "#991B1B", "icon": _SVG_ICONS["x_circle"]},
}


def configurar_matplotlib() -> None:
    """Configura gráficos limpos e legíveis inspirados em dashboards financeiros."""
    plt.rcParams.update({
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "axes.edgecolor": "#E5E7EB",
        "axes.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#F3F4F6",
        "grid.linestyle": "-",
        "grid.linewidth": 0.8,
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Segoe UI", "Roboto", "DejaVu Sans", "sans-serif"],
        "text.color": "#111827",
        "axes.labelcolor": "#4B5563",
        "axes.labelsize": 9.5,
        "xtick.color": "#6B7280",
        "ytick.color": "#6B7280",
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
        "figure.dpi": 100,
    })


def injetar_estilos() -> None:
    """Injeta CSS minimalista (sem gradientes, sem neon, sem bordas laterais grossas)."""
    st.html(
        """
        <style>
            .stApp {
                background-color: #F8F9FA;
                color: #111827;
            }
            .block-container {
                padding-top: 1.4rem !important;
                padding-bottom: 2.5rem !important;
                max-width: 1140px;
            }
            h1, h2, h3, h4 {
                color: #111827;
                letter-spacing: -0.02em;
            }
            /* Abas limpas estilo Stripe/Linear */
            .stTabs [data-baseweb="tab-list"] {
                gap: 1.5rem;
                border-bottom: 1px solid #E5E7EB;
                background: transparent;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 0.65rem 0.1rem;
                font-weight: 500;
                font-size: 0.92rem;
                color: #6B7280;
                background: transparent;
            }
            .stTabs [aria-selected="true"] {
                color: #111827 !important;
                font-weight: 600 !important;
            }
            /* Métricas nativas com números tabulares */
            [data-testid="stMetric"] {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0.9rem 1.05rem;
            }
            [data-testid="stMetricLabel"] {
                font-size: 0.8rem;
                color: #6B7280;
                font-weight: 500;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.45rem;
                font-weight: 600;
                color: #111827;
                font-variant-numeric: tabular-nums;
            }
            /* Containers com borda uniforme */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB !important;
                border-radius: 8px !important;
            }
            /* Botões sóbrios */
            .stButton > button, .stDownloadButton > button {
                border-radius: 6px;
                font-weight: 500;
                font-size: 0.88rem;
            }
            /* Cartões HTML customizados (sempre borda uniforme 1px, 8px radius) */
            .cf-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                flex-wrap: wrap;
                gap: 0.75rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid #E5E7EB;
                margin-bottom: 0.85rem;
            }
            .cf-brand {
                display: flex;
                align-items: center;
                gap: 0.65rem;
            }
            .cf-brand-mark {
                width: 34px;
                height: 34px;
                border-radius: 7px;
                background: #111827;
                color: #FFFFFF;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .cf-brand-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #111827;
                line-height: 1.2;
                letter-spacing: -0.02em;
            }
            .cf-brand-sub {
                font-size: 0.82rem;
                color: #6B7280;
                margin-top: 0.1rem;
            }
            .cf-meta-right {
                font-size: 0.78rem;
                color: #6B7280;
                text-align: right;
            }
            .cf-notice {
                display: flex;
                align-items: flex-start;
                gap: 0.55rem;
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 0.65rem 0.9rem;
                font-size: 0.81rem;
                color: #4B5563;
                line-height: 1.45;
                margin-bottom: 1rem;
            }
            .cf-notice-icon {
                color: #92400E;
                margin-top: 2px;
                flex-shrink: 0;
            }
            .cf-card {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 1.25rem 1.35rem;
                margin-bottom: 1rem;
            }
            .cf-hero-top {
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                flex-wrap: wrap;
                gap: 0.75rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid #F3F4F6;
                margin-bottom: 1rem;
            }
            .cf-label {
                font-size: 0.78rem;
                font-weight: 600;
                color: #6B7280;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }
            .cf-hero-value {
                font-size: 2rem;
                font-weight: 700;
                color: #111827;
                font-variant-numeric: tabular-nums;
                letter-spacing: -0.025em;
                margin-top: 0.15rem;
            }
            .cf-status-inline {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                font-size: 0.83rem;
                font-weight: 600;
            }
            .cf-eq-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 1rem;
                padding: 0.85rem 1rem;
                background: #F9FAFB;
                border: 1px solid #F3F4F6;
                border-radius: 6px;
                margin-bottom: 1.1rem;
            }
            .cf-eq-item-label {
                font-size: 0.76rem;
                color: #6B7280;
                font-weight: 500;
                margin-bottom: 0.2rem;
            }
            .cf-eq-item-value {
                font-size: 1.08rem;
                font-weight: 600;
                color: #111827;
                font-variant-numeric: tabular-nums;
            }
            .cf-eq-sub {
                font-size: 0.76rem;
                margin-top: 0.15rem;
                font-weight: 500;
            }
            .cf-bar-title {
                font-size: 0.82rem;
                font-weight: 600;
                color: #374151;
                margin-bottom: 0.45rem;
            }
            .cf-bar-track {
                display: flex;
                width: 100%;
                height: 10px;
                border-radius: 4px;
                overflow: hidden;
                background: #E5E7EB;
                margin-bottom: 0.65rem;
            }
            .cf-bar-legend {
                display: flex;
                flex-wrap: wrap;
                gap: 1.2rem;
                font-size: 0.8rem;
                color: #4B5563;
                font-variant-numeric: tabular-nums;
            }
            .cf-legend-item {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
            }
            .cf-legend-swatch {
                width: 8px;
                height: 8px;
                border-radius: 2px;
                display: inline-block;
            }
            .cf-diag-head {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
            }
            .cf-diag-title {
                font-size: 0.82rem;
                font-weight: 600;
                color: #4B5563;
            }
            .cf-diag-value {
                font-size: 1.35rem;
                font-weight: 700;
                color: #111827;
                font-variant-numeric: tabular-nums;
                margin-bottom: 0.2rem;
            }
            .cf-diag-ref {
                font-size: 0.79rem;
                color: #6B7280;
                margin-bottom: 0.65rem;
            }
            .cf-diag-rec {
                font-size: 0.84rem;
                color: #374151;
                line-height: 1.48;
                padding-top: 0.65rem;
                border-top: 1px solid #F3F4F6;
            }
            .cf-guide-num {
                font-size: 0.76rem;
                font-weight: 700;
                color: #B45309;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 0.3rem;
            }
            .cf-guide-title {
                font-size: 0.98rem;
                font-weight: 600;
                color: #111827;
                margin-bottom: 0.45rem;
            }
            .cf-guide-body {
                font-size: 0.84rem;
                color: #4B5563;
                line-height: 1.55;
            }
            @media (max-width: 768px) {
                .cf-eq-grid {
                    grid-template-columns: 1fr;
                    gap: 0.75rem;
                }
                .cf-meta-right {
                    text-align: left;
                }
                .cf-hero-value {
                    font-size: 1.65rem;
                }
            }
        </style>
        """
    )


def render_cabecalho() -> None:
    """Renderiza o cabeçalho editorial limpo (sem caixa escura pesada) e o aviso ético."""
    st.html(
        f"""
        <div class="cf-header">
            <div class="cf-brand">
                <div class="cf-brand-mark">{_SVG_ICONS["store"]}</div>
                <div>
                    <div class="cf-brand-title">Caixa Fácil · Vila Buriti</div>
                    <div class="cf-brand-sub">Controle financeiro e previsão de vendas para pequenos comércios</div>
                </div>
            </div>
            <div class="cf-meta-right">
                Projeto de Extensão · FMF Wyden<br>
                Tópicos de Big Data em Python · Prof. Ranyere Lima
            </div>
        </div>
        <div class="cf-notice">
            <span class="cf-notice-icon">{_SVG_ICONS["info"]}</span>
            <span>
                <strong>Base inicial simulada:</strong> os valores pré-carregados são 100% fictícios,
                calibrados por IBGE (PMC) e SEBRAE para fins didáticos. Substitua pelos números do seu
                comércio ou importe sua planilha CSV na barra lateral.
            </span>
        </div>
        """
    )


def render_hero_card(
    receita_anual: float,
    cmv_anual: float,
    fixas_anual: float,
    saldo_anual: float,
    margem_pct: float,
    pro_labore_mensal: float,
    saldo_medio_mensal: float,
    formatar_brl: Callable[[float], str],
) -> None:
    """Renderiza o resumo financeiro principal e a barra de composição de cada R$ 100."""
    despesas_anuais = cmv_anual + fixas_anual
    folga_mensal = saldo_medio_mensal - pro_labore_mensal

    if receita_anual > 0:
        pct_cmv = max(0.0, (cmv_anual / receita_anual) * 100.0)
        pct_fixas = max(0.0, (fixas_anual / receita_anual) * 100.0)
        pct_lucro = max(0.0, (saldo_anual / receita_anual) * 100.0)
    else:
        pct_cmv = pct_fixas = pct_lucro = 0.0

    soma_bar = pct_cmv + pct_fixas + pct_lucro
    if soma_bar > 0:
        w_cmv = (pct_cmv / soma_bar) * 100.0
        w_fixas = (pct_fixas / soma_bar) * 100.0
        w_lucro = (pct_lucro / soma_bar) * 100.0
    else:
        w_cmv = w_fixas = w_lucro = 0.0

    if saldo_anual <= 0:
        status_key = "alerta"
        margem_texto = f"Margem real: {margem_pct:.1f}% (prejuízo)"
    elif margem_pct < 10.0:
        status_key = "atencao"
        margem_texto = f"Margem real: {margem_pct:.1f}% (apertada)"
    else:
        status_key = "saudavel"
        margem_texto = f"Margem real: {margem_pct:.1f}%"

    st_info = _STATUS_MAP[status_key]

    if folga_mensal >= 0:
        folga_cor = "#166534"
        folga_texto = f"Cobre o pró-labore com folga de {formatar_brl(folga_mensal)}/mês"
    else:
        folga_cor = "#991B1B"
        folga_texto = f"Faltam {formatar_brl(abs(folga_mensal))}/mês para cobrir o pró-labore"

    cor_lucro_bar = "#166534" if saldo_anual > 0 else "#991B1B"

    st.html(
        f"""
        <div class="cf-card">
            <div class="cf-hero-top">
                <div>
                    <div class="cf-label">Lucro líquido acumulado (12 meses)</div>
                    <div class="cf-hero-value">{formatar_brl(saldo_anual)}</div>
                </div>
                <div class="cf-status-inline" style="color: {st_info['color']};">
                    {st_info['icon']}
                    <span>{margem_texto}</span>
                </div>
            </div>
            <div class="cf-eq-grid">
                <div>
                    <div class="cf-eq-item-label">Total que entrou (vendas)</div>
                    <div class="cf-eq-item-value">{formatar_brl(receita_anual)}</div>
                    <div class="cf-eq-sub" style="color: #6B7280;">Faturamento bruto anual</div>
                </div>
                <div>
                    <div class="cf-eq-item-label">Total que saiu (mercadorias + fixas)</div>
                    <div class="cf-eq-item-value">{formatar_brl(despesas_anuais)}</div>
                    <div class="cf-eq-sub" style="color: #6B7280;">Estoque {formatar_brl(cmv_anual)} · Fixas {formatar_brl(fixas_anual)}</div>
                </div>
                <div>
                    <div class="cf-eq-item-label">Lucro médio por mês</div>
                    <div class="cf-eq-item-value" style="color: {folga_cor};">{formatar_brl(saldo_medio_mensal)}</div>
                    <div class="cf-eq-sub" style="color: {folga_cor};">{folga_texto}</div>
                </div>
            </div>
            <div class="cf-bar-title">Para onde foi cada R$ 100 vendidos</div>
            <div class="cf-bar-track">
                <div style="width: {w_cmv:.2f}%; background: #374151;"></div>
                <div style="width: {w_fixas:.2f}%; background: #B45309;"></div>
                <div style="width: {w_lucro:.2f}%; background: {cor_lucro_bar};"></div>
            </div>
            <div class="cf-bar-legend">
                <span class="cf-legend-item">
                    <span class="cf-legend-swatch" style="background: #374151;"></span>
                    <strong>R$ {pct_cmv:.1f}</strong>&nbsp;Mercadorias / estoque ({pct_cmv:.1f}%)
                </span>
                <span class="cf-legend-item">
                    <span class="cf-legend-swatch" style="background: #B45309;"></span>
                    <strong>R$ {pct_fixas:.1f}</strong>&nbsp;Contas fixas ({pct_fixas:.1f}%)
                </span>
                <span class="cf-legend-item">
                    <span class="cf-legend-swatch" style="background: {cor_lucro_bar};"></span>
                    <strong>R$ {pct_lucro:.1f}</strong>&nbsp;Lucro real livre ({pct_lucro:.1f}%)
                </span>
            </div>
        </div>
        """
    )


def render_semaforo_card(
    titulo: str,
    valor_destaque: str,
    referencia: str,
    status: str,
    badge_texto: str,
    recomendacao: str,
) -> None:
    """Renderiza cartão de diagnóstico SEBRAE sem pílulas e sem bordas laterais grossas."""
    st_info = _STATUS_MAP.get(status, _STATUS_MAP["atencao"])

    st.html(
        f"""
        <div class="cf-card">
            <div class="cf-diag-head">
                <span class="cf-diag-title">{titulo}</span>
                <span class="cf-status-inline" style="color: {st_info['color']};">
                    {st_info['icon']}
                    <span>{badge_texto}</span>
                </span>
            </div>
            <div class="cf-diag-value">{valor_destaque}</div>
            <div class="cf-diag-ref">{referencia}</div>
            <div class="cf-diag-rec">
                <strong>Recomendação:</strong> {recomendacao}
            </div>
        </div>
        """
    )


def render_alerta_reserva(
    mes_vale: str,
    saldo_vale: float,
    pro_labore: float,
    reserva_estimada: float,
    pct_reserva: int,
    formatar_brl: Callable[[float], str],
) -> None:
    """Exibe diagnóstico objetivo sobre a cobertura do mês mais fraco pela reserva sazonal."""
    deficit = max(0.0, pro_labore - saldo_vale)

    if deficit == 0:
        st_info = _STATUS_MAP["saudavel"]
        titulo = f"Seu caixa cobre o pró-labore mesmo em {mes_vale}"
        texto = (
            f"O lucro estimado em {mes_vale} ({formatar_brl(saldo_vale)}) supera seu pró-labore "
            f"({formatar_brl(pro_labore)}). Guardando {pct_reserva}% dos meses fortes (Jun, Nov e Dez), "
            f"você ainda forma uma reserva extra de {formatar_brl(reserva_estimada)} para capital de giro."
        )
    elif reserva_estimada >= deficit:
        st_info = _STATUS_MAP["atencao"]
        sobra = reserva_estimada - deficit
        titulo = f"A reserva sazonal cobre a queda de {mes_vale} sem empréstimo"
        texto = (
            f"Em {mes_vale}, faltariam {formatar_brl(deficit)} para completar o pró-labore. "
            f"Guardando {pct_reserva}% do lucro de Jun, Nov e Dez ({formatar_brl(reserva_estimada)}), "
            f"você cobre o mês inteiro e ainda mantém {formatar_brl(sobra)} de margem de segurança."
        )
    else:
        st_info = _STATUS_MAP["alerta"]
        falta = deficit - reserva_estimada
        titulo = f"Reserva insuficiente para cobrir {mes_vale}"
        texto = (
            f"Em {mes_vale}, faltam {formatar_brl(deficit)} para pagar o pró-labore. "
            f"A meta atual de {pct_reserva}% acumula {formatar_brl(reserva_estimada)}, deixando "
            f"descoberto {formatar_brl(falta)}. Aumente a meta de economia nos picos ou ajuste a retirada mensal."
        )

    st.html(
        f"""
        <div class="cf-card" style="padding: 1rem 1.2rem;">
            <div class="cf-status-inline" style="color: {st_info['color']}; margin-bottom: 0.35rem;">
                {st_info['icon']}
                <span>{titulo}</span>
            </div>
            <div style="font-size: 0.85rem; color: #374151; line-height: 1.5;">
                {texto}
            </div>
        </div>
        """
    )


def render_card_guia(numero: str, titulo: str, texto: str) -> None:
    """Renderiza passo numerado limpo para o guia prático de gestão."""
    st.html(
        f"""
        <div class="cf-card" style="height: 100%;">
            <div class="cf-guide-num">Passo {numero}</div>
            <div class="cf-guide-title">{titulo}</div>
            <div class="cf-guide-body">{texto}</div>
        </div>
        """
    )
