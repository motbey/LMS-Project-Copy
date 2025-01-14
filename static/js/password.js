document.addEventListener("DOMContentLoaded", function () {
  const passwordInput = document.getElementById("password");
  const confirmInput = document.getElementById("confirm_password");
  const strengthIndicator = document.querySelector(".password-strength");
  const form = document.querySelector("form");

  // Password strength checker
  passwordInput.addEventListener("input", function () {
    const password = this.value;
    const strength = checkPasswordStrength(password);
    updateStrengthIndicator(strength);
  });

  // Password match checker
  confirmInput.addEventListener("input", function () {
    if (this.value !== passwordInput.value) {
      this.setCustomValidity("Passwords do not match");
    } else {
      this.setCustomValidity("");
    }
  });

  // Form submission validation
  form.addEventListener("submit", function (e) {
    const password = passwordInput.value;
    const strength = checkPasswordStrength(password);

    if (strength < 3) {
      e.preventDefault();
      alert("Password does not meet minimum requirements");
    }
  });

  function checkPasswordStrength(password) {
    let strength = 0;

    // Length check
    if (password.length >= 8) strength++;

    // Uppercase check
    if (/[A-Z]/.test(password)) strength++;

    // Lowercase check
    if (/[a-z]/.test(password)) strength++;

    // Number check
    if (/[0-9]/.test(password)) strength++;

    // Special character check
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    return strength;
  }

  function updateStrengthIndicator(strength) {
    strengthIndicator.className = "password-strength";

    if (strength >= 4) {
      strengthIndicator.classList.add("strength-strong");
    } else if (strength >= 2) {
      strengthIndicator.classList.add("strength-medium");
    } else if (strength >= 1) {
      strengthIndicator.classList.add("strength-weak");
    }
  }
});
