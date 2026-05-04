import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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

# ==========================================
# SIDEBAR: PEMILIHAN DATASET
# ==========================================
st.sidebar.title("⚙️ Pengaturan Dataset")
dataset_choice = st.sidebar.radio(
    "Pilih Sumber Dataset:",
    ["Dataset Tanpa Augmentasi (Original Gambo)", "Dataset Dengan Augmentasi (Gambo + EMNIST)"]
)

if dataset_choice == "Dataset Dengan Augmentasi (Gambo + EMNIST)":
    csv_path = 'csv_metadata/Dataset_Dyslexia_EMNIST.csv'
else:
    csv_path = 'csv_metadata/Dataset_Dyslexia_NoAugmentation.csv'

st.sidebar.info(f"**File Aktif:**\n`{csv_path}`")

# Load master dataset untuk Metrik dan EDA
@st.cache_data
def load_master_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data
def load_compressed_csv(path):
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

df_master = load_master_data(csv_path)

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
            try:
                colors = ['#E74C3C', '#2ECC71'] if 'Dyslexia' in str(class_counts.index[0]) else ['#2ECC71', '#E74C3C']
                class_counts.plot(kind='bar', color=colors, ax=ax)
                ax.set_ylabel("Jumlah Gambar")
                ax.tick_params(axis='x', rotation=0)
                st.pyplot(fig)
            finally:
                plt.close(fig)
            
        with col2:
            st.markdown("#### Proporsi Stratified (Train vs Test)")
            train_counts = df_master[df_master['split'] == 'Train']['target_class'].value_counts(normalize=True).rename({0: 'Normal', 1: 'Dyslexia'}) * 100
            test_counts = df_master[df_master['split'] == 'Test']['target_class'].value_counts(normalize=True).rename({0: 'Normal', 1: 'Dyslexia'}) * 100
            
            comparison_df = pd.DataFrame({'Train (%)': train_counts, 'Test (%)': test_counts})
            st.dataframe(comparison_df.style.format("{:.2f}%"), width='stretch')
            st.info("💡 **Stratifikasi Berhasil!** Proporsi kelas Normal dan Dyslexia identik di set Train dan Test, mencegah adanya Domain Shift.")
    else:
        st.error("csv_metadata/Dataset_Dyslexia_EMNIST.csv tidak ditemukan!")

# ==========================================
# TAB 2: BUSINESS QUESTIONS & EDA
# ==========================================
with tab2:
    st.markdown("### 🎯 Pertanyaan Bisnis & EDA Heatmap")
    st.write("Apakah pola goresan tulisan tangan dapat digunakan sebagai indikator tingkat keparahan disleksia?")
    
    # Tentukan suffix gambar berdasarkan dataset yang dipilih
    is_noAugmentation = dataset_choice == "Dataset Tanpa Augmentasi (Original Gambo)"
    img_suffix = '_noAugmentation' if is_noAugmentation else '_EMNIST'
    
    if df_master is not None:
        st.markdown("#### 📊 Distribusi Kelas per Split")
        img_path = f'assets/class_distribution{img_suffix}.png'
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
        else:
            st.error(f"Gambar {img_path} tidak ditemukan.")
        st.divider()
        
        st.markdown("#### 📈 Distribusi Keparahan (Severity Score)")
        img_path = f'assets/severity_distribution{img_suffix}.png'
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
        else:
            st.error(f"Gambar {img_path} tidak ditemukan.")
        st.divider()
        
        st.markdown("#### 🖼️ Sampel Kelas: Normal vs Corrected vs Reversal")
        st.write("Berikut adalah perbandingan wujud asli tulisan dari 3 kelas utama:")
        img_path = f'assets/class_samples{img_suffix}.png'
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
        else:
            st.error(f"Gambar {img_path} tidak ditemukan.")
        st.divider()

        st.markdown("#### 🖼️ Sampel Visual Keparahan Tulisan")
        if is_noAugmentation:
            st.write("Berikut adalah perbandingan wujud asli tulisan dari penderita gejala ringan (Skor 1) hingga parah (Skor 6):")
        else:
            st.write("Berikut adalah perbandingan wujud asli tulisan dari penderita gejala ringan (Skor 2) hingga parah (Skor 6):")
            
        img_path = f'assets/severity_samples{img_suffix}.png'
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
        else:
            st.error(f"Gambar {img_path} tidak ditemukan.")
        st.divider()
            
    # === HEATMAP ===
    if is_noAugmentation:
        st.markdown("#### 🔥 Heatmap Rata-rata Piksel: Skor 1 (Paling Ringan) vs Skor 6 (Parah)")
        st.write("Visualisasi ini membuktikan secara matematis bahwa ada perbedaan ketebalan goresan (koreksi/reversal) antara penderita gejala ringan dan parah.")
        if os.path.exists('assets/heatmap_noAugmentation.png'):
            st.image('assets/heatmap_noAugmentation.png', width='stretch')
            st.success("**Rata-rata selisih intensitas piksel:** ~16.57 (skala 0-255). Semakin menyala (kuning/putih) warna di Heatmap, semakin sering terjadi coretan berulang di area tersebut.")
        else:
            st.warning("⚠️ File `assets/heatmap_noAugmentation.png` tidak ditemukan.")
    else:
        st.markdown("#### 🔥 Heatmap Rata-rata Piksel: Skor 1 (Paling Ringan) vs Skor 6 (Parah)")
        st.write("Visualisasi ini membuktikan secara matematis bahwa ada perbedaan ketebalan goresan (koreksi/reversal) antara penderita gejala ringan dan parah.")
        if os.path.exists('assets/heatmap_EMNIST.png'):
            st.image('assets/heatmap_EMNIST.png', width='stretch')
            st.success("**Rata-rata selisih intensitas piksel:** ~14.00 (skala 0-255). Semakin menyala (kuning/putih) warna di Heatmap, semakin sering terjadi coretan berulang di area tersebut.")
        else:
            st.warning("⚠️ File `assets/heatmap_EMNIST.png` tidak ditemukan.")
        
    st.divider()
    if df_master is not None:
        st.markdown("#### 🔠 Karakter Paling Sering Muncul")
        
        chars = df_master['file_name'].str.extract(r'([a-zA-Z0-9])')[0].str.lower()
        char_counts = chars.value_counts().head(20)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        try:
            char_counts.plot(kind='bar', color='#9B59B6', ax=ax)
            ax.set_title('Top 20 Karakter Terbanyak dalam Dataset')
            ax.set_ylabel('Jumlah Kemunculan')
            ax.set_xlabel('Karakter')
            ax.tick_params(axis='x', rotation=0)
            st.pyplot(fig)
        finally:
            plt.close(fig)
        st.info("💡 Grafik ini membantu memvalidasi apakah huruf rawan disleksia seperti **b, d, p, q** sudah terwakili dengan baik dalam dataset.")

# ==========================================
# TAB 3: DATA PREP & STRATIFICATION
# ==========================================
with tab3:
    st.markdown("### ⚖️ Balancing & Kategori Data")
    
    if dataset_choice == "Dataset Dengan Augmentasi (Gambo + EMNIST)":
        st.write("Dataset Gambo asli memiliki ketidakseimbangan kelas (*Class Imbalance*) di mana tulisan Disleksia jauh lebih banyak dari tulisan Normal. Kami menyelesaikan ini dengan menambahkan EMNIST.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.error("**Before:** Imbalance Dataset\n- Dyslexia: ~115,000\n- Normal: ~58,000")
        with col2:
            st.success("**After:** Balanced (~1:1 Ratio)\n- Dyslexia (Gambo): ~142,000\n- Normal (Gambo + EMNIST): ~131,000")
    else:
        st.write("Dataset ini merupakan versi murni dari Gambo tanpa tambahan sintesis dari EMNIST.")
        if df_master is not None:
            dys_count = len(df_master[df_master['target_class'] == 1])
            norm_count = len(df_master[df_master['target_class'] == 0])
            st.info(f"**Komposisi Saat Ini:** Terdapat **{dys_count:,}** sampel tulisan Disleksia dan **{norm_count:,}** sampel tulisan Normal.")
        
    if df_master is not None:
        st.divider()
        
        # Mengecek kolom apa yang tersedia untuk komposisi data
        col_to_stack = None
        if 'source' in df_master.columns:
            col_to_stack = 'source'
            chart_title = 'Proporsi Sumber Data (Gambo vs EMNIST)'
        elif 'folder_category' in df_master.columns:
            col_to_stack = 'folder_category'
            chart_title = 'Proporsi Kategori Folder (Normal / Corrected / Reversal)'
            
        if col_to_stack:
            st.markdown(f"#### 🥧 {chart_title}")
            
            source_counts = df_master.groupby(['target_class', col_to_stack]).size().unstack(fill_value=0)
            source_counts.index = ['Normal (0)', 'Dyslexia (1)']
            
            fig, ax = plt.subplots(figsize=(8, 4))
            try:
                available_sources = source_counts.columns.tolist()
                
                # Pewarnaan dinamis
                color_map = {'gambo': '#F39C12', 'emnist': '#3498DB', 'normal': '#2ECC71', 'corrected': '#E74C3C', 'reversal': '#9B59B6'}
                colors = [color_map.get(s.lower(), '#95A5A6') for s in available_sources]
                
                source_counts.plot(kind='bar', stacked=True, ax=ax, color=colors)
                ax.set_title(chart_title)
                ax.set_ylabel('Jumlah Gambar')
                ax.tick_params(axis='x', rotation=0)
                ax.legend(title=col_to_stack.title())
                
                for c in ax.containers:
                    ax.bar_label(c, label_type='center', color='white', fontweight='bold', fmt='%d')
                    
                st.pyplot(fig)
            finally:
                plt.close(fig)

# ==========================================
# TAB 4: DATASET VIEWER (COMPRESSED CSV)
# ==========================================
with tab4:
    st.markdown("### 👁️ Eksplorasi Data (Compressed CSV)")

    is_noAugmentation = dataset_choice == "Dataset Tanpa Augmentasi (Original Gambo)"
    csv_file = 'csv_metadata/dyslexialens_test_noAugmentation.csv.gz' if is_noAugmentation else 'csv_metadata/dyslexialens_test_EMNIST.csv.gz'
    df_pixels = load_compressed_csv(csv_file)
    
    file_size_mb = os.path.getsize(csv_file) / (1024 * 1024) if os.path.exists(csv_file) else 0
    total_imgs = len(df_pixels) if df_pixels is not None else 0
    
    st.write(f"Viewer ini meload data secara *offline* dari file `{csv_file}` tanpa membaca folder gambar fisik. File berukuran ~{file_size_mb:.1f}MB ini mengandung **{total_imgs:,} gambar** test 28x28!")
    
    if df_pixels is None:
        st.warning(f"⏳ File `{csv_file}` belum ditemukan.")
    else:
        st.success(f"✅ Berhasil memuat {total_imgs:,} gambar dari `{csv_file}`!")
        
        filter_class = st.selectbox("Pilih Kelas:", ['Normal (0)', 'Dyslexia (1)'])
        target_val = 0 if 'Normal' in filter_class else 1
        
        subset = df_pixels[df_pixels['label'] == target_val]
        
        if len(subset) > 0:
            try:
                st.write(f"Menampilkan 10 sampel gambar acak dari total **{len(subset):,}** gambar kelas ini:")
                samples = subset.sample(min(10, len(subset)))
                
                cols = st.columns(5)
                for i, (_, row) in enumerate(samples.iterrows()):
                    pixels = row.drop('label').values.astype(np.float64).reshape(28, 28)
                    fig, ax = plt.subplots(figsize=(2,2))
                    try:
                        ax.imshow(pixels, cmap='gray', vmin=0, vmax=255)
                        ax.axis('off')
                        cols[i % 5].pyplot(fig)
                    finally:
                        plt.close(fig)
                    
                st.divider()
                st.markdown("#### 📈 Analisis Piksel Interaktif")
                
                n_samples = min(300, len(subset))
                avg_sample = subset.sample(n_samples, random_state=42)
                pixel_data = avg_sample.drop(columns=['label']).values.astype(np.float64)
                avg_image = np.mean(pixel_data, axis=0).reshape(28, 28)
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.write("**Rata-Rata Goresan (Ghost Image)**")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    try:
                        ax.imshow(avg_image, cmap='gray', vmin=0, vmax=255)
                        ax.axis('off')
                        ax.set_title(f"Pola Rata-rata dari {n_samples} sampel acak")
                        st.pyplot(fig)
                    finally:
                        plt.close(fig)
                    
                with col_chart2:
                    st.write("**Distribusi Ketebalan Tinta (Intensitas Piksel)**")
                    flat_pixels = pixel_data.flatten()
                    stroke_pixels = flat_pixels[flat_pixels > 10]
                    
                    fig, ax = plt.subplots(figsize=(5, 4))
                    try:
                        ax.hist(stroke_pixels, bins=30, color='#34495E', alpha=0.7)
                        ax.set_title("Distribusi Intensitas Piksel Goresan (>10)")
                        ax.set_xlabel("Intensitas (0-255)")
                        ax.set_ylabel("Frekuensi")
                        st.pyplot(fig)
                    finally:
                        plt.close(fig)
                    
                    mean_intensity = np.mean(stroke_pixels) if len(stroke_pixels) > 0 else 0
                    st.caption(f"Rata-rata intensitas goresan untuk {n_samples} sampel ini: **{mean_intensity:.1f}**")
                
                del pixel_data, flat_pixels, stroke_pixels, avg_image
            except Exception as e:
                st.error(f"⚠️ Terjadi error saat memproses data: {e}")
        else:
            st.error("Tidak ada data untuk kelas ini.")
