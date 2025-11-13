// app/frontend/static/API.js

/**
 * Objek API berisi fungsi untuk berkomunikasi dengan backend Flask.
 * Tidak memakai export agar bisa dipakai langsung di browser tanpa error "API is not defined".
 */
const API = {
  // Ganti baseURL ini sesuai alamat backend Flask kamu
  baseURL: "http://127.0.0.1:5000/api",

  /**
   * Upload file dataset (CSV/XLSX/JSON) ke backend Flask.
   * Endpoint: POST /api/upload
   */
  async uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${this.baseURL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Upload failed: ${errText}`);
      }

      // Hasil JSON dari backend (kolom, preview, dsb)
      return await response.json();
    } catch (error) {
      console.error("❌ Upload error:", error);
      throw new Error("Failed to upload dataset. Please try again.");
    }
  },

  /**
   * Jalankan analisis regresi berdasarkan input user.
   * Endpoint: POST /api/analyze
   */
  async runAnalysis(payload) {
    try {
      const response = await fetch(`${this.baseURL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Analysis failed: ${errText}`);
      }

      // Hasil analisis regresi (koefisien, metrik, dll)
      return await response.json();
    } catch (error) {
      console.error("❌ Analysis error:", error);
      throw new Error("Regression analysis failed. Please check your input.");
    }
  },

  /**
   * (Opsional) Ambil daftar model regresi dari backend.
   * Endpoint: GET /api/models
   */
  async getModels() {
    try {
      const response = await fetch(`${this.baseURL}/models`);
      if (!response.ok) throw new Error(await response.text());
      return await response.json();
    } catch (error) {
      console.error("❌ Failed to load models:", error);
      throw new Error("Cannot load available regression models.");
    }
  },
};

// 🟢 Tidak ada 'export' agar variabel API bisa diakses global di main.js
