document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const message = document.getElementById("login-message");
    const submitButton = document.getElementById("login-button");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        message.textContent = "";
        message.className = "login-message";

        const formData = new FormData(form);

        submitButton.disabled = true;
        submitButton.textContent = "Signing in...";

        try {
            const response = await fetch("/auth/login/", {
                method: "POST",
                body: new URLSearchParams(formData),
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
            });

            const data = await response.json();

            if (!response.ok) {
                message.textContent = data.error || "Unable to sign in.";
                message.className = "login-message error";

                submitButton.disabled = false;
                submitButton.textContent = "Sign in";
                return;
            }

            window.location.href = "/dashboard/";
        } catch (error) {
            message.textContent = "Unable to connect to the server.";
            message.className = "login-message error";

            submitButton.disabled = false;
            submitButton.textContent = "Sign in";
        }
    });
});
