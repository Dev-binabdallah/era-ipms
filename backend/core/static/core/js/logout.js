document.addEventListener("DOMContentLoaded", function () {
    const logoutButton = document.getElementById("logout-button");

    if (!logoutButton) {
        return;
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

    logoutButton.addEventListener("click", async function () {
        logoutButton.disabled = true;
        logoutButton.textContent = "Signing out...";

        try {
            const response = await fetch("/auth/logout/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                },
            });

            const contentType =
                response.headers.get("content-type") || "";

            if (!contentType.includes("application/json")) {
                throw new Error(
                    `Server returned HTTP ${response.status}.`
                );
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to sign out."
                );
            }

            window.location.href = "/login/";
        } catch (error) {
            logoutButton.disabled = false;
            logoutButton.textContent = "Sign out";

            const message = document.getElementById("dashboard-message");

            if (message) {
                message.textContent =
                    error.message || "Unable to sign out.";
                message.className = "dashboard-message error";
            }
        }
    });
});
