import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN (UI/UX)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Analytics E-Commerce | UTS Visdat",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .insight-box {
        background-color: #eef6ff;
        padding: 15px;
        border-left: 5px solid #1e88e5;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LOAD DATASET KAGGLE
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Membaca file CSV dengan pemisah titik koma (;)
    df = pd.read_csv('data/ecommerce sales Dataset.csv', sep=';')
    return df

df_raw = load_data()

# ---------------------------------------------------------
# 3. FILTER INTERAKTIF
# ---------------------------------------------------------
st.sidebar.title("🎛️ Filter Data")
st.sidebar.markdown("---")

# Filter 1: Kategori Produk
categories = df_raw['Product_Category'].dropna().unique().tolist() if 'Product_Category' in df_raw.columns else []
selected_category = st.sidebar.multiselect(
    "Kategori Produk",
    options=categories,
    default=categories
)

# Filter 2: Wilayah (State)
states = df_raw['State'].dropna().unique().tolist() if 'State' in df_raw.columns else []
selected_state = st.sidebar.multiselect(
    "Wilayah (State)",
    options=states,
    default=states
)

# Penerapan Filter
filtered_df = df_raw[
    (df_raw['Product_Category'].isin(selected_category)) &
    (df_raw['State'].isin(selected_state))
]

# ---------------------------------------------------------
# 4. HEADER & KPI CARDS
# ---------------------------------------------------------
st.title("📊 Executive Sales & Customer Analytics Dashboard")
st.caption("Projek Ujian Tengah Semester — Mata Kuliah Visualisasi Data (UNSURYA)")
st.markdown("---")

if filtered_df.empty:
    st.warning("⚠️ Data tidak ditemukan untuk kombinasi filter ini.")
    st.stop()

total_orders = filtered_df['Order_ID'].nunique() if 'Order_ID' in filtered_df.columns else len(filtered_df)
total_customers = filtered_df['Customer_ID'].nunique() if 'Customer_ID' in filtered_df.columns else 0
total_categories = filtered_df['Product_Category'].nunique() if 'Product_Category' in filtered_df.columns else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Transaksi", f"{total_orders:,}".replace(",", "."))
with col2:
    st.metric("Total Pelanggan", f"{total_customers:,}".replace(",", "."))
with col3:
    st.metric("Variasi Kategori", f"{total_categories} Kategori")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. STORYTELLING & ANALISIS WAWASAN
# ---------------------------------------------------------
st.markdown("""
<div class="insight-box">
    <h4>💡 Wawasan Utama (Executive Insights):</h4>
    <ul>
        <li><b>Kategori Dominan:</b> Kategori <i>Electronics</i> dan <i>Beauty</i> mencatatkan frekuensi pesanan tertinggi.</li>
        <li><b>Sebaran Wilayah:</b> Konsentrasi pelanggan terbesar berasal dari negara bagian dengan pusat perkotaan utama.</li>
        <li><b>Diversifikasi Produk:</b> Tingginya variasi produk memberikan kontribusi positif terhadap loyalitas basis pelanggan.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. VARIASI BAGAN / CHARTS
# ---------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("1. Distribusi Pesanan per Kategori (Bar Chart)")
    df_cat = filtered_df['Product_Category'].value_counts().reset_index()
    df_cat.columns = ['Product_Category', 'Jumlah_Pesanan']
    
    fig_bar = px.bar(
        df_cat, x='Jumlah_Pesanan', y='Product_Category', orientation='h',
        labels={'Jumlah_Pesanan': 'Total Pesanan', 'Product_Category': 'Kategori'},
        color='Jumlah_Pesanan',
        color_continuous_scale='Blues',
        template='plotly_white'
    )
    st.plotly_chart(fig_bar, width='stretch')

with c2:
    st.subheader("2. Proporsi Pesanan per Wilayah/State (Donut Chart)")
    df_state = filtered_df['State'].value_counts().head(5).reset_index()
    df_state.columns = ['State', 'Jumlah_Pesanan']
    
    fig_pie = px.pie(
        df_state, values='Jumlah_Pesanan', names='State',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, width='stretch')

c3, c4 = st.columns(2)

with c3:
    st.subheader("3. Top 10 Produk Terlaris (Bar Chart)")
    df_prod = filtered_df['Product_Name'].value_counts().head(10).reset_index()
    df_prod.columns = ['Product_Name', 'Jumlah_Pesanan']
    
    fig_top = px.bar(
        df_prod, x='Product_Name', y='Jumlah_Pesanan',
        labels={'Product_Name': 'Nama Produk', 'Jumlah_Pesanan': 'Total Pesanan'},
        color='Jumlah_Pesanan',
        color_continuous_scale='Greens',
        template='plotly_white'
    )
    st.plotly_chart(fig_top, width='stretch')

with c4:
    st.subheader("4. Sebaran Pesanan Berdasarkan Kota (Treemap)")
    df_city = filtered_df.groupby(['State', 'City']).size().reset_index(name='Jumlah')
    
    fig_tree = px.treemap(
        df_city, path=['State', 'City'], values='Jumlah',
        color='Jumlah',
        color_continuous_scale='Viridis',
        template='plotly_white'
    )
    st.plotly_chart(fig_tree, width='stretch')

# ---------------------------------------------------------
# 7. TABEL DATA MENTAH
# ---------------------------------------------------------
with st.expander("🔍 Lihat Data Mentah"):
    st.dataframe(filtered_df, width='stretch')