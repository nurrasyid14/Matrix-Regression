/**
 * API.js — Handles all communication between the frontend and Flask backend.
 * Now with session persistence via cookies (credentials: 'include')
 */

const API = {
    /**
     * Upload dataset file to Flask backend.
     * @param {File} file - The dataset file to upload.
     * @returns {Promise<object>} - JSON response from backend.
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('dataset', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
                credentials: 'include', // ✅ allow Flask session cookies
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Gagal mengunggah file.');
            }

            return await response.json();
        } catch (error) {
            console.error('Error in uploadFile:', error);
            throw error;
        }
    },

    /**
     * Run regression analysis on uploaded dataset.
     * @param {string[]} selectedFeatures - Array of feature names.
     * @param {string} selectedTarget - Target variable name.
     * @param {string} modelType - Type of regression ('linear', 'ridge', 'polynomial').
     * @returns {Promise<object>} - JSON response containing regression results.
     */
    async runAnalysis(selectedFeatures, selectedTarget, modelType = 'linear') {
        try {
            const response = await fetch('/api/run-regression', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', // ✅ ensure session persistence
                body: JSON.stringify({
                    features: selectedFeatures,
                    target: selectedTarget,
                    modelType: modelType,
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