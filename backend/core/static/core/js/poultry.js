document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("poultry-message");
    const poultryList = document.getElementById("poultry-list");
    const poultryCount = document.getElementById("poultry-count");

    const stockList = document.getElementById("stock-list");
    const stockCount = document.getElementById("stock-count");

    const eggList = document.getElementById("egg-list");
    const eggCount = document.getElementById("egg-count");

    const feedList = document.getElementById("feed-list");
    const feedCount = document.getElementById("feed-count");

    const healthList = document.getElementById("health-list");
    const healthCount = document.getElementById("health-count");

    const salesList = document.getElementById("sales-list");
    const salesCount = document.getElementById("sales-count");

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
                "Unable to load poultry information."
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
                    this poultry information.
                </p>
            </div>
        `;
    }

    function renderPoultryGroups(groups) {
        poultryCount.textContent = groups.length;
        poultryList.innerHTML = "";

        if (!groups.length) {
            poultryList.innerHTML = `
                <div class="empty-state">
                    <strong>No poultry groups found</strong>
                    <p>
                        No authorized poultry groups are
                        currently available.
                    </p>
                </div>
            `;
            return;
        }

        groups.forEach(function (group) {
            const card = document.createElement("article");
            card.className = "poultry-card";

            const name = document.createElement("h4");
            name.textContent =
                group.group_name || "Unnamed group";

            const category = document.createElement("span");
            category.className = "project-status";
            category.textContent =
                group.poultry_category || "Category not set";

            const breed = document.createElement("p");
            breed.textContent =
                `Breed/Type: ${
                    group.breed_or_type || "Not provided"
                }`;

            const status = document.createElement("small");
            status.textContent =
                `Status: ${group.status || "Not set"}`;

            card.appendChild(name);
            card.appendChild(category);
            card.appendChild(breed);
            card.appendChild(status);

            poultryList.appendChild(card);
        });
    }

    function renderStock(movements) {
        stockCount.textContent = movements.length;
        stockList.innerHTML = "";

        if (!movements.length) {
            stockList.innerHTML = `
                <div class="empty-state">
                    <strong>No stock movements found</strong>
                    <p>No authorized stock movements are available.</p>
                </div>
            `;
            return;
        }

        movements.forEach(function (movement) {
            const card = document.createElement("article");
            card.className = "poultry-record-card";

            const title = document.createElement("h4");
            title.textContent =
                movement.movement_type || "Stock movement";

            const details = document.createElement("p");
            details.textContent =
                `Group ID: ${movement.poultry_group_id}`
                + ` | Date: ${
                    movement.movement_date || "Not set"
                }`;

            const quantity = document.createElement("small");
            quantity.textContent =
                `Quantity: ${movement.quantity ?? "Not set"}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(quantity);

            stockList.appendChild(card);
        });
    }

    function renderEggs(records) {
        eggCount.textContent = records.length;
        eggList.innerHTML = "";

        if (!records.length) {
            eggList.innerHTML = `
                <div class="empty-state">
                    <strong>No egg production records found</strong>
                    <p>No authorized egg production records are available.</p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "poultry-record-card";

            const title = document.createElement("h4");
            title.textContent = "Egg production";

            const details = document.createElement("p");
            details.textContent =
                `Group ID: ${record.poultry_group_id}`
                + ` | Date: ${
                    record.production_date || "Not set"
                }`;

            const totals = document.createElement("small");
            totals.textContent =
                `Produced: ${record.eggs_produced}`
                + ` | Used: ${record.eggs_used}`
                + ` | Sold: ${record.eggs_sold}`
                + ` | Remaining: ${record.eggs_remaining}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(totals);

            eggList.appendChild(card);
        });
    }

    function renderFeed(records) {
        feedCount.textContent = records.length;
        feedList.innerHTML = "";

        if (!records.length) {
            feedList.innerHTML = `
                <div class="empty-state">
                    <strong>No feed records found</strong>
                    <p>No authorized feed records are available.</p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "poultry-record-card";

            const title = document.createElement("h4");
            title.textContent =
                record.feed_source || "Feed record";

            const details = document.createElement("p");
            details.textContent =
                `Group ID: ${record.poultry_group_id}`
                + ` | Date: ${record.record_date || "Not set"}`;

            const quantity = document.createElement("small");
            quantity.textContent =
                `Quantity: ${record.quantity ?? "Not set"}`
                + ` ${record.unit || ""}`
                + ` | Cost: ${record.cost ?? "Not set"}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(quantity);

            feedList.appendChild(card);
        });
    }

    function renderHealth(records) {
        healthCount.textContent = records.length;
        healthList.innerHTML = "";

        if (!records.length) {
            healthList.innerHTML = `
                <div class="empty-state">
                    <strong>No health records found</strong>
                    <p>No authorized health records are available.</p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "poultry-record-card";

            const title = document.createElement("h4");
            title.textContent =
                record.condition_type || "Health record";

            const details = document.createElement("p");
            details.textContent =
                `Group ID: ${record.poultry_group_id}`
                + ` | Date: ${record.record_date || "Not set"}`;

            const affected = document.createElement("small");
            affected.textContent =
                `Number affected: ${
                    record.number_affected ?? "Not set"
                }`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(affected);

            healthList.appendChild(card);
        });
    }

    function renderSales(records) {
        salesCount.textContent = records.length;
        salesList.innerHTML = "";

        if (!records.length) {
            salesList.innerHTML = `
                <div class="empty-state">
                    <strong>No poultry sales found</strong>
                    <p>No authorized poultry sales are available.</p>
                </div>
            `;
            return;
        }

        records.forEach(function (record) {
            const card = document.createElement("article");
            card.className = "poultry-record-card";

            const title = document.createElement("h4");
            title.textContent = "Poultry sale";

            const details = document.createElement("p");
            details.textContent =
                `Group ID: ${record.poultry_group_id}`
                + ` | Date: ${record.sale_date || "Not set"}`;

            const amount = document.createElement("small");
            amount.textContent =
                `Quantity: ${record.quantity}`
                + ` | Total: ${record.total_amount ?? "Not set"}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(amount);

            salesList.appendChild(card);
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

    async function loadPoultry() {
        try {
            await loadUser();

            await Promise.all([
                loadResource(
                    "/poultry-groups/",
                    renderPoultryGroups,
                    poultryList,
                    poultryCount
                ),
                loadResource(
                    "/poultry-stock-movements/",
                    function (data) {
                        renderStock(
                            data.poultry_stock_movements
                        );
                    },
                    stockList,
                    stockCount
                ),
                loadResource(
                    "/egg-production/",
                    function (data) {
                        renderEggs(data.egg_production);
                    },
                    eggList,
                    eggCount
                ),
                loadResource(
                    "/feed-records/",
                    function (data) {
                        renderFeed(data.feed_records);
                    },
                    feedList,
                    feedCount
                ),
                loadResource(
                    "/poultry-health-records/",
                    function (data) {
                        renderHealth(
                            data.poultry_health_records
                        );
                    },
                    healthList,
                    healthCount
                ),
                loadResource(
                    "/poultry-sales/",
                    function (data) {
                        renderSales(data.poultry_sales);
                    },
                    salesList,
                    salesCount
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
                "Unable to load poultry information.",
                "error"
            );
        }
    }

    loadPoultry();
});
