const UI = (function () {
  let coefChart = null;
  let accuracyChart = null;

  function clearSelectors() {
    document.getElementById("feature-selector").innerHTML = "";
    document.getElementById("target-selector").innerHTML = "";
    document.getElementById("preview").innerHTML = "";
  }

  function populateColumnSelectors(columns) {
    clearSelectors();
    const featureContainer = document.getElementById("feature-selector");
    const targetContainer = document.getElementById("target-selector");

    columns.forEach(col => {
      // feature checkbox
      const wrapper = document.createElement("div");
      wrapper.className = "flex items-center gap-2 mb-1";
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.name = "feature";
      cb.value = col;
      cb.id = `feat-${col}`;
      const lbl = document.createElement("label");
      lbl.htmlFor = cb.id;
      lbl.innerText = col;
      wrapper.appendChild(cb);
      wrapper.appendChild(lbl);
      featureContainer.appendChild(wrapper);

      // target radio
      const rwrap = document.createElement("div");
      rwrap.className = "flex items-center gap-2 mb-1";
      const radio = document.createElement("input");
      radio.type = "radio";
      radio.name = "target";
      radio.value = col;
      radio.id = `tgt-${col}`;
      const rlbl = document.createElement("label");
      rlbl.htmlFor = radio.id;
      rlbl.innerText = col;
      rwrap.appendChild(radio);
      rwrap.appendChild(rlbl);
      targetContainer.appendChild(rwrap);
    });
  }

  function showPreview(dfRowsHtml) {
    // A simple HTML-based preview (server can return small HTML if desired)
    const preview = document.getElementById("preview");
    preview.innerHTML = dfRowsHtml || "<div class='text-xs text-gray-500'>No preview available</div>";
  }

  function showStatus(msg, isError = false) {
    const s = document.getElementById("status");
    s.textContent = msg;
    s.className = isError ? "text-sm text-red-600" : "text-sm text-gray-600";
  }

  function resetDashboard() {
    document.getElementById("equation").textContent = "—";
    document.getElementById("metric-r2").textContent = "—";
    document.getElementById("metric-mse").textContent = "—";
    document.getElementById("metric-rmse").textContent = "—";
    document.getElementById("metric-mae").textContent = "—";
    document.getElementById("metric-ev").textContent = "—";
    if (coefChart) { coefChart.destroy(); coefChart = null; }
    if (accuracyChart) { accuracyChart.destroy(); accuracyChart = null; }
  }

  function renderCoefficients(labels, data) {
    const ctx = document.getElementById("coef-chart").getContext("2d");
    if (coefChart) coefChart.destroy();
    coefChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Coefficient",
          data,
          backgroundColor: labels.map(() => "rgba(59,130,246,0.7)")
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }

  function renderAccuracy(points, line) {
    const ctx = document.getElementById("accuracy-chart").getContext("2d");
    if (accuracyChart) accuracyChart.destroy();
    const scatterData = {
      datasets: [
        {
          label: "Actual vs Predicted",
          data: points.map(p => ({ x: p.x, y: p.y })),
          showLine: false,
          pointRadius: 4,
          pointBackgroundColor: "rgba(16,185,129,0.9)"
        },
        {
          label: "Identity",
          data: line.map(p => ({ x: p.x, y: p.y })),
          type: "line",
          borderColor: "rgba(79,70,229,0.8)",
          borderWidth: 1,
          fill: false,
          showLine: true,
          pointRadius: 0
        }
      ]
    };

    accuracyChart = new Chart(ctx, {
      type: "scatter",
      data: scatterData,
      options: {
        scales: {
          x: { title: { display: true, text: "Actual" } },
          y: { title: { display: true, text: "Predicted" } }
        },
        plugins: { legend: { display: true } }
      }
    });
  }

  function displayResults(resp) {
    // summary
    document.getElementById("equation").textContent = resp.equation || resp.summary || "—";

    // metrics (if available)
    if (resp.metrics) {
      document.getElementById("metric-r2").textContent = resp.metrics["R²"] ?? resp.r2 ?? "—";
      document.getElementById("metric-mse").textContent = resp.metrics["MSE"] ?? resp.mse ?? "—";
      document.getElementById("metric-rmse").textContent = resp.metrics["RMSE"] ?? resp.rmse ?? "—";
      document.getElementById("metric-mae").textContent = resp.metrics["MAE"] ?? resp.mae ?? "—";
      document.getElementById("metric-ev").textContent = resp.metrics["Explained Variance"] ?? resp.ev ?? "—";
    }

    // coefficients (object or chart data)
    if (resp.featureChartData) {
      renderCoefficients(resp.featureChartData.labels, resp.featureChartData.datasets[0].data);
    } else if (resp.coefficients) {
      const keys = Object.keys(resp.coefficients).slice(1); // skip intercept
      const vals = Object.values(resp.coefficients).slice(1);
      renderCoefficients(keys, vals);
    }

    // accuracy
    if (resp.accuracyChartData) {
      renderAccuracy(resp.accuracyChartData.points, resp.accuracyChartData.line);
    }
  }

  return {
    populateColumnSelectors,
    showPreview,
    showStatus,
    resetDashboard,
    displayResults,
    clearSelectors
  };
})();
