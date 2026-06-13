/* =========================================================
   register.js · Trade Mirror · Formulario de operación
   ========================================================= */

(function () {
  'use strict';

  // ── Referencias DOM ──────────────────────────────────────
  const form        = document.getElementById('tradeForm');
  const buyBtn      = document.getElementById('buyBtn');
  const sellBtn     = document.getElementById('sellBtn');
  const radioInputs = document.querySelectorAll('input[name="direction"]');

  const entryInput  = document.getElementById('entry_price');
  const exitInput   = document.getElementById('exit_price');
  const tpInput     = document.getElementById('take_profit');
  const slInput     = document.getElementById('stop_loss');
  const qtyInput    = document.getElementById('quantity');
  const rrDisplay   = document.getElementById('rrDisplay');
  const rrValue     = document.getElementById('rrValue');
  const riskValue   = document.getElementById('riskValue');

  const tagsWrap    = document.getElementById('tagsWrap');
  const tagsList    = document.getElementById('tagsList');
  const tagsInput   = document.getElementById('tagsInput');
  const tagsHidden  = document.getElementById('tagsHidden');

  const emotionChips = document.querySelectorAll('.emotion-chip');


  // ── Fecha/hora por defecto ────────────────────────────────
  (function setDefaultDate() {
    const el  = document.getElementById('opened_at');
    if (!el || el.value) return;
    const now = new Date();
    const pad = n => String(n).padStart(2, '0');
    el.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}` +
               `T${pad(now.getHours())}:${pad(now.getMinutes())}`;
  })();


  // ── Dirección BUY / SELL ──────────────────────────────────
  function syncDirectionUI() {
    const val = document.querySelector('input[name="direction"]:checked')?.value;
    buyBtn.classList.toggle('active-buy', val === 'BUY');
    sellBtn.classList.toggle('active-sell', val === 'SELL');
  }

  radioInputs.forEach(r => r.addEventListener('change', syncDirectionUI));
  syncDirectionUI();

  // Clic en toda la etiqueta también marca el radio
  [buyBtn, sellBtn].forEach(label => {
    label.addEventListener('click', () => {
      const radio = label.querySelector('input[type="radio"]');
      if (radio) { radio.checked = true; syncDirectionUI(); }
    });
  });


  // ── Cálculo R:R ──────────────────────────────────────────
  function calcRR() {
    const entry = parseFloat(entryInput?.value);
    const tp    = parseFloat(tpInput?.value);
    const sl    = parseFloat(slInput?.value);
    const qty   = parseFloat(qtyInput?.value);

    if (!isFinite(entry) || !isFinite(tp) || !isFinite(sl) || entry === sl) {
      rrDisplay.style.display = 'none';
      return;
    }

    const reward = Math.abs(tp - entry);
    const risk   = Math.abs(entry - sl);
    const rr     = (reward / risk).toFixed(2);

    rrValue.textContent  = `1 : ${rr}`;
    riskValue.textContent = isFinite(qty) && qty > 0
      ? `$${(risk * qty).toFixed(2)}`
      : `$${risk.toFixed(4)} / unidad`;

    rrDisplay.style.display = 'inline-flex';
  }

  [entryInput, tpInput, slInput, qtyInput].forEach(el => {
    el?.addEventListener('input', calcRR);
  });


  // ── Tags input ────────────────────────────────────────────
  const tagValues = new Set();

  function renderTags() {
    tagsList.innerHTML = '';
    tagValues.forEach(tag => {
      const chip = document.createElement('span');
      chip.className = 'tag-chip';
      chip.innerHTML = `${tag}<button type="button" aria-label="Eliminar ${tag}">&times;</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        tagValues.delete(tag);
        renderTags();
      });
      tagsList.appendChild(chip);
    });
    tagsHidden.value = [...tagValues].join(',');
  }

  tagsInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      const val = tagsInput.value.trim().replace(/,/g, '');
      if (val && tagValues.size < 10) {
        tagValues.add(val.toLowerCase());
        renderTags();
        tagsInput.value = '';
      }
    }
    if (e.key === 'Backspace' && !tagsInput.value && tagValues.size) {
      const last = [...tagValues].pop();
      tagValues.delete(last);
      renderTags();
    }
  });

  tagsWrap.addEventListener('click', () => tagsInput.focus());


  // ── Emociones (toggle visual) ─────────────────────────────
  emotionChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const checkbox = chip.querySelector('input[type="checkbox"]');
      if (!checkbox) return;
      checkbox.checked = !checkbox.checked;
      chip.classList.toggle('checked', checkbox.checked);
    });
  });


  // ── Toast minimalista ─────────────────────────────────────
  function toast(msg, type = 'success') {
    document.querySelectorAll('.tm-toast').forEach(el => el.remove());

    const icons = {
      success: '<i class="bi bi-check-circle-fill" style="color:#2c7da0"></i>',
      warn:    '<i class="bi bi-exclamation-triangle-fill" style="color:#e6a017"></i>',
      error:   '<i class="bi bi-x-circle-fill" style="color:#c0392b"></i>',
    };

    const el = document.createElement('div');
    el.className = `tm-toast toast-${type}`;
    el.innerHTML = `${icons[type] || icons.success} <span>${msg}</span>`;
    document.body.appendChild(el);

    setTimeout(() => el.remove(), 3000);
  }


  // ── Validación y envío ────────────────────────────────────
  form.addEventListener('submit', function (e) {
    const pair     = document.getElementById('symbol')?.value;
    const qty      = parseFloat(document.getElementById('quantity')?.value);
    const entry    = parseFloat(document.getElementById('entry_price')?.value);
    const platform = document.getElementById('platform')?.value;
    const date     = document.getElementById('opened_at')?.value;

    if (!pair) {
      e.preventDefault();
      toast('Selecciona un par o activo.', 'warn');
      return;
    }
    if (!isFinite(qty) || qty <= 0) {
      e.preventDefault();
      toast('Ingresa una cantidad válida (mayor a 0).', 'warn');
      document.getElementById('quantity')?.focus();
      return;
    }
    if (!isFinite(entry) || entry <= 0) {
      e.preventDefault();
      toast('Ingresa un precio de entrada válido.', 'warn');
      document.getElementById('entry_price')?.focus();
      return;
    }
    if (!platform) {
      e.preventDefault();
      toast('Selecciona la plataforma o broker.', 'warn');
      return;
    }
    if (!date) {
      e.preventDefault();
      toast('Selecciona la fecha y hora.', 'warn');
      return;
    }
    // Si todo OK, el form hace submit normal (Flask lo maneja)
  });

})();
