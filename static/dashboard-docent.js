function renderAnalyseLijst(titel, items, naamVeld) {
  if (!items.length) {
    return `
      <div class="col-md-4">
        <h3 class="h6">${titel}</h3>
        <p class="text-muted mb-0">Geen data gevonden.</p>
      </div>
    `;
  }

  const regels = items.map(item => `
    <div class="mb-3">
      <div class="d-flex justify-content-between gap-3">
        <strong>${item[naamVeld]}</strong>
        <span class="badge bg-${item.color}">
          ${item.status} (${item.score}%)
        </span>
      </div>
      <div class="progress mt-2" style="height: 8px;">
        <div class="progress-bar bg-${item.color}" style="width: ${item.score}%;"></div>
      </div>
    </div>
  `).join("");

  return `
    <div class="col-md-4">
      <h3 class="h6">${titel}</h3>
      ${regels}
    </div>
  `;
}

function laadKlasanalyse() {
  const klasSelect = document.getElementById("klas_id");
  const container = document.getElementById("docentKlasanalyse");

  if (!klasSelect || !container) {
    return;
  }

  const klasId = klasSelect.value;
  container.innerHTML = `<p class="text-muted mb-0">Klasanalyse laden...</p>`;

  fetch("/api/docent/klasanalyse?klas_id=" + encodeURIComponent(klasId))
    .then(response => {
      if (!response.ok) {
        throw new Error("Kon klasanalyse niet laden");
      }

      return response.json();
    })
    .then(data => {
      container.innerHTML = `
        <div class="row g-4">
          ${renderAnalyseLijst("Leerlingen", data.leerlingen, "naam")}
          ${renderAnalyseLijst("Leerdoelen", data.leerdoelen, "titel")}
          ${renderAnalyseLijst("Niveaus", data.niveaus, "level")}
        </div>
      `;
    })
    .catch(() => {
      container.innerHTML = `<p class="text-danger mb-0">Klasanalyse kon niet worden geladen.</p>`;
    });
}

function laadLeerlingen() {
  const klasSelect = document.getElementById("klas_id");
  const placeholder = document.getElementById("leerlingen-placeholder");

  if (!klasSelect || !placeholder) {
    return;
  }

  const klasId = klasSelect.value;
  placeholder.innerHTML = `
    <div class="card shadow-sm mt-3">
      <div class="card-body">
        <h2 class="h5 card-title">Leerlingen</h2>
        <p class="text-muted mb-0">Leerlingen laden...</p>
      </div>
    </div>
  `;

  const params = new URLSearchParams();
  if (klasId) {
    params.append("klas_id", klasId);
  }

  fetch("/dashboard-docent/leerlingen-fragment?" + params.toString())
    .then(response => {
      if (!response.ok) {
        throw new Error("Kon leerlingen niet laden");
      }
      return response.text();
    })
    .then(html => {
      placeholder.innerHTML = html;
      window.history.replaceState({}, "", "/dashboard-docent?klas_id=" + encodeURIComponent(klasId));
    })
    .catch(() => {
      placeholder.innerHTML = `
        <div class="card shadow-sm mt-3">
          <div class="card-body">
            <h2 class="h5 card-title">Leerlingen</h2>
            <p class="text-danger mb-0">Fout bij laden van leerlingen.</p>
          </div>
        </div>
      `;
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const klasSelect = document.getElementById("klas_id");

  if (klasSelect) {
    klasSelect.addEventListener("change", laadLeerlingen);
    klasSelect.addEventListener("change", laadKlasanalyse);
  }

  laadKlasanalyse();
});