document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("poultry-message");
    const poultryList = document.getElementById("poultry-list");
    const poultryCount = document.getElementById("poultry-count");

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
                data.error || "Unable to load poultry groups."
            );
            error.status = response.status;
            throw error;
        }

        return data;
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

            const type = document.createElement("span");
            type.className = "project-status";
            type.textContent =
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
            card.appendChild(type);
            card.appendChild(breed);
            card.appendChild(status);

            poultryList.appendChild(card);
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadPoultry() {
        try {
            await loadUser();

            const data = await fetchJson(
                "/poultry-groups/"
            );

            renderPoultryGroups(data.poultry_groups);
            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            if (error.status === 403) {
                poultryCount.textContent = "0";

                poultryList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            poultry groups.
                        </p>
                    </div>
                `;

                showMessage("");
                return;
            }

            showMessage(
                error.message ||
                "Unable to load poultry groups.",
                "error"
            );
        }
    }

    loadPoultry();
});
