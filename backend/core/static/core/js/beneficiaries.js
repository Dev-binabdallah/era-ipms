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

    const assessmentsList = document.getElementById(
        "assessments-list"
    );

    const assessmentCount = document.getElementById(
        "assessment-count"
    );

    const homeVisitsList = document.getElementById(
        "home-visits-list"
    );

    const homeVisitCount = document.getElementById(
        "home-visit-count"
    );

    const referralsList = document.getElementById(
        "referrals-list"
    );

    const referralCount = document.getElementById(
        "referral-count"
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
                "Unable to load beneficiary services."
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

    function renderAssessments(assessments) {
        assessmentCount.textContent = assessments.length;
        assessmentsList.innerHTML = "";

        if (!assessments.length) {
            assessmentsList.innerHTML = `
                <div class="empty-state">
                    <strong>No assessments found</strong>
                    <p>
                        No authorized disability assessments
                        are currently available.
                    </p>
                </div>
            `;
            return;
        }

        assessments.forEach(function (assessment) {
            const card = document.createElement("article");
            card.className = "service-card";

            const title = document.createElement("h4");
            title.textContent =
                assessment.assessment_type ||
                "Disability assessment";

            const details = document.createElement("p");
            details.textContent =
                `Beneficiary ID: ${assessment.beneficiary_id}`
                + ` | Date: ${
                    assessment.assessment_date || "Not set"
                }`;

            const disabilityType = document.createElement("p");
            disabilityType.textContent =
                `Disability type: ${
                    assessment.disability_type || "Not set"
                }`;

            const needs = document.createElement("small");
            needs.textContent =
                `Needs: ${assessment.needs || "Not recorded"}`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(disabilityType);
            card.appendChild(needs);

            assessmentsList.appendChild(card);
        });
    }

    function renderHomeVisits(visits) {
        homeVisitCount.textContent = visits.length;
        homeVisitsList.innerHTML = "";

        if (!visits.length) {
            homeVisitsList.innerHTML = `
                <div class="empty-state">
                    <strong>No home visits found</strong>
                    <p>
                        No authorized home visits are currently
                        available.
                    </p>
                </div>
            `;
            return;
        }

        visits.forEach(function (visit) {
            const card = document.createElement("article");
            card.className = "service-card";

            const title = document.createElement("h4");
            title.textContent =
                visit.purpose || "Home visit";

            const details = document.createElement("p");
            details.textContent =
                `Beneficiary ID: ${visit.beneficiary_id}`
                + ` | Date: ${visit.visit_date || "Not set"}`;

            const support = document.createElement("p");
            support.textContent =
                `Support: ${
                    visit.support_provided ||
                    "Not recorded"
                }`;

            const followUp = document.createElement("small");
            followUp.textContent =
                `Follow-up required: ${
                    visit.follow_up_required ? "Yes" : "No"
                }`;

            card.appendChild(title);
            card.appendChild(details);
            card.appendChild(support);
            card.appendChild(followUp);

            homeVisitsList.appendChild(card);
        });
    }

    function renderReferrals(referrals) {
        referralCount.textContent = referrals.length;
        referralsList.innerHTML = "";

        if (!referrals.length) {
            referralsList.innerHTML = `
                <div class="empty-state">
                    <strong>No referrals found</strong>
                    <p>
                        No authorized referrals are currently
                        available.
                    </p>
                </div>
            `;
            return;
        }

        referrals.forEach(function (referral) {
            const card = document.createElement("article");
            card.className = "service-card";

            const title = document.createElement("h4");
            title.textContent =
                referral.destination || "Referral";

            const status = document.createElement("span");
            status.className = "project-status";
            status.textContent =
                referral.status || "Not set";

            const details = document.createElement("p");
            details.textContent =
                `Beneficiary ID: ${referral.beneficiary_id}`
                + ` | Date: ${
                    referral.referral_date || "Not set"
                }`;

            const reason = document.createElement("small");
            reason.textContent =
                `Reason: ${
                    referral.reason || "Not recorded"
                }`;

            card.appendChild(title);
            card.appendChild(status);
            card.appendChild(details);
            card.appendChild(reason);

            referralsList.appendChild(card);
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
            const data = await fetchJson(
                "/beneficiaries/"
            );

            renderBeneficiaries(data.beneficiaries);
        } catch (error) {
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
                return;
            }

            throw error;
        }
    }

    async function loadAssessments() {
        try {
            const data = await fetchJson(
                "/disability-assessments/"
            );

            renderAssessments(data.assessments);
        } catch (error) {
            if (error.status === 403) {
                assessmentCount.textContent = "0";

                assessmentsList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            disability assessments.
                        </p>
                    </div>
                `;
                return;
            }

            throw error;
        }
    }

    async function loadHomeVisits() {
        try {
            const data = await fetchJson(
                "/home-visits/"
            );

            renderHomeVisits(data.home_visits);
        } catch (error) {
            if (error.status === 403) {
                homeVisitCount.textContent = "0";

                homeVisitsList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            home visits.
                        </p>
                    </div>
                `;
                return;
            }

            throw error;
        }
    }

    async function loadReferrals() {
        try {
            const data = await fetchJson(
                "/referrals/"
            );

            renderReferrals(data.referrals);
        } catch (error) {
            if (error.status === 403) {
                referralCount.textContent = "0";

                referralsList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            referrals.
                        </p>
                    </div>
                `;
                return;
            }

            throw error;
        }
    }

    async function loadBeneficiaryServices() {
        try {
            await loadUser();

            await Promise.all([
                loadBeneficiaries(),
                loadAssessments(),
                loadHomeVisits(),
                loadReferrals(),
            ]);

            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            showMessage(
                error.message ||
                "Unable to load beneficiary services.",
                "error"
            );
        }
    }

    loadBeneficiaryServices();
});
