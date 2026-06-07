(function () {
  const password        = document.getElementById('password');
  const confirmPassword = document.getElementById('confirm_password');

  if (!password || !confirmPassword) return;

  // Valida en tiempo real que las contraseñas coincidan
  function validarContrasenas() {
    if (confirmPassword.value === '') return;

    if (password.value !== confirmPassword.value) {
      confirmPassword.setCustomValidity('Las contraseñas no coinciden');
      confirmPassword.classList.add('is-invalid');
      confirmPassword.classList.remove('is-valid');
    } else {
      confirmPassword.setCustomValidity('');
      confirmPassword.classList.remove('is-invalid');
      confirmPassword.classList.add('is-valid');
    }
  }

  password.addEventListener('input', validarContrasenas);
  confirmPassword.addEventListener('input', validarContrasenas);

  // Resalta ícono al enfocar
  document.querySelectorAll('.input-icon-group input, .input-icon-group select').forEach(el => {
    el.addEventListener('focus', () => el.parentElement.classList.add('focused'));
    el.addEventListener('blur',  () => el.parentElement.classList.remove('focused'));
  });
})();
