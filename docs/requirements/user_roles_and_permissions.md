# ERA Integrated Project Management System (ERA-IPMS)

## User Roles and Permissions

### Document Information

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** User Roles and Permissions
**Version:** 1.1
**Date:** September 2026
**Prepared By:** Abdullahi Abdi Mohamed

# 1. Introduction

ERA-IPMS will be used by people with different organisational, programme, technical, financial, and operational responsibilities within Emergency Response Aid (ERA).

Because the system will contain beneficiary, disability, project, poultry, farm, financial, staff, volunteer, member, monitoring, and organisational information, users must not automatically have access to all information or functions.

ERA-IPMS will therefore use controlled authentication and authorisation based on:

1. User title.
2. Assigned permissions.
3. Assigned operational responsibilities.
4. Project or activity assignments where applicable.
5. Record-level access rules.

The system will follow the principle of least privilege. Users should receive only the access required to perform their authorised responsibilities.

# 2. Purpose

The purpose of this document is to:

* Define the initial ERA-IPMS user titles.
* Distinguish titles from permissions and responsibilities.
* Define the permission types used by the system.
* Define the initial access direction for each title.
* Define record-level access principles.
* Define responsibility-based access.
* Protect beneficiary, financial, and organisational information.
* Provide a foundation for implementing application permissions and access control.
* Support the design of authentication, database relationships, workflows, and application interfaces.

# 3. Title, Permission, and Responsibility Model

ERA-IPMS shall distinguish three related but separate concepts.

## 3.1 Title

A title identifies the user's organisational or system position.

The initial titles are:

1. **Admin**
2. **Director**
3. **Programme Coordinator**
4. **Finance**
5. **Member**

These titles are not intended to be permanent bundles of every possible permission.

Future titles may be created by an authorised Admin when organisational requirements change.

## 3.2 Permission

A permission identifies an action a user is authorised to perform.

The initial permission types are:

| Permission | Meaning                                                            |
| ---------- | ------------------------------------------------------------------ |
| View       | View authorised information                                        |
| Add        | Create authorised records                                          |
| Edit       | Modify authorised records                                          |
| Delete     | Delete records where explicitly permitted                          |
| Approve    | Approve authorised records, referrals, activities, or transactions |
| Export     | Export authorised information                                      |
| Manage     | Perform broader management functions within an authorised module   |
| Administer | Perform system-level administration                                |

Permissions shall be enforced by the application backend and shall not depend only on hiding or showing interface elements.

## 3.3 Responsibility

A responsibility identifies the programme or operational area assigned to a user.

Examples include:

* Disability services
* Beneficiary assessment
* Home visits
* Referral management
* Referral follow-up
* Community awareness
* Project coordination
* Activity implementation
* Poultry operations
* Small farm operations
* Finance
* Monitoring and evaluation
* Reporting

A Member may therefore have the **Member** title while being assigned one or more specific responsibilities.

# 4. Initial User Titles

The initial ERA-IPMS titles are:

| Title                 | Primary Responsibility                 |
| --------------------- | -------------------------------------- |
| Admin                 | System Administration                  |
| Director              | Programme Oversight and M&E            |
| Programme Coordinator | Programme and Project Coordination     |
| Finance               | Sales, Expenses, and Financial Records |
| Member                | Assigned Programme Responsibilities    |

These titles form the initial governance baseline.

They may be expanded in future versions if validated organisational requirements require additional titles.

# 5. General Access Principles

All ERA-IPMS access shall follow these principles.

## 5.1 Authentication

Users must authenticate before accessing protected system functions.

The approved authentication direction is:

* Username or email plus password.
* Strong password security requirements.
* Inactive users cannot access the system.
* Secure session management.
* Logout must invalidate the authenticated session.

## 5.2 Least Privilege

Users shall receive only the permissions required for their authorised responsibilities.

A title does not automatically provide unrestricted access to every system record.

## 5.3 Responsibility-Based Access

A user's access to programme functionality may depend on their assigned responsibility.

For example, a Member assigned to disability services may receive access to beneficiary assessment and referral functions without automatically receiving access to finance.

## 5.4 Record-Level Access

Module-level permissions alone are not sufficient.

The system shall also restrict which records a user can access.

Examples include:

* A Member may access beneficiaries they personally registered, assessed, or visited, subject to assigned permissions.
* A Member may access their own authorised operational records.
* A Member may access their own contribution totals within projects to which they are assigned.
* Users may access project or activity records according to their assignment and permissions.
* Financial records shall only be available to users authorised to access financial information.

Record-level restrictions shall be enforced by the backend.

## 5.5 Technical Access vs Programme Authority

Technical administration and programme decision-making are separate concepts.

An Admin may have technical authority to configure the system and manage users, titles, and permissions.

This does not automatically mean that the Admin has programme decision-making authority.

Programme authority shall remain subject to the permissions and governance rules assigned to the relevant users.

# 6. Title 1 - Admin

## 6.1 Purpose

The Admin title is responsible for system administration and authorised administrative functions.

The Admin is responsible for maintaining the system's user access structure and supporting the technical operation of ERA-IPMS.

## 6.2 Main Responsibilities

Admin may:

* Create user accounts.
* Update user accounts.
* Activate user accounts.
* Deactivate user accounts.
* Reset user passwords through authorised procedures.
* Assign titles.
* Create future or custom titles.
* Assign permissions to titles or users according to the approved access model.
* Assign operational responsibilities.
* Manage system-level configuration.
* Support system maintenance.
* Review audit information.
* Perform authorised project administration.
* Support system security and administration.

## 6.3 Project Authority

Admin may create, update, and manage projects where authorised by the system governance model.

Project creation is initially assigned to:

* Admin
* Director

Admin project authority does not automatically grant programme decision authority.

## 6.4 Admin Access

| Function                  | Initial Access                                       |
| ------------------------- | ---------------------------------------------------- |
| User Management           | Administer                                           |
| Title Management          | Administer                                           |
| Permission Management     | Administer                                           |
| Responsibility Assignment | Manage                                               |
| System Settings           | Administer                                           |
| Audit Log                 | View / Manage where authorised                       |
| Beneficiaries             | According to assigned administrative permission      |
| Disability Records        | According to assigned administrative permission      |
| Home Visits               | According to assigned administrative permission      |
| Referrals                 | According to assigned administrative permission      |
| Follow-Ups                | According to assigned administrative permission      |
| Projects                  | Manage                                               |
| Activities                | Manage where authorised                              |
| Poultry                   | According to assigned permission                     |
| Farm                      | According to assigned permission                     |
| Finance                   | According to assigned permission                     |
| Staff and Members         | Manage authorised administrative records             |
| Dashboard                 | Administrative and authorised management information |
| Reports                   | Generate / Export where authorised                   |

Admin shall not automatically receive unrestricted programme access simply because the user has technical administration privileges.

# 7. Title 2 - Director

## 7.1 Purpose

The Director provides programme oversight, management oversight, and monitoring and evaluation oversight.

The Director uses ERA-IPMS to review organisational performance, project progress, programme information, and management information.

## 7.2 Main Responsibilities

The Director may:

* Provide programme oversight.
* Review project performance.
* Review activity implementation.
* Review beneficiary service information.
* Review disability service information.
* Review referrals and follow-ups.
* Review poultry and farm performance.
* Review authorised financial information.
* Review management reports.
* Oversee monitoring and evaluation.
* Review project and activity continuation.
* Participate in project creation and management decisions.
* Approve records or activities where specifically authorised.

## 7.3 Director Access

| Function              | Initial Access                    |
| --------------------- | --------------------------------- |
| User Management       | No                                |
| Title Management      | No                                |
| Permission Management | No                                |
| System Settings       | No                                |
| Dashboard             | Full management view              |
| Beneficiaries         | View                              |
| Disability Records    | View                              |
| Home Visits           | View                              |
| Referrals             | View / Approve where authorised   |
| Follow-Ups            | View                              |
| Projects              | Manage / Approve where authorised |
| Activities            | View / Approve where authorised   |
| Poultry               | View                              |
| Farm                  | View                              |
| Finance               | View / Approve where authorised   |
| Staff and Members     | View                              |
| M&E                   | Oversight                         |
| Reports               | Generate                          |
| Export                | Export authorised reports         |

The Director should normally review and oversee operational information rather than directly modify routine field records unless explicitly authorised.

# 8. Title 3 - Programme Coordinator

## 8.1 Purpose

The Programme Coordinator manages programme and project coordination and supports operational implementation.

The Programme Coordinator provides day-to-day coordination of projects, activities, and related programme information.

## 8.2 Main Responsibilities

The Programme Coordinator may:

* Coordinate projects.
* Manage project information.
* Plan activities.
* Record activities.
* Monitor implementation.
* Assign activities to Members.
* Review beneficiary services.
* Review disability assessments.
* Review home visits.
* Monitor referrals.
* Monitor referral follow-ups.
* Coordinate programme activities.
* Track project progress.
* Prepare project reports.
* Review authorised poultry and farm information.
* Coordinate with Finance on authorised project information.

## 8.3 Programme Coordinator Access

| Function              | Initial Access                                |
| --------------------- | --------------------------------------------- |
| User Management       | No                                            |
| Title Management      | No                                            |
| Permission Management | No                                            |
| System Settings       | No                                            |
| Dashboard             | View                                          |
| Beneficiaries         | View / Add / Edit according to responsibility |
| Disability Records    | View / Add / Edit according to responsibility |
| Home Visits           | View / Add / Edit                             |
| Referrals             | View / Add / Edit                             |
| Follow-Ups            | View / Add / Edit                             |
| Projects              | Manage                                        |
| Activities            | Manage                                        |
| Poultry               | View                                          |
| Farm                  | View                                          |
| Finance               | View authorised project information           |
| Staff and Members     | View / Assign Activities                      |
| M&E                   | View authorised programme information         |
| Reports               | Generate                                      |
| Export                | Export authorised reports                     |

The Programme Coordinator shall not manage system users, titles, permissions, or system settings unless separately assigned an authorised administrative permission.

# 9. Title 4 - Finance

## 9.1 Purpose

The Finance title is responsible for authorised financial records.

Finance focuses on financial transactions and financial information rather than beneficiary service delivery or operational programme records.

## 9.2 Main Responsibilities

Finance may:

* Record sales.
* Record income.
* Record expenses.
* Categorise expenses.
* Record project expenses.
* Record poultry-related financial transactions.
* Record farm-related financial transactions.
* Review financial transactions.
* Maintain authorised financial records.
* Prepare financial summaries.
* Generate financial reports.
* Export authorised financial reports.

The initial finance scope is basic financial management.

It is not intended to implement full accounting functionality in the initial version.

## 9.3 Finance Access

| Function              | Initial Access                                     |
| --------------------- | -------------------------------------------------- |
| User Management       | No                                                 |
| Title Management      | No                                                 |
| Permission Management | No                                                 |
| System Settings       | No                                                 |
| Dashboard             | Financial view                                     |
| Beneficiaries         | No                                                 |
| Disability Records    | No                                                 |
| Home Visits           | No                                                 |
| Referrals             | No                                                 |
| Follow-Ups            | No                                                 |
| Projects              | View relevant project information                  |
| Activities            | View relevant information                          |
| Poultry               | View authorised financial information              |
| Farm                  | View authorised financial information              |
| Finance               | Manage                                             |
| Staff and Members     | No, unless separately authorised                   |
| M&E                   | View authorised financial summaries where required |
| Reports               | Financial reports                                  |
| Export                | Export authorised financial reports                |

Finance shall not require detailed beneficiary or disability information to perform ordinary financial responsibilities.

# 10. Title 5 - Member

## 10.1 Purpose

Member is the general operational title for users who perform assigned programme, community, field, poultry, farm, or other operational responsibilities.

Member is intentionally a general title.

Members receive their actual operational access through assigned permissions and responsibilities.

## 10.2 Possible Member Responsibilities

A Member may be assigned responsibilities such as:

* Disability services.
* Beneficiary registration.
* Disability assessment.
* Home visits.
* Referral creation.
* Referral follow-up.
* Community awareness.
* Project activities.
* Poultry operations.
* Farm operations.
* Data collection.
* Other validated programme responsibilities.

## 10.3 Member Access Principle

A Member does not automatically receive access to every programme module.

Access depends on:

1. Assigned permissions.
2. Assigned responsibilities.
3. Project assignments.
4. Activity assignments.
5. Record-level access rules.

## 10.4 Beneficiary Access

Where authorised, a Member may:

* Register beneficiaries.
* View authorised beneficiary records.
* Edit authorised beneficiary records.
* Record disability assessments.
* Record home visits.
* Create referrals.
* Submit referrals.
* Record follow-up information.
* View records connected to their authorised work.

A Member should normally access beneficiary records they personally registered, assessed, or visited, subject to the permissions and responsibility assigned to them.

## 10.5 Referral Access

Members may create and submit referrals where their responsibilities permit.

Referral approval shall be performed by an authorised person with the appropriate approval permission.

Creating a referral does not automatically give the Member approval authority.

## 10.6 Poultry and Farm Access

Members assigned poultry or farm responsibilities may maintain authorised operational records.

Examples include:

* Poultry stock.
* Poultry groups or categories.
* Egg production.
* Feed usage.
* Poultry health events.
* Poultry deaths.
* Farm activities.
* Crops.
* Harvests.
* Farm-to-poultry produce transfers.

Operational quantity records and financial transactions are separate.

Financial transactions are handled through the Finance module according to the user's authorised permissions.

## 10.7 Member Contribution Access

Members may view their own authorised contribution totals for projects to which they are assigned.

This may include information such as:

* Activities participated in.
* Activities completed.
* Beneficiary-related contributions.
* Other authorised project contribution measures.

A Member shall not automatically receive access to another Member's private contribution information.

## 10.8 Member Access Summary

| Function              | Initial Access                                |
| --------------------- | --------------------------------------------- |
| User Management       | No                                            |
| Title Management      | No                                            |
| Permission Management | No                                            |
| System Settings       | No                                            |
| Dashboard             | Limited authorised view                       |
| Beneficiaries         | Responsibility-based                          |
| Disability Records    | Responsibility-based                          |
| Home Visits           | Responsibility-based                          |
| Referrals             | Add / View / Edit according to responsibility |
| Follow-Ups            | Responsibility-based                          |
| Projects              | View assigned projects                        |
| Activities            | View / Update assigned activities             |
| Poultry               | Responsibility-based                          |
| Farm                  | Responsibility-based                          |
| Finance               | No, unless separately authorised              |
| Staff and Members     | No, unless separately authorised              |
| M&E                   | Limited authorised operational information    |
| Reports               | Limited authorised reports                    |
| Export                | Only where explicitly authorised              |

# 11. Future and Custom Titles

The system shall support future titles.

An Admin may create a new title when there is a validated organisational requirement.

A future title should be configured by assigning:

1. Title name.
2. Permissions.
3. Operational responsibilities.
4. Project or activity scope where applicable.
5. Record-level access rules.

Examples of possible future titles may include specialised programme, technical, monitoring, or operational positions.

These examples do not form part of the initial five-title baseline unless formally approved.

# 12. Permission Matrix

The following matrix represents the initial access direction.

| Module / Function         | Admin             | Director                        | Programme Coordinator       | Finance                       | Member                           |
| ------------------------- | ----------------- | ------------------------------- | --------------------------- | ----------------------------- | -------------------------------- |
| User Management           | Administer        | No                              | No                          | No                            | No                               |
| Title Management          | Administer        | No                              | No                          | No                            | No                               |
| Permission Management     | Administer        | No                              | No                          | No                            | No                               |
| Responsibility Assignment | Manage            | No                              | No                          | No                            | No                               |
| System Settings           | Administer        | No                              | No                          | No                            | No                               |
| Audit Log                 | Authorised        | View                            | View authorised             | View authorised               | Own/authorised events            |
| Dashboard                 | Admin             | Full View                       | View                        | Financial View                | Limited View                     |
| Beneficiaries             | Authorised        | View                            | View/Add/Edit               | No                            | Responsibility-based             |
| Disability Records        | Authorised        | View                            | View/Add/Edit               | No                            | Responsibility-based             |
| Home Visits               | Authorised        | View                            | View/Add/Edit               | No                            | Responsibility-based             |
| Referrals                 | Authorised        | View/Approve where authorised   | View/Add/Edit               | No                            | Add/View/Edit where authorised   |
| Follow-Ups                | Authorised        | View                            | View/Add/Edit               | No                            | Responsibility-based             |
| Projects                  | Manage            | Manage/Approve where authorised | Manage                      | View relevant                 | Assigned projects                |
| Activities                | Manage            | View/Approve                    | Manage                      | View relevant                 | Assigned activities              |
| Poultry                   | Authorised        | View                            | View                        | Financial view                | Responsibility-based             |
| Farm                      | Authorised        | View                            | View                        | Financial view                | Responsibility-based             |
| Finance                   | Authorised        | View/Approve where authorised   | View authorised information | Manage                        | No unless separately authorised  |
| Staff/Members             | Manage authorised | View                            | View/Assign Activities      | No                            | No unless separately authorised  |
| M&E                       | Authorised        | Oversight                       | Programme view              | Financial view where required | Assigned operational information |
| Reports                   | Manage            | Generate                        | Generate                    | Financial Reports             | Limited authorised reports       |
| Export                    | Authorised        | Authorised                      | Authorised                  | Authorised financial          | Only explicitly authorised       |

The matrix represents the baseline direction. Detailed permissions may be assigned more precisely during implementation.

## 12.1 Title-Level Permission Baseline for Implementation

The following baseline defines the initial title-level permissions to be represented in the `title_permissions` table.

Title-level permissions define the types of operations a title may perform. They do not by themselves grant unrestricted access to all records.

| Permission | Admin | Director | Programme Coordinator | Finance | Member |
| ---------- | :---: | :------: | :-------------------: | :-----: | :----: |
| View       | ✓ | ✓ | ✓ | ✓ | ✓ |
| Add        | ✓ | — | ✓ | ✓ | ✓* |
| Edit       | ✓ | — | ✓ | ✓ | ✓* |
| Delete     | ✓ | — | — | — | — |
| Approve    | ✓ | ✓ | — | — | — |
| Export     | ✓ | ✓ | ✓ | ✓ | — |
| Manage     | ✓ | ✓ | ✓ | ✓ | — |
| Administer | ✓ | — | — | — | — |

`*` Member Add/Edit permissions are subject to assigned operational responsibilities and record-level authorization.

### 12.1.1 Authorization Interpretation

The title-level baseline shall be combined with:

1. Assigned operational responsibility.
2. Project assignment.
3. Activity assignment where applicable.
4. User-created, user-assessed, or user-visited record relationships where applicable.
5. Record-level authorization rules.
6. Separate approval authority where required.

A title-level permission must not be interpreted as unrestricted access to every record in a module.

### 12.1.2 Administrative Authority

`Administer` is restricted to the Admin title in the initial baseline.

Administrative authority does not automatically grant programme decision-making authority. Programme governance and approval responsibilities remain governed by the Director and other explicitly authorised users.

### 12.1.3 Approval Authority

`Approve` is separate from `Add` and `Edit`.

The initial baseline grants title-level approval permission to Director. Specific approval workflows may impose additional record, project, programme, or responsibility-level restrictions.

### 12.1.4 Member Authorization

Member is a general operational title.

Member access shall primarily be determined by assigned responsibilities and applicable project/activity assignments. Member users do not receive Delete, Approve, Export, Manage, or Administer permissions in the initial baseline.

### 12.1.5 Implementation Boundary

This baseline is the authorization foundation for the initial `title_permissions` seed.

It does not replace record-level authorization logic and does not by itself determine access to beneficiary, disability, financial, poultry, farm, project, activity, or other operational records.

## 12.2 Responsibility Baseline for Implementation

The following responsibilities define the initial operational areas that may be assigned to users.

Responsibilities determine the operational scope of a user's access. They do not independently grant permissions. Access shall be determined by the combination of title-level permissions, assigned responsibilities, project/activity assignments, and record-level authorization rules.

| Responsibility Code | Responsibility Name |
| -------------------- | ------------------- |
| `DISABILITY_SERVICES` | Disability Services |
| `BENEFICIARY_REGISTRATION` | Beneficiary Registration |
| `DISABILITY_ASSESSMENT` | Disability Assessment |
| `HOME_VISITS` | Home Visits |
| `REFERRALS_FOLLOW_UP` | Referrals and Follow-Up |
| `COMMUNITY_AWARENESS` | Community Awareness |
| `PROJECT_ACTIVITIES` | Project Activities |
| `POULTRY_OPERATIONS` | Poultry Operations |
| `FARM_OPERATIONS` | Farm Operations |
| `PROJECT_COORDINATION` | Project Coordination |
| `FINANCIAL_OPERATIONS` | Financial Operations |
| `MONITORING_EVALUATION` | Monitoring and Evaluation |

### 12.2.1 Responsibility Interpretation

A responsibility identifies an operational area in which a user may be authorised to work.

A responsibility does not automatically grant View, Add, Edit, Delete, Approve, Export, Manage, or Administer permissions.

The applicable title-level permission must exist before a responsibility can contribute to authorisation.

### 12.2.2 Responsibility and Record-Level Access

Responsibility assignments shall be combined with applicable project, activity, and record-level authorization rules.

For example, a user assigned `POULTRY_OPERATIONS` may work with authorised poultry records only when the user's title permissions and applicable project or record-level rules also permit the requested operation.

### 12.2.3 Initial Responsibility Scope

The initial responsibility baseline covers:

- Disability and beneficiary services.
- Beneficiary registration.
- Disability assessment.
- Home visits.
- Referrals and follow-up.
- Community awareness.
- Project and activity operations.
- Poultry operations.
- Farm operations.
- Project coordination.
- Financial operations.
- Monitoring and evaluation.

Additional responsibilities may be introduced when validated operational requirements require them.

### 12.2.4 Reporting Boundary

Reporting is not initially defined as a standalone responsibility.

Reporting access shall be controlled through the applicable operational responsibility, title-level permissions, and record-level authorization. Export access remains separately controlled through the `EXPORT` permission.

## 12.3 Title-to-Responsibility Eligibility Baseline

The following baseline defines which operational responsibilities may be assigned to users based on their title.

This is an eligibility baseline, not an automatic assignment rule. A user's title does not automatically assign all responsibilities listed for that title.

| Responsibility | Admin | Director | Programme Coordinator | Finance | Member |
| -------------- | :---: | :------: | :-------------------: | :-----: | :----: |
| Disability Services | — | ✓ | ✓ | — | ✓ |
| Beneficiary Registration | — | ✓ | ✓ | — | ✓ |
| Disability Assessment | — | ✓ | ✓ | — | ✓ |
| Home Visits | — | ✓ | ✓ | — | ✓ |
| Referrals and Follow-Up | — | ✓ | ✓ | — | ✓ |
| Community Awareness | — | ✓ | ✓ | — | ✓ |
| Project Activities | — | ✓ | ✓ | — | ✓ |
| Poultry Operations | — | ✓ | ✓ | — | ✓ |
| Farm Operations | — | ✓ | ✓ | — | ✓ |
| Project Coordination | — | ✓ | ✓ | — | — |
| Financial Operations | — | ✓ | ✓ | ✓ | — |
| Monitoring and Evaluation | — | ✓ | ✓ | ✓ | ✓ |

### 12.3.1 Eligibility Interpretation

The table defines the initial responsibility areas that may be assigned to users holding the corresponding title.

Eligibility does not automatically create a responsibility assignment.

Actual user responsibility assignments shall be made according to the user's operational duties and least-privilege requirements.

### 12.3.2 Administrative Title

The Admin title does not automatically receive operational responsibilities.

Administrative authority is provided through the applicable title-level permissions, including `ADMINISTER`, and does not automatically create programme or operational responsibility.

### 12.3.3 Director and Programme Coordinator

Director and Programme Coordinator users may be assigned broad operational responsibilities where required by their programme or coordination duties.

Specific assignments shall remain subject to organisational requirements and least-privilege principles.

### 12.3.4 Finance

Finance users may be assigned `FINANCIAL_OPERATIONS` and, where required, `MONITORING_EVALUATION`.

Financial responsibility does not automatically provide access to beneficiary, disability, home visit, referral, poultry, or farm operational records.

### 12.3.5 Member

Member users shall normally receive only the operational responsibilities required for their assigned duties.

A Member title does not automatically grant every Member-eligible responsibility.

### 12.3.6 Assignment Boundary

Responsibility assignment shall remain separate from:

1. Title assignment.
2. Title-level permission assignment.
3. Project assignment.
4. Activity assignment.
5. Record-level authorization.

All applicable authorization conditions must be satisfied before an operation is permitted.

## 12.4 User Responsibility Assignment Rules

User responsibilities shall be assigned explicitly according to the user's operational duties and least-privilege requirements.

A responsibility shall not be inferred solely from the user's title.

### 12.4.1 Multiple Responsibilities

A user may have multiple active responsibilities where required by their authorised duties.

Each responsibility shall be independently recorded in the `user_responsibilities` table.

### 12.4.2 Assignment Authority

Responsibility assignments shall be performed only by users with the appropriate administrative or management authority.

The `assigned_by` field shall identify the user who performed the assignment where applicable.

### 12.4.3 Responsibility Eligibility

A responsibility may be assigned only where it is compatible with the user's title-level authorization baseline and the user's actual operational duties.

An assignment must not be used to bypass title-level permission restrictions.

### 12.4.4 Activation and Deactivation

Responsibility assignments shall support activation and deactivation through the `is_active` field.

Deactivating a responsibility shall remove it from the user's active operational authorization without requiring historical assignment data to be physically deleted.

### 12.4.5 Least-Privilege Assignment

Users shall receive only the responsibilities necessary for their authorised duties.

New responsibility assignments shall not automatically grant project-wide or system-wide access.

### 12.4.6 Project and Activity Scope

Where applicable, responsibility assignments shall be combined with project and activity assignments.

A user having an active responsibility does not by itself grant access to every project, activity, or record associated with that responsibility.

### 12.4.7 Administrative Boundary

The Admin title provides system-level administrative permissions but does not automatically create programme responsibilities.

Administrative users may manage responsibility assignments where authorised, while operational responsibility remains separately assigned.

### 12.4.8 Auditability

Responsibility assignment and deactivation shall remain auditable.

Historical assignment information shall be preserved where required for accountability and audit purposes.

# 13. Record-Level Access Rules

Record-level access is a mandatory part of the access-control design.

## 13.1 Beneficiary Records

Beneficiary information may contain personal and sensitive information.

Access shall therefore consider:

* User permissions.
* Assigned responsibility.
* User-created records.
* User-assessed records.
* User-visited records.
* Project assignment.
* Programme assignment.

A user with general beneficiary View permission does not necessarily have access to every beneficiary record.

## 13.2 Project Records

Project access may depend on:

* User title.
* Project assignment.
* Permission.
* Responsibility.

Admin and Director are initially authorised for project creation.

Programme Coordinators manage projects and activities within their authorised programme scope.

Members generally access projects and activities to which they are assigned.

## 13.3 Financial Records

Financial information shall be restricted to authorised users.

Finance has primary financial management responsibility.

Director may review or approve authorised financial information where required.

Programme Coordinator may view authorised project financial information required for programme coordination.

Members do not receive financial access by default.

## 13.4 Poultry and Farm Records

Operational poultry and farm information may be accessed according to assigned responsibilities.

Members assigned operational responsibilities may create and update relevant records.

Programme Coordinator and Director may review authorised operational information.

Finance handles the financial side of poultry and farm transactions.

# 14. Approval Rules

Approval is a separate permission from Add or Edit.

A user who creates a record does not automatically have permission to approve it.

Examples:

* A Member may create and submit a referral.
* An authorised person may approve the referral.
* A user may record an activity without automatically being authorised to approve it.
* Financial approval shall require explicit authorisation.
* Project and activity approval shall follow the assigned governance permissions.

Approval workflows will be defined in greater detail in the System Workflows document.

# 15. Delete and Archive Rules

Delete permission shall not imply that every record may be physically deleted.

In particular:

* Beneficiary records should normally be archived or made inactive rather than physically deleted.
* Important operational and financial records should have appropriate retention and audit considerations.
* Delete permissions shall be assigned only where justified by the record type and workflow.

The detailed database behaviour for deletion, archiving, and record retention will be defined during database design.

# 16. Audit and Accountability

Important system actions should be recorded in the audit log.

Audit information should include, where applicable:

* User who performed the action.
* Action performed.
* Record affected.
* Date and time.
* Previous value where appropriate.
* New value where appropriate.
* Relevant project or module context.

The audit trail supports accountability and helps identify unauthorised or incorrect changes.

# 17. Confidentiality and Data Protection

ERA-IPMS may contain personal, beneficiary, disability, financial, and organisational information.

The system shall therefore follow these principles:

* Authentication is required for protected functions.
* Access is permission-controlled.
* Record-level restrictions are enforced.
* Passwords are never stored in plain text.
* Real beneficiary information must not be used in development or testing.
* Fictional or anonymised data should be used during development and testing.
* Credentials and secrets must not be committed to the public repository.
* Confidential organisational information must not be publicly published.
* Audit information should be retained for important system actions.

# 18. Relationship to Other Documents

This document shall remain consistent with:

* Project Concept Note.
* README.
* Needs Assessment.
* Stakeholder Analysis.
* Software Requirements Specification.
* System Workflows.
* Database Entity Design.
* ERD documentation.
* Database schema.

If a conflict is identified between documents, the conflict shall be documented and resolved before implementation rather than silently resolved in code.

# 19. Implementation Guidance

The access-control implementation should follow this conceptual model:

```text
User
  ↓
Title
  ↓
Permissions
  ↓
Responsibilities
  ↓
Project / Activity Assignment
  ↓
Record-Level Access
  ↓
Allowed Actions
```

For example:

```text
Member
  ↓
Disability Services Responsibility
  ↓
Beneficiary + Assessment + Referral Permissions
  ↓
Assigned Programme / Project
  ↓
Authorised Beneficiary Records
  ↓
Register / View / Edit / Submit Referral
```

Another example:

```text
Finance
  ↓
Finance Permissions
  ↓
Authorised Financial Records
  ↓
Project / Poultry / Farm Transactions
  ↓
View / Add / Edit / Manage / Report
```

# 20. Initial Governance Summary

The initial governance model is:

### Admin

System administration, user management, title and permission management, responsibility assignment, system configuration, and authorised project administration.

### Director

Programme oversight, M&E oversight, management review, and authority relating to project and activity continuation.

### Programme Coordinator

Programme and project coordination, activity management, implementation monitoring, and operational oversight.

### Finance

Sales, income, expenses, financial records, and authorised financial reporting.

### Member

Assigned programme responsibilities and operational records within authorised scope.

The model intentionally avoids creating a separate fixed system title for every operational function.

# 21. Future Permission Expansion

The permission framework may later be expanded with more granular permissions if validated requirements require them.

Possible future permissions may include:

* View own records.
* View assigned records.
* View project records.
* Add own records.
* Edit own records.
* Approve.
* Reject.
* Submit.
* Assign.
* Archive.
* Restore.
* Import.
* Export.
* Manage.
* Administer.

Such permissions should be introduced through documented change control.

# 22. Conclusion

ERA-IPMS will initially use five user titles:

1. **Admin**
2. **Director**
3. **Programme Coordinator**
4. **Finance**
5. **Member**

These titles are separate from permissions and responsibilities.

The system will use least-privilege access, responsibility-based access, project and activity assignment, and record-level access controls.

Admin will manage the system's access structure and authorised administrative functions. Director will provide programme and M&E oversight. Programme Coordinator will manage programme and project operations. Finance will manage authorised financial information. Members will perform assigned operational responsibilities.

The model is designed to support future organisational growth without requiring a complete redesign of the permission system.

This document provides the approved baseline for the next documentation stage: **System Workflows**.
