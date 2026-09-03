# ERA Integrated Project Management System (ERA-IPMS)

## Project Concept Note

**Project Title:** ERA Integrated Project Management System (ERA-IPMS)
**Project Type:** Web-Based Information and Project Management System
**Initial Pilot Organisation:** Emergency Response Aid (ERA)
**System Owner and Developer:** Abdullahi Abdi Mohamed
**Current Version:** 1.1
**Status:** Documentation and Architecture Baseline
**Date:** September 2026
**Database:** MariaDB/MySQL
**Backend:** Python/Django

## 1. Background

Emergency Response Aid (ERA) is a Community-Based Organisation involved in disability services, community advocacy and awareness, poultry farming, and small-scale farming activities.

ERA provides disability-related services including home visits, assessments, referrals, follow-up support, capacity-building activities, advocacy, and awareness activities. ERA members and other authorised personnel may participate in delivering and supporting these services according to their assigned responsibilities.

ERA also manages livelihood activities, including a small poultry project and a small farm. The poultry project currently focuses mainly on egg production and includes local and Kienyeji chickens. ERA plans to expand the poultry project in the future to support additional activities such as meat production and breeding.

The small farm grows bananas, local or natural vegetables, and sukuma wiki. Farm activities include planting, watering, weeding, and harvesting. Farm produce can support the poultry project as feed, while future surplus produce may also be sold.

Much of ERA's information has traditionally been managed using manual and paper-based documentation. ERA-IPMS is being developed as a centralised digital system to improve information management, monitoring, coordination, accountability, and reporting.

## 2. Problem Statement

ERA has experienced challenges associated with manual and fragmented information management.

These challenges include:

* Difficulty finding older beneficiary and activity records.
* Risk of losing or damaging paper records.
* Risk of duplicate beneficiary records.
* Time-consuming report preparation.
* Difficulty determining the total number of beneficiaries served.
* Difficulty tracking referrals and follow-ups.
* Difficulty monitoring poultry numbers and production.
* Lack of structured feed and poultry health records.
* Difficulty monitoring farm production and harvests.
* Difficulty consolidating farm and poultry expenses.
* Difficulty monitoring project and activity progress.
* Difficulty producing consistent organisational and project reports.
* Difficulty providing management with timely information for decision-making.

ERA-IPMS is intended to address these challenges through structured digital records, controlled access, centralised information, monitoring features, dashboards, and reporting.

## 3. Project Goal

The goal of ERA-IPMS is to develop a centralised web-based information and project management system that improves the recording, management, coordination, monitoring, analysis, accountability, and reporting of ERA's disability services, projects, activities, poultry operations, small farm activities, and financial information.

## 4. Project Objectives

The project aims to:

1. Digitise selected manual records currently used by ERA.
2. Improve the registration and management of beneficiary information.
3. Support the recording and tracking of disability assessments, home visits, referrals, and follow-ups.
4. Allow authorised Members to perform and record disability awareness, assessments, referrals, and follow-up activities.
5. Improve monitoring of poultry numbers, egg production, feed, illnesses, deaths, and related activities.
6. Introduce structured digital records for small farm activities, crops, harvests, expenses, and produce transfers to poultry.
7. Support the management and coordination of projects and organisational activities.
8. Provide controlled access based on user titles, permissions, and assigned responsibilities.
9. Support Members in viewing their own contributed activities and contribution totals for projects to which they are assigned.
10. Support the Programme Coordinator in coordinating programme implementation and reviewing operational records.
11. Support the Director in monitoring programme performance and making authorised decisions concerning project and activity continuation.
12. Support Finance personnel in recording and managing sales, expenses, and authorised financial information.
13. Provide Admin with system administration and user access management capabilities.
14. Improve the management of staff, volunteers, and Member responsibilities.
15. Provide management with a central dashboard containing key organisational information.
16. Improve the speed, consistency, accountability, and quality of organisational and project reporting.

## 5. Proposed Solution

ERA-IPMS will be developed as a web-based information management and project management system.

The system will provide authorised users with a central platform for recording, managing, searching, monitoring, coordinating, and reporting organisational information.

The system will use a flexible authorisation structure based on three separate concepts:

### 5.1 Titles

A title identifies the organisational position or system title assigned to a user.

The initial ERA-IPMS titles are:

1. **Admin**
2. **Director**
3. **Programme Coordinator**
4. **Finance**
5. **Member**

Additional titles may be created when ERA's organisational structure changes or new responsibilities emerge.

Admin will be responsible for creating, updating, assigning, and managing titles within the system.

### 5.2 Permissions

Permissions define what actions a user may perform within the system.

The initial permission types are:

* View
* Add
* Edit
* Delete
* Approve
* Export
* Manage
* Administer

Admin will be able to assign permissions to titles.

A newly created title will not automatically receive unrestricted access. Its permissions must be explicitly configured by Admin.

### 5.3 Responsibilities

Responsibilities define the operational work assigned to a person.

Examples include:

* Disability awareness
* Disability assessment
* Referrals
* Referral follow-up
* Home visits
* Poultry management
* Farm activities
* Project activities
* Monitoring and evaluation
* Programme coordination
* Other responsibilities approved by ERA

A Member will use one general **Member** title while their specific programme responsibilities may differ.

For example, one Member may be responsible for disability services while another Member may be responsible for poultry activities.

## 6. Initial User Titles and Responsibilities

### 6.1 Admin

**Primary responsibility:** System Administration

Admin will be responsible for:

* Managing user accounts.
* Activating and deactivating users.
* Assigning titles to users.
* Creating new titles.
* Updating titles.
* Removing titles where authorised.
* Assigning permissions to titles.
* Managing system-level access.
* Managing authorised organisational records.
* Creating, updating, and removing projects where authorised.
* Managing system configuration.
* Supporting account and access administration.

Admin's technical authority does not automatically mean that Admin makes programme decisions reserved for the Director.

### 6.2 Director

**Primary responsibility:** Programme Oversight and Monitoring and Evaluation

The Director will be responsible for:

* Monitoring programme performance.
* Reviewing M&E information.
* Reviewing project and activity progress.
* Providing programme oversight.
* Reviewing project and activity continuation.
* Giving authorised approval for continuation of projects and activities.
* Reviewing management information and reports.
* Supporting organisational decision-making.

### 6.3 Programme Coordinator

**Primary responsibility:** Programme and Project Coordination

The Programme Coordinator will be responsible for:

* Coordinating project implementation.
* Coordinating activities.
* Monitoring day-to-day programme implementation.
* Reviewing records submitted by Members.
* Coordinating Member assignments and programme responsibilities where authorised.
* Following up on incomplete programme records.
* Reviewing disability service, poultry, farm, and activity records as authorised.
* Supporting project reporting.
* Providing programme information to the Director.
* Supporting the continuity and effective implementation of approved projects and activities.

The Programme Coordinator will not automatically have system administration privileges.

### 6.4 Finance

**Primary responsibility:** Sales, Expenses, and Financial Records

Finance will be responsible for:

* Recording organisational sales.
* Recording poultry sales.
* Recording farm produce sales where applicable.
* Recording organisational expenses.
* Recording project expenses.
* Recording poultry expenses.
* Recording farm expenses.
* Maintaining authorised financial records.
* Reviewing financial transactions.
* Preparing financial summaries and reports.

Operational quantities may be recorded by Members or other authorised personnel, while financial transactions and monetary records remain under Finance access.

### 6.5 Member

**Primary responsibility:** Assigned Programme Responsibilities

Members will perform programme work according to responsibilities assigned to them.

Depending on their assigned responsibilities, Members may:

* Conduct community awareness.
* Conduct disability assessments.
* Record beneficiary information.
* Conduct home visits.
* Create and submit referrals.
* Conduct referral follow-ups.
* Record follow-up outcomes.
* Participate in project activities.
* Manage assigned poultry activities.
* Record poultry information.
* Participate in farm activities.
* Record assigned farm activities.
* Contribute to other authorised organisational activities.

Members will only access records authorised for their assigned responsibilities.

A Member will be able to view their own relevant records and their own contribution totals for projects to which they have contributed.

## 7. Major System Modules

The proposed system will initially include the following major modules.

### 7.1 Administration and Access Management

This module will support:

* User accounts.
* Titles.
* Permissions.
* Responsibility assignments.
* User activation and deactivation.
* Password management.
* Access control.
* Administrative records.

### 7.2 Disability and Beneficiary Management

This module will support:

* Beneficiary registration.
* Duplicate checking before registration.
* Disability assessments.
* Home visit records.
* Referrals.
* Referral approval.
* Referral tracking.
* Follow-up assignments.
* Follow-up records.
* Follow-up outcomes.
* Beneficiary searching.
* Controlled beneficiary access.

Members will primarily access beneficiaries they personally registered, assessed, or visited, subject to their assigned permissions.

### 7.3 Project and Activity Management

This module will support:

* Project registration.
* Project management.
* Project status.
* Activity planning.
* Activity assignment.
* Recording completed activities.
* Tracking upcoming activities.
* Tracking pending activities.
* Recording Member participation.
* Tracking individual Member contributions.
* Project and activity reporting.
* Authorised project and activity continuation decisions.

Projects may be created by Admin or Director according to their respective permissions.

The Director will have authority over programme oversight and authorised continuation decisions.

### 7.4 Poultry Management

This module will support:

* Poultry or flock records.
* Poultry categories or groups.
* Chicken and chick purchases.
* Poultry received.
* Poultry sales.
* Poultry deaths.
* Poultry adjustments.
* Egg production.
* Feed usage.
* Purchased feed.
* Feed received from the small farm.
* Poultry health records.
* Poultry-related operational activities.
* Assigned poultry responsibilities.

Members assigned to poultry responsibilities will maintain operational records.

Finance will manage the associated financial transactions.

### 7.5 Small Farm Management

This module will support:

* Crop records.
* Planting activities.
* Watering activities.
* Weeding activities.
* Harvest records.
* Farm expenses.
* Produce transferred to poultry.
* Future farm produce sales and income records.
* Assigned farm responsibilities.

### 7.6 Staff, Volunteers, and Member Management

The system will support:

* Staff records.
* Volunteer records.
* Member records.
* User accounts.
* Titles.
* Permissions.
* Assigned responsibilities.
* User status.

### 7.7 Finance Management

The initial finance module will support basic financial record management rather than full accounting.

It will include:

* Sales.
* Expenses.
* Project expenses.
* Poultry expenses.
* Farm expenses.
* Other authorised organisational financial records.
* Financial summaries.
* Financial reports.

Advanced accounting functionality remains outside the initial scope.

### 7.8 Monitoring and Evaluation

The M&E functionality will support:

* Programme indicators.
* Project monitoring.
* Activity monitoring.
* Progress information.
* Management information.
* M&E reporting.
* Director oversight.

### 7.9 Dashboard and Reporting

The system dashboard should provide authorised users with information appropriate to their responsibilities.

Management information may include:

* Total beneficiaries.
* Number of home visits.
* Number of referrals.
* Referral follow-up and completion status.
* Current poultry numbers.
* Egg production.
* Feed usage and purchases.
* Poultry illnesses and deaths.
* Farm crops and harvests.
* Farm expenses.
* Organisational and project expenses.
* Number of activities conducted.
* Member contribution totals.
* Number of staff and Members.
* Upcoming activities.
* Pending activities.
* Project progress.
* M&E information.

Users should only see dashboard information permitted by their title, permissions, and assigned responsibilities.

## 8. Information Access and Accountability

ERA-IPMS will follow the principle of least privilege.

Users should receive only the access necessary to perform their authorised responsibilities.

The system will distinguish between:

* What a user is called.
* What a user is permitted to do.
* What a user is responsible for doing.
* Which records the user is authorised to access.

For sensitive beneficiary information, access will be restricted according to the user's authorised records.

Members will generally access beneficiaries they personally registered, assessed, or visited.

Members will not automatically receive access to all beneficiary records.

Members will also not automatically receive access to financial records.

Finance users will not require access to detailed disability information to perform financial responsibilities.

Important system and record activities will be auditable.

## 9. Disability Service Workflow

The planned digital disability service process is:

```text
Person Identified
       ↓
Beneficiary Search
       ↓
Existing Record Found?
   ↙            ↘
 Yes             No
  ↓               ↓
Use Existing    Register
  ↓               ↓
Assessment / Service Activity
       ↓
Needs Identified
       ↓
Referral Created
       ↓
Referral Submitted
       ↓
Authorised Review / Approval
       ↓
Referral Follow-Up
       ↓
Outcome Recorded
```

Members with the appropriate responsibility and permissions may conduct awareness, assessments, referrals, and follow-ups.

The system will record the responsible user and relevant dates for important activities.

## 10. Poultry and Small Farm Relationship

ERA's small farm and poultry activities are connected.

Farm produce may be transferred to the poultry project and used as feed.

Poultry feed may therefore come from:

1. Produce from the small farm.
2. Purchased local feed.

The system will record farm-to-poultry transfers separately from purchased feed.

The operational record and financial record will remain distinguishable.

For example:

```text
Small Farm
    ↓
Harvest
    ↓
Produce Transfer
    ↓
Poultry Feed
```

Where a poultry or farm product is sold, the operational quantity and financial transaction may be recorded separately.

## 11. Project and Activity Governance

ERA-IPMS will distinguish between system administration and programme governance.

Admin will have system-level authority to manage authorised project records and system access.

The Director will provide programme oversight and make authorised decisions concerning continuation of projects and activities.

The Programme Coordinator will coordinate implementation and monitor operational progress.

Members will carry out assigned activities and record their contributions.

This separation is intended to improve accountability while allowing the system to remain flexible as ERA's organisational structure develops.

## 12. System Scope

### 12.1 Included in the Initial Scope

The first version of ERA-IPMS will include:

* User authentication.
* User administration.
* Dynamic titles.
* Configurable permissions.
* Responsibility assignments.
* Beneficiary management.
* Disability assessment records.
* Home visit records.
* Referral and follow-up tracking.
* Project management.
* Activity management.
* Member contribution tracking.
* Poultry management.
* Small farm management.
* Staff and volunteer records.
* Basic finance and expense management.
* Sales records.
* Management dashboard.
* Monitoring and evaluation information.
* Basic reporting.
* Record searching.
* Audit and accountability features for important records.

### 12.2 Future Scope

Potential future developments may include:

* Mobile application.
* Offline data collection.
* SMS or messaging notifications.
* Advanced monitoring and evaluation.
* Advanced financial management and accounting.
* Multi-organisation support.
* Commercial licensing for other CBOs or NGOs.
* Advanced analytics.
* Expanded reporting.
* External partner access.
* KoboToolbox integration.
* Excel import.
* Additional integrations.

These features are not required for the initial MVP unless subsequently approved.

## 13. Technology Direction

The current technology direction is:

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| HTML          | Web page structure                        |
| CSS           | User interface design and styling         |
| JavaScript    | Client-side interaction where required    |
| Python        | Backend programming and application logic |
| Django        | Python web framework                      |
| MariaDB/MySQL | Relational database                       |
| Git/GitHub    | Source control and project versioning     |

ERA-IPMS will be developed and maintained using VS Code as the primary development environment.

## 14. Development Approach

The project will follow a controlled, incremental development process.

### Phase 1: Documentation and Architecture Baseline

* Review existing project documentation.
* Resolve contradictions between documents.
* Update organisational roles.
* Define titles, permissions, and responsibilities.
* Confirm workflows.
* Confirm information-access rules.
* Confirm database design requirements.
* Establish the approved documentation baseline.

### Phase 2: Database Design Alignment

* Review the authoritative database design.
* Align entities with the approved requirements.
* Review relationships.
* Review keys and constraints.
* Review access-control entities.
* Update the Entity Relationship Diagram.
* Update the authoritative database schema.

### Phase 3: Backend Alignment

* Configure Django for MariaDB/MySQL.
* Align Django models with the approved database design.
* Implement titles, permissions, and responsibilities.
* Implement record-level access controls.
* Implement audit requirements.
* Complete authentication and security requirements.

### Phase 4: Core Module Development

* Administration.
* Beneficiaries and disability services.
* Projects and activities.
* Poultry.
* Small farm.
* Finance.
* Staff and Members.
* M&E.

### Phase 5: User Interface Development

The UI will follow a professional NGO/public-facing design direction.

The interface should prioritise:

* Clear navigation.
* Consistent spacing.
* Good accessibility.
* Strong readability.
* Appropriate information density.
* Simple forms.
* Clear status information.
* Responsive layouts.
* Professional ERA branding when the official logo and branding assets are provided.

The UI will avoid unnecessary decorative trends that reduce usability or resemble generic SaaS interfaces.

### Phase 6: Testing

* Unit testing.
* Integration testing.
* Authentication testing.
* Permission testing.
* Record-level access testing.
* Workflow testing.
* Database testing.
* User acceptance testing.
* Security testing.
* Testing with fictional or anonymised data.

### Phase 7: Deployment and Training

* Production database preparation.
* Application deployment.
* Security configuration.
* User account setup.
* Training.
* Documentation.
* Monitoring.
* Maintenance.

## 15. Data Protection and Confidentiality

ERA-IPMS may manage beneficiary and organisational information requiring appropriate protection.

During development:

* Real beneficiary data will not be uploaded to the public GitHub repository.
* Fictional or appropriately anonymised data will be used for testing.
* Passwords and credentials will not be committed to the repository.
* Secret keys and database credentials will be stored outside source code.
* Environment variables and secret files will be excluded using `.gitignore`.
* Confidential organisational records will not be publicly published.
* Users will only access records authorised by their permissions and responsibilities.
* Important system activities will be recorded for accountability where appropriate.

## 16. Expected Benefits

ERA-IPMS is expected to provide:

* Centralised information management.
* Faster retrieval of records.
* Reduced dependence on paper records.
* Improved beneficiary record management.
* Better referral and follow-up tracking.
* Better monitoring of disability services.
* Better monitoring of poultry and farm activities.
* Improved financial record management.
* Better project and activity monitoring.
* Clearer responsibility and access control.
* Improved accountability.
* Easier management reporting.
* Improved consistency and quality of reports.
* Better information for organisational decision-making.
* A flexible foundation that can grow with ERA.

## 17. Ownership and Pilot Arrangement

ERA-IPMS is currently developed and owned by Abdullahi Abdi Mohamed.

Emergency Response Aid (ERA) serves as the initial pilot organisation and provides the operational context and requirements used to guide development.

The project may later be adapted, expanded, or licensed for use by other Community-Based Organisations, Non-Governmental Organisations, or organisations with similar information management requirements, subject to future ownership, licensing, and organisational agreements.

## 18. Project Status

**Current Status: Active Development with Documentation and Architecture Baseline Under Review**

The initial operational requirements have been documented and the project has progressed beyond the original planning-only stage.

The project now includes an implemented Django backend foundation and a working custom authentication and session mechanism.

The current development process is being reorganised around an approved documentation-first approach.

Before further major code or database changes, the existing project documentation will be reviewed and updated to establish a consistent requirements and architecture baseline.

The approved sequence is:

```text
Documentation Review
        ↓
Requirements Alignment
        ↓
Architecture Baseline
        ↓
Database Design Alignment
        ↓
Backend Alignment
        ↓
Core Module Development
        ↓
UI Development
        ↓
Testing
        ↓
Deployment
```

## 19. Development and Change Control

ERA-IPMS development will follow a controlled change process.

For each major development step:

1. Review the relevant requirement or design document.
2. Identify contradictions or missing requirements.
3. Approve the required documentation change.
4. Update the document in VS Code.
5. Review the Git diff.
6. Verify the document.
7. Commit the completed change.
8. Push the commit to GitHub.
9. Proceed to the next approved development step.

GitHub's `main` branch will remain the project source of truth.

Documentation changes will be completed before corresponding code or database changes whenever the change affects system architecture, requirements, permissions, workflows, or data structures.

## 20. Conclusion

ERA-IPMS is being developed as a practical digital information and project management system for Emergency Response Aid.

The system will support disability services, beneficiary management, projects, activities, poultry, small farming, finance, staff and Member management, monitoring and evaluation, dashboards, and reporting.

The new access-control architecture separates **Title**, **Permission**, and **Responsibility**.

The initial titles are:

```text
Admin
Director
Programme Coordinator
Finance
Member
```

Admin is responsible for System Administration and controls user access, titles, and permissions.

The Director provides programme oversight and M&E.

The Programme Coordinator coordinates programme and project implementation.

Finance manages sales, expenses, and authorised financial records.

Members perform assigned programme responsibilities and have access only to records and activities authorised for them.

Additional titles and responsibilities may be introduced as ERA's organisational needs evolve.

The project will continue through a documentation-first development process so that requirements, workflows, database design, backend implementation, and user interface design remain consistent throughout development.