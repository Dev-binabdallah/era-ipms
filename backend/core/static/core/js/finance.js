document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("finance-message");
    const financeList = document.getElementById("finance-list");
    const financeCount = document.getElementById("finance-count");
    const financeTotal = document.getElementById("finance-total");

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
                "Unable to load financial transactions."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function renderTransactions(transactions) {
        financeCount.textContent = transactions.length;

        let total = 0;

        transactions.forEach(function (transaction) {
            total += Number(transaction.amount || 0);
        });

        financeTotal.textContent = total.toFixed(2);
        financeList.innerHTML = "";

        if (!transactions.length) {
            financeList.innerHTML = `
                <div class="empty-state">
                    <strong>No financial transactions found</strong>
                    <p>
                        No authorized financial transactions
                        are currently available.
                    </p>
                </div>
            `;
            return;
        }

        transactions.forEach(function (transaction) {
            const card = document.createElement("article");
            card.className = "finance-card";

            const heading = document.createElement("div");
            heading.className = "finance-card-heading";

            const category = document.createElement("h4");
            category.textContent =
                transaction.category || "Uncategorised";

            const amount = document.createElement("strong");
            amount.textContent =
                Number(transaction.amount || 0).toFixed(2);

            heading.appendChild(category);
            heading.appendChild(amount);

            const details = document.createElement("p");
            details.textContent =
                `${transaction.transaction_type || "Type not set"}`
                + " | "
                + `${transaction.transaction_date || "Date not set"}`;

            const status = document.createElement("small");
            status.textContent =
                `Status: ${transaction.status || "Not set"}`;

            card.appendChild(heading);
            card.appendChild(details);
            card.appendChild(status);

            financeList.appendChild(card);
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadFinance() {
        try {
            await loadUser();

            const data = await fetchJson(
                "/financial-transactions/"
            );

            renderTransactions(
                data.financial_transactions
            );

            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            if (error.status === 403) {
                financeCount.textContent = "0";
                financeTotal.textContent = "0.00";

                financeList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            financial transactions.
                        </p>
                    </div>
                `;

                showMessage("");
                return;
            }

            showMessage(
                error.message ||
                "Unable to load financial transactions.",
                "error"
            );
        }
    }

    loadFinance();
});
