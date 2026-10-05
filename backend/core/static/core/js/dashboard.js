document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("dashboard-message");
    const logoutButton = document.getElementById("logout-button");

    function showMessage(text, type = "") {
        message.textContent = text;
        message.className = `dashboard-message ${type}`.trim();
    }

    function getCsrfToken() {
        const tokenInput = document.querySelector(
            'input[name="csrfmiddlewaretoken"]'
        );

        if (tokenInput && tokenInput.value) {
            return tokenInput.value;
        }

        const cookie = document.cookie
            .split("; ")
            .find((row) => row.startsWith("csrftoken="));

        return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
    }

    async function fetchJson(url, options = {}) {
        const requestOptions = {
            credentials: "same-origin",
            ...options,
        };

        if ((requestOptions.method || "GET").toUpperCase() !== "GET") {
            requestOptions.headers = {
                ...(requestOptions.headers || {}),
                "X-CSRFToken": getCsrfToken(),
            };
        }

        const response = await fetch(url, requestOptions);

        const contentType =
            response.headers.get("content-type") || "";

        if (!contentType.includes("application/json")) {
            const error = new Error(
                `Server returned HTTP ${response.status}.`
            );
            error.status = response.status;
            throw error;
        }

        const data = await response.json();

        if (!response.ok) {
            const error = new Error(
                data.error || "Unable to load dashboard data."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function setCount(id, value) {
        const element = document.getElementById(id);
        element.textContent = value ?? 0;
    }

    function renderActivityStatus(data) {
        const summary = data.activity_status_summary;

        document.getElementById("activity-total").textContent =
            `${summary.total} total`;

        document.getElementById("status-planned").textContent =
            summary.planned;

        document.getElementById("status-ongoing").textContent =
            summary.ongoing;

        document.getElementById("status-pending").textContent =
            summary.pending;

        document.getElementById("status-completed").textContent =
            summary.completed;

        document.getElementById("status-cancelled").textContent =
            summary.cancelled;
    }

    function renderFinancialSummary(data) {
        const summary = data.financial_summary;

        document.getElementById("financial-total").textContent =
            summary.total_amount;

        document.getElementById("financial-count").textContent =
            summary.total_transactions;

        const container = document.getElementById("financial-types");
        container.innerHTML = "";

        const entries = Object.entries(summary.by_transaction_type);

        if (!entries.length) {
            container.innerHTML = "<p>No transaction data available.</p>";
            return;
        }

        entries.forEach(([type, details]) => {
            const row = document.createElement("div");
            row.className = "financial-type-row";

            const label = document.createElement("span");
            label.textContent = type;

            const value = document.createElement("strong");
            value.textContent =
                `${details.count} record(s) | ${details.total_amount}`;

            row.appendChild(label);
            row.appendChild(value);
            container.appendChild(row);
        });
    }

    async function loadDashboard() {
        showMessage("Loading dashboard...");

        try {
            const user = await fetchJson("/auth/me/");

            document.getElementById("user-name").textContent =
                user.username;

            document.getElementById("user-title").textContent =
                user.title;

            const [summary, activityStatus, financialSummary] =
                await Promise.all([
                    fetchJson("/dashboard/summary/"),
                    fetchJson("/dashboard/activity-status-summary/"),
                    fetchJson("/dashboard/financial-summary/"),
                ]);

            const counts = summary.summary;

            setCount("count-projects", counts.projects);
            setCount("count-activities", counts.activities);
            setCount("count-beneficiaries", counts.beneficiaries);
            setCount("count-referrals", counts.referrals);
            setCount("count-poultry-groups", counts.poultry_groups);
            setCount("count-farm-crops", counts.farm_crops);
            setCount(
                "count-financial-transactions",
                counts.financial_transactions
            );
            setCount("count-me-indicators", counts.me_indicators);

            renderActivityStatus(activityStatus);
            renderFinancialSummary(financialSummary);

            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            showMessage(
                error.message || "Unable to load dashboard.",
                "error"
            );
        }
    }

    logoutButton.addEventListener("click", async function () {
        logoutButton.disabled = true;
        logoutButton.textContent = "Signing out...";

        try {
            await fetchJson("/auth/logout/", {
                method: "POST",
            });

            window.location.href = "/login/";
        } catch (error) {
            logoutButton.disabled = false;
            logoutButton.textContent = "Sign out";
            showMessage(
                error.message || "Unable to sign out.",
                "error"
            );
        }
    });

    loadDashboard();
});
