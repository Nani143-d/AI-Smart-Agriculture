document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector('button[type="submit"], button:not([type])');
      if (button && form.checkValidity()) {
        button.dataset.originalText = button.textContent;
        button.textContent = "Processing…";
        button.disabled = true;
      }
    });
  });
});
