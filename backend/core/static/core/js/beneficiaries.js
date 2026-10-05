document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById(
        "beneficiaries-message"
    );
    const beneficiaryList = document.getElementById(
        "beneficiaries-list"
    );
    const beneficiaryCount = document.getElementById(
        "beneficiary-count"
    );

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
                "Unable to load beneficiary records."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function renderBeneficiaries(beneficiaries) {
        beneficiaryCount.textContent = beneficiaries.length;
        beneficiaryList.innerHTML = "";

        if (!beneficiaries.length) {
            beneficiaryList.innerHTML = `
                <div class="empty-state">
                    <strong>No beneficiary records found</strong>
                    <p>
                        No authorized beneficiary records are
                        currently available.
                    </p>
                </div>
            `;
            return;
        }

        beneficiaries.forEach(function (beneficiary) {
            const card = document.createElement("article");
            card.className = "beneficiary-card";

            const name = document.createElement("h4");
            name.textContent =
                `${beneficiary.first_name} ${beneficiary.last_name}`;

            const code = document.createElement("span");
            code.className = "project-status";
            code.textContent =
                beneficiary.beneficiary_code || "No code";

            const details = document.createElement("p");
            details.textContent =
                beneficiary.location ||
                "Location not provided.";

            const status = document.createElement("small");
            status.textContent =
                `Status: ${beneficiary.status || "Not set"}`;

            card.appendChild(name);
            card.appendChild(code);
            card.appendChild(details);
            card.appendChild(status);

            beneficiaryList.appendChild(card);
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadBeneficiaries() {
        try {
            await loadUser();

            const data = await fetchJson(
                "/beneficiaries/"
            );

            renderBeneficiaries(data.beneficiaries);
            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            if (error.status === 403) {
                beneficiaryCount.textContent = "0";

                beneficiaryList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            beneficiaries.
                        </p>
                    </div>
                `;

                showMessage("");
                return;
            }

            showMessage(
                error.message ||
                "Unable to load beneficiary records.",
                "error"
            );
        }
    }

    loadBeneficiaries();
});
