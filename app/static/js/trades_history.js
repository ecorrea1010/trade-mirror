(function () {
  const rowsPerPage = 6;
  let currentPage  = 1;
  let trades       = [];
  let filtered     = [];

  const tbody             = document.getElementById("tradeTableBody");
  const paginationInfo    = document.getElementById("paginationInfo");
  const paginationButtons = document.getElementById("paginationButtons");
  const searchInput       = document.getElementById("searchInput");
  const clearSearchBtn    = document.getElementById("clearSearchBtn");

  function renderTable() {
    const total    = filtered.length;
    const totalPages = Math.ceil(total / rowsPerPage) || 1;
    if (currentPage > totalPages) currentPage = totalPages;

    const start = (currentPage - 1) * rowsPerPage;
    const rows  = filtered.slice(start, start + rowsPerPage);

    if (rows.length === 0) {
      tbody.innerHTML = `<tr class="empty-row"><td colspan="7">No hay operaciones registradas aún.</td></tr>`;
      paginationInfo.innerText = "";
      paginationButtons.innerHTML = "";
      return;
    }

    tbody.innerHTML = rows.map(t => {
      const tipo   = t.type === "compra"
        ? `<span class="badge-buy"><i class="bi bi-arrow-up-short"></i> Compra</span>`
        : `<span class="badge-sell"><i class="bi bi-arrow-down-short"></i> Venta</span>`;
      const estado = t.status === "completado"
        ? `<span class="status-completed"><i class="bi bi-check-circle-fill me-1"></i> Completado</span>`
        : `<span class="status-pending"><i class="bi bi-hourglass-split me-1"></i> Pendiente</span>`;
      const qty = t.quantity % 1 !== 0 ? t.quantity.toFixed(4) : t.quantity;

      return `<tr>
        <td><span class="fw-semibold" style="color:#2c7da0;">${t.id}</span></td>
        <td><strong>${t.pair}</strong></td>
        <td>${tipo}</td>
        <td>${qty}</td>
        <td>$${parseFloat(t.price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
        <td>${t.date}</td>
        <td>${estado}</td>
      </tr>`;
    }).join("");

    const endCount = Math.min(start + rowsPerPage, total);
    paginationInfo.innerText = `Mostrando ${start + 1} - ${endCount} de ${total} operaciones`;

    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    if (totalPages <= 1) { paginationButtons.innerHTML = ""; return; }

    let html = `<button class="page-btn" data-page="prev" ${currentPage === 1 ? "disabled" : ""}>
                  <i class="bi bi-chevron-left"></i></button>`;

    let start = Math.max(1, currentPage - 2);
    let end   = Math.min(totalPages, currentPage + 2);
    if (end - start < 4) {
      if (start === 1) end = Math.min(totalPages, 5);
      else if (end === totalPages) start = Math.max(1, totalPages - 4);
    }

    for (let i = start; i <= end; i++) {
      html += `<button class="page-btn ${i === currentPage ? "active-page" : ""}" data-page="${i}">${i}</button>`;
    }

    html += `<button class="page-btn" data-page="next" ${currentPage === totalPages ? "disabled" : ""}>
               <i class="bi bi-chevron-right"></i></button>`;

    paginationButtons.innerHTML = html;

    paginationButtons.querySelectorAll(".page-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const val = btn.getAttribute("data-page");
        if (val === "prev" && currentPage > 1)          currentPage--;
        else if (val === "next" && currentPage < totalPages) currentPage++;
        else if (!isNaN(parseInt(val)))                 currentPage = parseInt(val);
        renderTable();
      });
    });
  }

  function applyFilter() {
    const term = searchInput.value.trim().toLowerCase();
    filtered   = term === ""
      ? [...trades]
      : trades.filter(t =>
          t.pair.toLowerCase().includes(term) ||
          t.type.toLowerCase().includes(term)
        );
    currentPage = 1;
    renderTable();
  }

  searchInput.addEventListener("input", applyFilter);
  clearSearchBtn.addEventListener("click", () => {
    searchInput.value = "";
    applyFilter();
  });

  // Inicializa con array vacío — cuando conectes la DB
  // reemplaza esto por un fetch a tu endpoint JSON
  trades   = [];
  filtered = [...trades];
  renderTable();
})();