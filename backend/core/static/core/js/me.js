document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("me-message");
    const indicatorCount = document.getElementById("me-indicator-count");
    const recordCount = document.getElementById("me-record-count");
    const indicatorList = document.getElementById("me-indicator-list");

    function showMessage(text, type = "") {
        message.textContent = text;
        message.className =
            `dashboard-message ${type}`.trim();
    }

    async function fetchJson(url) {
        const response = await fetch(url, {
            credentials: "same-origin",
        });

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
                data.error ||
                "Unable to load M&E information."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function renderIndicators(indicators) {
        indicatorCount.textContent = indicators.length;

        let totalRecords = 0;

        indicators.forEach(function (indicator) {
            totalRecords += Number(indicator.record_count || 0);
        });

        recordCount.textContent = totalRecords;
        indicatorList.innerHTML = "";

        if (!indicators.length) {
            indicatorList.innerHTML = `
                <div class="empty-state">
                    <strong>No indicators found</strong>
                    <p>
                        No authorized M&E indicators are
                        currently available.
                    </p>
                </div>
            `;
            return;
        }

        indicators.forEach(function (indicator) {
            const card = document.createElement("article");
            card.className = "me-card";

            const heading = document.createElement("div");
            heading.className = "me-card-heading";

            const name = document.createElement("h4");
            name.textContent =
                indicator.indicator_name || "Unnamed indicator";

            const status = document.createElement("strong");
            status.textContent =
                indicator.status || "Not set";

            heading.appendChild(name);
            heading.appendChild(status);

            const target = document.createElement("p");
            target.textContent =
                `Target: ${indicator.target_value ?? "Not set"}`
                + ` ${indicator.unit || ""}`.trim();

            const latest = document.createElement("p");
            latest.textContent =
                `Latest value: ${
                    indicator.latest_recorded_value ?? "No record"
                }`;

            const records = document.createElement("small");
            records.textContent =
                `Records: ${indicator.record_count || 0}`;

            card.appendChild(heading);
            card.appendChild(target);
            card.appendChild(latest);
            card.appendChild(records);

            indicatorList.appendChild(card);
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadMonitoringAndEvaluation() {
        try {
            await loadUser();

            const data = await fetchJson(
                "/me-indicators/summary/"
            );

            renderIndicators(
                data.me_indicators_summary
            );

            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            if (error.status === 403) {
                indicatorCount.textContent = "0";
                recordCount.textContent = "0";

                indicatorList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            M&E indicators.
                        </p>
                    </div>
                `;

                showMessage("");
                return;
            }

            showMessage(
                error.message ||
                "Unable to load M&E information.",
                "error"
            );
        }
    }

    loadMonitoringAndEvaluation();
});
