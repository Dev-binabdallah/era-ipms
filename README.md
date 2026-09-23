ERA Integrated Project Management System (ERA-IPMS)

Project Overview

ERA Integrated Project Management System (ERA-IPMS) is a web-based information and project management system being developed to support the management, monitoring, accountability, and reporting of organisational and project activities.

The system is initially designed around the operational needs of Emergency Response Aid (ERA), which serves as the initial pilot organisation and requirements-validation partner.

ERA-IPMS provides a centralised platform for managing authorised information related to beneficiaries and disability services, projects and activities, poultry, small farm activities, finance, monitoring and evaluation, and related operational records.

The project has progressed beyond the initial documentation and architecture stage. Core backend functionality, database integration, authentication, authorization, API endpoints, and automated tests are now being implemented and expanded incrementally.

Project Baseline

| Item | Current baseline |
|---|---|
| Project | ERA Integrated Project Management System (ERA-IPMS) |
| Project type | Web-Based Information and Project Management System |
| Initial pilot organisation | Emergency Response Aid (ERA) |
| System owner/developer | Abdullahi Abdi Mohamed |
| Version | 1.1 |
| Current status | Active backend implementation and testing |
| Backend | Python / Django |
| Database | MariaDB / MySQL |
| Source of truth | GitHub main branch |

Why is ERA-IPMS Being Developed?

ERA requires practical ways to organise information associated with its organisational and project activities. ERA-IPMS is being developed to reduce fragmented record keeping and provide authorised users with relevant information through a central system.

The system is being developed to support:

Improved record management.

Beneficiary and disability-related activity management.

Home visits, referrals, and referral follow-ups.

Project and activity management.

Poultry production and operational tracking.

Small farm activity and harvest tracking.

Farm-to-poultry transfer tracking where applicable.

Basic sales, income, expense, and financial transaction recording.

Monitoring and evaluation.

Controlled access to organisational and programme information.

Management dashboards and reporting as further functionality is implemented.

Better accountability through controlled access and auditability.

Who Is ERA-IPMS For?

The initial system is being developed for Emergency Response Aid (ERA).

The initial user titles are:

Admin - System Administration

Director - Programme Oversight and M&E

Programme Coordinator - Programme and Project Coordination

Finance - Sales, Expenses, and Financial Records

Member - Assigned Programme Responsibilities

These are titles rather than fixed application roles with permanently bundled permissions.

The system distinguishes three concepts:

Title: the user's organisational or system title, such as Admin, Director, Programme Coordinator, Finance, or Member.

Permission: the action a user is authorised to perform, such as View, Add, Edit, Delete, Approve, Export, Manage, or Administer.

Responsibility: the programme or operational area assigned to a user, such as disability services, assessments, referrals and follow-ups, poultry, farm activities, project coordination, or M&E.

The authorization system uses these concepts together with the relevant resource and record scope when determining whether an authenticated user can access a protected operation or record.

Administrators can create future or custom titles and assign permissions according to the system's access-control design.

Initial Access and Governance Direction

ERA-IPMS uses controlled authentication and authorization.

The current implementation includes:

Users can sign in using username or email and password.

Access to protected operations is controlled through application permissions.

Programme and operational access can also depend on assigned responsibilities.

Record-level and scope-based authorization is applied where required.

Beneficiary records can be archived or made inactive rather than physically deleted.

The broader governance direction includes:

Admin: system administration and authorised administrative functions.

Director: programme oversight and M&E oversight.

Programme Coordinator: programme and project coordination and operational oversight.

Finance: financial records, sales, and expenses, including poultry and farm-related financial transactions.

Member: assigned programme responsibilities and operational records within the user's authorised scope.

Project and other resource access is controlled according to the applicable permission, responsibility, resource, and record-level authorization rules.

Future titles and additional permissions or responsibilities may be introduced as the system develops.

Audit logging remains part of the approved minimum viable system direction.

Main System Modules

The system is being developed as a set of related operational modules. Several modules already have implemented backend APIs and automated tests, while other functionality remains under development.

Administration and Access Management

Current functionality includes:

Authentication.

Users.

Titles and permissions.

Responsibility assignments.

Permission-based access control.

Responsibility-based access control.

Resource-level authorization.

Record-level and scope-based access control.

Authorization services, policies, decorators, and authorization-aware querysets.

Audit logging remains part of the wider approved system direction.

Beneficiary and Disability Management

Current functionality includes:

Beneficiary registration and retrieval.

Beneficiary listing.

Beneficiary updates.

Beneficiary archive functionality.

Disability assessments.

Home visits.

Referrals.

Referral approval.

Referral follow-ups.

Controlled beneficiary record access.

Project and Activity Management

Current functionality includes:

Projects.

Project listing and detail retrieval.

Project updates.

Project assignments.

Activities.

Activity assignments.

Activity participants.

Project and activity authorization.

Poultry Management

Current functionality includes:

Poultry groups.

Poultry stock movements.

Egg production.

Feed records.

Poultry health records.

Poultry sales.

Related poultry operational records.

Small Farm Management

Current functionality includes:

Farm crops.

Farm activities.

Harvests.

Farm-to-poultry transfers.

Farm-related operational records.

Finance

Current functionality includes:

Financial transactions.

Project-related financial transactions.

Organisation-related financial transactions.

Poultry-related financial transactions.

Farm-related financial transactions.

Sales and expense records within the implemented financial transaction structure.

The current scope is basic financial transaction management, not full accounting.

Monitoring and Evaluation

Current functionality includes:

M&E indicator creation.

M&E indicator listing.

M&E indicator retrieval.

M&E indicator updates.

M&E indicator deletion.

M&E indicator record creation.

M&E indicator record listing.

M&E indicator record updates.

M&E indicator record deletion.

Staff, Volunteers, and Members

Staff, volunteer, and member management remains part of the wider system scope.

The current implementation focuses on the user, title, permission, responsibility, and authorization structures required by the backend.

Additional staff and volunteer management functionality may be implemented as the project progresses.

Dashboard and Reporting

Dashboards, management summaries, routine reports, and authorised data exports remain part of the wider system scope.

These features are not considered fully implemented unless the corresponding functionality has been developed and verified.

Poultry and Small Farm Relationship

The poultry and small farm modules are related operational areas within ERA-IPMS.

The system supports separate records for poultry and farm activities while allowing controlled links between the two areas where required.

The current implementation includes:

Poultry groups and poultry stock movements.

Egg production.

Feed records.

Poultry health records.

Poultry sales.

Farm crops.

Farm activities.

Harvest records.

Farm-to-poultry transfers.

Financial transactions related to poultry and farm activities.

The farm-to-poultry transfer functionality provides a controlled way to record relevant movement of farm outputs into poultry operations.

The two modules remain separately managed so that poultry records and farm records can be maintained independently while still supporting relevant operational relationships.

Information Access and Accountability

ERA-IPMS is designed around controlled access to organisational and programme information.

Authorization is applied according to the requirements of the protected operation and may consider:

User authentication.

Permission.

Responsibility.

Resource.

Record.

Project or organisational scope.

The current authorization implementation uses centralized authorization services together with policy mappings, decorators, and authorization-aware querysets.

Protected resources currently include areas such as:

Projects and activities.

Beneficiaries and disability-related records.

Referrals and referral follow-ups.

Poultry records.

Farm records.

Financial transactions.

M&E indicators and indicator records.

The system is designed so that users only access records and operations within their authorised scope.

Beneficiary records can be archived or made inactive when they should no longer be treated as active records, rather than relying on physical deletion.

Automated tests are used to verify authorization behaviour, protected endpoints, access boundaries, and relevant record-level rules.

Technology Direction

ERA-IPMS is currently being developed using the following technologies:

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| Django | Web application framework |
| MariaDB / MySQL | Relational database |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Client-side interaction where required |
| Django Test Framework | Automated backend testing |
| Git / GitHub | Source code and version control |

The current backend architecture is based on Django with MariaDB/MySQL.

The application uses Django's request handling, database integration, authentication, authorization, and testing capabilities.

The project is currently focused on backend implementation and API development, with user interface and reporting functionality being developed according to the project roadmap.

Java is not part of the current technology baseline.

Development Approach

Development follows a controlled implementation and testing process based on the approved project documentation and system architecture.

The current implementation process includes:

Review the required functionality.

Implement the relevant backend endpoint, service, or authorization logic.

Apply the applicable permission, responsibility, resource, and record-level authorization rules.

Add or update automated tests.

Run Django system checks and relevant tests.

Review the implementation and related changes.

Update the documentation and development log where required.

Commit completed work after verification.

The development environment is centred on VS Code, with its integrated terminal used for Django, Git, MariaDB/MySQL, and related development commands.

New functionality is being added incrementally so that implementation, authorization, testing, and documentation can be reviewed together.

Project Roadmap

The project has progressed from documentation and architecture planning into active backend implementation, API development, authorization, and automated testing.

The current development path is:

Documentation, Planning and Requirements
↓
Architecture and Database Baseline
↓
Django Application Foundation
↓
Authentication and Access Control
↓
Core Programme and Beneficiary Modules
↓
Project and Activity Management
↓
Poultry, Farm and Finance Modules
↓
Monitoring and Evaluation Modules
↓
Continued API Development and Automated Testing
↓
Dashboard, Reporting, and Additional User Interface Features
↓
Security Review and Deployment Preparation

The current development work is focused on completing and refining backend functionality, expanding automated test coverage, and implementing remaining system requirements.

The implementation order may be adjusted as requirements and technical findings are reviewed.

Repository Structure

The main project structure currently includes:

era-ipms/
│
├── README.md
├── LICENSE
├── .gitignore
├── development_log.md
│
├── docs/
│   ├── planning/
│   ├── requirements/
│   ├── system-design/
│   ├── database/
│   │   └── erd/
│   ├── testing/
│   └── deployment/
│
├── backend/
│   ├── config/
│   └── core/
│       ├── authorization/
│       ├── migrations/
│       ├── tests/
│       ├── models.py
│       ├── views.py
│       └── admin.py
│
└── database/
    └── schema.sql

The backend contains the Django application, authorization components, migrations, models, views, administrative configuration, and automated tests.

The database directory contains the approved database schema baseline.

The documentation directory contains project planning, requirements, system design, database, testing, and deployment documentation.

The development log records significant implementation and project changes.

The repository structure may continue to evolve as implementation progresses.

Data Protection and Security

ERA-IPMS may manage organisational information and potentially sensitive beneficiary information.

Development and deployment should therefore follow appropriate security and data-protection practices.

The project baseline requires that:

Real beneficiary information is not used in development or testing.

Fictional or anonymised data is used for testing.

Passwords and credentials are not stored in the repository.

Secrets are supplied through appropriate environment or deployment configuration.

Confidential organisational information is not published in the repository.

Access to beneficiary and operational information is controlled by permissions and record-level access.

Security-sensitive configuration is reviewed before deployment.

Documentation and Change Control

GitHub is the project source of truth, with the main branch representing the current approved project state.

Changes to requirements, permissions, workflows, database structures, or architecture should be documented before implementation where practical.

Contradictions between project documents should be identified and resolved during the documentation baseline review rather than silently resolved in code.

The README describes the current project baseline. Detailed requirements and technical definitions remain in the corresponding documents under docs/.

Future Scope

The initial release is intentionally focused on the agreed ERA pilot requirements.

Future capabilities may include additional reporting, integrations, expanded organisational support, or other features identified through validated requirements and later project phases.

Future scope should not be treated as part of the initial implementation unless it is formally added to the approved requirements.

Project Status

Current Status: Active Backend Implementation and Testing

ERA-IPMS has progressed from the original documentation and architecture baseline to an active Django backend with database integration, authentication, centralized authorization, protected API endpoints, and automated tests.

Implemented backend functionality currently covers several operational areas, including:

Beneficiaries and disability-related services.

Projects and activities.

Referrals and referral follow-ups.

Poultry operations.

Small farm operations.

Financial transactions.

Monitoring and evaluation indicators and indicator records.

Recent development has focused on expanding API functionality, authorization coverage, automated testing, and record management.

Development is continuing incrementally. Existing functionality is being tested and reviewed while remaining system requirements and user interface features are implemented.

The project should be considered an active development system rather than a final production release.

Intellectual Property

ERA-IPMS is currently developed and owned by Abdullahi Abdi Mohamed.

Emergency Response Aid (ERA) serves as the initial pilot organisation and requirements-validation partner.

ERA organisational data, beneficiary information, confidential records, and other sensitive information are not included in this repository.

License

Copyright © 2026 Abdullahi Abdi Mohamed. All rights reserved.

ERA-IPMS is proprietary software. Public access to this repository does not grant permission to copy, modify, redistribute, sublicense, or commercially use the software without prior written permission from the copyright holder.

See the LICENSE file for further information.

Author

Abdullahi Abdi Mohamed

Documentation Baseline Version: 1.1
Date: September 2026