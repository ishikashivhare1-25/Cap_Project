import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
import pickle
import json
import os
import joblib
import traceback

warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap)');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #0a0f1e; color: #e8eaf0; }

[data-testid="stSidebar"] { background: #0d1428 !important; border-right: 1px solid #1e2d50; }
[data-testid="stSidebar"] * { color: #c5cee8 !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #7b8fc0 !important; font-size: 0.75rem !important;
    text-transform: uppercase; letter-spacing: 0.08em;
}
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #0f1e3d 100%);
    border: 1px solid #1e3460; border-radius: 12px;
    padding: 1.2rem 1.4rem; margin-bottom: 0.5rem;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
}
.metric-label { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: #4b7db8;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.3rem; }
.metric-value { font-size: 1.7rem; font-weight: 800; color: #e8f0ff; line-height: 1; }
.metric-sub { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #3b82f6; margin-top: 0.25rem; }
.best-badge {
    display: inline-block; background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white; font-size: 0.6rem; font-family: 'DM Mono', monospace;
    text-transform: uppercase; letter-spacing: 0.1em; padding: 2px 8px;
    border-radius: 20px; margin-left: 8px; vertical-align: middle;
}
.section-header { font-size: 0.7rem; font-family: 'DM Mono', monospace; color: #3b82f6;
    text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 0.5rem; }
.section-title { font-size: 1.5rem; font-weight: 800; color: #e8f0ff;
    margin-bottom: 1.5rem; line-height: 1.2; }
.hero {
    background: linear-gradient(135deg, #0d1e3f 0%, #0a1628 50%, #091422 100%);
    border: 1px solid #1e3460; border-radius: 16px;
    padding: 2rem 2.5rem; margin-bottom: 2rem; position: relative; overflow: hidden;
}
.hero::after {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
}
.hero-title {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #06b6d4, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.15; margin-bottom: 0.5rem;
}
.hero-sub { color: #5a78b0; font-family: 'DM Mono', monospace;
    font-size: 0.8rem; letter-spacing: 0.05em; }
.insight-box {
    background: #0d1428; border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 0.9rem 1.2rem; margin: 0.5rem 0;
    font-size: 0.88rem; color: #a0b4d8; line-height: 1.6;
}
.insight-box strong { color: #60a5fa; }
.insight-box.cyan  { border-left-color: #06b6d4; }
.insight-box.green { border-left-color: #10b981; }
.insight-box.amber { border-left-color: #f59e0b; }
.insight-box.purple{ border-left-color: #a78bfa; }
.model-row {
    display: flex; align-items: center; background: #0d1428;
    border: 1px solid #1a2d4e; border-radius: 8px; padding: 0.75rem 1rem;
    margin: 0.35rem 0; font-family: 'DM Mono', monospace; font-size: 0.8rem;
}
.model-row.best { border-color: #3b82f6; background: linear-gradient(90deg, #0d1e3f, #0d1428); }
.model-name   { flex: 2; font-weight: 500; color: #c5cee8; }
.model-metric { flex: 1; text-align: center; color: #5a78b0; }
.model-metric.highlight { color: #60a5fa; font-weight: 500; }
.stTabs [data-baseweb="tab-list"] { background: #0d1428; border-radius: 8px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #4b7db8 !important; border-radius: 6px;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    text-transform: uppercase; letter-spacing: 0.08em; padding: 0.5rem 1rem;
}
.stTabs [aria-selected="true"] { background: #1e3460 !important; color: #60a5fa !important; }
.whatif-card {
    background: linear-gradient(135deg, #0d1e3f 0%, #091422 100%);
    border: 1px solid #1e3460; border-radius: 12px; padding: 1.4rem; margin-bottom: 1rem;
}
.whatif-title {
    font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #06b6d4;
    text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;
}
.delta-positive { color: #10b981; font-weight: 700; }
.delta-negative { color: #ef4444; font-weight: 700; }
.ai-badge {
    display: inline-block; background: linear-gradient(90deg, #6366f1, #06b6d4);
    color: white; font-size: 0.6rem; font-family: 'DM Mono', monospace;
    text-transform: uppercase; letter-spacing: 0.1em; padding: 2px 10px;
    border-radius: 20px; margin-left: 8px; vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# ── Dark matplotlib style ─────────────────────────────────────────────────────
def set_dark_style():
    plt.rcParams.update({
        "figure.facecolor": "#0a0f1e", "axes.facecolor": "#0d1428",
        "axes.edgecolor": "#1e3460", "axes.labelcolor": "#7b8fc0",
        "axes.titlecolor": "#c5cee8", "xtick.color": "#4b7db8",
        "ytick.color": "#4b7db8", "grid.color": "#1a2d4e",
        "grid.linewidth": 0.5, "text.color": "#c5cee8",
        "legend.facecolor": "#0d1428", "legend.edgecolor": "#1e3460",
        "legend.fontsize": 8, "font.family": "monospace",
    })

set_dark_style()

MODEL_COLORS = {
    "ARIMA": "#ef4444", "SARIMA": "#f59e0b",
    "HoltWinters": "#3b82f6",
}



MODELS_DIR = "models"
XLSX_CANDIDATES = [
    "rideBookings_preprocessed1.xlsx",
    os.path.join(MODELS_DIR, "rideBookings_preprocessed1.xlsx"),
]
            # ── Load Model Metrics CSV ───────────────────────────────────────────────────
def load_model_metrics():

    metrics_path = os.path.join(
        MODELS_DIR,
        "model_metrics.csv"
    )

    if os.path.exists(metrics_path):

        return pd.read_csv(metrics_path)

    st.warning("⚠️ model_metrics.csv not found")

    return pd.DataFrame()
# ── Model Loading ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_models():
    models, errors = {}, {}
    individual = {
        "ARIMA":       "arima_model.pkl",
        "SARIMA":      "sarima_model.pkl",
        "HoltWinters": "holtwinters_model.pkl",
    }
    for display_name, fname in individual.items():
        path = os.path.join(MODELS_DIR, fname)
        if os.path.exists(path):
            try:
                models[display_name] = joblib.load(path)
            except Exception as e:
                errors[display_name] = f"Failed to load {fname}: {e}"
        else:
            errors[display_name] = f"{fname} not found in {MODELS_DIR}/"

    # Prophet support (optional)
    prophet_path = os.path.join(MODELS_DIR, "prophet_model.json")
    if os.path.exists(prophet_path):
        try:
            from prophet.serialize import model_from_json
            with open(prophet_path, "r") as f:
                models["Prophet"] = model_from_json(json.load(f))
        except (ImportError, Exception) as e:
            errors["Prophet"] = f"Prophet load failed: {e}"
    
    return models, errors

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_train_data():
    xlsx_path = next((c for c in XLSX_CANDIDATES if os.path.exists(c)), None)
    if xlsx_path is None:
        return _synthetic_data(), True
    
    try:
        df = pd.read_excel(xlsx_path)
        
        # Handle different datetime column formats
        dt_col = None
        for col in df.columns:
            if any(x in col.strip().lower() for x in ["datetime", "date", "time"]):
                dt_col = col
                break
        
        if dt_col is None and "Date" in df.columns and "Time" in df.columns:
            df["datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str))
            dt_col = "datetime"
        
        if dt_col is None:
            raise ValueError(f"No datetime column found. Columns: {list(df.columns)}")
        
        df[dt_col] = pd.to_datetime(df[dt_col])
        df = df.set_index(dt_col).sort_index()
        
        # Resample to daily demand (count bookings per day)
        series = df.resample("D").size().rename("demand").fillna(0)
        
        if len(series) < 10:
            raise ValueError("Too few daily records generated.")
            
        return series, False
    except Exception as e:
        st.error(f"❌ Error reading Excel: {e}")
        return _synthetic_data(), True

def _synthetic_data():
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    n = len(dates)
    trend = np.linspace(390, 415, n)
    weekly = 12 * np.sin(2 * np.pi * np.arange(n) / 7)
    noise = np.random.normal(0, 10, n)
    spikes = np.zeros(n); spikes[[30,60,150,200,300]] = [30,-40,45,-35,20]
    return pd.Series(np.clip(trend+weekly+noise+spikes, 355, 465), index=dates, name="demand")

# ── Forecasting ───────────────────────────────────────────────────────────────
def forecast_with_model(name, obj, horizon, last_date, train):
    future_idx = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon, freq="D")
    try:
        if hasattr(obj, "forecast"):
            fc = obj.forecast(steps=horizon)
            vals = fc.values if hasattr(fc, "values") else np.array(fc)
            return pd.Series(vals[:horizon], index=future_idx)
        if hasattr(obj, "predict"):
            start = len(train)
            fc = obj.predict(start=start, end=start + horizon - 1)
            vals = fc.values if hasattr(fc, "values") else np.array(fc)
            return pd.Series(vals[:horizon], index=future_idx)
        if hasattr(obj, "make_future_dataframe"):
            future = obj.make_future_dataframe(periods=horizon)
            pred = obj.predict(future)
            yhat = pred["yhat"].values[-horizon:]
            return pd.Series(yhat, index=future_idx)
    except Exception as e:
        st.toast(f"⚠️ {name} forecast error: {e}", icon="⚠️")
    
    # Fallback
    np.random.seed(abs(hash(name)) % 9999)
    base = train.iloc[-30:].mean()
    return pd.Series(base + np.random.normal(0, 3, horizon), index=future_idx)

def build_forecasts(models, train, horizon):
    last_date = train.index[-1]
    results = {}
    for display_name in ["ARIMA","SARIMA","HoltWinters","Prophet"]:
        if display_name in models:
            results[display_name] = forecast_with_model(
                display_name, models[display_name], horizon, last_date, train)
    if len(results) >= 2:
        results["Ensemble"] = pd.DataFrame(results).mean(axis=1)
    if not results:
        future_idx = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon, freq="D")
        base = train.iloc[-30:].mean(); np.random.seed(7)
        for nm, off, amp in [("ARIMA",0,2),("SARIMA",-2,4),("HoltWinters",1,5),("Prophet",3,8)]:
            results[nm] = pd.Series(
                base+off+amp*np.sin(2*np.pi*np.arange(horizon)/7)+np.random.normal(0,2,horizon),
                index=future_idx)
        results["Ensemble"] = pd.DataFrame(results).mean(axis=1)
    return pd.DataFrame(results)

# ── Dynamic Insight Engine ────────────────────────────────────────────────────
# ── Intelligent Insight Engine ───────────────────────────────────────────────
def generate_dynamic_insights(
    forecasts,
    train,
    horizon,
    selected_models
):

    if forecasts.empty or not selected_models:

        return []

    insights = []

    # Use Ensemble if available
    base_model = (
        "Ensemble"
        if "Ensemble" in forecasts.columns
        else selected_models[0]
    )

    fc = forecasts[base_model]

    hist_mean = train.mean()

    forecast_mean = fc.mean()

    pct_change = (
        (forecast_mean - hist_mean)
        / hist_mean
    ) * 100

    volatility = fc.std()

    trend = (
        fc.iloc[-1] - fc.iloc[0]
    ) / len(fc)

    peak_day = fc.idxmax().strftime("%b %d")

    peak_value = fc.max()

    # ── Demand vs History ─────────────────────────────────────────
    if pct_change > 5:

        insights.append(
            f"📈 Forecasted demand is expected to increase by "
            f"{pct_change:.1f}% compared to historical averages."
        )

    elif pct_change < -5:

        insights.append(
            f"📉 Demand is projected to decline by "
            f"{abs(pct_change):.1f}% compared to historical levels."
        )

    else:

        insights.append(
            f"➡️ Forecasted demand remains closely aligned with "
            f"historical trends."
        )

    # ── Volatility ────────────────────────────────────────────────
    if volatility > 15:

        insights.append(
            f"⚠️ Demand variability is relatively high "
            f"(σ={volatility:.1f}), indicating possible fluctuations."
        )

    else:

        insights.append(
            f"✅ Forecast variability remains low "
            f"(σ={volatility:.1f}), suggesting stable predictions."
        )

    # ── Peak Demand ───────────────────────────────────────────────
    insights.append(
        f"🚖 Peak demand is expected around {peak_day}, "
        f"with projected bookings reaching approximately "
        f"{peak_value:.0f} rides."
    )

    # ── Trend ─────────────────────────────────────────────────────
    if trend > 0.3:

        insights.append(
            f"📊 Demand shows a gradual upward trajectory "
            f"throughout the forecast horizon."
        )

    elif trend < -0.3:

        insights.append(
            f"📉 Forecasts indicate a mild downward trend over time."
        )

    else:

        insights.append(
            f"📌 Demand trend remains relatively stable "
            f"without major directional changes."
        )

    # ── Recommendation ────────────────────────────────────────────
    if peak_value > hist_mean * 1.05:

        insights.append(
            f"🧠 Recommendation: Increase driver availability "
            f"during forecasted peak periods."
        )

    else:

        insights.append(
            f"🧠 Recommendation: Current operational capacity "
            f"appears sufficient."
        )

    return insights

# ── What-If Simulator ─────────────────────────────────────────────────────────
def render_whatif_simulator(forecasts, train, selected_models):
    st.markdown('<div class="section-header">· What-If Demand Simulator</div>', unsafe_allow_html=True)
    
    col_levers, col_results = st.columns([1, 1])

    with col_levers:
        st.markdown('<div class="whatif-card">', unsafe_allow_html=True)
        st.markdown('<div class="whatif-title">⚙️ Demand Levers</div>', unsafe_allow_html=True)

        demand_shift = st.slider("Overall demand shift (%)", -40, 40, 0, 5)
        seasonal_boost = st.slider("Weekend surge (%)", 0, 50, 0, 5)
        driver_capacity = st.slider("Driver capacity (%)", 50, 150, 100, 10)
        price_scenario = st.selectbox("Pricing", ["No change", "Fare +10%", "Fare -10%", "Surge"], index=0)
        st.markdown('</div>', unsafe_allow_html=True)

    base_model = "Ensemble" if "Ensemble" in forecasts.columns else (selected_models[0] if selected_models else None)
    if base_model is None:
        st.warning("No forecast available to simulate.")
        return

    base_fc = forecasts[base_model].copy()
    adjusted = base_fc * (1 + demand_shift / 100)

    if seasonal_boost > 0:
        adjusted[adjusted.index.dayofweek >= 5] *= (1 + seasonal_boost / 100)

    price_fx = {"No change": 0, "Fare +10%": -0.05, "Fare -10%": 0.07, "Surge": 0.15}
    adjusted *= (1 + price_fx[price_scenario])

    AVG_FARE = 150
    base_total = base_fc.sum()
    adj_total = adjusted.sum()
    delta_book = adj_total - base_total
    delta_pct = (delta_book / base_total) * 100

    with col_results:
        st.markdown('<div class="whatif-card">', unsafe_allow_html=True)
        st.markdown('<div class="whatif-title">📊 Impact</div>', unsafe_allow_html=True)

        dc = "delta-positive" if delta_book >= 0 else "delta-negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Bookings</div>
            <div class="metric-value">{adj_total:,.0f}</div>
            <div class="metric-sub">
                <span class="{dc}">{delta_book:+,.0f} ({delta_pct:+.1f}%)</span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart
    fig_s, ax_s = plt.subplots(figsize=(12, 3.8))
    ax_s.plot(base_fc.index, base_fc.values, color="#3b82f6", lw=1.2, ls="--", label="Baseline", alpha=0.7)
    ax_s.plot(adjusted.index, adjusted.values, color="#10b981", lw=1.8, label="Simulated", alpha=0.95)
    ax_s.fill_between(adjusted.index, base_fc.values, adjusted.values,
                    where=(adjusted.values >= base_fc.values), color="#10b981", alpha=0.12)
    ax_s.fill_between(adjusted.index, base_fc.values, adjusted.values,
                    where=(adjusted.values < base_fc.values), color="#ef4444", alpha=0.12)
    ax_s.set_title("Baseline vs Simulated Demand", fontsize=10, color="#c5cee8")
    ax_s.legend(fontsize=7); ax_s.grid(True, axis="y", alpha=0.3)
    ax_s.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    fig_s.autofmt_xdate()
    st.pyplot(fig_s, use_container_width=True); plt.close()

# ═════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═════════════════════════════════════════════════════════════════════════════

with st.spinner("Loading models and data…"):

    models, load_errors = load_models()

    train, is_synthetic = load_train_data()

    metrics_df = load_model_metrics()
loaded_display_names = [n for n in ["ARIMA","SARIMA","HoltWinters"] if n in models]
if not metrics_df.empty:

    best_model = metrics_df.loc[
        metrics_df["MAPE"].idxmin(),
        "Model"
    ]

    best_mape = metrics_df["MAPE"].min()

else:

    best_model = "N/A"

    best_mape = 0

best_mape = metrics_df["MAPE"].min()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 1.5rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#3b82f6;
                    text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.3rem;">
            RIDE DEMAND FORECAST</div>
        <div style="font-size:1.2rem;font-weight:800;color:#e8f0ff;">Control Panel</div>
    </div>""", unsafe_allow_html=True)

    if is_synthetic:
        st.warning("⚠️ Using synthetic data.\nPlace `rideBookings_preprocessed1.xlsx` in root or `models/`")
    else:
        st.success(f"✅ Real data · {len(train)} days")

    if loaded_display_names:
        st.success(f"✅ Models: {', '.join(loaded_display_names)}")
    else:
        st.warning("⚠️ No models — using smart fallback")

    if load_errors:
        with st.expander("⚠️ Load errors"):
            for k, v in load_errors.items():
                st.caption(f"**{k}**: {v}")

    st.markdown("---")
    horizon = st.slider("Days ahead", 30, 180, 90, 15)
    
    available_models = ["ARIMA","SARIMA","HoltWinters","Prophet","Ensemble"]
    st.markdown("**Models**")
    show = {m: st.checkbox(m, value=(m != "Ensemble")) for m in available_models}
    
    st.markdown("---")
    history_days = st.slider("History days", 30, len(train), min(90, len(train)), 15)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#2d4a7a;line-height:1.8;">
        📅 {train.index[0].date()} → {train.index[-1].date()}<br>
        📊 Days: {len(train)} · Mean: {train.mean():.0f}<br>
        📈 Std: {train.std():.1f} · Min: {train.min():.0f} · Max: {train.max():.0f}
    </div>""", unsafe_allow_html=True)

# ── Generate forecasts ────────────────────────────────────────────────────────
with st.spinner("Generating forecasts…"):
    forecasts = build_forecasts(models, train, horizon)

selected_models = [m for m in available_models if show.get(m) and m in forecasts.columns]

# ── Hero & KPIs ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Demand Forecasting<br>Intelligence Platform</div>
    <div class="hero-sub">Ride Booking Demand · Multi-Model · What-If Analysis</div>
</div>""", unsafe_allow_html=True)

k1,k2,k3,k4,k5 = st.columns(5)
for (label, val, sub), col in zip([
    ("AVG DEMAND", f"{train.mean():.0f}", "bookings/day"),
    ("HORIZON", f"{horizon}d", "ahead"),
    ("MODELS", str(len(loaded_display_names)) or "Fallback", "active"),
    ("BEST MAPE", f"{best_mape:.2f}%", best_model),
    ("DATA PTS", str(len(train)), "days"),
], [k1,k2,k3,k4,k5]):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Forecast", "📊 Comparison", "🔍 Diagnostics", "💡 Insights + Simulator"
])

# ── Tab 1: Forecast View ─────────────────────────────────────────────────────
with tab1:
    col_chart, col_side = st.columns([3,1])
    with col_chart:
        st.markdown('<div class="section-header">· Multi-Model Forecast</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(12,5))
        hist_slice = train.iloc[-history_days:]
        ax.plot(hist_slice.index, hist_slice.values, color="#e8f0ff", lw=1.5, label="History")
        ax.axvline(x=forecasts.index[0], color="#334d80", lw=1, ls="--", alpha=0.7)
        for m in selected_models:
            ax.plot(forecasts.index, forecasts[m], color=MODEL_COLORS.get(m,"#888"),
                lw=2 if m=="Ensemble" else 1.2, label=m, alpha=0.85)
        ax.set_title("Demand Forecast", fontsize=12, color="#c5cee8", pad=15)
        ax.legend(fontsize=8); ax.grid(True, axis="y", alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        fig.autofmt_xdate()
        st.pyplot(fig, use_container_width=True); plt.close()

    with col_side:
        st.markdown('<div class="section-header">· Stats</div>', unsafe_allow_html=True)
        for m in selected_models:
            fc = forecasts[m]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label" style="color:{MODEL_COLORS.get(m,'#888')}">{m}</div>
                <div class="metric-value">{fc.mean():.0f}</div>
                <div class="metric-sub">σ {fc.std():.1f}</div>
            </div>""", unsafe_allow_html=True)

# ── Tab 2: Model Comparison ──────────────────────────────────────────────────
with tab2:
    col_tbl, col_viz = st.columns([1,1])
    with col_tbl:
            with col_tbl:

                # ── Table Header ───────────────────────────────────────────────
                st.markdown("""
                <div class="model-row"
                    style="
                        background:#0f1e3d;
                        font-weight:700;
                        border:1px solid #3b82f6;
                    ">
                    <div class="model-name">MODEL</div>
                    <div class="model-metric">MAE</div>
                    <div class="model-metric">RMSE</div>
                    <div class="model-metric">MAPE%</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Model Rows ─────────────────────────────────────────────────
            for _, row in metrics_df.iterrows():

                model = row["Model"]

                is_best = model == best_model

                badge = '<span class="best-badge">BEST</span>' if is_best else ""

                st.markdown(f"""
                <div class="model-row {'best' if is_best else ''}">
                    <div class="model-name">{model}{badge}</div>
                    <div class="model-metric">{row['MAE']:.2f}</div>
                    <div class="model-metric">{row['RMSE']:.2f}</div>
                    <div class="model-metric">{row['MAPE']:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)
    
    with col_viz:
        fig3, axes3 = plt.subplots(2,2, figsize=(7,5))
        fig3.patch.set_facecolor("#0a0f1e")
        fig3.suptitle("Model Performance", fontsize=10, color="#c5cee8", y=0.98)
        for ax, (metric, label) in zip(axes3.flat, [("MAE","MAE"),("RMSE","RMSE"),("MSE","MSE"),("MAPE","MAPE")]):
            ax.set_facecolor("#0d1428")
            vals = metrics_df[metric].values
            bars = ax.bar(range(len(vals)),
                        vals,
                            color=list(MODEL_COLORS.values())[:len(vals)],
                            alpha=0.8
                        )

                        # Highlight best model
            best_idx = np.argmin(vals)

            bars[best_idx].set_edgecolor("#60a5fa")

            bars[best_idx].set_linewidth(2)

            # Dynamic zoom for better visibility
            min_val = min(vals)

            max_val = max(vals)

            padding = (max_val - min_val) * 0.4

            if padding == 0:
                padding = 1

            ax.set_ylim(
                min_val - padding,
                max_val + padding
            )

            # Add value labels on top of bars
            for bar in bars:

                height = bar.get_height()

                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    height,
                    f"{height:.2f}",
                    ha='center',
                    va='bottom',
                    fontsize=7,
                    color="#c5cee8"
                )

            ax.set_title(label, fontsize=9, color="#7b8fc0")

            ax.set_xticks(range(len(vals)))

            _ = ax.set_xticklabels(
                [m[:4] for m in metrics_df["Model"]],
                rotation=45,
                fontsize=7
            )

            ax.tick_params(axis="y", labelsize=7)

            plt.tight_layout()
        st.pyplot(fig3, use_container_width=True); plt.close()

# ── Tab 3: Diagnostics ───────────────────────────────────────────────────────
with tab3:

    st.markdown(
        '<div class="section-header">· FORECAST DIAGNOSTICS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Demand Behavior & Stability Analysis</div>',
        unsafe_allow_html=True
    )

    # ── Row 1 ─────────────────────────────────────────────────────
    col_d1, col_d2 = st.columns(2)

    # ── Demand Trend ──────────────────────────────────────────────
    with col_d1:

        rolling_mean = train.rolling(14).mean()

        fig_t, ax_t = plt.subplots(figsize=(6,4))

        ax_t.plot(
            train.index,
            train.values,
            color="#3b82f6",
            alpha=0.35,
            label="Daily Demand"
        )

        ax_t.plot(
            rolling_mean.index,
            rolling_mean.values,
            color="#06b6d4",
            linewidth=2,
            label="14-Day Trend"
        )

        ax_t.set_title(
            "Demand Trend Stability",
            color="#c5cee8"
        )

        ax_t.legend(fontsize=8)

        ax_t.grid(True, alpha=0.3)

        st.pyplot(fig_t, use_container_width=True)

        plt.close()

    # ── Volatility ────────────────────────────────────────────────
    with col_d2:

        rolling_std = train.rolling(14).std()

        fig_v, ax_v = plt.subplots(figsize=(6,4))

        ax_v.plot(
            rolling_std.index,
            rolling_std.values,
            color="#f59e0b",
            linewidth=2
        )

        ax_v.fill_between(
            rolling_std.index,
            rolling_std.values,
            alpha=0.15,
            color="#f59e0b"
        )

        ax_v.set_title(
            "Demand Volatility",
            color="#c5cee8"
        )

        ax_v.grid(True, alpha=0.3)

        st.pyplot(fig_v, use_container_width=True)

        plt.close()

    # ── Row 2 ─────────────────────────────────────────────────────
    col_d3, col_d4 = st.columns(2)

    # ── Weekly Seasonality ────────────────────────────────────────
    with col_d3:

        weekly_avg = train.groupby(
            train.index.dayofweek
        ).mean()

        day_names = [
            "Mon","Tue","Wed",
            "Thu","Fri","Sat","Sun"
        ]

        fig_w, ax_w = plt.subplots(figsize=(6,4))

        bars = ax_w.bar(
            day_names,
            weekly_avg.values,
            color=[
                "#3b82f6",
                "#3b82f6",
                "#3b82f6",
                "#3b82f6",
                "#3b82f6",
                "#06b6d4",
                "#06b6d4"
            ],
            alpha=0.85
        )

        best_day = np.argmax(weekly_avg.values)

        bars[best_day].set_edgecolor("#60a5fa")

        bars[best_day].set_linewidth(2)

        ax_w.set_title(
            "Weekly Demand Pattern",
            color="#c5cee8"
        )

        ax_w.grid(axis="y", alpha=0.3)

        st.pyplot(fig_w, use_container_width=True)

        plt.close()

    # ── Distribution ──────────────────────────────────────────────
    with col_d4:

        fig_h, ax_h = plt.subplots(figsize=(6,4))

        ax_h.hist(
            train.values,
            bins=25,
            color="#8b5cf6",
            alpha=0.8,
            edgecolor="#1e3460"
        )

        ax_h.axvline(
            train.mean(),
            color="#f59e0b",
            linewidth=2,
            linestyle="--",
            label=f"Mean = {train.mean():.0f}"
        )

        ax_h.set_title(
            "Demand Distribution",
            color="#c5cee8"
        )

        ax_h.legend(fontsize=8)

        ax_h.grid(True, alpha=0.3)

        st.pyplot(fig_h, use_container_width=True)

        plt.close()

    # ── Insights ──────────────────────────────────────────────────
    st.markdown("""
    <div class="insight-box cyan">
    <strong>Diagnostics Summary:</strong><br>
    • Demand remains relatively stable with moderate volatility.<br>
    • Weekly seasonality patterns are visible across weekends.<br>
    • Distribution appears approximately normal with limited extreme spikes.<br>
    • Forecasting models are expected to remain stable under current demand behavior.
    </div>
    """, unsafe_allow_html=True)

# ── Tab 4: Insights + Simulator ──────────────────────────────────────────────
with tab4:
    st.markdown(
        f'<div class="section-header">· AI Insights <span class="ai-badge">LIVE</span></div>',
        unsafe_allow_html=True,
    )
    
    dyn = generate_dynamic_insights(
    forecasts,
    train,
    horizon,
    selected_models
)

    if dyn:

        for insight in dyn:

            st.markdown(
                f'<div class="insight-box">{insight}</div>',
                unsafe_allow_html=True
            )
    
    st.markdown("<hr style='border-color:#1e3460;margin:2rem 0;'>", unsafe_allow_html=True)
    render_whatif_simulator(forecasts, train, selected_models)

st.markdown(f"""
<div style="text-align:center;font-family:'DM Mono',monospace;font-size:0.7rem;
            color:#4b7db8;padding:1.5rem 0;border-top:1px solid #1e3460;margin-top:2rem;">
    🚀 Demand Forecasting Platform · {train.index[0].year}-{train.index[-1].year}
</div>""", unsafe_allow_html=True)
