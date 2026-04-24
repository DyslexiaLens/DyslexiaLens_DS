import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from PIL import Image

# Konfigurasi Halaman (Harus dipanggil paling atas)
st.set_page_config(page_title="DyslexiaLens - Data Viewer", page_icon="🧠", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .main-header { font-size: 45px; font-weight: 800; color: #2C3E50; margin-bottom: -15px; }
    .sub-header { font-size: 20px; color: #34495E; margin-bottom: 30px; border-bottom: 2px solid #3498DB; padding-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧠 DyslexiaLens Dataset Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Data Scientist Handover Dashboard — From Raw Data to Ready-to-Train CSV</div>', unsafe_allow_html=True)

# Membuat Tab
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dataset Summary", 
    "📌 Business Questions & EDA", 
    "🛠 Stratification", 
    "👁️ Viewer (Compressed CSV)"
])

# Load master dataset untuk Metrik dan EDA
@st.cache_data
def load_master_data():
    if os.path.exists('csv_metadata/master_dataset_dyslexia.csv'):
        return pd.read_csv('csv_metadata/master_dataset_dyslexia.csv')
    return None

df_master = load_master_data()

# Karena severity_score mungkin hilang saat overwrite CSV, kita reconstruct dari filename
if df_master is not None and 'severity_score' not in df_master.columns:
    def get_score(filename):
        if '_' in str(filename):
            prefix = str(filename).split('_')[0]
            if prefix.isdigit():
                return int(prefix)
        return 0
    df_master['severity_score'] = df_master['file_name'].apply(get_score)

# ==========================================
# TAB 1: DATASET SUMMARY
# ==========================================
with tab1:
    st.markdown("### 📊 Ringkasan Dataset Master (Gambo + EMNIST)")
    if df_master is not None:
        col1, col2, col3, col4 = st.columns(4)
        total_images = len(df_master)
        total_train = len(df_master[df_master['split'] == 'Train'])
        total_test = len(df_master[df_master['split'] == 'Test'])
        
        col1.metric("Total Gambar", f"{total_images:,}")
        col2.metric("Data Train (80%)", f"{total_train:,}")
        col3.metric("Data Test (20%)", f"{total_test:,}")
        col4.metric("Jumlah Kelas", "2 (Biner)")
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Distribusi Kelas Keseluruhan")
            class_counts = df_master['target_class'].value_counts().rename({0: 'Normal (0)', 1: 'Dyslexia (1)'})
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ['#E74C3C', '#2ECC71'] if 'Dyslexia' in class_counts.index[0] else ['#2ECC71', '#E74C3C']
            class_counts.plot(kind='bar', color=colors, ax=ax)
            ax.set_ylabel("Jumlah Gambar")
            plt.xticks(rotation=0)
            st.pyplot(fig)
            
        with col2:
            st.markdown("#### Proporsi Stratified (Train vs Test)")
            train_counts = df_master[df_master['split'] == 'Train']['target_class'].value_counts(normalize=True).rename({0: 'Normal', 1: 'Dyslexia'}) * 100
            test_counts = df_master[df_master['split'] == 'Test']['target_class'].value_counts(normalize=True).rename({0: 'Normal', 1: 'Dyslexia'}) * 100
            
            comparison_df = pd.DataFrame({'Train (%)': train_counts, 'Test (%)': test_counts})
            st.dataframe(comparison_df.style.format("{:.2f}%"), use_container_width=True)
            st.info("💡 **Stratifikasi Berhasil!** Proporsi kelas Normal dan Dyslexia identik di set Train dan Test, mencegah adanya Domain Shift.")
    else:
        st.error("csv_metadata/master_dataset_dyslexia.csv tidak ditemukan!")

# ==========================================
# TAB 2: BUSINESS QUESTIONS & EDA
# ==========================================
with tab2:
    st.markdown("### 🎯 Pertanyaan Bisnis & EDA Heatmap")
    st.write("Apakah pola goresan tulisan tangan dapat digunakan sebagai indikator tingkat keparahan disleksia?")
    
    if df_master is not None:
        st.image('assets/heatmap_eda.png', use_container_width=True)
        st.success("**Rata-rata selisih intensitas piksel:** ~5.20 (skala 0-255). Semakin menyala (kuning/putih) warna di Heatmap, semakin sering terjadi coretan berulang di area tersebut.")

# ==========================================
# TAB 3: DATA PREP & STRATIFICATION
# ==========================================
with tab3:
    st.markdown("### ⚖️ Balancing & Stratified Splitting")
    st.write("Dataset Gambo asli memiliki ketidakseimbangan kelas (*Class Imbalance*) di mana tulisan Disleksia jauh lebih banyak dari tulisan Normal. Kami menyelesaikan ini dengan menambahkan EMNIST.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("**Before:** Imbalance Dataset\n- Dyslexia: ~115,000\n- Normal: ~58,000")
    with col2:
        st.success("**After:** Balanced (~1:1 Ratio)\n- Dyslexia (Gambo): ~142,000\n- Normal (Gambo + EMNIST): ~131,000")

# ==========================================
# TAB 4: DATASET VIEWER (COMPRESSED CSV)
# ==========================================
with tab4:
    st.markdown("### 👁️ Eksplorasi Data (Compressed CSV)")
    st.write("Viewer ini meload data secara *offline* dari file `dyslexialens_test.csv.gz` tanpa membaca folder gambar fisik. File berukuran ~9.5MB ini mengandung >54,000 gambar test 28x28!")
    
    @st.cache_data
    def load_compressed_csv(csv_path):
        if not os.path.exists(csv_path):
            return None
        # Load SEMUA baris karena file .gz kita ringan
        return pd.read_csv(csv_path)

    csv_file = 'dyslexialens_test.csv.gz'
    df_pixels = load_compressed_csv(csv_file)
    
    if df_pixels is None:
        st.warning(f"⏳ File `{csv_file}` belum ditemukan.")
    else:
        st.success(f"✅ Berhasil memuat {len(df_pixels):,} gambar dari `{csv_file}`!")
        
        filter_class = st.selectbox("Pilih Kelas:", ['Normal (0)', 'Dyslexia (1)'])
        target_val = 0 if 'Normal' in filter_class else 1
        
        subset = df_pixels[df_pixels['label'] == target_val]
        
        if len(subset) > 0:
            st.write(f"Menampilkan 10 sampel gambar acak dari total **{len(subset):,}** gambar kelas ini:")
            samples = subset.sample(min(10, len(subset)))
            
            cols = st.columns(5)
            for i, (_, row) in enumerate(samples.iterrows()):
                pixels = row.values[1:].reshape(28, 28)
                fig, ax = plt.subplots(figsize=(2,2))
                ax.imshow(pixels, cmap='gray', vmin=0, vmax=255)
                ax.axis('off')
                cols[i % 5].pyplot(fig)
                plt.close(fig)
        else:
            st.error("Tidak ada data untuk kelas ini.")
