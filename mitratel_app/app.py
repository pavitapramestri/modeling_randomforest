from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

TABLEAU_URL = "https://public.tableau.com"  # Ganti dengan URL Tableau kamu

MODEL_STATS = {
    'algorithm': 'Random Forest + RUS',
    'accuracy': '69.71%',
    'f1_score': '72.94%',
    'cv_accuracy': '69.57% ± 0.82%',
    'training_rows': '52,427',
    'top_feature_1': 'site_code',
    'top_feature_2': 'scope_of_work',
}

MONTH_NAMES = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
    7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}

# Load CSV hasil prediksi
CSV_PATH = os.path.join(os.path.dirname(__file__), 'hasil_prediksi_severity.csv')

def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, sep=None, engine='python')
        df.columns = df.columns.str.strip()
        # Fix koma desimal → titik
        for col in ['confidence_score', 'confidence_minor', 'confidence_major']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
        return df
    return pd.DataFrame()

def month_to_name(month_num):
    try:
        return MONTH_NAMES.get(int(month_num), str(month_num))
    except:
        return str(month_num)

@app.route('/')
def landing():
    return render_template('landing.html', tableau_url=TABLEAU_URL, model_stats=MODEL_STATS)

@app.route('/dashboard')
def dashboard():
    df = load_data()
    kota_list = sorted(df['kota_kabupaten'].dropna().unique().tolist()) if not df.empty else []
    return render_template('dashboard.html', kota_list=kota_list, tableau_url=TABLEAU_URL, model_stats=MODEL_STATS)

@app.route('/api/sites')
def get_sites():
    kota = request.args.get('kota', '')
    df = load_data()
    if df.empty or not kota:
        return jsonify([])
    sites = sorted(df[df['kota_kabupaten'] == kota]['nama_site'].dropna().unique().tolist())
    return jsonify(sites)

@app.route('/api/predict')
def predict():
    kota = request.args.get('kota', '')
    site = request.args.get('site', '')
    df = load_data()

    if df.empty or not kota or not site:
        return jsonify({'error': 'Data tidak tersedia'}), 400

    # Filter data untuk site yang dipilih
    site_df = df[(df['kota_kabupaten'] == kota) & (df['nama_site'] == site)]

    if site_df.empty:
        return jsonify({'error': 'Site tidak ditemukan'}), 404

    # Ambil prediksi terbaru (baris terakhir)
    latest = site_df.iloc[-1]

    # Hitung mayoritas prediksi
    major_count = (site_df['predicted_severity'] == 'Major').sum()
    minor_count = (site_df['predicted_severity'] == 'Minor').sum()
    dominant = 'Major' if major_count >= minor_count else 'Minor'

    # Confidence rata-rata
    avg_confidence = float(site_df['confidence_score'].mean())

    # Histori maintenance (semua record site ini)
    histori = site_df[['month', 'scope_of_work', 'actual_severity', 'predicted_severity', 'confidence_score']].copy()
    histori = histori.sort_values('month', ascending=False)
    histori_list = histori.head(10).to_dict('records')

    # Format confidence score
    for row in histori_list:
        row['confidence_score'] = f"{float(row['confidence_score'])*100:.1f}%"
        row['month'] = month_to_name(row['month'])

    result = {
        'site': site,
        'kota': kota,
        'predicted_severity': dominant,
        'confidence_score': f"{avg_confidence*100:.1f}%",
        'total_records': len(site_df),
        'major_count': int(major_count),
        'minor_count': int(minor_count),
        'histori': histori_list,
    }
    return jsonify(result)

@app.route('/api/map-data')
def map_data():
    df = load_data()
    if df.empty:
        return jsonify([])

    # Agregasi per kota
    summary = df.groupby('kota_kabupaten').agg(
        total=('nama_site', 'count'),
        major=('predicted_severity', lambda x: (x == 'Major').sum()),
        minor=('predicted_severity', lambda x: (x == 'Minor').sum()),
    ).reset_index()

    summary['dominant'] = summary.apply(
        lambda r: 'Major' if r['major'] >= r['minor'] else 'Minor', axis=1
    )
    summary['major_rate'] = (summary['major'] / summary['total'] * 100).round(1)

    return jsonify(summary.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
