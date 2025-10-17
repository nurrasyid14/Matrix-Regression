document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("file-upload");
  const fileNameSpan = document.getElementById("file-name");
  const btnRun = document.getElementById("btn-run");
  const btnReset = document.getElementById("btn-reset");
  const selectAllBtn = document.getElementById("select-all-features");
  const deselectAllBtn = document.getElementById("deselect-all-features");
  const regressionType = document.getElementById("regression-type");
  const polyOptions = document.getElementById("polynomial-options");
  const ridgeOptions = document.getElementById("ridge-options");

  // Show/hide regression-specific options
  regressionType.addEventListener("change", () => {
    const v = regressionType.value;
    polyOptions.classList.toggle("hidden", v !== "polynomial");
    ridgeOptions.classList.toggle("hidden", v !== "ridge");
  });

  // File selection & upload
  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    fileNameSpan.textContent = file.name;
    UI.showStatus("Uploading...");

    try {
      const result = await API.uploadFile(file);
      UI.showStatus("File uploaded. Columns loaded.");
      UI.populateColumnSelectors(result.columns);
    } catch (err) {
      UI.showStatus(err.message, true);
    }
  });

  // Select all / deselect all features
  selectAllBtn.addEventListener("click", () => {
    document.querySelectorAll("#feature-selector input[type=checkbox]").forEach(cb => cb.checked = true);
  });
  deselectAllBtn.addEventListener("click", () => {
    document.querySelectorAll("#feature-selector input[type=checkbox]").forEach(cb => cb.checked = false);
  });

  // Reset dashboard
  btnReset.addEventListener("click", () => {
    UI.resetDashboard();
    UI.clearSelectors();
    fileInput.value = "";
    fileNameSpan.textContent = "No file chosen";
    UI.showStatus("Reset done.");
  });

  // Run analysis
  btnRun.addEventListener("click", async () => {
    const selectedFeatures = Array.from(document.querySelectorAll("#feature-selector input[type=checkbox]:checked")).map(i => i.value);
    const selectedTarget = document.querySelector("#target-selector input[type=radio]:checked")?.value;

    if (!selectedFeatures.length) { UI.showStatus("Select at least one feature", true); return; }
    if (!selectedTarget) { UI.showStatus("Select a target variable", true); return; }

    // Determine regression options
    let modelType = regressionType.value;
    let degree = undefined;
    let alpha = undefined;

    if (modelType === "polynomial") {
      degree = parseInt(document.getElementById("poly-degree").value || "2", 10);
    } else if (modelType === "ridge") {
      alpha = parseFloat(document.getElementById("ridge-alpha").value || "1.0");
    }

    UI.showStatus("Running analysis...");

    try {
      // Call API with correct arguments
      const resp = await API.runAnalysis(selectedFeatures, selectedTarget, modelType, degree, alpha);
      UI.showStatus("Analysis complete.");
      UI.displayResults(resp);
    } catch (err) {
      UI.showStatus(err.message, true);
    }
  });
});
