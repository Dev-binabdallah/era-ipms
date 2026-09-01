# ERA Integrated Project Management System (ERA-IPMS)

## What is ERA-IPMS?

ERA Integrated Project Management System (ERA-IPMS) is a web-based information management system being developed to support the management, monitoring, and reporting of organisational and project activities.

The system is initially being designed around the operational needs of Emergency Response Aid (ERA), which serves as the initial pilot organisation and requirements-validation partner.

ERA-IPMS will provide a centralised system for managing information related to disability activities, poultry farming, and a small vegetable farm that supports the poultry project.

## Why is ERA-IPMS Being Developed?

ERA-IPMS is being developed to improve how organisational and project information is recorded, organised, monitored, and reported.

The system aims to reduce fragmented record keeping and provide a central platform where authorised users can access relevant information.

The project will support:

* Improved record management.
* Easier monitoring of project activities.
* Poultry production tracking.
* Small farm activity and harvest tracking.
* Disability-related activity management.
* Basic income and expense recording.
* Monitoring and evaluation.
* Management dashboards.
* Routine reporting.

## Who Is ERA-IPMS For?

The initial system is being developed for Emergency Response Aid (ERA) as the pilot organisation.

Potential system users include:

* System Administrator.
* Programme Coordinator.
* Field Officers.
* Finance personnel.
* Monitoring and Evaluation personnel.
* ERA management.

The system may later be adapted and licensed for use by other Community-Based Organisations (CBOs), Non-Governmental Organisations (NGOs), and organisations with similar project management and reporting requirements.

## Technology Stack

ERA-IPMS is being developed using the following technologies:

| Technology | Purpose                                                              |
| ---------- | -------------------------------------------------------------------- |
| HTML       | Creates the structure of web pages and forms                         |
| CSS        | Controls the design and appearance of the user interface             |
| Python     | Handles backend application logic                                    |
| Django     | Python web framework used to build the web application               |
| MySQL      | Stores and manages structured system data                            |
| Java       | May be used only where specifically required by project requirements |

## Planned Modules

The initial version of ERA-IPMS is planned to include:

1. User Authentication and Access Control.
2. Project Management.
3. Disability Activity and Beneficiary Management.
4. Poultry Management.
5. Small Vegetable Farm Management.
6. Activity Management.
7. Basic Financial Management.
8. Monitoring and Evaluation.
9. Management Dashboard.
10. Reporting.

Additional features may be introduced in future versions based on validated organisational requirements.

## Development Status

**Current Stage: Planning and Requirements Analysis**

The current focus of the project includes:

* Project concept development.
* Requirements gathering.
* Needs assessment.
* User and stakeholder identification.
* User roles and permissions.
* System workflow design.
* Database planning.

Software development will proceed after the requirements and system design have been sufficiently defined.

## Project Roadmap

```text
Phase 1 — Planning and Requirements
        ↓
Phase 2 — Database Design and Development
        ↓
Phase 3 — Django Development
        ↓
Phase 4 — Authentication and Permissions
        ↓
Phase 5 — Core Modules
        ↓
Phase 6 — Dashboard, Finance and M&E
        ↓
Phase 7 — Reporting
        ↓
Phase 8 — Testing and Deployment
```

## Project Structure

```text
era-ipms/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── planning/
│   ├── requirements/
│   ├── system-design/
│   ├── database/
│   ├── testing/
│   └── deployment/
│
├── backend/
├── frontend/
├── database/
└── tests/
```

## Data Protection

ERA-IPMS may eventually manage organisational and potentially sensitive information.

For this reason:

* Real beneficiary information will not be used during development.
* Fictional or anonymised data will be used for testing.
* Passwords and credentials will not be stored in the repository.
* Environment files containing secrets will be excluded using `.gitignore`.
* Confidential organisational information will not be published in the repository.

## Intellectual Property

ERA-IPMS is currently developed and owned by **Abdullahi Abdi Mohamed**.

Emergency Response Aid (ERA) serves as the initial pilot organisation and requirements-validation partner.

ERA organisational data, beneficiary information, confidential records, and other sensitive information are not included in this repository.

## License

Copyright © 2026 Abdullahi Abdi Mohamed. All rights reserved.

ERA-IPMS is proprietary software. Public access to this repository does not grant permission to copy, modify, redistribute, sublicense, or commercially use the software without prior written permission from the copyright holder.

See the `LICENSE` file for further information.

## Author

**Abdullahi Abdi Mohamed**

## Project Status

🚧 **Currently under planning and requirements analysis.**