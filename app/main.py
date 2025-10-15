import os
import pandas as pd
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS  # Impor CORS
from werkzeug.utils import secure_filename
from sklearn.model_selection import train_test_split

# Impor dari modul Anda
from dataset_receiver.dataset_gate import DatasetGate
from regressor.linear_regression import LinearRegression

# --- Konfigurasi Aplikasi Flask ---
# Membuat instance aplikasi.
# Konfigurasi ini memberi tahu Flask di mana menemukan file HTML dan file statis (CSS/JS)
app = Flask(_name_, template_folder='frontend/templates', static_folder='frontend/static')

# PERBAIKAN: Mengaktifkan CORS untuk mengizinkan permintaan dari frontend
CORS(app)

# Konfigurasi dasar untuk upload dan session
UPLOAD_FOLDER = "uploads_temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'ini-adalah-kunci-rahasia-yang-sangat-aman' # Ganti ini nanti

# --- Rute untuk Menampilkan Halaman Web ---

@app.route("/")
def index():
    """Menampilkan halaman utama (index.html)."""
    return render_template("index.html")

# --- Rute API untuk Frontend ---

@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    """
    Menerima file yang diunggah dari frontend, memprosesnya,
    dan menyimpan hasilnya di session pengguna.
    """
    # PERBAIKAN: Kunci 'dataset' harus cocok dengan yang ada di api.js
    if "dataset" not in request.files:
        return jsonify({"error": "Kunci 'dataset' tidak ditemukan dalam permintaan. Pastikan frontend mengirim file dengan benar."}), 400

    file = request.files["dataset"]
    if file.filename == "":
        return jsonify({"error": "Nama file kosong."}), 400

    try:
        # Simpan file sementara dengan aman
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Gunakan DatasetGate Anda untuk memuat file
        df = DatasetGate.quick_load(filepath, numeric_only=True)

        # Simpan DataFrame sebagai format JSON di dalam sesi
        session['dataset_json'] = df.to_json(orient='split')

        # Hapus file sementara setelah tidak diperlukan lagi
        os.remove(filepath)

        # Kirim kembali daftar kolom ke frontend agar bisa ditampilkan
        return jsonify({"columns": df.columns.tolist()})

    except Exception as e:
        # Memberikan pesan error yang lebih informatif jika terjadi kesalahan
        return jsonify({"error": f"Gagal memproses file di backend: {str(e)}"}), 500


@app.route("/api/run-regression", methods=["POST"])
def run_regression_analysis():
    """
    Menjalankan analisis regresi berdasarkan data dari session
    dan konfigurasi yang dikirim oleh frontend.
    """
    if 'dataset_json' not in session:
        return jsonify({"error": "Dataset tidak ditemukan di session. Mohon unggah file terlebih dahulu."}), 400

    try:
        # Muat kembali DataFrame dari data JSON yang tersimpan di session
        df = pd.read_json(session['dataset_json'], orient='split')

        # Ambil konfigurasi (fitur & target) dari frontend
        config = request.json
        features = config.get("features")
        target = config.get("target")

        if not features or not target:
            return jsonify({"error": "Fitur atau target tidak disediakan dalam permintaan."}), 400

        # Siapkan data untuk model
        X = df[features]
        y = df[target]

        # Bagi data untuk pengujian akurasi model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Latih model regresi linear Anda
        model = LinearRegression(normalize=True)
        model.fit(X_train, y_train)
        
        # Buat prediksi pada data uji
        predictions = model.predict(X_test)

        # --- Siapkan Respons JSON yang Sesuai untuk Frontend ---

        # 1. Buat string persamaan model
        coeffs = model.coefficients()
        intercept = coeffs[0]
        feature_coeffs = coeffs[1:]
        equation = f"{target} = {intercept:.4f} + " + " + ".join([f"({coef:.4f} * {feat})" for feat, coef in zip(features, feature_coeffs)])

        # 2. Siapkan data untuk Bar Chart (Pengaruh Fitur)
        feature_chart_data = {
            'labels': features,
            'datasets': [{
                'label': 'Koefisien',
                'data': feature_coeffs.tolist(),
                'backgroundColor': 'rgba(153, 102, 255, 0.6)'
            }]
        }

        # 3. Siapkan data untuk Scatter Plot (Akurasi Model)
        y_test_list = y_test.tolist()
        predictions_list = predictions.flatten().tolist()
        min_val = min(min(y_test_list), min(predictions_list))
        max_val = max(max(y_test_list), max(predictions_list))
        
        accuracy_chart_data = {
            'points': [{'x': actual, 'y': pred} for actual, pred in zip(y_test_list, predictions_list)],
            'line': [{'x': min_val, 'y': min_val}, {'x': max_val, 'y': max_val}]
        }

        return jsonify({
            "equation": equation,
            "featureChartData": feature_chart_data,
            "accuracyChartData": accuracy_chart_data
        })

    except Exception as e:
        import traceback
        traceback.print_exc() # Mencetak error detail di terminal untuk debugging
        return jsonify({"error": f"Analisis gagal: {str(e)}"}), 500

if _name_ == "_main_":
    # Jalankan aplikasi dalam mode debug untuk melihat error
    app.run(host="0.0.0.0", port=5000, debug=True)
