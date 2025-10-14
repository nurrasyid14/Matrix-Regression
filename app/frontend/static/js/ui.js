/**
 * Mengelola semua manipulasi DOM (membuat elemen, menampilkan hasil).
 */

// Objek untuk menyimpan instance chart agar bisa dihancurkan sebelum membuat yang baru
const charts = {
    featureChart: null,
    accuracyChart: null
};

const UI = {
    /**
     * Mengisi container pemilih kolom dengan checkbox dan radio button.
     * @param {string[]} columns - Array berisi nama-nama kolom dari dataset.
     */
    populateColumnSelectors(columns) {
        const featureSelector = document.getElementById('feature-selector');
        const targetSelector = document.getElementById('target-selector');

        // Kosongkan container sebelum mengisi
        featureSelector.innerHTML = '';
        targetSelector.innerHTML = '';

        columns.forEach(column => {
            // Buat checkbox untuk fitur
            const featureDiv = document.createElement('div');
            featureDiv.className = 'flex items-center';
            featureDiv.innerHTML = `
                <input id="feature-${column}" type="checkbox" value="${column}" name="feature" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                <label for="feature-${column}" class="ml-3 block text-sm text-gray-700">${column}</label>
            `;
            featureSelector.appendChild(featureDiv);

            // Buat radio button untuk target
            const targetDiv = document.createElement('div');
            targetDiv.className = 'flex items-center';
            targetDiv.innerHTML = `
                <input id="target-${column}" type="radio" value="${column}" name="target" class="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-500">
                <label for="target-${column}" class="ml-3 block text-sm text-gray-700">${column}</label>
            `;
            targetSelector.appendChild(targetDiv);
        });

        document.getElementById('selectors-container').classList.remove('hidden');
        document.getElementById('action-button-container').classList.remove('hidden');
    },

    /**
     * Menampilkan hasil analisis di UI.
     * @param {object} results - Objek hasil dari backend.
     */
    displayResults(results) {
        // Tampilkan persamaan
        const equationEl = document.getElementById('regression-equation');
        equationEl.textContent = results.equation || 'Gagal memuat persamaan.';
        
        // Buat Bar Chart untuk Pengaruh Fitur
        this.createFeatureChart(results.featureChartData);

        // Buat Scatter Plot untuk Akurasi
        this.createAccuracyChart(results.accuracyChartData);

        document.getElementById('output-card').classList.remove('hidden');
    },

    createFeatureChart(data) {
        const ctx = document.getElementById('feature-chart').getContext('2d');
        if (charts.featureChart) {
            charts.featureChart.destroy();
        }
        charts.featureChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, title: { display: true, text: 'Nilai Koefisien' } },
                    x: { title: { display: true, text: 'Fitur' } }
                }
            }
        });
    },

    createAccuracyChart(data) {
        const ctx = document.getElementById('accuracy-chart').getContext('2d');
        if (charts.accuracyChart) {
            charts.accuracyChart.destroy();
        }
        charts.accuracyChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Aktual vs. Prediksi',
                        data: data.points,
                        backgroundColor: 'rgba(59, 130, 246, 0.5)'
                    },
                    {
                        label: 'Garis Ideal',
                        data: data.line,
                        type: 'line',
                        borderColor: 'rgba(239, 68, 68, 1)',
                        borderWidth: 2,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: { type: 'linear', position: 'bottom', title: { display: true, text: 'Nilai Aktual' } },
                    y: { title: { display: true, text: 'Nilai Prediksi' } }
                }
            }
        });
    },

    /**
     * Menampilkan atau menyembunyikan loading spinner.
     * @param {boolean} show - True untuk menampilkan, false untuk menyembunyikan.
     */
    toggleLoading(show) {
        const spinner = document.getElementById('loading-spinner');
        const resultsContainer = document.getElementById('results-container');
        
        if (show) {
            spinner.classList.remove('hidden');
            resultsContainer.classList.add('hidden');
            document.getElementById('output-card').classList.remove('hidden');
        } else {
            spinner.classList.add('hidden');
            resultsContainer.classList.remove('hidden');
        }
    },

    /**
     * Menampilkan pesan error sederhana kepada pengguna.
     * @param {string} message - Pesan error yang akan ditampilkan.
     */
    showError(message) {
        alert(message); // Untuk kesederhanaan, kita gunakan alert.
    }
};

