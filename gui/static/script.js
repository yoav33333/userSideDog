document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("output");

  // Collapse/expand groups
  document.querySelectorAll("legend").forEach(legend => {
    legend.style.cursor = "pointer";
    legend.addEventListener("click", () => {
      legend.parentElement.classList.toggle("collapsed");
    });
  });

  // Handle input changes
  document.querySelectorAll("input").forEach(input => {
    input.addEventListener("change", async () => {
      const key = input.name;
      const value = input.value;

      const data = {};
      data[key] = value;
      await syncForm();
      const response = await fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (result.success) {
        output.innerHTML = `<span style='color:green;'>✔ ${key} updated</span>`;
        await syncForm();  // 🔁 refresh UI with latest values
      } else {
        output.innerHTML = `<span style='color:red;'>✖ ${key} error:</span><ul>` +
          result.errors.map(e => `<li>${e}</li>`).join('') + "</ul>";
      }
    });
  });

  // 🔁 Sync HTML with latest data from server
  async function syncForm() {
    const response = await fetch("/data");
    const data = await response.json();

    for (const [group, vars] of Object.entries(data)) {
      for (const [name, val] of Object.entries(vars)) {
        const input = document.querySelector(`input[name='${group}::${name}']`);
        if (input && document.activeElement !== input) {
          input.value = val;
        }
      }
    }
  }

  // 🕓 Optionally: refresh every 5 seconds
  setInterval(syncForm, 5000);
});
