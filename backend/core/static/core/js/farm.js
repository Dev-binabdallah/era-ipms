document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("farm-message");
    const farmList = document.getElementById("farm-list");
    const farmCount = document.getElementById("farm-count");

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
                data.error || "Unable to load farm crops."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function renderFarmCrops(crops) {
        farmCount.textContent = crops.length;
        farmList.innerHTML = "";

        if (!crops.length) {
            farmList.innerHTML = `
                <div class="empty-state">
                    <strong>No farm crops found</strong>
                    <p>
                        No authorized farm crops are
                        currently available.
                    </p>
                </div>
            `;
            return;
        }

        crops.forEach(function (crop) {
            const card = document.createElement("article");
            card.className = "farm-card";

            const name = document.createElement("h4");
            name.textContent =
                crop.crop_name || "Unnamed crop";

            const status = document.createElement("span");
            status.className = "project-status";
            status.textContent =
                crop.status || "Status not set";

            const description = document.createElement("p");
            description.textContent =
                crop.description ||
                "No description provided.";

            const planting = document.createElement("small");
            planting.textContent =
                `Planting date: ${
                    crop.planting_date || "Not set"
                }`;

            card.appendChild(name);
            card.appendChild(status);
            card.appendChild(description);
            card.appendChild(planting);

            farmList.appendChild(card);
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadFarm() {
        try {
            await loadUser();

            const data = await fetchJson("/farm-crops/");

            renderFarmCrops(data.farm_crops);
            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            if (error.status === 403) {
                farmCount.textContent = "0";

                farmList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            farm crops.
                        </p>
                    </div>
                `;

                showMessage("");
                return;
            }

            showMessage(
                error.message ||
                "Unable to load farm crops.",
                "error"
            );
        }
    }

    loadFarm();
});
