/**
 * Titik masuk utama, mengikat semua event listener dan mengontrol alur aplikasi.
 */

document.addEventListener('DOMContentLoaded', () => {
    // === ELEMEN DOM ===
    const fileInput = document.getElementById('file-upload');
    const fileNameSpan = document.getElementById('file-name');
    const runAnalysisBtn = document.getElementById('run-analysis-btn');
    const selectAllBtn = document.getElementById('select-all-features');
    const deselectAllBtn = document.getElementById('deselect-all-features');
    
    let uploadedColumns = [];

    // === EVENT LISTENERS ===

    // Event listener untuk input file
    fileInput.addEventListener('change', async () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileNameSpan.textContent = file.name;
            
            // Otomatis unggah setelah file dipilih
            try {
                const result = await API.uploadFile(file);
                if (result && result.columns) {
                    uploadedColumns = result.columns;
                    UI.populateColumnSelectors(uploadedColumns);
                    fileNameSpan.textContent = `Berhasil diunggah: ${file.name}`;
                } else {
                    throw new Error("Format respons dari server tidak valid.");
                }
            } catch (error) {
                UI.showError(`Gagal memproses file: ${error.message}`);
                fileNameSpan.textContent = 'Gagal mengunggah file.';
            }
        }
    });

    // Event listener untuk tombol "Jalankan Analisis"
    runAnalysisBtn.addEventListener('click', async () => {
        const selectedFeatures = Array.from(document.querySelectorAll('input[name="feature"]:checked'))
                                     .map(cb => cb.value);
        const selectedTarget = document.querySelector('input[name="target"]:checked')?.value;

        // Validasi
        if (selectedFeatures.length === 0) {
            UI.showError('Pilih setidaknya satu kolom fitur.');
            return;
        }
        if (!selectedTarget) {
            UI.showError('Pilih satu kolom target.');
            return;
        }
        if (selectedFeatures.includes(selectedTarget)) {
            UI.showError('Kolom target tidak boleh sama dengan kolom fitur.');
            return;
        }

        UI.toggleLoading(true);

        try {
            const results = await API.runAnalysis(selectedFeatures, selectedTarget);
            UI.displayResults(results);
        } catch (error) {
            UI.showError(`Analisis gagal: ${error.message}`);
        } finally {
            UI.toggleLoading(false);
        }
    });
    
    // Event listener untuk tombol "Pilih Semua Fitur"
    selectAllBtn.addEventListener('click', () => {
        document.querySelectorAll('input[name="feature"]').forEach(checkbox => {
            checkbox.checked = true;
        });
    });
    
    // Event listener untuk tombol "Hapus Semua Fitur"
    deselectAllBtn.addEventListener('click', () => {
        document.querySelectorAll('input[name="feature"]').forEach(checkbox => {
            checkbox.checked = false;
        });
    });
});

