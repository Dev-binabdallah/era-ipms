document.addEventListener("DOMContentLoaded", function () {
    const message = document.getElementById("projects-message");

    const projectList =
        document.getElementById("projects-list");

    const projectCount =
        document.getElementById("project-count");

    const activitiesList =
        document.getElementById("activities-list");

    const activityCount =
        document.getElementById("activity-count");

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
                "Unable to load project information."
            );
            error.status = response.status;
            throw error;
        }

        return data;
    }

    function renderAssignmentList(container, assignments, type) {
        container.innerHTML = "";

        if (!assignments.length) {
            container.innerHTML = `
                <div class="assignment-empty">
                    <strong>No assignments found</strong>
                    <p>
                        No users are currently assigned.
                    </p>
                </div>
            `;
            return;
        }

        assignments.forEach(function (assignment) {
            const item = document.createElement("div");
            item.className = "assignment-item";

            const user = document.createElement("strong");
            user.textContent =
                `User ${assignment.user_id}`;

            const status = document.createElement("span");

            if (type === "project") {
                status.textContent =
                    assignment.is_active ? "Active" : "Inactive";
            } else {
                status.textContent =
                    assignment.status || "Not set";
            }

            item.appendChild(user);
            item.appendChild(status);

            if (assignment.assigned_at) {
                const assignedAt = document.createElement("small");
                assignedAt.textContent =
                    `Assigned: ${assignment.assigned_at}`;
                item.appendChild(assignedAt);
            }

            container.appendChild(item);
        });
    }

    function renderAssignmentSection(card, assignments, type) {
        const section = document.createElement("section");
        section.className = "assignment-section";

        const heading = document.createElement("h5");
        heading.textContent = "Assignments";

        const list = document.createElement("div");
        list.className = "assignment-list";

        section.appendChild(heading);
        section.appendChild(list);

        renderAssignmentList(list, assignments, type);

        card.appendChild(section);
    }

    function renderAssignmentError(card, messageText) {
        const section = document.createElement("section");
        section.className = "assignment-section";

        const heading = document.createElement("h5");
        heading.textContent = "Assignments";

        const message = document.createElement("div");
        message.className = "assignment-empty";

        const strong = document.createElement("strong");
        strong.textContent = "Assignments unavailable";

        const paragraph = document.createElement("p");
        paragraph.textContent = messageText;

        message.appendChild(strong);
        message.appendChild(paragraph);

        section.appendChild(heading);
        section.appendChild(message);

        card.appendChild(section);
    }

    async function loadProjectAssignments(card, projectId) {
        try {
            const data = await fetchJson(
                `/projects/${projectId}/assignments/`
            );

            renderAssignmentSection(
                card,
                data.assignments || [],
                "project"
            );
        } catch (error) {
            if (error.status === 403) {
                renderAssignmentError(
                    card,
                    "You do not have permission to view project assignments."
                );
                return;
            }

            renderAssignmentError(
                card,
                "Unable to load project assignments."
            );
        }
    }

    async function loadActivityAssignments(card, activityId) {
        try {
            const data = await fetchJson(
                `/activities/${activityId}/assignments/`
            );

            renderAssignmentSection(
                card,
                data.assignments || [],
                "activity"
            );
        } catch (error) {
            if (error.status === 403) {
                renderAssignmentError(
                    card,
                    "You do not have permission to view activity assignments."
                );
                return;
            }

            renderAssignmentError(
                card,
                "Unable to load activity assignments."
            );
        }
    }

    function renderProjects(projects) {
        projectCount.textContent = projects.length;
        projectList.innerHTML = "";

        if (!projects.length) {
            projectList.innerHTML = `
                <div class="empty-state">
                    <strong>No projects found</strong>
                    <p>
                        No authorized projects are currently
                        available.
                    </p>
                </div>
            `;
            return;
        }

        projects.forEach(function (project) {
            const card = document.createElement("article");
            card.className = "project-card";

            const title = document.createElement("h4");
            title.textContent = project.project_name;

            const status = document.createElement("span");
            status.className = "project-status";
            status.textContent =
                project.status || "Not set";

            const description = document.createElement("p");
            description.textContent =
                project.description ||
                "No description provided.";

            const dates = document.createElement("small");

            const start =
                project.start_date || "Not set";

            const end =
                project.end_date || "Not set";

            dates.textContent =
                `Start: ${start} | End: ${end}`;

            card.appendChild(title);
            card.appendChild(status);
            card.appendChild(description);
            card.appendChild(dates);

            projectList.appendChild(card);

            loadProjectAssignments(
                card,
                project.project_id
            );
        });
    }

    function renderActivities(activities) {
        activityCount.textContent = activities.length;
        activitiesList.innerHTML = "";

        if (!activities.length) {
            activitiesList.innerHTML = `
                <div class="empty-state">
                    <strong>No activities found</strong>
                    <p>
                        No authorized activities are currently
                        available.
                    </p>
                </div>
            `;
            return;
        }

        activities.forEach(function (activity) {
            const card = document.createElement("article");
            card.className = "activity-card";

            const title = document.createElement("h4");
            title.textContent =
                activity.activity_name || "Unnamed activity";

            const status = document.createElement("span");
            status.className = "activity-status";
            status.textContent =
                activity.status || "Not set";

            const description = document.createElement("p");
            description.textContent =
                activity.description ||
                "No description provided.";

            const details = document.createElement("small");

            const activityDate =
                activity.activity_date || "Date not set";

            const location =
                activity.location || "Location not set";

            details.textContent =
                `Project ID: ${activity.project_id}`
                + ` | Date: ${activityDate}`
                + ` | Location: ${location}`;

            card.appendChild(title);
            card.appendChild(status);
            card.appendChild(description);
            card.appendChild(details);

            if (activity.results) {
                const results = document.createElement("p");
                results.textContent =
                    `Results: ${activity.results}`;
                card.appendChild(results);
            }

            activitiesList.appendChild(card);

            loadActivityAssignments(
                card,
                activity.activity_id
            );
        });
    }

    async function loadUser() {
        const user = await fetchJson("/auth/me/");

        document.getElementById("user-name").textContent =
            user.username;

        document.getElementById("user-title").textContent =
            user.title;
    }

    async function loadProjects() {
        try {
            const data = await fetchJson("/projects/");
            renderProjects(data.projects);
        } catch (error) {
            if (error.status === 403) {
                projectCount.textContent = "0";

                projectList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            projects.
                        </p>
                    </div>
                `;
                return;
            }

            throw error;
        }
    }

    async function loadActivities() {
        try {
            const data = await fetchJson("/activities/");
            renderActivities(data.activities);
        } catch (error) {
            if (error.status === 403) {
                activityCount.textContent = "0";

                activitiesList.innerHTML = `
                    <div class="empty-state">
                        <strong>Access restricted</strong>
                        <p>
                            You do not have permission to view
                            activities.
                        </p>
                    </div>
                `;
                return;
            }

            throw error;
        }
    }

    async function loadProjectsAndActivities() {
        try {
            await loadUser();

            await Promise.all([
                loadProjects(),
                loadActivities(),
            ]);

            showMessage("");
        } catch (error) {
            if (error.status === 401) {
                window.location.href = "/login/";
                return;
            }

            showMessage(
                error.message ||
                "Unable to load project information.",
                "error"
            );
        }
    }

    loadProjectsAndActivities();
});
