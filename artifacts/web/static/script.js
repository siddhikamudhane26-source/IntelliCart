document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-menu]");
  menuToggle?.addEventListener("click", () => {
    menu?.classList.toggle("is-open");
  });

  document.querySelectorAll("[data-dismiss-flash]").forEach((button) => {
    button.addEventListener("click", () => button.closest(".flash")?.remove());
  });
  window.setTimeout(() => {
    document.querySelectorAll(".flash").forEach((flash) => {
      flash.style.opacity = "0";
      flash.style.transform = "translateX(20px)";
      window.setTimeout(() => flash.remove(), 250);
    });
  }, 5500);

  document.querySelectorAll("[data-quantity-minus]").forEach((button) => {
    button.addEventListener("click", () => {
      const input = button.parentElement?.querySelector("[data-quantity-input]");
      if (input) input.value = Math.max(Number(input.min || 1), Number(input.value || 1) - 1);
    });
  });
  document.querySelectorAll("[data-quantity-plus]").forEach((button) => {
    button.addEventListener("click", () => {
      const input = button.parentElement?.querySelector("[data-quantity-input]");
      if (input) input.value = Math.min(Number(input.max || 999), Number(input.value || 1) + 1);
    });
  });

  const statElements = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window && statElements.length) {
    const observer = new IntersectionObserver((entries, instance) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const element = entry.target;
        const raw = element.dataset.count || "0";
        const numeric = Number(raw);
        if (!Number.isNaN(numeric) && numeric > 0) {
          const suffix = raw.includes("%") ? "%" : raw.includes("K") ? "K+" : "";
          const target = suffix ? numeric : numeric;
          let current = 0;
          const step = Math.max(1, Math.ceil(target / 32));
          const timer = window.setInterval(() => {
            current = Math.min(target, current + step);
            element.textContent = `${current.toLocaleString()}${suffix}`;
            if (current >= target) window.clearInterval(timer);
          }, 28);
        }
        instance.unobserve(element);
      });
    }, { threshold: 0.4 });
    statElements.forEach((element) => observer.observe(element));
  }
});