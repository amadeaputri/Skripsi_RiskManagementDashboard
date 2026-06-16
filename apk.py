# =========================================
# IMPORT LIBRARY
# =========================================
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

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

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #151d2e;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-red: #ef4444;
    --accent-yellow: #f59e0b;
    --accent-green: #10b981;
    --text-primary: #f1f5f9;
    --text-muted: #94a3b8;
    --border: rgba(59,130,246,0.15);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.08), transparent 35%),
        radial-gradient(circle at bottom right, rgba(6,182,212,0.06), transparent 35%),
        var(--bg-primary);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Title */
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: white !important;
}

/* Metric */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
}

/* Plotly */
[data-testid="stPlotlyChart"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 10px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--border);
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(
        135deg,
        var(--accent-blue),
        var(--accent-cyan)
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem !important;
    font-weight: 700 !important;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(59,130,246,0.3);
}

/* Input */
.stNumberInput input {
    background: var(--bg-card) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

/* Card */
.custom-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 1.2rem;
    border-radius: 14px;
    margin-bottom: 1rem;
}

/* Text */
.small-text {
    color: var(--text-muted);
    font-size: 0.9rem;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================
@st.cache_data
def load_data():
    return pd.read_csv(
        'HASIL_RISK_SCORING_SKALA_1002.csv',
        sep=';'
    )

df = load_data()

# =========================================
# LOAD MODEL
# =========================================
@st.cache_resource
def load_model():
    with open('model_random_forest.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# =========================================
# SIDEBAR
# =========================================
st.sidebar.markdown("""
<h2 style='text-align:center; color:white;'>
PT. BERJAYA MANDIRI INDONESIA
</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.subheader("Filter Data")

# FILTER
list_tahun = ['Semua'] + sorted(df['Tahun'].astype(str).unique().tolist())
selected_tahun = st.sidebar.selectbox('Pilih Tahun', list_tahun)

list_bulan = ['Semua'] + sorted(df['Bulan'].astype(str).unique().tolist())
selected_bulan = st.sidebar.selectbox('Pilih Bulan', list_bulan)

list_supplier = ['Semua'] + sorted(df['Supplier'].astype(str).unique().tolist())
selected_supplier = st.sidebar.selectbox('Pilih Supplier', list_supplier)

st.sidebar.markdown("---")

# MENU BUTTON
halaman = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Prediksi Risiko"]
)

# =========================================
# FILTER DATA
# =========================================
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
# DASHBOARD
# =========================================
if halaman == "Dashboard":

    st.title("RISK MANAGEMENT DASHBOARD")

    st.markdown("---")

    # METRIC
    avg_risk = round(filtered_df['Risk_Score_100'].mean(), 1)
    avg_delay = round(filtered_df['Hari_Keterlambatan'].mean(), 1)
    total_shipments = len(filtered_df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Risk Score", avg_risk)

    with col2:
        st.metric("Average Delay", avg_delay)

    with col3:
        st.metric("Total Shipments", total_shipments)

    st.markdown("")

    # CHARTS
    col4, col5 = st.columns(2)

    with col4:

        st.subheader("Distribusi Risiko")

        risk_count = filtered_df['Kategori_Risiko'].value_counts()

        fig_pie = px.pie(
            values=risk_count.values,
            names=risk_count.index,
            hole=0.55,
            color_discrete_sequence=[
                '#10b981',
                '#f59e0b',
                '#ef4444'
            ]
        )

        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    with col5:

        st.subheader("Trend Risk Score")

        trend_df = filtered_df.groupby(
            'Bulan'
        )['Risk_Score_100'].mean().reset_index()

        fig_line = px.line(
            trend_df,
            x='Bulan',
            y='Risk_Score_100',
            markers=True,
            color_discrete_sequence=['#3b82f6']
        )

        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

    st.markdown("")

    # TABLE
    st.subheader("Detail Data Risiko")

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
# HALAMAN PREDIKSI
# =========================================
if halaman == "Prediksi Risiko":

    st.title("PREDIKSI RISIKO")

    st.markdown("---")

    st.markdown("""
    <div class="custom-card">

    <h3>Petunjuk Pengisian</h3>

    <div class="small-text">

    Sebelum melakukan prediksi, pengguna harus melakukan proses risk scoring terlebih dahulu.

    Input dilakukan menggunakan nilai skor untuk setiap indikator risiko.

    <br><br>

    <b>Keterangan Skor:</b>

    <ul>
    <li>1 = Risiko Rendah</li>
    <li>2 = Risiko Sedang</li>
    <li>3 = Risiko Tinggi</li>
    </ul>

    <b>Indikator Risiko:</b>

    <ul>
    <li>Keterlambatan Pengiriman</li>
    <li>Durasi Bea Cukai</li>
    <li>Kelengkapan Dokumen</li>
    <li>Status Monitoring</li>
    <li>Deviasi Estimasi</li>
    <li>Durasi Klarifikasi</li>
    </ul>

    </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        skor_keterlambatan = st.number_input(
            'Skor Keterlambatan',
            min_value=1,
            max_value=3,
            value=1
        )

        skor_bea = st.number_input(
            'Skor Bea Cukai',
            min_value=1,
            max_value=3,
            value=1
        )

    with col2:

        skor_dokumen = st.number_input(
            'Skor Dokumen',
            min_value=0,
            max_value=2,
            value=0
        )

        skor_monitoring = st.number_input(
            'Skor Monitoring',
            min_value=0,
            max_value=2,
            value=0
        )

    with col3:

        skor_deviasi = st.number_input(
            'Skor Deviasi',
            min_value=1,
            max_value=3,
            value=1
        )

        skor_klarifikasi = st.number_input(
            'Skor Klarifikasi',
            min_value=1,
            max_value=3,
            value=1
        )

    st.markdown("")

    # PREDIKSI
    if st.button("⚡ Prediksi Risiko"):

        input_data = pd.DataFrame([[
            skor_keterlambatan,
            skor_bea,
            skor_dokumen,
            skor_monitoring,
            skor_deviasi,
            skor_klarifikasi
        ]], columns=[
            'Skor_Keterlambatan',
            'Skor_Bea_Cukai',
            'Skor_Dokumen',
            'Skor_Monitoring',
            'Skor_Deviasi',
            'Skor_Klarifikasi'
        ])

        prediksi = model.predict(input_data)[0]

        kelas = {
            0: 'High',
            1: 'Low',
            2: 'Medium'
        }

        hasil = kelas.get(prediksi, prediksi)

        st.markdown("---")

        # HASIL
        if hasil == "High":

            st.error("⚠️ Risiko Tinggi (High Risk)")

            st.markdown("""
            <div class="custom-card">

            <h3>Rekomendasi Mitigasi</h3>

            <div class="small-text">

            • Segera lakukan evaluasi terhadap proses impor<br>
            • Tingkatkan monitoring supply chain secara berkala<br>
            • Pastikan dokumen impor lengkap dan valid<br>
            • Lakukan koordinasi dengan supplier dan bea cukai<br>
            • Minimalkan keterlambatan klarifikasi dokumen<br>
            • Siapkan alternatif supplier apabila risiko meningkat

            </div>

            </div>
            """, unsafe_allow_html=True)

        elif hasil == "Medium":

            st.warning("🟡 Risiko Sedang (Medium Risk)")

            st.markdown("""
            <div class="custom-card">

            <h3>Rekomendasi Mitigasi</h3>

            <div class="small-text">

            • Lakukan monitoring secara rutin<br>
            • Evaluasi potensi keterlambatan pengiriman<br>
            • Tingkatkan akurasi estimasi pengiriman<br>
            • Pastikan proses dokumen berjalan sesuai prosedur

            </div>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.success("✅ Risiko Rendah (Low Risk)")

            st.markdown("""
            <div class="custom-card">

            <h3>Rekomendasi Mitigasi</h3>

            <div class="small-text">

            • Pertahankan performa supply chain<br>
            • Lakukan monitoring berkala<br>
            • Pastikan stabilitas proses impor tetap terjaga

            </div>

            </div>
            """, unsafe_allow_html=True)