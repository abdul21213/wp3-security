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
  }
});