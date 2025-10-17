/**
 * API.js — Handles all communication with the Flask backend.
 * Works with Flask sessions (credentials included) and supports multiple regression types.
 */

const API = {
  /**
   * Upload dataset to the backend.
   * @param {File} file
   * @returns {Promise<object>} Response containing column names, etc.
   */
  async uploadFile(file) {
    const formData = new FormData();
    formData.append("dataset", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
        credentials: "include", // <--- keep session active in Flask
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ error: response.statusText }));
        throw new Error(err.error || "Gagal mengunggah file ke server.");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in uploadFile:", error);
      throw error;
    }
  },

  /**
   * Run regression analysis.
   * @param {object} payload - Configuration { features, target, modelType, degree?, alpha? }
   * @returns {Promise<object>} Response with model summary, metrics, and charts
   */
  async runAnalysis(payload) {
    try {
      const response = await fetch("/api/run-regression", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        credentials: "include", // <--- essential for Flask session persistence
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ error: response.statusText }));
        throw new Error(err.error || "Gagal menjalankan analisis regresi.");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in runAnalysis:", error);
      throw error;
    }
  },
};
