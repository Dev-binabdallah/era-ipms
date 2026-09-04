ERA Integrated Project Management System (ERA-IPMS)

Project Overview

ERA Integrated Project Management System (ERA-IPMS) is a web-based information and project management system being developed to support the management, monitoring, accountability, and reporting of organisational and project activities.

The system is initially being designed around the operational needs of Emergency Response Aid (ERA), which serves as the initial pilot organisation and requirements-validation partner.

ERA-IPMS is intended to provide a centralised platform for managing authorised information related to disability services and beneficiary activities, projects and activities, poultry, a small farm, finance, staff and members, monitoring and evaluation, dashboards, and reporting.

Project Baseline

Item

Current baseline

Project

ERA Integrated Project Management System (ERA-IPMS)

Project type

Web-Based Information and Project Management System

Initial pilot organisation

Emergency Response Aid (ERA)

System owner/developer

Abdullahi Abdi Mohamed

Version

1.1

Status

Documentation and Architecture Baseline

Backend

Python / Django

Database

MariaDB / MySQL

Source of truth

GitHub main branch

This baseline is being established before further application and database development. Documentation, requirements, workflows, permissions, data structures, and architecture are being aligned first so that implementation is based on an agreed system design.

Why is ERA-IPMS Being Developed?

ERA currently requires practical ways to organise information associated with its organisational and project activities. ERA-IPMS is being developed to reduce fragmented record keeping and provide authorised users with relevant information through a central system.

The system is intended to support:

Improved record management.

Beneficiary and disability-related activity management.

Home visits, referrals, and follow-ups.

Project and activity management.

Poultry production tracking.

Small farm activity and harvest tracking.

Basic sales, income, and expense recording.

Staff, volunteers, and member information.

Monitoring and evaluation.

Management dashboards.

Routine and management reporting.

Better accountability through controlled access and auditability.

Who Is ERA-IPMS For?

The initial system is being developed for Emergency Response Aid (ERA).

The initial user titles are:

Admin - System Administration

Director - Programme Oversight and M&E

Programme Coordinator - Programme and Project Coordination

Finance - Sales, Expenses, and Financial Records

Member - Assigned Programme Responsibilities

These are titles, not fixed application roles with permanently bundled permissions.

The system distinguishes three concepts:

Title: the user's organisational or system title, such as Admin, Director, Programme Coordinator, Finance, or Member.

Permission: the actions a user is authorised to perform, such as View, Add, Edit, Delete, Approve, Export, Manage, or Administer.

Responsibility: the programme or operational area assigned to a user, such as disability services, assessments, referrals and follow-ups, poultry, farm activities, project coordination, or M&E.

Administrators can create future/custom titles and assign permissions individually. Record-level access is also required so that users do not automatically receive unrestricted access to all organisational information.

Initial Access and Governance Direction

ERA-IPMS will use controlled authentication and authorisation.

The approved authentication direction is:

Users can sign in using username or email and password.

Passwords must follow a strong security policy.

Access is controlled by application permissions.

Users should only access records and actions authorised for their title, permissions, responsibilities, and record-level scope.

Beneficiary records are intended to be archived or made inactive rather than physically deleted.

An audit log is part of the approved minimum viable system direction.

The initial governance direction includes:

Admin: system administration, user/title/permission management, and authorised project administration. Technical authority does not automatically grant programme decision authority.

Director: programme oversight, M&E oversight, and authority relating to continuation of projects and activities.

Programme Coordinator: programme and project coordination and operational oversight.

Finance: financial records, sales, and expenses, including poultry and farm-related financial transactions.

Member: assigned programme responsibilities and operational records within their authorised scope.

Project creation is initially assigned to Admin and Director. Future titles may be created by Admin.

Main System Modules

The initial scope includes the following modules:

Administration and Access Management

Authentication.

Users.

Titles and permissions.

Responsibility assignments.

Access control.

Audit logging.

Beneficiary and Disability Management

Beneficiary registration and search.

Disability information and assessments.

Home visits.

Referrals.

Referral follow-ups.

Controlled beneficiary record access.

Project and Activity Management

Projects.

Activities.

Activity participants.

Project assignment and coordination.

Activity monitoring.

Poultry Management

Poultry stock transactions.

Egg production.

Feed records.

Poultry health records.

Poultry categories/groups.

Poultry sales and related operational records.

Small Farm Management

Farm crops.

Farm activities.

Harvests.

Farm-related operational records.

Farm-to-poultry feed transfer tracking where applicable.

Staff, Volunteers, and Members

Staff and volunteer information.

Member responsibilities and assignments.

Controlled operational access.

Finance

Sales.

Expenses.

Basic financial records.

Poultry and farm-related financial transactions.

The initial scope is basic financial management, not full accounting.

Monitoring and Evaluation

M&E indicators.

Project and activity monitoring.

Management-level monitoring information.

Dashboard and Reporting

Management dashboards.

Operational summaries.

Routine reports.

Authorised data exports where permitted.

Poultry and Small Farm Relationship

The poultry and small farm modules are related operationally.

The farm may produce crops and other materials that can support poultry activities. Where farm produce is transferred for poultry feed, the system should provide a record of that transfer so that farm outputs and poultry inputs can be tracked consistently.

Poultry records will support operational quantities such as stock, eggs, feed, health events, and sales. Financial transactions associated with these activities are handled through the finance module according to the user's authorised permissions.

Information Access and Accountability

ERA-IPMS is designed around least-privilege access.

A user's title alone does not automatically provide unrestricted access. Permissions and responsibilities determine what actions and programme areas the user may access, while record-level controls further restrict access where required.

Examples of the approved access direction include:

Members access their own authorised operational records and own contribution totals per project.

Members can access beneficiary records they personally registered, assessed, or visited, subject to the applicable permissions.

Members can create and submit referrals, while approval is performed by an authorised person.

Members maintain operational poultry records within their authorised scope.

Admin and Programme Coordinator can review authorised poultry information.

Finance manages authorised financial transactions.

Director provides programme oversight and M&E oversight.

These rules will be refined and formalised in the User Roles and Permissions and Software Requirements Specification documents.

Technology Direction

ERA-IPMS is being developed using:

Technology

Purpose

Python

Backend application logic

Django

Web application framework

MariaDB / MySQL

Relational database

HTML

Web page structure

CSS

User interface styling

JavaScript

Client-side interaction where required

The current architecture direction is Django with MariaDB/MySQL. Java is not part of the current technology baseline.

Development Approach

Development follows a documentation-first and controlled implementation process.

The current sequence is:

Project Concept Note.

README baseline.

Needs Assessment.

Stakeholder Analysis.

Software Requirements Specification.

User Roles and Permissions.

System Workflows.

Database Entity Design.

ERD documentation.

Database schema.

Development Log.

Application and database implementation after the documentation baseline is aligned.

Each logical documentation step should be reviewed and committed before moving to the next step.

The development environment is centred on VS Code, with its integrated terminal used for Django, Git, MariaDB/MySQL, and related development commands.

Project Roadmap

Phase 1  Documentation, Planning and Requirements
              ↓
Phase 2  Architecture and Database Baseline
              ↓
Phase 3  Django Application Foundation
              ↓
Phase 4  Authentication, Titles, Permissions and Access Control
              ↓
Phase 5  Core Programme and Beneficiary Modules
              ↓
Phase 6  Poultry, Farm and Finance Modules
              ↓
Phase 7  M&E, Dashboard and Reporting
              ↓
Phase 8  Testing, Security Review and Deployment

The detailed implementation order may be adjusted after the documentation and architecture review.

Repository Structure

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
│   │   └── erd/
│   ├── testing/
│   ├── deployment/
│   └── development_log.md
│
├── backend/
│   ├── config/
│   └── core/
│
├── frontend/
├── database/
└── tests/

The repository structure may evolve as implementation progresses, but changes should be documented and kept consistent with the approved architecture.

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

Current Status: Documentation and Architecture Baseline

The Project Concept Note has been updated to version 1.1, and the README is being aligned with that baseline.

The project is not yet at the stage where new application pages or database architecture changes should be introduced solely from assumptions. The remaining documentation baseline must first be reviewed for consistency before implementation proceeds.

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