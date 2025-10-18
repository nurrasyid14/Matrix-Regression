// app/frontend/static/main.js

import API from "./API.js";

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

  // ---------------------------
  // Show/hide options based on regression type
  // ---------------------------
  regressionType.addEventListener("change", () => {
    const type = regressionType.value;
    polyOptions.classList.toggle("hidden", type !== "polynomial");
    ridgeOptions.classList.toggle("hidden", type !== "ridge");
  });

  // ---------------------------
  // File selection & upload
  // ---------------------------
  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    fileNameSpan.textContent = file.name;
    UI.showStatus("Uploading dataset...");

    try {
      const result = await API.uploadFile(file);
      UI.showStatus("Dataset uploaded successfully.");
      UI.populateColumnSelectors(result.columns);
      UI.showPreview(result.preview);
    } catch (err) {
      UI.showStatus(err.message, true);
    }
  });

  // ---------------------------
  // Select / Deselect all features
  // ---------------------------
  selectAllBtn.addEventListener("click", () => {
    document.querySelectorAll("#feature-selector input[type=checkbox]").forEach(cb => cb.checked = true);
  });
  deselectAllBtn.addEventListener("click", () => {
    document.querySelectorAll("#feature-selector input[type=checkbox]").forEach(cb => cb.checked = false);
  });

  // ---------------------------
  // Reset everything
  // ---------------------------
  btnReset.addEventListener("click", () => {
    UI.resetDashboard();
    UI.clearSelectors();
    fileInput.value = "";
    fileNameSpan.textContent = "No file chosen";
    UI.showStatus("Reset complete.");
  });

  // ---------------------------
  // Run regression analysis
  // ---------------------------
  btnRun.addEventListener("click", async () => {
    const selectedFeatures = Array.from(
      document.querySelectorAll("#feature-selector input[type=checkbox]:checked")
    ).map(cb => cb.value);

    const selectedTarget = document.querySelector("#target-selector input[type=radio]:checked")?.value;

    if (!selectedFeatures.length) {
      UI.showStatus("Select at least one feature.", true);
      return;
    }
    if (!selectedTarget) {
      UI.showStatus("Select a target variable.", true);
      return;
    }

    // Prepare payload for API
    const payload = {
      features: selectedFeatures,
      target: selectedTarget,
      modelType: regressionType.value
    };

    if (regressionType.value === "polynomial") {
      payload.degree = parseInt(document.getElementById("poly-degree").value || "2", 10);
    } else if (regressionType.value === "ridge") {
      payload.alpha = parseFloat(document.getElementById("ridge-alpha").value || "1.0");
    }

    UI.showStatus("Running regression analysis...");

    try {
      const result = await API.runAnalysis(payload);
      UI.showStatus("Analysis complete.");
      UI.displayResults(result);
    } catch (err) {
      UI.showStatus(err.message, true);
    }
  });
});
