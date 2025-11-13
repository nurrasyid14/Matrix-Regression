// app/frontend/static/main.js

import API from "./API.js";

document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("file-upload");
  const fileNameLabel = document.getElementById("file-name");
  const btnChoose = document.getElementById("btn-choose");
  const btnRun = document.getElementById("btn-run");
  const btnReset = document.getElementById("btn-reset");
  const regressionType = document.getElementById("regression-type");
  const polyOptions = document.getElementById("polynomial-options");
  const ridgeOptions = document.getElementById("ridge-options");
  const polyDegreeInput = document.getElementById("poly-degree");
  const ridgeAlphaInput = document.getElementById("ridge-alpha");

  // -------------------------
  // File Upload
  // -------------------------
  btnChoose.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", async () => {
    if (!fileInput.files.length) return;

    const file = fileInput.files[0];
    fileNameLabel.textContent = file.name;

    try {
      UI.showStatus("Uploading dataset...");
      const resp = await API.uploadFile(file);

      UI.showStatus(resp.message);
      UI.populateColumnSelectors(resp.columns);
      UI.showPreview(resp.preview);
    } catch (error) {
      UI.showStatus(error.message, true);
    }
  });

  // -------------------------
  // Regression type toggle options
  // -------------------------
  regressionType.addEventListener("change", () => {
    const val = regressionType.value;
    polyOptions.classList.toggle("hidden", val !== "polynomial");
    ridgeOptions.classList.toggle("hidden", val !== "ridge");
  });

  // -------------------------
  // Run Analysis
  // -------------------------
  btnRun.addEventListener("click", async () => {
    try {
      UI.showStatus("Running regression analysis...");
      
      // Ambil feature & target
      const features = Array.from(document.querySelectorAll("input[name='feature']:checked")).map(f => f.value);
      const targetEl = document.querySelector("input[name='target']:checked");
      const target = targetEl ? targetEl.value : null;

      if (!features.length || !target) {
        UI.showStatus("Please select features and target.", true);
        return;
      }

      // Payload
      const payload = {
        features,
        target,
        modelType: regressionType.value,
        degree: parseInt(polyDegreeInput.value) || 2,
        alpha: parseFloat(ridgeAlphaInput.value) || 1.0
      };

      const resp = await API.runAnalysis(payload);
      UI.displayResults(resp);
      UI.showStatus("Analysis completed successfully.");
    } catch (error) {
      UI.showStatus(error.message, true);
    }
  });

  // -------------------------
  // Reset dashboard
  // -------------------------
  btnReset.addEventListener("click", () => {
    UI.resetDashboard();
    UI.clearSelectors();
    fileInput.value = "";
    fileNameLabel.textContent = "No file chosen";
    UI.showStatus("Dashboard reset.");
  });

  // -------------------------
  // Select/Deselect all features
  // -------------------------
  document.getElementById("select-all-features").addEventListener("click", () => {
    document.querySelectorAll("input[name='feature']").forEach(f => f.checked = true);
  });

  document.getElementById("deselect-all-features").addEventListener("click", () => {
    document.querySelectorAll("input[name='feature']").forEach(f => f.checked = false);
  });
});
