// Auto-dismiss flash alerts after a few seconds.
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const closeBtn = alert.querySelector(".btn-close");
      if (closeBtn) closeBtn.click();
    }, 5000);
  });
});
