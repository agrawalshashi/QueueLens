const form = document.getElementById("prediction-form");
const predictButton = document.getElementById("predict-button");
const formError = document.getElementById("form-error");
const resultSection = document.getElementById("result-section");

async function readJson(response) {
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || `Request failed (${response.status})`);
    }
    return data;
}

function fillSelect(id, values) {
    const select = document.getElementById(id);
    select.replaceChildren();

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = `Select ${id.replace("_", " ")}`;
    placeholder.disabled = true;
    placeholder.selected = true;
    select.appendChild(placeholder);

    values.forEach((value) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}

async function checkHealth() {
    const pill = document.getElementById("connection-pill");
    try {
        const response = await fetch("/api/health");
        const data = await readJson(response);
        pill.textContent = data.model_loaded ? "API online" : "Model missing";
        pill.classList.toggle("online", Boolean(data.model_loaded));
        pill.classList.remove("offline");
    } catch (error) {
        pill.textContent = "API offline";
        pill.classList.add("offline");
        pill.classList.remove("online");
    }
}

async function loadOptions() {
    try {
        const response = await fetch("/api/options");
        const data = await readJson(response);

        ["agency", "complaint_type", "borough"].forEach((key) => {
            const values = data.options[key] || [];
            fillSelect(key, values);
            if (values.length === 0) {
                throw new Error(`No dropdown values found for ${key}.`);
            }
        });
    } catch (error) {
        formError.textContent =
            `Could not load dropdown options: ${error.message}. Check the Flask terminal.`;
        predictButton.disabled = true;
    }
}

function showResult(data) {
    resultSection.classList.remove("hidden");

    const isHigh = data.risk_level === "High";
    document.getElementById("result-title").textContent =
        isHigh ? "Elevated delay risk" : "Lower estimated delay risk";

    const badge = document.getElementById("risk-badge");
    badge.textContent = `${data.risk_level} risk`;
    badge.className = `risk-badge ${isHigh ? "high" : "lower"}`;

    document.getElementById("probability-value").textContent =
        `${data.probability_percent}%`;

    const meter = document.getElementById("meter-fill");
    meter.style.width = `${Math.max(0, Math.min(100, data.probability_percent))}%`;
    meter.classList.toggle("high", isHigh);

    document.getElementById("result-message").textContent = data.message;
    document.getElementById("result-disclaimer").textContent =
        `${data.disclaimer} Decision threshold: ${(data.threshold * 100).toFixed(0)}%.`;

    resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    formError.textContent = "";
    predictButton.disabled = true;
    predictButton.textContent = "Estimating...";

    const hourInput = document.getElementById("created_hour") || document.getElementById("created_hours");
    const payload = {
        agency: document.getElementById("agency").value,
        complaint_type: document.getElementById("complaint_type").value,
        borough: document.getElementById("borough").value,
        created_hour: Number(hourInput ? hourInput.value : 12),
        created_day: Number(document.getElementById("created_day").value),
        created_month: Number(document.getElementById("created_month").value),
    };

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await readJson(response);
        showResult(data);
    } catch (error) {
        formError.textContent = error.message;
    } finally {
        predictButton.disabled = false;
        predictButton.innerHTML = 'Estimate delay risk <span aria-hidden="true">→</span>';
    }
});

checkHealth();
loadOptions();
