(function () {
  const form          = document.getElementById('loginForm');
  const forgotLink    = document.getElementById('forgotLink');

  // Muestra alerta flotante temporal
  function mostrarAlerta(mensaje, tipo) {
    const existing = document.querySelector('.floating-alert');
    if (existing) existing.remove();

    const alertDiv = document.createElement('div');
    alertDiv.className = 'floating-alert';
    alertDiv.role = 'alert';

    const esExito = tipo === 'success';
    alertDiv.style.backgroundColor = esExito ? '#e2f3e4' : '#fff3e0';
    alertDiv.style.borderLeft      = esExito
      ? '4px solid #2c7da0'
      : '4px solid #e6a017';

    const icono = esExito
      ? '<i class="bi bi-check-circle-fill me-2" style="color:#2c7da0;"></i>'
      : '<i class="bi bi-info-circle-fill me-2" style="color:#e6a017;"></i>';

    alertDiv.innerHTML = `${icono} ${mensaje}`;
    document.body.appendChild(alertDiv);

    setTimeout(() => alertDiv?.remove(), 2800);
  }

  // Resalta ícono al enfocar input
  document.querySelectorAll('.input-icon-group input').forEach(input => {
    input.addEventListener('focus', () => input.parentElement.classList.add('focused'));
    input.addEventListener('blur',  () => input.parentElement.classList.remove('focused'));
  });

  // Olvidaste contraseña (demo)
  if (forgotLink) {
    forgotLink.addEventListener('click', e => {
      e.preventDefault();
      mostrarAlerta('Se enviaría un enlace de recuperación a tu correo.', 'info');
    });
  }
})();
