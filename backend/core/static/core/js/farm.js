document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("farm-message");

    const farmList = document.getElementById("farm-list");
    const farmCount = document.getElementById("farm-count");

    const activityList = document.getElementById("activity-list");
    const activityCount =
        document.getElementById("activity-count");

    const harvestList = document.getElementById("harvest-list");
    const harvestCount =
        document.getElementById("harvest-count");

    const transferList =
        document.getElementById("transfer-list");
    const transferCount =
        document.getElementById("transfer-count");

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
                "Unable to load farm information."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function renderRestricted(list, count) {
        count.textContent = "0";

        list.innerHTML = `
            <div class="empty-state">
                <strong>Access restricted</strong>
                <p>
                    You do not have permission to view
                    this farm information.
                </p>
            </div>
        `;
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

    function renderActivities(records) {
        activityCount.textContent = records.length;
        activityList.innerHTML = "";

        if (!records.length) {
            activityList.innerHTML = `
                <div class="empty-state">
                    <strong>No farm activities found</strong>
                    <p>
                        No authorized farm activities
                        are available.
                    </p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "farm-record-card";

            const title = document.createElement("h4");
            title.textContent =
                record.activity_type || "Farm activity";

            const details = document.createElement("p");
            details.textContent =
                `Crop ID: ${record.crop_id}`
                + ` | Date: ${
                    record.activity_date || "Not set"
                }`;

            const description =
                document.createElement("small");
            description.textContent =
                record.description ||
                "No description provided.";

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(description);

            activityList.appendChild(card);
        });
    }

    function renderHarvests(records) {
        harvestCount.textContent = records.length;
        harvestList.innerHTML = "";

        if (!records.length) {
            harvestList.innerHTML = `
                <div class="empty-state">
                    <strong>No harvests found</strong>
                    <p>
                        No authorized harvest records
                        are available.
                    </p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "farm-record-card";

            const title = document.createElement("h4");
            title.textContent = "Harvest";

            const details = document.createElement("p");
            details.textContent =
                `Crop ID: ${record.crop_id}`
                + ` | Date: ${
                    record.harvest_date || "Not set"
                }`;

            const quantity = document.createElement("small");
            quantity.textContent =
                `Quantity: ${record.quantity ?? "Not set"}`
                + ` ${record.unit || ""}`
                + ` | Use: ${record.usage_type || "Not set"}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(quantity);

            if (record.notes) {
                const notes = document.createElement("small");
                notes.textContent = `Notes: ${record.notes}`;
                card.appendChild(notes);
            }

            harvestList.appendChild(card);
        });
    }

    function renderTransfers(records) {
        transferCount.textContent = records.length;
        transferList.innerHTML = "";

        if (!records.length) {
            transferList.innerHTML = `
                <div class="empty-state">
                    <strong>No poultry transfers found</strong>
                    <p>
                        No authorized poultry transfer
                        records are available.
                    </p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "farm-record-card";

            const title = document.createElement("h4");
            title.textContent = "Poultry transfer";

            const details = document.createElement("p");
            details.textContent =
                `Harvest ID: ${record.harvest_id}`
                + ` | Group ID: ${record.poultry_group_id}`
                + ` | Date: ${
                    record.transfer_date || "Not set"
                }`;

            const quantity = document.createElement("small");
            quantity.textContent =
                `Quantity: ${record.quantity ?? "Not set"}`
                + ` ${record.unit || ""}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(quantity);

            if (record.notes) {
                const notes = document.createElement("small");
                notes.textContent = `Notes: ${record.notes}`;
                card.appendChild(notes);
            }

            transferList.appendChild(card);
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadResource(
        url,
        render,
        list,
        count
    ) {
        try {
            const data = await fetchJson(url);
            render(data);
        } catch (error) {
            if (error.status === 403) {
                renderRestricted(list, count);
                return;
            }

            throw error;
        }
    }

    async function loadFarm() {
        try {
            await loadUser();

            await Promise.all([
                loadResource(
                    "/farm-crops/",
                    function (data) {
                        renderFarmCrops(data.farm_crops);
                    },
                    farmList,
                    farmCount
                ),
                loadResource(
                    "/farm-activities/",
                    function (data) {
                        renderActivities(
                            data.farm_activities
                        );
                    },
                    activityList,
                    activityCount
                ),
                loadResource(
                    "/harvests/",
                    function (data) {
                        renderHarvests(data.harvests);
                    },
                    harvestList,
                    harvestCount
                ),
                loadResource(
                    "/farm-poultry-transfers/",
                    function (data) {
                        renderTransfers(
                            data.farm_poultry_transfers
                        );
                    },
                    transferList,
                    transferCount
                ),
            ]);

            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            showMessage(
                error.message ||
                "Unable to load farm information.",
                "error"
            );
        }
    }

    loadFarm();
});
