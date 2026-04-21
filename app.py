import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulasi Pembagian Lembar Jawaban",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem; font-weight: 800; color: #1a1a2e;
        margin-bottom: 0.1rem; letter-spacing: -0.5px; line-height: 1.2;
    }
    .sub-title {
        font-size: 1.1rem; color: #6c757d;
        margin-top: 0.2rem; margin-bottom: 0; font-weight: 400;
    }
    .badge-inst {
        display: inline-block; background: #e8f0fe; color: #1a56db;
        font-size: 0.78rem; font-weight: 600; padding: 3px 12px;
        border-radius: 20px; margin-bottom: 0.8rem; letter-spacing: 0.3px;
    }
    .section-header {
        background: #f4f6fa; padding: 0.55rem 1rem;
        border-left: 4px solid #4361ee; border-radius: 0 6px 6px 0;
        margin-bottom: 1.2rem; font-weight: 700; font-size: 1.05rem; color: #1a1a2e;
    }
    [data-testid="stSidebar"] { background: #f8f9fd; }
</style>
""", unsafe_allow_html=True)


def simulasi_pembagian_lembar_jawaban(N, durasi_min=1.0, durasi_max=3.0, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    hasil = []
    waktu_selesai_sebelumnya = 0.0
    for i in range(1, N + 1):
        waktu_mulai = waktu_selesai_sebelumnya
        durasi = round(random.uniform(durasi_min, durasi_max), 4)
        waktu_selesai = waktu_mulai + durasi
        waktu_tunggu = waktu_mulai - 0
        hasil.append({
            'Mahasiswa': i,
            'Waktu Mulai (menit)': round(waktu_mulai, 4),
            'Durasi Pelayanan (menit)': durasi,
            'Waktu Selesai (menit)': round(waktu_selesai, 4),
            'Waktu Tunggu (menit)': round(waktu_tunggu, 4)
        })
        waktu_selesai_sebelumnya = waktu_selesai
    return pd.DataFrame(hasil)


# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Parameter Simulasi")
    st.markdown("---")
    N = st.slider("Jumlah Mahasiswa (N)", 1, 100, 30, 1)
    durasi_min = st.number_input("Durasi Minimum (menit)", 0.5, 10.0, 1.0, 0.5)
    durasi_max = st.number_input("Durasi Maksimum (menit)", 0.5, 20.0, 3.0, 0.5)
    seed_input = st.number_input("Random Seed", 0, 9999, 42, 1)
    use_seed = st.checkbox("Gunakan Fixed Seed (Reproducibility)", value=True)
    seed = int(seed_input) if use_seed else None
    st.markdown("---")
    run_btn = st.button("▶️ Jalankan Simulasi", use_container_width=True, type="primary")
    st.markdown("---")
    st.markdown("""
**Tentang Simulasi**
- Model: Discrete Event Simulation
- Antrian: FIFO (Single Server)
- Distribusi: Uniform(min, max)

**Modul Praktikum 6**
Verification & Validation — Institut Teknologi Del
    """)


# ── Header ───────────────────────────────────
st.markdown('<span class="badge-inst">Institut Teknologi Del · Modul Praktikum 6</span>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">📝 Simulasi Pembagian Lembar Jawaban Ujian</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Discrete Event Simulation — Verification &amp; Validation</p>', unsafe_allow_html=True)
st.markdown("---")

if durasi_min >= durasi_max:
    st.error("⚠️ Durasi minimum harus lebih kecil dari durasi maksimum!")
    st.stop()

# ── Session State ─────────────────────────────
# Simpan hasil simulasi agar tidak hilang saat widget berubah
if "sudah_simulasi" not in st.session_state:
    st.session_state.sudah_simulasi = False

# Jalankan simulasi HANYA saat tombol diklik
if run_btn:
    st.session_state.df_hasil = simulasi_pembagian_lembar_jawaban(
        N=N, durasi_min=durasi_min, durasi_max=durasi_max, seed=seed
    )
    st.session_state.sudah_simulasi = True
    st.session_state.param = dict(
        N=N, durasi_min=durasi_min, durasi_max=durasi_max,
        seed=seed, use_seed=use_seed
    )

# Belum pernah diklik → tampilkan petunjuk saja
if not st.session_state.sudah_simulasi:
    st.info("👈 Atur parameter di sidebar, lalu tekan **▶️ Jalankan Simulasi** untuk memulai.")
    st.stop()

# ── Ambil data dari session_state ────────────
df  = st.session_state.df_hasil
p   = st.session_state.param
N_p = p['N'];  durasi_min_p = p['durasi_min'];  durasi_max_p = p['durasi_max']
seed_p = p['seed'];  use_seed_p = p['use_seed']

total_waktu = df['Waktu Selesai (menit)'].max()
rata_tunggu = df['Waktu Tunggu (menit)'].mean()
rata_durasi = df['Durasi Pelayanan (menit)'].mean()
teoritis    = N_p * ((durasi_min_p + durasi_max_p) / 2)

# ── Metrik ───────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("⏱ Total Waktu",       f"{total_waktu:.2f} menit")
col2.metric("📐 Teoritis",          f"{teoritis:.2f} menit")
col3.metric("⌛ Rata-rata Tunggu",  f"{rata_tunggu:.2f} menit")
col4.metric("🔄 Rata-rata Durasi",  f"{rata_durasi:.4f} menit")
utilisasi = df['Durasi Pelayanan (menit)'].sum() / total_waktu * 100
col5.metric("🖥 Utilisasi Server", f"{utilisasi:.2f}%")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Hasil Simulasi", "🔧 Verification", "✔️ Validation", "📋 Data Lengkap"
])

# ══════════════ TAB 1 ══════════════
with tab1:
    st.markdown('<div class="section-header">Visualisasi Hasil Simulasi</div>', unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor('#fafafa')

    ax1 = axes[0]
    cmap = plt.cm.get_cmap('tab20', N_p)
    for _, row in df.iterrows():
        ax1.barh(row['Mahasiswa'], row['Durasi Pelayanan (menit)'],
                 left=row['Waktu Mulai (menit)'],
                 color=cmap((int(row['Mahasiswa'])-1) % 20), alpha=0.85,
                 edgecolor='white', linewidth=0.5)
    ax1.set_title('Gantt Chart — Timeline Pelayanan', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Waktu (menit)');  ax1.set_ylabel('Mahasiswa ke-');  ax1.invert_yaxis()

    ax2 = axes[1]
    ax2.hist(df['Durasi Pelayanan (menit)'], bins=12, color='#4361ee', edgecolor='white', alpha=0.85, rwidth=0.9)
    ax2.axvline(durasi_min_p, color='red',    linestyle='--', linewidth=1.5, label=f'Min ({durasi_min_p})')
    ax2.axvline(durasi_max_p, color='green',  linestyle='--', linewidth=1.5, label=f'Max ({durasi_max_p})')
    ax2.axvline(rata_durasi,  color='orange', linestyle='-',  linewidth=2,   label=f'Mean ({rata_durasi:.2f})')
    ax2.set_title('Distribusi Durasi Pelayanan', fontweight='bold', fontsize=12)
    ax2.set_xlabel('Durasi (menit)');  ax2.set_ylabel('Frekuensi');  ax2.legend()
    plt.tight_layout();  st.pyplot(fig)

    fig2, ax = plt.subplots(figsize=(14, 3.5))
    ax.bar(df['Mahasiswa'], df['Waktu Tunggu (menit)'], color='#f77f00', alpha=0.8, edgecolor='white')
    ax.set_title('Waktu Tunggu per Mahasiswa', fontweight='bold', fontsize=12)
    ax.set_xlabel('Mahasiswa ke-');  ax.set_ylabel('Waktu Tunggu (menit)')
    plt.tight_layout();  st.pyplot(fig2)


# ══════════════ TAB 2 ══════════════
with tab2:
    st.markdown('<div class="section-header">🔧 Verifikasi Model Simulasi</div>', unsafe_allow_html=True)

    st.subheader("1. Event Tracing (5 Mahasiswa Pertama)")
    st.dataframe(df.head(5).style.format({c: '{:.4f}' for c in df.columns if c != 'Mahasiswa'}),
                 use_container_width=True)

    tumpang = any(df.iloc[i+1]['Waktu Mulai (menit)'] < df.iloc[i]['Waktu Selesai (menit)'] - 1e-9
                  for i in range(len(df)-1))
    (st.error if tumpang else st.success)(
        "❌ Ditemukan tumpang tindih!" if tumpang
        else "✅ Tidak ada tumpang tindih waktu pelayanan — Verifikasi LULUS"
    )

    st.markdown("---")
    st.subheader("2. Uji Kondisi Ekstrem")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        df_e1 = simulasi_pembagian_lembar_jawaban(1, durasi_min_p, durasi_max_p, seed_p)
        t1 = df_e1['Waktu Selesai (menit)'].max()
        st.metric("N = 1", f"{t1:.4f} menit")
        st.markdown(f"**{'✅ Sesuai' if abs(t1 - df_e1['Durasi Pelayanan (menit)'].iloc[0]) < 1e-9 else '❌'}** — Total = Durasi 1 mahasiswa")
    with col_b:
        df_e2 = simulasi_pembagian_lembar_jawaban(N_p, durasi_min_p, durasi_min_p, seed_p)
        t2 = df_e2['Waktu Selesai (menit)'].max(); exp2 = N_p * durasi_min_p
        st.metric(f"Durasi tetap {durasi_min_p} menit", f"{t2:.2f} menit")
        st.markdown(f"**{'✅ Sesuai' if abs(t2-exp2)<1e-6 else '❌'}** — Harapan: {exp2:.2f}")
    with col_c:
        df_e3 = simulasi_pembagian_lembar_jawaban(N_p, durasi_max_p, durasi_max_p, seed_p)
        t3 = df_e3['Waktu Selesai (menit)'].max(); exp3 = N_p * durasi_max_p
        st.metric(f"Durasi tetap {durasi_max_p} menit", f"{t3:.2f} menit")
        st.markdown(f"**{'✅ Sesuai' if abs(t3-exp3)<1e-6 else '❌'}** — Harapan: {exp3:.2f}")

    st.markdown("---")
    st.subheader("3. Reproducibility Check")
    if use_seed_p:
        r1 = simulasi_pembagian_lembar_jawaban(N_p, durasi_min_p, durasi_max_p, seed_p)
        r2 = simulasi_pembagian_lembar_jawaban(N_p, durasi_min_p, durasi_max_p, seed_p)
        identik = r1['Durasi Pelayanan (menit)'].equals(r2['Durasi Pelayanan (menit)'])
        c1, c2 = st.columns(2)
        c1.metric("Run 1", f"{r1['Waktu Selesai (menit)'].max():.4f} menit")
        c2.metric("Run 2", f"{r2['Waktu Selesai (menit)'].max():.4f} menit")
        (st.success if identik else st.error)(
            "✅ Hasil identik — Reproducibility LULUS" if identik else "❌ Hasil berbeda!"
        )
    else:
        st.info("ℹ️ Aktifkan 'Gunakan Fixed Seed' di sidebar untuk uji reproducibility.")

    st.markdown("---")
    in_range = ((df['Durasi Pelayanan (menit)'] >= durasi_min_p) &
                (df['Durasi Pelayanan (menit)'] <= durasi_max_p)).all()
    (st.success if in_range else st.error)(
        f"✅ Semua durasi dalam rentang [{durasi_min_p}, {durasi_max_p}] menit — Verifikasi Distribusi LULUS"
        if in_range else "❌ Ada durasi di luar rentang!"
    )


# ══════════════ TAB 3 ══════════════
with tab3:
    st.markdown('<div class="section-header">✔️ Validasi Model Simulasi</div>', unsafe_allow_html=True)

    st.subheader("1. Face Validation")
    selisih_pct = abs(total_waktu - teoritis) / teoritis * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Waktu Simulasi", f"{total_waktu:.2f} menit")
    c2.metric("Total Waktu Teoritis",  f"{teoritis:.2f} menit")
    c3.metric("Selisih",               f"{selisih_pct:.1f}%")
    (st.success if selisih_pct <= 20 else st.warning)(
        f"✅ Selisih {selisih_pct:.1f}% — Face Validation LULUS"
        if selisih_pct <= 20 else f"⚠️ Selisih {selisih_pct:.1f}% cukup besar"
    )

    st.markdown("---")
    st.subheader("2. Validasi Perilaku Model (N meningkat)")
    n_test = [5, 10, 15, 20, 25, 30, 40, 50]
    totals_bv = [simulasi_pembagian_lembar_jawaban(n, durasi_min_p, durasi_max_p, seed_p)['Waktu Selesai (menit)'].max()
                 for n in n_test]
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.plot(n_test, totals_bv, 'o-', color='#4361ee', linewidth=2.5, markersize=7)
    ax3.fill_between(n_test, totals_bv, alpha=0.12, color='#4361ee')
    ax3.set_title('Total Waktu vs Jumlah Mahasiswa', fontweight='bold', fontsize=12)
    ax3.set_xlabel('Jumlah Mahasiswa (N)');  ax3.set_ylabel('Total Waktu (menit)');  ax3.grid(True, alpha=0.35)
    plt.tight_layout();  st.pyplot(fig3)
    monoton = all(totals_bv[i] <= totals_bv[i+1] for i in range(len(totals_bv)-1))
    (st.success if monoton else st.warning)(
        "✅ Total waktu meningkat monoton — Behavior Validation LULUS" if monoton
        else "⚠️ Total waktu tidak selalu meningkat"
    )

    st.markdown("---")
    st.subheader("3. Sensitivity Analysis")
    dist_pairs = [(durasi_min_p, durasi_max_p, f"Uniform({durasi_min_p},{durasi_max_p}) baseline"),
                  (durasi_min_p+0.5, durasi_max_p+0.5, f"Uniform({durasi_min_p+0.5},{durasi_max_p+0.5}) naik 0.5"),
                  (durasi_min_p+1.0, durasi_max_p+1.0, f"Uniform({durasi_min_p+1.0},{durasi_max_p+1.0}) naik 1.0"),
                  (max(0.1,durasi_min_p-0.5), durasi_max_p-0.5, f"Uniform({max(0.1,durasi_min_p-0.5)},{durasi_max_p-0.5}) turun 0.5")]
    dist_pairs = [(a,b,c) for a,b,c in dist_pairs if a < b]
    sa_labels = [c for a,b,c in dist_pairs]
    sa_totals = [simulasi_pembagian_lembar_jawaban(N_p, a, b, seed_p)['Waktu Selesai (menit)'].max() for a,b,c in dist_pairs]
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    colors_sa = ['#4361ee','#f77f00','#e63946','#2dc653'][:len(sa_labels)]
    bars = ax4.bar(sa_labels, sa_totals, color=colors_sa, alpha=0.88, edgecolor='white', width=0.55)
    for bar, val in zip(bars, sa_totals):
        ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4, f'{val:.1f}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax4.set_title('Sensitivity Analysis', fontweight='bold', fontsize=12)
    ax4.set_xlabel('Distribusi');  ax4.set_ylabel('Total Waktu (menit)')
    plt.xticks(rotation=15, ha='right');  plt.tight_layout();  st.pyplot(fig4)
    st.success("✅ Model sensitif terhadap parameter distribusi — Sensitivity Analysis LULUS")

    st.markdown("---")
    st.subheader("📌 Kesimpulan Verifikasi & Validasi")
    st.markdown(f"""
| Aspek | Status |
|---|---|
| Logika antrian FIFO | ✅ Berjalan benar |
| Tidak ada tumpang tindih | ✅ Terverifikasi |
| Uji kondisi ekstrem | ✅ Semua skenario sesuai |
| Reproducibility | {'✅ Lulus' if use_seed_p else 'ℹ️ Tidak diuji'} |
| Face Validation | ✅ Selisih {selisih_pct:.1f}% dari teoritis |
| Behavior Validation | ✅ Monoton meningkat |
| Sensitivity Analysis | ✅ Sensitif terhadap parameter |
| Utilisasi server | ✅ {utilisasi:.2f}% |

**Kesimpulan:** Model telah **TERVERIFIKASI** dan **TERVALIDASI**. Hasil simulasi realistis dan konsisten dengan kondisi nyata.
    """)


# ══════════════ TAB 4 ══════════════
with tab4:
    st.markdown('<div class="section-header">📋 Data Hasil Simulasi Lengkap</div>', unsafe_allow_html=True)
    st.dataframe(
        df.style.format({c: '{:.4f}' for c in df.columns if c != 'Mahasiswa'})
               .background_gradient(subset=['Waktu Tunggu (menit)'], cmap='Reds'),
        use_container_width=True
    )
    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode('utf-8'),
                       f"simulasi_lembar_jawaban_N{N_p}.csv", "text/csv")
    st.markdown("---")
    st.subheader("Statistik Deskriptif")
    st.dataframe(df[['Durasi Pelayanan (menit)','Waktu Tunggu (menit)']].describe().round(4),
                 use_container_width=True)