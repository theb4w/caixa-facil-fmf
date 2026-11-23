# -*- coding: utf-8 -*-
"""
Módulo de lógica de negócio e modelos estatísticos/preditivos para o Caixa Fácil Vila Buriti.
Contém regras setoriais SEBRAE, formatações contábeis e treinamento dos modelos preditivos.
"""

from typing import Any
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import streamlit as st


# Faixas de referência setorial SEBRAE por perfil
FAIXAS_SEBRAE: dict[str, dict[str, float]] = {
    "Mercadinho": {"cmv_min": 65.0, "cmv_max": 80.0, "margem_min": 8.0, "margem_max": 20.0},
    "Lanchonete": {"cmv_min": 30.0, "cmv_max": 40.0, "margem_min": 10.0, "margem_max": 25.0},
    "Misto":      {"cmv_min": 48.0, "cmv_max": 62.0, "margem_min": 12.0, "margem_max": 25.0},
}

# Configurações de parâmetros operacionais por perfil de negócio
PERFIS_CONFIG: dict[str, dict[str, float]] = {
    "Mercadinho": {"receita_dia_base": 620.0, "cmv_medio": 0.68, "fixo_dia": 115.0, "ticket_medio": 34.0},
    "Lanchonete": {"receita_dia_base": 480.0, "cmv_medio": 0.37, "fixo_dia": 220.0, "ticket_medio": 22.0},
    "Misto":      {"receita_dia_base": 560.0, "cmv_medio": 0.56, "fixo_dia": 145.0, "ticket_medio": 29.0},
}


def formatar_brl(valor: float) -> str:
    """Formata float no padrão monetário brasileiro (R$ 1.234,56 ou -R$ 1.234,56)."""
    abs_v = abs(valor)
    texto = f"{abs_v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if valor < 0:
        return f"-R$ {texto}"
    return f"R$ {texto}"


@st.cache_data
def carregar_base_mensal_padrao() -> pd.DataFrame:
    """Retorna a série mensal simulada de 12 meses calibrada (IBGE/SEBRAE)."""
    dados = {
        "Meses": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        "Mes_Num": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "Receita_Bruta": [
            14200.00, 13500.00, 14800.00, 15100.00, 15900.00, 16800.00,
            16400.00, 17100.00, 17500.00, 18200.00, 18900.00, 21500.00,
        ],
        "Custo_Mercadorias": [
            8100.00, 7800.00, 8400.00, 8550.00, 8900.00, 9300.00,
            9100.00, 9450.00, 9600.00, 9950.00, 10300.00, 11500.00,
        ],
        "Despesas_Fixas": [
            3200.00, 3150.00, 3250.00, 3300.00, 3350.00, 3500.00,
            3450.00, 3500.00, 3550.00, 3650.00, 3700.00, 4100.00,
        ],
        "Qtd_Vendas": [500, 490, 520, 530, 540, 560, 550, 570, 580, 590, 610, 660],
    }
    return pd.DataFrame(dados)


def calcular_indicadores_mensais(df_base: pd.DataFrame) -> pd.DataFrame:
    """Calcula colunas derivadas contábeis sobre o DataFrame mensal."""
    df = df_base.copy()
    if "Mes_Num" not in df.columns:
        df["Mes_Num"] = np.arange(1, len(df) + 1)
    df["Despesas_Totais"] = df["Custo_Mercadorias"] + df["Despesas_Fixas"]
    df["Saldo_Liquido"] = df["Receita_Bruta"] - df["Despesas_Totais"]
    df["Margem_Liquida_%"] = np.where(
        df["Receita_Bruta"] > 0,
        (df["Saldo_Liquido"] / df["Receita_Bruta"]) * 100.0,
        0.0,
    )
    df["CMV_%"] = np.where(
        df["Receita_Bruta"] > 0,
        (df["Custo_Mercadorias"] / df["Receita_Bruta"]) * 100.0,
        0.0,
    )
    df["Ticket_Medio"] = np.where(
        df["Qtd_Vendas"] > 0,
        df["Receita_Bruta"] / df["Qtd_Vendas"],
        0.0,
    )
    return df


def diagnosticar_sebrae(
    cmv_pct: float,
    margem_pct: float,
    saldo_medio: float,
    pro_labore: float,
    perfil: str,
) -> dict[str, dict[str, str]]:
    """Gera diagnóstico de conformidade SEBRAE para CMV e governança PF/PJ."""
    faixa = FAIXAS_SEBRAE.get(perfil, FAIXAS_SEBRAE["Misto"])
    cmv_min = faixa["cmv_min"]
    cmv_max = faixa["cmv_max"]
    margem_min = faixa["margem_min"]
    margem_max = faixa["margem_max"]

    # Diagnóstico de CMV
    if cmv_min <= cmv_pct <= cmv_max:
        cmv_status = "saudavel"
        cmv_badge = "Saudável"
        cmv_rec = "Seu custo de mercadorias está equilibrado com o padrão setorial, preservando a margem operacional."
    elif cmv_pct > cmv_max:
        cmv_status = "alerta"
        cmv_badge = "Alerta"
        cmv_rec = "CMV acima do recomendado: renegocie com fornecedores ou revise margens de precificação para estancar perdas."
    else:
        cmv_status = "atencao"
        cmv_badge = "Atenção"
        cmv_rec = "CMV abaixo da faixa típica: verifique se todas as notas de compras foram devidamente escrituradas."

    cmv_ref = f"Faixa SEBRAE ({perfil}): {cmv_min:.0f}% a {cmv_max:.0f}%"

    # Diagnóstico de PF/PJ e Pró-Labore
    folga = saldo_medio - pro_labore
    if pro_labore > saldo_medio:
        pf_status = "alerta"
        pf_badge = "Alerta"
        pf_rec = (
            f"Risco de descapitalização: o pró-labore ({formatar_brl(pro_labore)}) supera o saldo líquido "
            f"médio mensal ({formatar_brl(saldo_medio)}), consumindo capital de giro."
        )
    elif margem_pct < margem_min or folga < (saldo_medio * 0.15):
        pf_status = "atencao"
        pf_badge = "Atenção"
        pf_rec = "Folga financeira reduzida após pró-labore: reduza despesas fixas para recompor a reserva do caixa."
    else:
        pf_status = "saudavel"
        pf_badge = "Saudável"
        pf_rec = (
            f"Saudável: o saldo médio ({formatar_brl(saldo_medio)}) cobre o pró-labore fixo e preserva "
            f"{formatar_brl(folga)}/mês para reinvestimento e capital de giro."
        )

    pf_ref = f"Faixa SEBRAE ({perfil}): {margem_min:.0f}% a {margem_max:.0f}% de margem líquida"

    return {
        "cmv": {
            "status": cmv_status,
            "badge": cmv_badge,
            "referencia": cmv_ref,
            "recomendacao": cmv_rec,
        },
        "pf_pj": {
            "status": pf_status,
            "badge": pf_badge,
            "referencia": pf_ref,
            "recomendacao": pf_rec,
        },
    }


@st.cache_resource
def treinar_motor_big_data() -> tuple[
    pd.DataFrame,
    LinearRegression,
    RandomForestRegressor,
    pd.DataFrame,
    dict[str, dict[str, float]],
]:
    """Gera os 10.950 registros diários (seed=42) e treina os modelos supervisionados."""
    np.random.seed(42)
    fatores_mes = {
        1: 0.90, 2: 0.85, 3: 0.93, 4: 0.95, 5: 0.99, 6: 1.05,
        7: 1.02, 8: 1.06, 9: 1.08, 10: 1.12, 11: 1.16, 12: 1.32,
    }
    perfis_config = PERFIS_CONFIG

    datas = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    registros: list[dict[str, Any]] = []

    for i in range(1, 31):
        perfil = ["Mercadinho", "Lanchonete", "Misto"][(i - 1) // 10]
        cfg = perfis_config[perfil]
        fator_porte = np.random.uniform(0.80, 1.25)

        for data in datas:
            mes = data.month
            dia_semana = data.day_of_week
            dia_mes = data.day

            fator_dia_semana = 1.15 if dia_semana in [4, 5] else (0.88 if dia_semana == 6 else 1.00)
            semana_pagamento = 1 if (1 <= dia_mes <= 10 or 15 <= dia_mes <= 22) else 0
            fator_pag = 1.12 if semana_pagamento == 1 else 0.94

            ruido = np.random.normal(1.0, 0.08)
            receita = max(
                120.0,
                cfg["receita_dia_base"] * fator_porte * fatores_mes[mes] * fator_dia_semana * fator_pag * ruido,
            )

            cmv_pct = np.clip(np.random.normal(cfg["cmv_medio"], 0.025), 0.25, 0.78)
            custo_merc = receita * cmv_pct
            desp_fixa = cfg["fixo_dia"] * fator_porte * np.random.uniform(0.95, 1.05)
            saldo = receita - (custo_merc + desp_fixa)
            qtd_vendas = max(5, int(round(receita / np.random.normal(cfg["ticket_medio"], 2.0))))

            registros.append({
                "Comercio_ID": f"COM_{i:02d}",
                "Perfil": perfil,
                "Data": data,
                "Mes_Num": mes,
                "Dia_Semana": dia_semana,
                "Semana_Pagamento": semana_pagamento,
                "Fator_Porte": round(fator_porte, 3),
                "Qtd_Vendas": qtd_vendas,
                "Receita_Bruta": round(receita, 2),
                "Custo_Mercadorias": round(custo_merc, 2),
                "Despesas_Fixas_Dia": round(desp_fixa, 2),
                "Saldo_Liquido": round(saldo, 2),
                "Margem_Liquida_%": round((saldo / receita) * 100, 2),
            })

    df_grande = pd.DataFrame(registros)
    df_ml = pd.get_dummies(df_grande, columns=["Perfil"], drop_first=True)
    colunas_features = [
        "Mes_Num", "Dia_Semana", "Semana_Pagamento", "Fator_Porte",
        "Perfil_Mercadinho", "Perfil_Misto",
    ]

    estratos = df_grande["Mes_Num"].astype(str) + "_" + df_grande["Perfil"]
    X_train, X_test, y_train, y_test = train_test_split(
        df_ml[colunas_features],
        df_ml["Receita_Bruta"],
        test_size=0.20,
        random_state=42,
        stratify=estratos,
    )

    lr = LinearRegression().fit(X_train, y_train)
    pred_lr = lr.predict(X_test)

    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42).fit(X_train, y_train)
    pred_rf = rf.predict(X_test)

    metricas_df = pd.DataFrame([
        {
            "Modelo": "Regressão Linear Múltipla",
            "MAE": mean_absolute_error(y_test, pred_lr),
            "RMSE": np.sqrt(mean_squared_error(y_test, pred_lr)),
            "R2": r2_score(y_test, pred_lr),
        },
        {
            "Modelo": "Random Forest Regressor",
            "MAE": mean_absolute_error(y_test, pred_rf),
            "RMSE": np.sqrt(mean_squared_error(y_test, pred_rf)),
            "R2": r2_score(y_test, pred_rf),
        },
    ])

    return df_grande, lr, rf, metricas_df, PERFIS_CONFIG


def converter_venda_diaria_para_porte(venda_dia_normal: float, perfil: str) -> tuple[float, bool]:
    """Converte venda diária média em fator de porte (0.80 a 1.25) e sinaliza se houve corte."""
    fator = venda_dia_normal / PERFIS_CONFIG[perfil]["receita_dia_base"]
    fator_clipped = float(np.clip(fator, 0.80, 1.25))
    houve_corte = bool(fator < 0.80 or fator > 1.25)
    return fator_clipped, houve_corte


def calcular_projecao_linear(df_calc: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    """Ajusta Regressão Linear sobre Mes_Num e projeta os próximos 3 meses."""
    df = df_calc.copy()
    if "Mes_Num" not in df.columns:
        df["Mes_Num"] = np.arange(1, len(df) + 1)

    modelo_simples = LinearRegression().fit(df[["Mes_Num"]], df["Receita_Bruta"])
    r2_simples = float(modelo_simples.score(df[["Mes_Num"]], df["Receita_Bruta"]))
    inc_simples = float(modelo_simples.coef_[0])
    prox_n = int(df["Mes_Num"].max()) if len(df) > 0 else 0

    df_proj = pd.DataFrame({
        "Mes_Num": [prox_n + 1, prox_n + 2, prox_n + 3],
        "Periodo": ["Jan/Ano 2", "Fev/Ano 2", "Mar/Ano 2"],
    })
    df_proj["Receita_Linear_Projetada"] = modelo_simples.predict(df_proj[["Mes_Num"]])
    return df_proj, inc_simples, r2_simples
