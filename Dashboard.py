import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import base64

# Konfigurasi Halaman (Harus dipanggil paling atas)
st.set_page_config(page_title="DyslexiaLens: Dashboard", page_icon="🧠", layout="wide")

DATASET_OPTIONS = {
    "Original (No Augmentation)": {
        "title_suffix": "Original Gambo",
        "csv_path": "Data/Dataset_Dyslexia_NoAugmentation_FeatureEngineering.csv",
        "image_folder": "Assets/noAugmentation",
        "image_suffix": "_noAugmentation.png",
        "test_csv": "Data/dyslexialens_test_noAugmentation.csv.gz",
    },
    "Augmented (Gambo + EMNIST)": {
        "title_suffix": "Gambo + EMNIST",
        "csv_path": "Data/Dataset_Dyslexia_EMNIST_FeatureEngineering.csv",
        "image_folder": "Assets/EMNIST",
        "image_suffix": "_EMNIST.png",
        "test_csv": "Data/dyslexialens_test_EMNIST.csv.gz",
    },
}


def get_dataset_assets(choice):
    return DATASET_OPTIONS[choice]


def load_custom_css():
    css_path = Path(__file__).parent / "Assets" / "Styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_section_header(subtitle, title, description=None):
    desc_html = f'<p style="opacity:0.7;font-size:0.95rem;max-width:600px;margin:0.8rem auto 0 auto;">{description}</p>' if description else ''
    st.markdown(f"""<div style="margin-bottom:2rem; text-align: center;">
<p style="font-size:0.8rem;font-weight:600;opacity:0.45;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.3rem 0;">{subtitle}</p>
<h2 style="font-size:1.6rem;font-weight:700;margin:0;letter-spacing:-0.03em;">{title}</h2>
{desc_html}
</div>""", unsafe_allow_html=True)


def get_logo_base64():
    logo_path = Path(__file__).parent / "Assets" / "Logo DyslexiaLens.png"
    if logo_path.exists():
        with open(logo_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# CSS Styling
load_custom_css()

# ==========================================
# NAVBAR: Brand + Dataset Toggle
# ==========================================
logo_b64 = get_logo_base64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:120px;vertical-align:bottom;">' if logo_b64 else ''

st.markdown(f"""<div class="site-navbar">
<div class="brand-wrapper" style="display:flex;align-items:center;justify-content:center;gap:0rem;">
{logo_html}
<div>
<div class="site-brand">DyslexiaLens</div>
<div class="site-subtitle">Dashboard</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# Dataset pills - inline, right after navbar
dataset_choice = st.radio(
    "Dataset:",
    ["Original (No Augmentation)", "Augmented (Gambo + EMNIST)"],
    horizontal=True,
)

dataset_assets = get_dataset_assets(dataset_choice)
csv_path = dataset_assets["csv_path"]

# ==========================================
# TABS - secondary navigation
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Summary",
    "Visual Analysis",
    "XAI Profiling",
    "Stratification",
    "A/B Testing",
    "Viewer",
])

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
    title_suffix = dataset_assets["title_suffix"]

    if df_master is not None:
        total_images = len(df_master)
        total_train = len(df_master[df_master['split'] == 'Train'])
        total_test  = len(df_master[df_master['split'] == 'Test'])
        dys_count   = len(df_master[df_master['target_class'] == 1])
        norm_count  = len(df_master[df_master['target_class'] == 0])
        train_pct   = (total_train / total_images) * 100 if total_images > 0 else 0
        test_pct    = (total_test  / total_images) * 100 if total_images > 0 else 0
        balance_ratio = min(dys_count, norm_count) / max(dys_count, norm_count) * 100 if max(dys_count, norm_count) > 0 else 0

        # ── Section Header ──────────────────────────────────────
        render_section_header("Dataset Overview", title_suffix)

        # ── Stat Cards ──────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        cards = [
            (c1, "🖼️", "Total Gambar",       f"{total_images:,}", "#3498db"),
            (c2, "🏋️", f"Train ({train_pct:.0f}%)", f"{total_train:,}", "#9b59b6"),
            (c3, "🧪", f"Test ({test_pct:.0f}%)",   f"{total_test:,}",  "#2ecc71"),
            (c4, "⚖️", "Class Balance",       f"{balance_ratio:.1f}%",  "#e67e22"),
        ]
        for col, icon, label, value, color in cards:
            col.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-radius:14px;padding:1.2rem 1.4rem;border-top:3px solid {color}; text-align: center;">
                <div style="font-size:1.5rem;margin-bottom:0.5rem;">{icon}</div>
                <div style="font-size:0.72rem;font-weight:600;opacity:0.45;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:0.3rem;">{label}</div>
                <div style="font-size:2rem;font-weight:700;letter-spacing:-0.03em;color:{color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        # ── Charts Row ──────────────────────────────────────────
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("##### Distribusi Kelas (Normal vs Disleksia)")
            class_counts = df_master['target_class'].value_counts().rename({0: 'Normal', 1: 'Dyslexia'})
            
            # Render as horizontal progress bars via HTML for dark-mode clarity
            max_val = class_counts.max()
            items = [
                ('Dyslexia', class_counts.get('Dyslexia', 0), '#e74c3c'),
                ('Normal',   class_counts.get('Normal', 0),   '#2ecc71'),
            ]
            bars_html = ""
            for label, count, color in items:
                pct = (count / max_val) * 100 if max_val > 0 else 0
                bars_html += f"""<div style="margin-bottom:1.2rem;">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.4rem;">
        <span style="font-size:0.95rem;font-weight:600;">{label}</span>
        <span style="font-size:1.3rem;font-weight:700;color:{color};">{count:,}</span>
    </div>
    <div style="width:100%;height:12px;background:rgba(255,255,255,0.06);border-radius:6px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{color},{color}cc);border-radius:6px;transition:width 0.6s ease;"></div>
    </div>
</div>"""

            st.markdown(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.4rem;">
{bars_html}
</div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("##### Proporsi Stratified Split")
            train_counts = df_master[df_master['split'] == 'Train']['target_class'] \
                               .value_counts(normalize=True).rename({0: 'Normal', 1: 'Dyslexia'}) * 100
            test_counts  = df_master[df_master['split'] == 'Test']['target_class'] \
                               .value_counts(normalize=True).rename({0: 'Normal', 1: 'Dyslexia'}) * 100

            # Render as custom HTML table for dark-mode
            rows_html = ""
            for cls_name in ['Dyslexia', 'Normal']:
                train_v = train_counts.get(cls_name, 0)
                test_v  = test_counts.get(cls_name, 0)
                color   = '#e74c3c' if cls_name == 'Dyslexia' else '#2ecc71'
                rows_html += f"""<tr>
    <td style="padding:0.7rem 1rem;font-weight:600;border-bottom:1px solid rgba(255,255,255,0.06);">
        <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{color};margin-right:0.5rem;"></span>{cls_name}
    </td>
    <td style="padding:0.7rem 1rem;text-align:center;font-weight:700;color:{color};border-bottom:1px solid rgba(255,255,255,0.06);">{train_v:.2f}%</td>
    <td style="padding:0.7rem 1rem;text-align:center;font-weight:700;color:{color};border-bottom:1px solid rgba(255,255,255,0.06);">{test_v:.2f}%</td>
</tr>"""
            
            st.markdown(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;overflow:hidden;">
<table style="width:100%;border-collapse:collapse;font-size:0.9rem;">
<thead>
<tr style="background:rgba(255,255,255,0.05);">
<th style="padding:0.7rem 1rem;text-align:left;font-weight:600;opacity:0.6;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;">Kelas</th>
<th style="padding:0.7rem 1rem;text-align:center;font-weight:600;opacity:0.6;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;">Train</th>
<th style="padding:0.7rem 1rem;text-align:center;font-weight:600;opacity:0.6;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;">Test</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>""", unsafe_allow_html=True)
            
            st.success("**Stratifikasi Berhasil!** Proporsi kelas identik di semua split: tidak ada *Domain Shift*.")
    else:
        st.error("❌ File dataset tidak ditemukan! Pastikan CSV tersedia di folder `Data/`.")


# ==========================================
# TAB 2: COMPUTER VISION ANALYTICS
# ==========================================
with tab2:
    img_folder = dataset_assets["image_folder"]
    img_suffix = dataset_assets["image_suffix"]

    # ── Section Header ────────────────────────────────────────
    render_section_header("Computer Vision", "Analisis Spasial & Piksel")

    # ── Section 1: Class Samples ──────────────────────────────
    col_img, col_info = st.columns([1.5, 1])
    with col_img:
        st.image(f'{img_folder}/class_samples{img_suffix}', use_container_width=True)
    with col_info:
        st.markdown("""<div style="background:rgba(52,152,219,0.07);border:1px solid rgba(52,152,219,0.2);
border-left:3px solid #3498db;border-radius:0 12px 12px 0;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">Visualisasi 1</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">Sampel Kelas: Normal vs Corrected vs Reversal</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Wujud asli matriks <strong>28×28 piksel</strong> untuk membandingkan huruf solid (Normal),
tarikan berulang (<em>Over-tracing / Corrected</em>), dan pembalikan orientasi huruf (<em>Reversal</em>).
</p>
<div style="display:flex;flex-direction:column;gap:0.5rem;">
<span style="background:rgba(46,204,113,0.15);color:#2ecc71;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Normal: goresan solid & konsisten</span>
<span style="background:rgba(231,76,60,0.15);color:#e74c3c;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Corrected: menebal/ragu-ragu</span>
<span style="background:rgba(155,89,182,0.15);color:#9b59b6;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Reversal: orientasi terbalik</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.divider()
    # ── Section 2: Severity Distribution ─────────────────────
    col_info2, col_img2 = st.columns([1, 1.5])
    with col_info2:
        st.markdown("""<div style="background:rgba(155,89,182,0.08);border:1px solid rgba(155,89,182,0.2);
border-right:3px solid #9b59b6;border-radius:12px 0 0 12px;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">Visualisasi 2</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">Distribusi Keparahan (Severity Score 0–6)</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Memetakan spektrum keparahan disleksia yang mendominasi dataset.
Skor <strong>0 = Normal</strong>, skor <strong>6 = Paling Parah</strong>
(skala asli sudah dikoreksi dari 9→1 menjadi 0→6).
</p>
<div style="display:flex;flex-direction:column;gap:0.5rem;">
<span style="background:rgba(46,204,113,0.15);color:#2ecc71;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Score 0 → Normal</span>
<span style="background:rgba(241,196,15,0.15);color:#f1c40f;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Score 1-3 → Ringan</span>
<span style="background:rgba(231,76,60,0.15);color:#e74c3c;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Score 4-6 → Parah</span>
</div>
</div>
""", unsafe_allow_html=True)
    with col_img2:
        st.image(f'{img_folder}/severity_distribution{img_suffix}', use_container_width=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.divider()

    # ── Section 3: Variance Heatmap ───────────────────────────
    st.markdown("""<div style="background:rgba(230,126,34,0.08);border:1px solid rgba(230,126,34,0.2);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1rem; text-align: center;">
<p style="margin:0;font-size:0.9rem;opacity:0.85;">
<strong>Pertanyaan Bisnis 2:</strong>
<em>Apakah pola visual tulisan tangan cukup kuat merepresentasikan kondisi kognitif disleksia, atau sekadar indikasi ambigu?</em>
</p>
</div>
""", unsafe_allow_html=True)

    col_img3, col_info3 = st.columns([1.5, 1])
    with col_img3:
        st.image(f'{img_folder}/variance_heatmap{img_suffix}', use_container_width=True)
    with col_info3:
        st.markdown("""<div style="background:rgba(230,126,34,0.07);border:1px solid rgba(230,126,34,0.2);
border-left:3px solid #e67e22;border-radius:0 12px 12px 0;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">Visualisasi 3</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">Variance Heatmap: Tremor vs Solid</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Memvisualisasikan variansi piksel per posisi. Area <strong>menyala (kuning/jingga)</strong>
pada heatmap Disleksia membuktikan tingginya inkonsistensi/tremor goresan.
</p>
<span style="background:rgba(46,204,113,0.15);color:#2ecc71;font-size:0.8rem;font-weight:700;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Pola sangat kuat: Disleksia jauh lebih bervariasi</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.divider()

    # ── Section 4: Heatmap Difference ────────────────────────
    col_info4, col_img4 = st.columns([1, 1.5])
    with col_info4:
        st.markdown("""<div style="background:rgba(46,204,113,0.07);border:1px solid rgba(46,204,113,0.18);
border-right:3px solid #2ecc71;border-radius:12px 0 0 12px;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">Visualisasi 4</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">Rata-rata Piksel: Ringan vs Parah</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Membedah <em>blind spots</em> spasial: titik koordinat mana yang paling sering
mengalami distorsi ekstrem pada kasus disleksia parah (Severity Score 6)
dibanding yang ringan (Severity Score 1).
</p>
<div style="display:flex;flex-direction:column;gap:0.5rem;">
<span style="background:rgba(241,196,15,0.15);color:#f1c40f;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Score 1 → Disleksia Ringan</span>
<span style="background:rgba(231,76,60,0.15);color:#e74c3c;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Score 6 → Disleksia Parah</span>
</div>
</div>
""", unsafe_allow_html=True)
    with col_img4:
        st.image(f'{img_folder}/heatmap{img_suffix}', use_container_width=True)




# ==========================================
# TAB 3: EXPLAINABLE AI (XAI) PROFILING
# ==========================================
with tab3:
    img_folder = dataset_assets["image_folder"]
    img_suffix = dataset_assets["image_suffix"]
    
    # ── Section Header ────────────────────────────────────────
    render_section_header("Explainable AI", "Interpretasi Klinis Fitur Geometri", 
        "Mengekstrak fitur turunan matematis sebagai <strong>Sidik Jari</strong> untuk memberikan transparansi (alasan logis) di balik setiap keputusan klasifikasi model AI.")

    # ── Section 1: XAI Boxplots ────────────────────────────
    st.markdown("""<div style="background:rgba(52,152,219,0.08);border:1px solid rgba(52,152,219,0.2);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.5rem; text-align: center;">
<p style="margin:0;font-size:0.9rem;opacity:0.85;">
<strong>Pertanyaan Bisnis 3:</strong>
<em>Bagaimana merancang sistem AI yang tidak hanya akurat, tetapi mampu menjelaskan mengapa suatu tulisan terindikasi disleksia?</em>
</p>
</div>
""", unsafe_allow_html=True)

    col_img5, col_info5 = st.columns([1.5, 1])
    with col_img5:
        st.image(f'{img_folder}/xai_boxplots{img_suffix}', use_container_width=True)
    with col_info5:
        st.markdown("""<div style="background:rgba(52,152,219,0.07);border:1px solid rgba(52,152,219,0.2);
border-left:3px solid #3498db;border-radius:0 12px 12px 0;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">Distribusi Fitur</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">Boxplot: Normal vs Dyslexia</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Membandingkan sebaran 6 fitur XAI antara tulisan Normal dan Disleksia.
Perbedaan yang mencolok menjadi bukti klinis arsitektur <em>Late Fusion</em>.
</p>
<div style="display:flex;flex-direction:column;gap:0.5rem;">
<span style="background:rgba(46,204,113,0.15);color:#2ecc71;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Kepadatan Tinta: indikator Over-tracing</span>
<span style="background:rgba(52,152,219,0.15);color:#3498db;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Transisi Garis: indikator Tremor</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.divider()

    # ── Section 2: XAI KDE Subtypes ──────────────────────
    st.markdown("""<div style="background:rgba(155,89,182,0.08);border:1px solid rgba(155,89,182,0.2);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.5rem; text-align: center;">
<p style="margin:0;font-size:0.9rem;opacity:0.85;">
<strong>Pertanyaan Bisnis 4:</strong>
<em>Bagaimana sistem dapat memberikan interpretasi klinis (Sub-tipe) terhadap hasil klasifikasinya?</em>
</p>
</div>
""", unsafe_allow_html=True)

    col_info6, col_img6 = st.columns([1, 1.5])
    with col_info6:
        st.markdown("""<div style="background:rgba(155,89,182,0.08);border:1px solid rgba(155,89,182,0.2);
border-right:3px solid #9b59b6;border-radius:12px 0 0 12px;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">Kerapatan Distribusi</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">KDE Profiling Sub-Tipe</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Membedah perbedaan distribusi fitur antara dua sub-tipe:
<em>Corrected</em> (ragu-ragu/menebalkan garis) dan <em>Reversal</em> (terbalik orientasi).
</p>
<div style="display:flex;flex-direction:column;gap:0.5rem;">
<span style="background:rgba(231,76,60,0.15);color:#e74c3c;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Corrected → Anomali Kepadatan Tinta</span>
<span style="background:rgba(155,89,182,0.15);color:#9b59b6;font-size:0.8rem;font-weight:600;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Reversal → Anomali Simetri Horizontal</span>
</div>
</div>
""", unsafe_allow_html=True)
    with col_img6:
        st.image(f'{img_folder}/xai_kde_subtypes{img_suffix}', use_container_width=True)

# ==========================================
# TAB 4: DATA PREP & STRATIFICATION
# ==========================================
with tab4:
    # ── Section Header ────────────────────────────────────────
    render_section_header("Data Engineering", "Balancing & Kategori Data", 
        "Mengatasi ketidakseimbangan kelas (<em>Class Imbalance</em>) untuk memastikan model AI tidak mengalami bias saat pelatihan.")
    
    st.markdown("""<div style="background:rgba(241,196,15,0.08);border:1px solid rgba(241,196,15,0.2);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.5rem; text-align: center;">
<p style="margin:0;font-size:0.9rem;opacity:0.85;">
<strong>Pertanyaan Bisnis 1:</strong>
<em>Apakah dataset ini sudah cukup representatif dan seimbang untuk melatih model AI?</em>
</p>
</div>
""", unsafe_allow_html=True)

    if dataset_choice == "Augmented (Gambo + EMNIST)":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div style="background:rgba(231,76,60,0.05);border:1px solid rgba(231,76,60,0.2);
border-left:3px solid #e74c3c;border-radius:12px;padding:1.2rem;height:100%; text-align: center;">
<h4 style="margin:0 0 0.5rem 0;color:#e74c3c;font-size:1.1rem;">Before (Original Gambo)</h4>
<p style="opacity:0.8;font-size:0.9rem;margin-bottom:0.8rem;">Sangat rentan terhadap <em>Majority Class Bias</em>.</p>
<div style="margin-bottom:0.8rem;">
    <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.2rem;"><span>Dyslexia</span><span style="font-weight:700;">120,463</span></div>
    <div style="width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;"><div style="width:100%;height:100%;background:#e74c3c;border-radius:3px;"></div></div>
</div>
<div>
    <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.2rem;"><span>Normal</span><span style="font-weight:700;">35,990</span></div>
    <div style="width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;"><div style="width:29.8%;height:100%;background:#2ecc71;border-radius:3px;"></div></div>
</div>
<p style="font-size:0.8rem;opacity:0.6;margin:1rem 0 0 0;">*(Rasio Kritis 3.35 : 1)*</p>
</div>
""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="background:rgba(46,204,113,0.05);border:1px solid rgba(46,204,113,0.2);
border-left:3px solid #2ecc71;border-radius:12px;padding:1.2rem;height:100%; text-align: center;">
<h4 style="margin:0 0 0.5rem 0;color:#2ecc71;font-size:1.1rem;">📈 After (Gambo + EMNIST)</h4>
<p style="opacity:0.8;font-size:0.9rem;margin-bottom:0.8rem;">Siap untuk pelatihan AI tanpa bias.</p>
<div style="margin-bottom:0.8rem;">
    <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.2rem;"><span>Dyslexia (Pruned)</span><span style="font-weight:700;">102,394</span></div>
    <div style="width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;"><div style="width:99.9%;height:100%;background:#e74c3c;border-radius:3px;"></div></div>
</div>
<div>
    <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:0.2rem;"><span>Normal (Augmented)</span><span style="font-weight:700;">102,439</span></div>
    <div style="width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;"><div style="width:100%;height:100%;background:#2ecc71;border-radius:3px;"></div></div>
</div>
<p style="font-size:0.8rem;opacity:0.6;margin:1rem 0 0 0;">*(Rasio Ekuilibrium ~1.00 : 1)*</p>
</div>
""", unsafe_allow_html=True)
            
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.success("**Kesimpulan:** Sangat seimbang! Penambahan dataset sintesis EMNIST dan penerapan algoritma *Fair Pruning* berhasil menekan rasio kelas secara masif hingga mencapai **1:1**.")
            
    else:
        if df_master is not None:
            dys_count = len(df_master[df_master['target_class'] == 1])
            norm_count = len(df_master[df_master['target_class'] == 0])
            st.markdown(f"""<div style="background:rgba(231,76,60,0.05);border:1px solid rgba(231,76,60,0.2);
border-left:3px solid #e74c3c;border-radius:12px;padding:1.2rem;margin-bottom:1rem; text-align: center;">
<h4 style="margin:0 0 0.5rem 0;color:#e74c3c;font-size:1.1rem;">Status Saat Ini (Imbalance)</h4>
<p style="opacity:0.8;font-size:0.9rem;margin-bottom:0.8rem;">Dataset asli Gambo ini murni tanpa intervensi data eksternal.</p>
<div style="font-size:0.9rem;opacity:0.9;margin-bottom:0.3rem;">• Tulisan Disleksia: <strong>{dys_count:,}</strong> sampel</div>
<div style="font-size:0.9rem;opacity:0.9;margin:0;">• Tulisan Normal: <strong>{norm_count:,}</strong> sampel</div>
</div>
""", unsafe_allow_html=True)
            
        st.error("**Kesimpulan:** Belum seimbang. Dataset asli ini masih sangat rentan terhadap *Class Imbalance*, di mana tulisan Disleksia jauh mendominasi. Risiko terjadinya *Majority Class Bias* saat pelatihan sangat tinggi.")
        
    if df_master is not None:
        st.divider()
        
        # Mengecek kolom apa yang tersedia untuk komposisi data
        col_to_stack = None
        if 'source' in df_master.columns:
            col_to_stack = 'source'
            chart_title = 'Komposisi Sumber Data (Gambo vs EMNIST)'
            desc = 'Komposisi sampel berdasarkan sumber datanya. Terlihat EMNIST mengisi celah besar pada kelas Normal.'
        elif 'folder_category' in df_master.columns:
            col_to_stack = 'folder_category'
            chart_title = 'Komposisi Kategori Folder (Asal Gambar)'
            desc = 'Komposisi sampel berdasarkan folder aslinya (Normal, Corrected, Reversal).'
            
        if col_to_stack:
            col_text, col_chart = st.columns([1, 1.5])
            with col_text:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
border-right:3px solid #3498db;border-radius:12px 0 0 12px;padding:1.2rem 1.4rem;height:100%;">
<p style="font-size:0.72rem;font-weight:600;opacity:0.4;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.6rem 0;">Distribusi Data</p>
<h4 style="margin:0 0 0.8rem 0;font-size:1.05rem;font-weight:700;">
{chart_title}
</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.6;margin:0;">
{desc}
</p>
</div>
""", unsafe_allow_html=True)

            with col_chart:
                source_counts = df_master.groupby(['target_class', col_to_stack]).size().unstack(fill_value=0)
                source_counts.index = ['Normal', 'Dyslexia']
                
                html_bars = ""
                available_sources = source_counts.columns.tolist()
                color_map = {'gambo': '#f39c12', 'emnist': '#3498db', 'normal': '#2ecc71', 'corrected': '#e74c3c', 'reversal': '#9b59b6'}
                
                for cls_name in ['Normal', 'Dyslexia']:
                    total_for_cls = source_counts.loc[cls_name].sum()
                    
                    if total_for_cls == 0:
                        continue
                        
                    bar_segments = ""
                    legend_html = ""
                    for src in available_sources:
                        count = source_counts.loc[cls_name, src]
                        if count > 0:
                            pct = (count / total_for_cls) * 100
                            color = color_map.get(src.lower(), '#95a5a6')
                            # Make label readable (dark for bright colors like gambo, normal)
                            text_color = "rgba(0,0,0,0.6)" if src.lower() in ['gambo', 'normal', 'emnist'] else "rgba(255,255,255,0.9)"
                            bar_segments += f'<div style="width:{pct}%;height:100%;background:{color};display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:{text_color};">{int(count):,}</div>'
                            legend_html += f'<span style="margin-right:1rem;font-size:0.8rem;"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{color};margin-right:0.3rem;"></span>{src.title()} ({pct:.1f}%)</span>'
                    
                    html_bars += f"""<div style="margin-bottom:1.5rem;">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.4rem;">
        <span style="font-size:0.95rem;font-weight:600;">{cls_name}</span>
        <span style="font-size:1.1rem;font-weight:700;">{int(total_for_cls):,}</span>
    </div>
    <div style="width:100%;height:24px;background:rgba(255,255,255,0.06);border-radius:6px;overflow:hidden;display:flex;margin-bottom:0.4rem;">
        {bar_segments}
    </div>
    <div style="opacity:0.8;">
        {legend_html}
    </div>
</div>"""
                
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.4rem;">
{html_bars}
</div>""", unsafe_allow_html=True)

# ==========================================
# TAB 5: A/B TESTING VALIDATION
# ==========================================
with tab5:
    # ── Section Header ────────────────────────────────────────
    render_section_header("Experiment Validation", "A/B Testing Augmentasi", 
        "Memvalidasi secara saintifik apakah injeksi jutaan piksel dari dataset EMNIST merusak integritas fitur asli dari tulisan tangan Gambo.")

    st.markdown("""<div style="background:rgba(230,126,34,0.08);border:1px solid rgba(230,126,34,0.2);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.5rem; text-align: center;">
<p style="margin:0;font-size:0.9rem;opacity:0.85;">
<strong>Pertanyaan Bisnis 5:</strong>
<em>Apakah aman secara klinis untuk menggabungkan dataset karakter digital (EMNIST) dengan dataset disleksia tulis tangan (Gambo)?</em>
</p>
</div>
""", unsafe_allow_html=True)

    col_img7, col_info7 = st.columns([1.6, 1])
    with col_img7:
        st.image('Assets/ab_testing_kde_overlay.png', use_container_width=True)
    with col_info7:
        st.markdown("""<div style="background:rgba(230,126,34,0.07);border:1px solid rgba(230,126,34,0.2);
border-left:3px solid #e67e22;border-radius:0 12px 12px 0;padding:1.4rem;
min-height:320px;display:flex;flex-direction:column;justify-content:center; align-items: center; text-align: center;">
<p style="font-size:0.7rem;font-weight:700;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.8rem 0;">KDE Overlay Comparison</p>
<h4 style="margin:0 0 0.7rem 0;font-size:1.05rem;font-weight:700;">Dataset A vs Dataset B</h4>
<p style="opacity:0.7;font-size:0.88rem;line-height:1.7;margin:0 0 1rem 0;">
Membandingkan kurva distribusi <strong>Dataset A (Gambo Asli / Merah)</strong>
melawan <strong>Dataset B (Gambo + EMNIST / Biru)</strong> pada semua metrik fitur XAI.
Grafik ini adalah perbandingan absolut, terlepas dari pilihan dataset pada navbar.
</p>
<span style="background:rgba(46,204,113,0.15);color:#2ecc71;font-size:0.8rem;font-weight:700;padding:0.3rem 0.8rem;border-radius:20px;display:inline-block;">Aman! Kurva nyaris bertumpuk: Negligible Effect Size pada Cohen's d</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# TAB 6: DATASET VIEWER (COMPRESSED CSV)
# ==========================================
with tab6:
    # ── Section Header ────────────────────────────────────────
    render_section_header("Raw Data", "Eksplorasi CSV (Test Set)", 
        "Melihat langsung wujud matriks piksel 28x28 yang dibaca dari file CSV terkompresi.")

    csv_file = dataset_assets["test_csv"]
    df_pixels = load_compressed_csv(csv_file)
    
    file_size_mb = os.path.getsize(csv_file) / (1024 * 1024) if os.path.exists(csv_file) else 0
    total_imgs = len(df_pixels) if df_pixels is not None else 0
    
    if df_pixels is None:
        st.warning(f"⏳ File `{csv_file}` belum ditemukan.")
    else:
        
        filter_class = st.selectbox("Pilih Kelas:", ['Normal (0)', 'Dyslexia (1)'])
        target_val = 0 if 'Normal' in filter_class else 1
        
        subset = df_pixels[df_pixels['label'] == target_val]
        
        if len(subset) > 0:
            try:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:1rem; text-align: center;">
<h4 style="margin:0 0 0.5rem 0;font-size:1.05rem;">10 Sampel Acak</h4>
<p style="margin:0;font-size:0.9rem;opacity:0.8;">Menampilkan cuplikan matriks dari total <strong>{len(subset):,}</strong> data kelas ini.</p>
</div>
""", unsafe_allow_html=True)
                
                samples = subset.sample(min(10, len(subset)))
                
                _, center_col, _ = st.columns([1, 4, 1])
                with center_col:
                    cols = st.columns(5)
                    for i, (_, row) in enumerate(samples.iterrows()):
                        pixels = row.drop('label').values.astype(np.float64).reshape(28, 28)
                        fig, ax = plt.subplots(figsize=(0.4, 0.4))
                        fig.patch.set_alpha(0)
                        try:
                            ax.imshow(pixels, cmap='gray', vmin=0, vmax=255)
                            ax.axis('off')
                            cols[i % 5].pyplot(fig, use_container_width=False)
                        finally:
                            plt.close(fig)
                    
                st.divider()
                
                st.markdown("""<div style="margin-bottom:1.5rem; text-align: center;">
<p style="font-size:0.8rem;font-weight:600;opacity:0.45;text-transform:uppercase;
letter-spacing:0.1em;margin:0 0 0.3rem 0;">Analytics</p>
<h3 style="font-size:1.3rem;font-weight:700;margin:0;letter-spacing:-0.03em;">
Analisis Piksel Interaktif
</h3>
</div>
""", unsafe_allow_html=True)
                
                n_samples = min(300, len(subset))
                avg_sample = subset.sample(n_samples, random_state=42)
                pixel_data = avg_sample.drop(columns=['label']).values.astype(np.float64)
                avg_image = np.mean(pixel_data, axis=0).reshape(28, 28)
                
                col_chart1, col_chart2 = st.columns([1, 1])
                
                with col_chart1:
                    st.markdown(f"""<div style="background:rgba(155,89,182,0.1);border:1px solid rgba(155,89,182,0.3);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:0.5rem; text-align: center;">
<h4 style="margin:0 0 0.2rem 0;color:#e056fd;font-size:1.05rem;">Rata-Rata Goresan (Ghost Image)</h4>
<p style="margin:0;opacity:0.8;font-size:0.85rem;">Pola dominan gabungan dari <strong>{n_samples}</strong> sampel acak. Titik terang menandakan area yang paling sering digores tebal.</p>
</div>
""", unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(1.5, 1.5))
                    fig.patch.set_alpha(0)
                    try:
                        ax.imshow(avg_image, cmap='magma', vmin=0, vmax=255)
                        ax.axis('off')
                        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
                        
                        inner_cols = st.columns([1, 1.2, 1])
                        inner_cols[1].pyplot(fig, use_container_width=True)
                    finally:
                        plt.close(fig)
                    
                with col_chart2:
                    flat_pixels = pixel_data.flatten()
                    stroke_pixels = flat_pixels[flat_pixels > 10]
                    mean_intensity = np.mean(stroke_pixels) if len(stroke_pixels) > 0 else 0
                    
                    st.markdown(f"""<div style="background:rgba(52,152,219,0.1);border:1px solid rgba(52,152,219,0.3);
border-radius:12px;padding:1rem 1.4rem;margin-bottom:0.5rem; text-align: center;">
<h4 style="margin:0 0 0.2rem 0;color:#7ed6df;font-size:1.05rem;">Distribusi Ketebalan Tinta</h4>
<p style="margin:0;opacity:0.8;font-size:0.85rem;">Sebaran intensitas piksel goresan (0-255). Rata-rata intensitas untuk sampel ini: <strong>{mean_intensity:.1f}</strong></p>
</div>
""", unsafe_allow_html=True)
                    
                    fig, ax = plt.subplots(figsize=(3.0, 2.0))
                    fig.patch.set_alpha(0)
                    ax.patch.set_alpha(0)
                    try:
                        ax.hist(stroke_pixels, bins=30, color='#3498db', alpha=0.8, edgecolor='none')
                        ax.set_xlabel("Intensitas (0-255)", color='#999999', fontsize=8)
                        ax.set_ylabel("Frekuensi", color='#999999', fontsize=8)
                        
                        ax.tick_params(colors='#999999', labelsize=7)
                        ax.spines[:].set_visible(False)
                        ax.yaxis.grid(True, linestyle='--', alpha=0.1, color='white')
                        ax.set_axisbelow(True)
                        fig.subplots_adjust(left=0.15, right=0.98, top=0.92, bottom=0.25)
                        
                        inner_cols = st.columns([0.5, 3, 0.5])
                        inner_cols[1].pyplot(fig, use_container_width=True)
                    finally:
                        plt.close(fig)
                
                del pixel_data, flat_pixels, stroke_pixels, avg_image
            except Exception as e:
                st.error(f"Terjadi error saat memproses data: {e}")
        else:
            st.error("Tidak ada data untuk kelas ini.")
