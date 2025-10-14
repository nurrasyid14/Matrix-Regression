/**
 * Mengelola semua komunikasi (request) ke API backend Flask.
 */

const API = {
    /**
     * Mengirim file ke backend untuk diunggah dan diproses.
     * @param {File} file - File yang akan diunggah.
     * @returns {Promise<object>} - Promise yang akan resolve dengan data hasil (misal: { columns: [...] }).
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('dataset', file);

        try {
            // Ganti '/api/upload' dengan endpoint Flask Anda yang sebenarnya
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Gagal mengunggah file.');
            }

            return await response.json();
        } catch (error) {
            console.error('Error in uploadFile:', error);
            throw error; // Lemparkan error agar bisa ditangkap di main.js
        }
    },

    /**
     * Mengirim konfigurasi analisis (fitur & target) ke backend.
     * @param {string[]} selectedFeatures - Array nama kolom fitur yang dipilih.
     * @param {string} selectedTarget - Nama kolom target yang dipilih.
     * @returns {Promise<object>} - Promise yang akan resolve dengan hasil analisis.
     */
    async runAnalysis(selectedFeatures, selectedTarget) {
        try {
            // Ganti '/api/run-regression' dengan endpoint Flask Anda yang sebenarnya
            const response = await fetch('/api/run-regression', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    features: selectedFeatures,
                    target: selectedTarget,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Gagal menjalankan analisis.');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error in runAnalysis:', error);
            throw error;
        }
    },
};

