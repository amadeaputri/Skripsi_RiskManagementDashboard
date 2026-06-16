# =========================================
# IMPORT LIBRARY
# =========================================
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title='Risk Management Dashboard',
    page_icon='📊',
    layout='wide'
)

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.cdnfonts.com/css/geist-sans');

/* ========================================
ROOT COLORS
======================================== */
:root {
    --bg-primary:    #f5f7ff;
    --bg-secondary:  #ffffff;
    --bg-card:       #ffffff;

    --primary:       #4B49AC;
    --secondary:     #98BDFF;

    --support-1:     #7DA0FA;
    --support-2:     #7978E9;
    --support-3:     #F3797E;

    --text-primary:  #1e293b;
    --text-muted:    #64748b;

    --border:        rgba(75,73,172,0.12);
    --shadow:        rgba(75,73,172,0.08);
}

/* ========================================
GLOBAL
======================================== */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background: var(--bg-primary) !important;
}

/* ========================================
MAIN CONTAINER
======================================== */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* ========================================
SIDEBAR
======================================== */
section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e5e7eb !important;
}

section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ========================================
SIDEBAR TITLE
======================================== */
section[data-testid="stSidebar"] h1 {
    font-family: 'Geist Sans', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    color: var(--primary) !important;
}

/* ========================================
RADIO HIDE
======================================== */
section[data-testid="stSidebar"] input[type="radio"] {
    display: none !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* ========================================
MENU NAVIGATION
======================================== */

/* Wrapper radiogroup */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.8rem !important;
    align-items: center !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Setiap item radio — cover semua kemungkinan selector Streamlit */
section[data-testid="stSidebar"] div[role="radiogroup"] > div {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"],
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    width: 90% !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    box-sizing: border-box !important;

    background: #f8faff !important;
    border: 1px solid transparent !important;
    border-radius: 12px !important;

    padding: 0.9rem 1rem !important;
    margin: 0 auto !important;

    transition: all 0.25s ease !important;
    cursor: pointer !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover,
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #eef2ff !important;
    transform: translateY(-2px) !important;
}

/* Teks label */
section[data-testid="stSidebar"] label[data-baseweb="radio"] p,
section[data-testid="stSidebar"] label[data-baseweb="radio"] div,
section[data-testid="stSidebar"] label[data-baseweb="radio"] span,
section[data-testid="stSidebar"] div[role="radiogroup"] label p,
section[data-testid="stSidebar"] div[role="radiogroup"] label div,
section[data-testid="stSidebar"] div[role="radiogroup"] label span {
    color: #4b5563 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    text-align: center !important;
    white-space: nowrap !important;
    width: 100% !important;
}

/* State aktif / checked */
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked),
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: var(--primary) !important;
    box-shadow: 0 6px 18px rgba(75,73,172,0.18) !important;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p,
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) div,
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) span,
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) div,
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span {
    color: white !important;
}

/* ========================================
TITLE
======================================== */
h1 {
    font-family: 'Geist Sans', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--primary) !important;
}

/* ========================================
SUBHEADER
======================================== */
h2, h3 {
    color: #6b7280 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ========================================
FILTER LABEL
======================================== */
.stSelectbox label,
.stSubheader {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-weight: 700 !important;
}

/* ========================================
METRIC CARD
======================================== */
[data-testid="stMetric"] {
    background: white !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 1.3rem !important;

    color: #1e293b !important;

    box-shadow:
        0 4px 20px rgba(15,23,42,0.04),
        0 1px 3px rgba(15,23,42,0.08);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    transition: 0.2s ease;
}

/* ========================================
METRIC TEXT
======================================== */
[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    color: #1e293b !important;
}

/* ========================================
CHART CARD
======================================== */
[data-testid="stPlotlyChart"] {
    background: white !important;
    border-radius: 18px !important;
    padding: 1rem !important;

    box-shadow:
        0 4px 20px rgba(15,23,42,0.04),
        0 1px 3px rgba(15,23,42,0.08);
}

/* ========================================
PLOTLY TEXT
======================================== */
.plotly .gtitle,
.plotly text {
    fill: #475569 !important;
}

/* ========================================
TABLE
======================================== */
[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 18px !important;
    overflow: hidden;
    border: none !important;

    box-shadow:
        0 4px 20px rgba(15,23,42,0.04),
        0 1px 3px rgba(15,23,42,0.08);
}

[data-testid="stDataFrame"] * {
    color: #334155 !important;
}

/* ========================================
INPUT
======================================== */
.stNumberInput input,
.stSelectbox > div > div {
    background: white !important;
    border: 1px solid #dbe4ff !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ========================================
SIDEBAR BUTTON — FIX CENTERING
======================================== */
section[data-testid="stSidebar"] .stButton {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stButton"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 90% !important;
    margin: 0 auto !important;
}

/* ========================================
BUTTON (GLOBAL)
======================================== */
.stButton > button {
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--support-2)
    ) !important;

    border: none !important;
    border-radius: 12px !important;

    color: white !important;
    -webkit-text-fill-color: white !important;

    font-weight: 700 !important;
    font-size: 0.95rem !important;

    width: 100%;
    padding: 0.9rem !important;

    box-shadow: 0 8px 20px rgba(75,73,172,0.18);

    transition: all 0.25s ease;
}

.stButton > button * {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* ========================================
SUCCESS ALERT
======================================== */
[data-testid="stAlert"] {
    border-radius: 14px !important;
}

/* ========================================
TEXT FIX
======================================== */
.stMarkdown,
.stText,
p {
    color: #334155 !important;
}

/* ========================================
SCROLLBAR
======================================== */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 10px;
}

/* ========================================
TEMPLATE BOX
======================================== */
.template-box {
    background: #f8faff;
    border: 1px solid #dbe4ff;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    line-height: 1.8;
}

.template-box code {
    background: #eef2ff;
    color: #4B49AC;
    padding: 0.15rem 0.45rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# CONSTANTS
# =========================================
FEATURE_COLS = ['Risk_Score_100']

REQUIRED_COLS = ['Risk_Score_100']

# Mapping label kelas dari output model
# Model sudah return string langsung: 'Low Risk', 'Medium Risk', 'High Risk'
KELAS = {
    0: 'Low Risk',
    1: 'Medium Risk',
    2: 'High Risk',
}

# =========================================
# LOAD DATA
# =========================================
@st.cache_data
def load_data():
    df = pd.read_csv('HASIL_RISK_SCORING.csv', sep=';')
    return df

df = load_data()

# =========================================
# LOAD MODEL
# =========================================
@st.cache_resource
def load_model():
    with open('model_random_forest_100.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# =========================================
# SIDEBAR
# =========================================
st.sidebar.markdown("""
<h1>
PT. BERJAYA<br>
MANDIRI INDONESIA
</h1>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# =========================================
# MENU
# =========================================
menu = st.sidebar.radio(
    "Menu",
    ["📊 Dashboard", "⚡ Prediksi Risiko"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# =========================================
# DASHBOARD
# =========================================
if menu == "📊 Dashboard":

    st.sidebar.subheader("Filter Data")

    # FILTER
    list_tahun = ['Semua'] + sorted(df['Tahun'].astype(str).unique().tolist())
    selected_tahun = st.sidebar.selectbox('Pilih Tahun', list_tahun)

    list_bulan = ['Semua'] + sorted(df['Bulan'].astype(str).unique().tolist())
    selected_bulan = st.sidebar.selectbox('Pilih Bulan', list_bulan)

    list_supplier = ['Semua'] + sorted(df['Supplier'].astype(str).unique().tolist())
    selected_supplier = st.sidebar.selectbox('Pilih Supplier', list_supplier)

    # FILTER DATA
    filtered_df = df.copy()

    if selected_tahun != 'Semua':
        filtered_df = filtered_df[
            filtered_df['Tahun'].astype(str) == selected_tahun
        ]

    if selected_bulan != 'Semua':
        filtered_df = filtered_df[
            filtered_df['Bulan'].astype(str) == selected_bulan
        ]

    if selected_supplier != 'Semua':
        filtered_df = filtered_df[
            filtered_df['Supplier'] == selected_supplier
        ]

    # =========================================
    # PLOTLY LAYOUT
    # =========================================
    PLOTLY_LAYOUT = dict(
        template='simple_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Plus Jakarta Sans',
            color='#475569',
            size=12
        ),
        margin=dict(l=10, r=10, t=10, b=10)
    )

    # =========================================
    # HEADER
    # =========================================
    st.title('RISK MANAGEMENT DASHBOARD')
    st.markdown('---')

    # =========================================
    # METRICS
    # =========================================
    avg_risk = round(filtered_df['Risk_Score_100'].mean(), 1)
    avg_delay = round(filtered_df['Hari_Keterlambatan'].mean(), 1)
    total_shipments = len(filtered_df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Risk Score", avg_risk)

    with col2:
        st.metric("Average Delay (Days)", avg_delay)

    with col3:
        st.metric("Total Shipments", total_shipments)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================
    # ROW 1
    # =========================================
    col4, col5 = st.columns([1, 2])

    with col4:
        st.subheader('Distribusi Risiko')

        risk_count = filtered_df['Kategori_Risiko'].value_counts()

        fig_pie = px.pie(
            values=risk_count.values,
            names=risk_count.index,
            hole=0.55,
            color_discrete_sequence=[
                '#4B49AC',
                '#F3797E',
                '#7DA0FA'
            ]
        )

        fig_pie.update_layout(**PLOTLY_LAYOUT)

        st.plotly_chart(fig_pie, use_container_width=True)

    with col5:
        st.subheader('Trend Risk Score')

        trend_df = (
            filtered_df
            .groupby('Bulan')['Risk_Score_100']
            .mean()
            .reset_index()
        )

        fig_line = px.line(
            trend_df,
            x='Bulan',
            y='Risk_Score_100',
            markers=True,
            color_discrete_sequence=['#7978E9']
        )

        fig_line.update_layout(**PLOTLY_LAYOUT)

        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================
    # ROW 2
    # =========================================
    col6, col7 = st.columns(2)

    with col6:
        st.subheader('Top Supplier Risiko')

        supplier_risk = (
            filtered_df.groupby('Supplier')['Risk_Score_100']
            .mean()
            .sort_values(ascending=True)
            .tail(5)
        )

        fig_bar = px.bar(
            x=supplier_risk.values,
            y=supplier_risk.index,
            orientation='h',
            color=supplier_risk.values,
            color_continuous_scale=[
                '#98BDFF',
                '#4B49AC'
            ],
            labels={'x': 'Risk Score', 'y': 'Supplier'}
        )

        fig_bar.update_coloraxes(showscale=False)
        fig_bar.update_layout(**PLOTLY_LAYOUT)

        st.plotly_chart(fig_bar, use_container_width=True)

    with col7:
        st.subheader('Penyebab Keterlambatan')

        alasan_count = (
            filtered_df['Alasan_Keterlambatan']
            .value_counts()
            .head(5)
        )

        fig_alasan = px.bar(
            x=alasan_count.values,
            y=alasan_count.index,
            orientation='h',
            color=alasan_count.values,
            color_continuous_scale=[
                '#7DA0FA',
                '#7978E9'
            ],
            labels={'x': 'Jumlah', 'y': 'Alasan Keterlambatan'}
        )

        fig_alasan.update_coloraxes(showscale=False)
        fig_alasan.update_layout(**PLOTLY_LAYOUT)

        st.plotly_chart(fig_alasan, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================
    # TABLE
    # =========================================
    st.subheader('Detail Data Risiko')

    show_columns = [
        'Tahun',
        'Bulan',
        'Supplier',
        'Negara_Asal',
        'Hari_Keterlambatan',
        'Risk_Score_100',
        'Kategori_Risiko'
    ]

    st.dataframe(
        filtered_df[show_columns],
        use_container_width=True
    )

# =========================================
# PREDIKSI RISIKO
# =========================================
if menu == "⚡ Prediksi Risiko":

    st.title('PREDIKSI RISIKO')
    st.markdown('---')

    st.info(
        "Upload file CSV atau Excel yang sudah memiliki kolom "
        "**Risk_Score_100** untuk mendapatkan prediksi kategori risiko dari model."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================
    # FORMAT INFO
    # =========================================
    st.markdown("""
    <div class="template-box">
        <strong style="color:#4B49AC;">📌 Format File yang Diperlukan</strong><br><br>
        <span style="font-size:0.85rem;color:#475569;">
        File CSV atau Excel wajib memiliki kolom <code>Risk_Score_100</code> sebagai input prediksi model
        (nama kolom harus <em>persis sama</em>):
        </span>
        <br><br>
        <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
            <thead>
                <tr style="border-bottom:2px solid #dbe4ff;">
                    <th style="text-align:left;padding:0.5rem 0.8rem;color:#4B49AC;">Nama Kolom</th>
                    <th style="text-align:left;padding:0.5rem 0.8rem;color:#4B49AC;">Nilai yang Valid</th>
                    <th style="text-align:left;padding:0.5rem 0.8rem;color:#4B49AC;">Keterangan</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding:0.5rem 0.8rem;"><code>Risk_Score_100</code></td>
                    <td style="padding:0.5rem 0.8rem;color:#64748b;">0 – 100</td>
                    <td style="padding:0.5rem 0.8rem;color:#64748b;">Skor risiko hasil perhitungan — digunakan model untuk memprediksi kategori</td>
                </tr>
            </tbody>
        </table>
        <br>
        <span style="font-size:0.8rem;color:#94a3b8;">
        💡 Kolom tambahan seperti <code>Nama_Supplier</code>, <code>Tahun</code>, <code>Bulan</code>, dll. boleh disertakan dan akan ikut tampil di hasil prediksi.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================
    # FILE UPLOADER
    # =========================================
    uploaded_file = st.file_uploader(
        'Upload file CSV atau Excel (.xlsx / .xls)',
        type=['csv', 'xlsx', 'xls'],
        help='Maksimum 200 MB per file'
    )

    if uploaded_file is not None:
        try:
            # Baca file
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext == 'csv':
                try:
                    upload_df = pd.read_csv(uploaded_file, sep=';')
                    if upload_df.shape[1] == 1:
                        uploaded_file.seek(0)
                        upload_df = pd.read_csv(uploaded_file, sep=',')
                except Exception:
                    uploaded_file.seek(0)
                    upload_df = pd.read_csv(uploaded_file, sep=',')
            else:
                upload_df = pd.read_excel(uploaded_file)

            # Normalkan nama kolom
            col_map = {col: col.strip().replace(' ', '_') for col in upload_df.columns}
            upload_df = upload_df.rename(columns=col_map)

            # Cek kolom wajib
            missing_cols = [c for c in REQUIRED_COLS if c not in upload_df.columns]

            if missing_cols:
                st.error(
                    f"❌ Kolom berikut tidak ditemukan: **{', '.join(missing_cols)}**\n\n"
                    "Pastikan nama kolom persis seperti tabel di atas."
                )
            else:
                st.success(f"✅ File berhasil dibaca — **{len(upload_df)} baris** ditemukan.")

                with st.expander("👁️ Preview Data yang Diupload", expanded=True):
                    st.dataframe(upload_df, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)
                _, btn_col, _ = st.columns([1, 1, 1])
                with btn_col:
                    run_batch = st.button('⚡ Jalankan Prediksi Batch', key='btn_batch')

                if run_batch:
                    # Validasi range Risk_Score_100
                    invalid_rs = upload_df[
                        (upload_df['Risk_Score_100'] < 0) | (upload_df['Risk_Score_100'] > 100)
                    ]
                    if not invalid_rs.empty:
                        st.warning(
                            f"⚠️ Kolom **Risk_Score_100**: {len(invalid_rs)} baris di luar rentang 0–100. "
                            "Baris tersebut tetap diproses."
                        )

                    # Prediksi pakai model (input: Risk_Score_100)
                    preds = model.predict(upload_df[FEATURE_COLS])
                    result_df = upload_df.copy()
                    result_df['Prediksi_Kategori'] = preds

                    # Susun kolom: kolom lain → Risk_Score_100 → Prediksi_Kategori
                    other_cols = [
                        c for c in result_df.columns
                        if c not in ['Risk_Score_100', 'Prediksi_Kategori']
                    ]
                    display_cols = other_cols + ['Risk_Score_100', 'Prediksi_Kategori']
                    result_df = result_df[display_cols]

                    # ── Hasil ──
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.subheader("📊 Hasil Prediksi Batch")
                    st.dataframe(result_df, use_container_width=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Summary metrics ──
                    total   = len(result_df)
                    low_n   = (result_df['Prediksi_Kategori'] == 'Low Risk').sum()
                    med_n   = (result_df['Prediksi_Kategori'] == 'Medium Risk').sum()
                    high_n  = (result_df['Prediksi_Kategori'] == 'High Risk').sum()
                    avg_rs  = round(result_df['Risk_Score_100'].mean(), 1)

                    m1, m2, m3, m4, m5 = st.columns(5)
                    m1.metric("Total Data", total)
                    m2.metric("Avg Risk Score", avg_rs)
                    m3.metric("Low Risk", low_n)
                    m4.metric("Medium Risk", med_n)
                    m5.metric("High Risk", high_n)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Distribusi & visualisasi ──
                    dist_col1, dist_col2 = st.columns([1, 2])

                    with dist_col1:
                        st.subheader("Distribusi Hasil")
                        dist = result_df['Prediksi_Kategori'].value_counts().reset_index()
                        dist.columns = ['Kategori', 'Jumlah']
                        st.dataframe(dist, use_container_width=True, hide_index=True)

                    with dist_col2:
                        st.subheader("Visualisasi Distribusi")
                        fig_dist = px.pie(
                            dist, values='Jumlah', names='Kategori', hole=0.5,
                            color='Kategori',
                            color_discrete_map={
                                'Low Risk':    '#F3797E',
                                'Medium Risk': '#7DA0FA',
                                'High Risk':   '#4B49AC'
                            }
                        )
                        fig_dist.update_layout(
                            template='simple_white',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(family='Plus Jakarta Sans', color='#475569', size=12),
                            margin=dict(l=10, r=10, t=10, b=10)
                        )
                        st.plotly_chart(fig_dist, use_container_width=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Download hasil ──
                    csv_result = result_df.to_csv(index=False).encode('utf-8')
                    dl_col, _ = st.columns([1, 3])
                    with dl_col:
                        st.download_button(
                            label='⬇️  Unduh Hasil Prediksi (CSV)',
                            data=csv_result,
                            file_name='hasil_prediksi_risiko.csv',
                            mime='text/csv'
                        )

        except Exception as e:
            st.error(f"❌ Gagal membaca file: {e}")
