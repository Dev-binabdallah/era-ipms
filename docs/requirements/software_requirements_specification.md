# ERA Integrated Project Management System (ERA-IPMS)

## Software Requirements Specification (SRS)

### Document Information

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** Software Requirements Specification
**Version:** 1.1
**Date:** September 2026
**Status:** Documentation Baseline
**Prepared By:** Abdullahi Abdi Mohamed

---

# 1. Introduction

## 1.1 Purpose

The ERA Integrated Project Management System (ERA-IPMS) is a web-based information management system for Emergency Response Aid (ERA).

The system is intended to move important organisational records from mainly manual and paper-based processes toward structured digital information management.

ERA-IPMS will provide authorised users with a central system for recording, managing, searching, monitoring, and reporting organisational information.

The system will initially support:

* User authentication and access control
* Beneficiary management
* Disability services
* Home visits
* Referrals and follow-ups
* Projects and activities
* Poultry operations
* Small-scale farming
* Basic financial management
* Staff and volunteer information
* Monitoring and evaluation
* Dashboards
* Basic reporting

## 1.2 Relationship to Other Project Documents

This SRS is derived from and must remain consistent with the approved project documentation baseline, including:

* Project Concept Note
* README
* Needs Assessment
* Stakeholder Analysis
* User Roles and Permissions
* System Workflows
* Database Entity Design
* ERD documentation

Where a later approved requirements document provides more detailed rules, the detailed document shall be used to define implementation behaviour.

Changes to approved requirements must be documented and reviewed before implementation.

# 2. Background

ERA is a community-based organisation working in areas including disability services, community advocacy and awareness, poultry farming, and small-scale agriculture.

Its activities include:

* Disability assessments
* Home visits
* Referrals
* Referral follow-ups
* Advocacy
* Awareness activities
* Capacity building
* Poultry operations
* Small-scale farming
* Project and community activities

ERA-IPMS is intended to improve the management of information generated through these activities.

# 3. Problem Statement

The current information-management environment creates challenges including:

* Difficulty locating historical beneficiary information
* Risk of loss or damage to paper records
* Duplicate records
* Time-consuming report preparation
* Difficulty determining beneficiaries served
* Difficulty tracking referrals and follow-ups
* Difficulty monitoring poultry numbers
* Difficulty monitoring egg production
* Limited structured feed records
* Difficulty monitoring poultry illness and deaths
* Limited structured farm records
* Difficulty consolidating farm expenses
* Difficulty consolidating project and organisational information
* Difficulty producing reliable management and project reports

ERA-IPMS shall address these problems through structured digital information management.

# 4. System Objectives

ERA-IPMS shall aim to:

1. Digitise important ERA records.
2. Centralise organisational and project information.
3. Improve beneficiary information management.
4. Improve disability-service tracking.
5. Improve home-visit tracking.
6. Improve referral and follow-up tracking.
7. Improve poultry monitoring.
8. Introduce structured farm records.
9. Improve basic financial record management.
10. Improve project and activity monitoring.
11. Provide useful management dashboards.
12. Improve report preparation.
13. Improve information retrieval.
14. Support evidence-based organisational decision-making.
15. Protect beneficiary and organisational information through controlled access.

# 5. System Scope

## 5.1 Initial Scope

The initial ERA-IPMS shall include:

* Authentication
* User management
* Dynamic titles and permissions
* Record-level access control
* Beneficiary management
* Disability assessment
* Home visits
* Referrals
* Referral follow-ups
* Project management
* Activity management
* Poultry management
* Small farm management
* Basic finance management
* Staff and volunteer records
* Dashboard
* Monitoring and evaluation information
* Basic reports
* Search and filtering
* Audit information for important system actions

## 5.2 Future Scope

The following capabilities may be considered after the initial implementation:

* PDF report exports
* Excel report exports
* Mobile application
* Offline data collection
* SMS notifications
* WhatsApp notifications
* Advanced M&E functionality
* KoboToolbox integration
* Excel import
* External partner access
* Multi-organisation support
* SaaS functionality

These features are not required for the initial MVP unless separately approved.

# 6. User and Access Model

## 6.1 Initial System Titles

ERA-IPMS shall initially support five approved titles:

1. **Admin**
2. **Director**
3. **Programme Coordinator**
4. **Finance**
5. **Member**

The title model is intentionally limited to these initial titles.

Administrators may create additional titles in the future where organisational requirements justify them.

## 6.2 Title, Permission, and Responsibility

ERA-IPMS shall distinguish between three separate concepts.

### Title

A title identifies a user's organisational or system position.

Examples:

* Admin
* Director
* Programme Coordinator
* Finance
* Member

### Permission

A permission defines an operation a user may perform.

Examples:

* View
* Add
* Edit
* Delete
* Approve
* Export
* Manage
* Administer

### Responsibility

A responsibility defines the operational area in which a user works.

Examples:

* Disability services
* Beneficiary registration
* Home visits
* Referrals
* Follow-ups
* Project coordination
* Poultry
* Farm
* Monitoring and evaluation
* Community awareness

Responsibilities shall not automatically become separate system titles.

## 6.3 Dynamic Titles

The system shall allow authorised administrators to:

* Create titles
* Modify titles
* Assign permissions to titles
* Remove permissions from titles
* Assign titles to users
* Change a user's title where authorised

The initial five titles remain the baseline titles.

## 6.4 Record-Level Access

Access shall not depend only on the user's title.

Where required, the system shall apply record-level restrictions so that users only access records for which they have appropriate authority.

For example, a Member may be restricted to records that the Member personally registered, assessed, visited, or otherwise created, according to the approved permission and responsibility rules.

## 6.5 Technical and Programme Authority

System administration authority shall not automatically grant programme decision-making authority.

The Admin title is primarily responsible for system administration and authorised system-level management.

Programme decisions remain subject to the appropriate organisational authority.

# 7. Functional Requirements

## FR-001: Authentication

The system shall:

* Allow authorised users to log in.
* Accept username or email with password.
* Reject invalid credentials.
* Prevent inactive users from accessing the system.
* Allow authenticated users to log out.
* Maintain authenticated sessions securely.

## FR-002: User Management

Authorised Admin users shall be able to:

* Create user accounts.
* Update user accounts.
* Activate user accounts.
* Deactivate user accounts.
* Assign titles.
* Change titles.
* Reset user passwords.
* Manage authorised user access.

The system shall not require the creation of a separate system role for every operational responsibility.

## FR-003: Permission Management

Authorised administrators shall be able to assign permissions to titles.

Permissions shall support operations such as:

* View
* Add
* Edit
* Delete
* Approve
* Export
* Manage
* Administer

The final permission matrix shall be documented in the User Roles and Permissions document.

## FR-004: Record-Level Authorisation

The system shall enforce record-level access where required.

A user may have permission to access a module while still being restricted from records outside the user's authorised scope.

Access restrictions shall be enforced by the backend and shall not rely only on hiding interface elements.

## FR-005: Audit Information

The system shall maintain audit information for important actions where required.

Audit information may include:

* User
* Action
* Record affected
* Date and time
* Relevant change information

Audit requirements shall be refined during database and workflow design.

# 8. Beneficiary Management

## FR-006: Beneficiary Registration

Authorised users shall be able to register beneficiaries.

The system may capture:

* Beneficiary identifier
* Name
* Age or date of birth where appropriate
* Sex
* Location
* Contact information where appropriate
* Disability information where applicable
* Registration date
* Service needs
* Relevant organisational information

Only necessary information shall be collected.

## FR-007: Beneficiary Search

Authorised users shall be able to search beneficiaries.

Search criteria may include:

* Beneficiary identifier
* Name
* Location
* Service status
* Other authorised fields

## FR-008: Beneficiary Update

Authorised users with appropriate permission shall be able to update beneficiary information.

Important changes should retain appropriate audit information.

## FR-009: Beneficiary Archiving

Beneficiary records shall not normally be physically deleted where doing so would compromise organisational history or reporting.

The system shall support an inactive or archived status where appropriate.

The final archive rules shall be defined during workflow and database design.

# 9. Disability Services

## FR-010: Disability Assessment

Authorised users with the appropriate disability-service responsibility shall be able to record disability assessments.

Assessment information shall capture relevant needs and service information.

## FR-011: Home Visits

Authorised users shall be able to record home visits.

A home-visit record may include:

* Beneficiary
* Visit date
* Person conducting the visit
* Purpose
* Observations
* Support provided
* Follow-up required
* Next action

## FR-012: Disability Service Tracking

The system shall allow authorised users to review relevant disability-service records according to their permissions and record-level access.

# 10. Referral Management

## FR-013: Referral Creation

Authorised users shall be able to create referral records.

A referral may include:

* Beneficiary
* Referral date
* Referral destination or service
* Reason
* Person making the referral
* Referral status

## FR-014: Referral Submission and Approval

Where approval is required:

* An authorised Member may create and submit a referral.
* An authorised person shall review and approve the referral.
* The system shall record the relevant status and action.

The exact approval authority shall be defined in the User Roles and Permissions and System Workflows documents.

## FR-015: Referral Status

The system shall support appropriate referral statuses, including:

* Pending
* Submitted
* Approved
* Follow-up required
* Completed
* Not completed
* Cancelled

Final status transitions shall be defined in the workflow documentation.

## FR-016: Referral Follow-Up

Authorised users shall be able to record referral follow-ups.

A follow-up may include:

* Follow-up date
* Person conducting follow-up
* Outcome
* Service received
* Remaining needs
* Next action

# 11. Project Management

## FR-017: Project Registration

Authorised Admin and Director users shall be able to create projects according to the approved governance model.

Project information may include:

* Project name
* Description
* Objectives
* Start date
* End date
* Status
* Responsible person
* Other approved project information

## FR-018: Project Management

Authorised users shall be able to manage project information according to their permissions.

The system shall support project status and project-level information.

## FR-019: Activity Management

Authorised users shall be able to record project and organisational activities.

Activity information may include:

* Activity name
* Project
* Date
* Location
* Responsible person
* Participants
* Description
* Status
* Results or outcomes

## FR-020: Activity Status

The system shall support appropriate activity statuses, such as:

* Planned
* Ongoing
* Completed
* Pending
* Cancelled

## FR-021: Activity Assignment

Authorised users shall be able to assign activities or responsibilities to users where permitted.

Members shall be able to see activities relevant to their assigned responsibilities and access rights.

# 12. Poultry Management

## FR-022: Poultry Groups and Categories

The system shall support poultry categories or groups to allow operational records to be organised appropriately.

The exact category structure shall be finalised during database design.

## FR-023: Poultry Records

Authorised users with poultry responsibilities shall be able to record:

* Poultry groups
* Poultry type
* Purchases
* Current quantities
* Production
* Feed
* Health information
* Deaths
* Sales
* Other authorised poultry activities

## FR-024: Poultry Quantity Tracking

The system shall maintain accurate poultry quantity changes.

Quantity changes may result from:

* Opening stock
* Purchases
* New production where applicable
* Deaths
* Sales
* Other approved movements

The system shall support calculation or reconciliation of current quantities from recorded movements.

## FR-025: Egg Production

Authorised users shall be able to record egg production.

Records may include:

* Date
* Number produced
* Number used
* Number sold
* Remaining quantity

## FR-026: Feed Management

The system shall support feed records including:

* Feed purchased
* Feed received from the farm
* Feed used
* Feed quantity
* Feed cost where applicable

## FR-027: Farm-to-Poultry Feed Transfer

Where farm produce is used to support poultry operations, the system shall support recording the transfer of farm produce to poultry feed.

The transfer should identify relevant quantities and dates.

## FR-028: Poultry Health

Authorised users shall be able to record:

* Illness
* Date identified
* Number affected
* Action taken
* Outcome

Poultry deaths shall also be recorded.

## FR-029: Poultry Sales

Authorised users with appropriate permissions shall be able to record poultry sales.

Financial details shall be accessible according to Finance permissions.

# 13. Small Farm Management

## FR-030: Crop Management

Authorised users with farm responsibilities shall be able to record crops grown by ERA.

Initial crops may include:

* Bananas
* Natural or local vegetables
* Sukuma wiki

The crop list shall remain configurable where appropriate.

## FR-031: Farm Activities

Authorised users shall be able to record farm activities such as:

* Planting
* Watering
* Weeding
* Harvesting
* Other approved activities

## FR-032: Harvest Records

Authorised users shall be able to record harvests.

A harvest record may include:

* Crop
* Date
* Quantity
* Unit
* Intended or actual use

Produce use may include:

* Used for poultry
* Used by ERA
* Sold
* Other authorised use

## FR-033: Farm-to-Poultry Transfer

The system shall allow farm produce used for poultry support to be recorded as a transfer to poultry operations.

This information shall support operational tracking and future reporting.

## FR-034: Farm Expenses

Authorised users shall be able to record farm-related expenses where permitted.

Examples include:

* Seeds
* Tools
* Farm inputs
* Transport
* Other approved farm expenses

# 14. Basic Finance Management

## FR-035: Expense Recording

Authorised Finance users shall be able to record organisational and project expenses.

Expense information may include:

* Date
* Amount
* Category
* Description
* Project where applicable
* Payment method where appropriate
* Responsible person
* Supporting reference where applicable

## FR-036: Expense Categories

The system shall support appropriate expense categories, including:

* Project expenses
* Poultry expenses
* Farm expenses
* Office expenses
* Transport
* Equipment
* Other authorised expenses

## FR-037: Income and Sales

The system shall support basic recording of relevant income and sales, including where applicable:

* Poultry sales
* Egg sales
* Farm produce sales
* Other authorised project or organisational income

This requirement is for basic financial management and reporting.

ERA-IPMS shall not initially implement full accounting functionality.

## FR-038: Financial Access

Finance users shall have access to authorised financial records.

Operational users may record operational quantities such as poultry or farm production while financial information remains subject to Finance permissions.

# 15. Staff and Volunteer Management

## FR-039: Staff Records

Authorised users shall be able to maintain staff information according to their permissions.

## FR-040: Volunteer Records

Authorised users shall be able to maintain volunteer information according to their permissions.

Records may include:

* Name
* Organisational title
* Contact information
* Start date
* Status
* Assigned responsibilities

Operational responsibility shall not automatically create a new system title.

# 16. Dashboard

## FR-041: Dashboard

The system shall provide dashboards appropriate to the user's permissions.

Management-level dashboards may include indicators such as:

* Beneficiaries
* Home visits
* Referrals
* Referral follow-ups
* Poultry quantities
* Egg production
* Feed
* Poultry illness and deaths
* Farm crops
* Harvests
* Farm expenses
* Organisational expenses
* Project expenses
* Project activities
* Staff and Members
* Upcoming activities
* Pending activities

Users shall only see information they are authorised to access.

# 17. Monitoring and Evaluation

## FR-042: Indicator Monitoring

The system shall support selected organisational and project indicators.

Initial indicators may include:

* Number of beneficiaries served
* Number of home visits
* Number of referrals
* Number of completed referrals
* Number of activities
* Poultry production
* Farm production

Advanced M&E functionality is considered future scope unless separately approved.

# 18. Reporting

## FR-043: Basic Report Generation

Authorised users shall be able to generate basic reports according to their permissions.

Initial reports may include:

* Beneficiary report
* Disability service report
* Home visit report
* Referral report
* Project activity report
* Poultry report
* Egg production report
* Farm report
* Expense report
* Management summary report

Reports shall respect record-level access restrictions.

## FR-044: Report Filtering

Authorised reports should support appropriate filtering, including:

* Date
* Project
* Beneficiary
* Activity
* Status
* Crop
* Poultry group or record
* Expense category

Advanced PDF and Excel export functionality is future scope unless separately approved.

# 19. Search and Filtering

## FR-045: Search

The system shall provide search functionality for authorised records.

Search results shall respect the user's permissions and record-level access.

## FR-046: Filtering

Authorised users shall be able to filter records using relevant criteria.

# 20. Notifications and Alerts

The initial MVP shall not require external SMS, WhatsApp, or similar notification services.

The system may provide basic internal status information for items requiring attention, such as:

* Pending referrals
* Follow-ups
* Pending activities
* Other approved operational items

External notifications remain future scope.

# 21. Non-Functional Requirements

## NFR-001: Usability

The system shall provide a simple and understandable interface.

The interface should support users with different levels of technical experience.

## NFR-002: Performance

The system should provide reasonable response times under expected initial organisational usage.

Performance requirements shall be refined after realistic usage and infrastructure requirements are established.

## NFR-003: Security

The system shall:

* Require authentication for protected functions.
* Enforce authorisation on the backend.
* Apply title and permission controls.
* Apply record-level access where required.
* Avoid storing passwords in plain text.
* Restrict unauthorised access.
* Protect session information.
* Apply appropriate security controls to sensitive information.

## NFR-004: Data Protection

Beneficiary and organisational information shall be protected against:

* Unauthorised access
* Unauthorised modification
* Unauthorised disclosure
* Accidental loss

Production information shall not be committed to the public GitHub repository.

## NFR-005: Auditability

Important system actions should be traceable to an authorised user where required.

## NFR-006: Reliability

The system should minimise data loss.

Database backup procedures shall be established before production deployment.

## NFR-007: Maintainability

The system shall use:

* Logical application structure
* Consistent naming
* Clear documentation
* Maintainable code
* Controlled configuration

## NFR-008: Scalability

The system should allow additional users, responsibilities, titles, and modules to be introduced without requiring a complete redesign.

## NFR-009: Browser Compatibility

The initial system shall operate through supported modern web browsers on computers and other supported devices.

## NFR-010: Accessibility and Readability

The user interface should use clear labels, readable text, sufficient contrast, understandable forms, and consistent navigation.

Accessibility requirements shall be refined during interface design and testing.

# 22. Technology Requirements

## 22.1 Frontend

The initial frontend shall use:

* HTML
* CSS
* JavaScript

## 22.2 Backend

The backend shall use:

* Python
* Django

## 22.3 Database

The project shall use:

* MariaDB/MySQL

The existing ERA-IPMS database design shall remain authoritative during the current documentation and architecture phase.

## 22.4 Version Control

The project shall use:

* Git
* GitHub

## 22.5 Development Environment

VS Code shall be the primary development environment.

The integrated terminal shall be used for development commands where appropriate, including Django, Git, database, testing, and environment-management commands.

# 23. Data Requirements

The system will require structured information for areas including:

### Identity and Access

* Users
* Titles
* Permissions
* User-title assignments
* Responsibility assignments
* Audit records

### Beneficiary and Disability Services

* Beneficiaries
* Disability assessments
* Home visits
* Referrals
* Referral follow-ups

### Projects

* Projects
* Activities
* Activity assignments
* Project-related information

### Poultry

* Poultry groups
* Poultry movements
* Poultry purchases
* Egg production
* Feed records
* Farm-to-poultry transfers
* Poultry health records
* Poultry deaths
* Poultry sales

### Farm

* Crops
* Farm activities
* Harvests
* Produce transfers
* Farm expenses

### Finance

* Expenses
* Expense categories
* Sales
* Income
* Financial references

### Human Resources

* Staff information
* Volunteer information
* Assigned responsibilities

The exact database entities, relationships, fields, constraints, indexes, and lifecycle rules shall be defined in the Database Entity Design and ERD documentation.

# 24. System Constraints

The initial project has the following constraints:

1. The system is initially developed for ERA.
2. The initial application is web-based.
3. Development uses Python, Django, MariaDB/MySQL, HTML, CSS, and JavaScript.
4. Initial testing shall use fictional, synthetic, or approved test data.
5. The MVP shall focus on essential functionality.
6. Internet availability may affect access to the web-based system.
7. Advanced mobile and external integration features are outside the initial MVP.
8. Production beneficiary information shall not be used during ordinary development or testing.
9. Existing database requirements must be reviewed before implementation changes are introduced.

# 25. Assumptions

The project assumes that:

* ERA will participate in requirements validation.
* ERA users will participate in testing.
* Users will receive appropriate training.
* Users will follow approved data-entry procedures.
* Information entered into the system will be reviewed for accuracy.
* ERA will establish appropriate data-protection procedures.
* The system will initially be used by authorised ERA personnel.
* Organisational responsibilities may change over time.
* New titles may be created by authorised administrators when required.
* Final permissions will be validated before production deployment.

# 26. MVP Requirements

The initial MVP shall prioritise the following:

## Authentication and Access

* Login
* Logout
* User management
* Five initial titles
* Permissions
* Record-level access

## Beneficiary and Disability Services

* Beneficiary registration
* Beneficiary search
* Disability assessment
* Home visits
* Referrals
* Referral approval where required
* Referral follow-ups

## Projects

* Project registration
* Project management
* Activity registration
* Activity assignment
* Activity status

## Poultry

* Poultry groups
* Poultry records
* Poultry quantity tracking
* Egg production
* Feed records
* Farm-to-poultry transfers
* Illness records
* Death records
* Sales

## Farm

* Crop records
* Farm activities
* Harvest records
* Farm-to-poultry produce transfers
* Farm expenses

## Finance

* Expense records
* Expense categories
* Basic sales/income records
* Financial reporting

## Management

* Dashboard
* Basic reports
* Search and filtering

# 27. Acceptance Criteria

ERA-IPMS shall be considered ready for initial deployment when:

1. Authorised users can securely log in.
2. Users can log out securely.
3. Inactive or unauthorised users cannot access protected functions.
4. Users receive access according to assigned titles and permissions.
5. Record-level restrictions operate as approved.
6. Admin users can manage authorised user accounts.
7. Admin users can manage titles and permissions where authorised.
8. Beneficiaries can be registered.
9. Beneficiary records can be searched and updated according to permissions.
10. Beneficiary records can be archived or made inactive where required.
11. Disability assessments can be recorded.
12. Home visits can be recorded.
13. Referrals can be created.
14. Referral approval workflows operate where required.
15. Referral follow-ups can be recorded.
16. Projects can be created and managed by authorised users.
17. Activities can be created, assigned, and tracked.
18. Poultry records can be maintained.
19. Poultry quantities can be tracked.
20. Egg production can be recorded.
21. Feed can be recorded.
22. Farm produce transferred to poultry can be recorded.
23. Poultry illnesses and deaths can be recorded.
24. Poultry and egg sales can be recorded where authorised.
25. Farm crops and activities can be recorded.
26. Harvests can be recorded.
27. Farm produce use and transfers can be recorded.
28. Expenses can be recorded.
29. Basic sales and income can be recorded where applicable.
30. Management users can view authorised key indicators.
31. Basic reports can be generated.
32. Search and filtering operate according to access rights.
33. Important system actions can be audited where required.
34. Unauthorised users cannot access restricted information.
35. Testing can be performed using approved fictional or test data without major defects.

# 28. Future Development

Following successful implementation and validation of the MVP, ERA-IPMS may be expanded with:

* PDF exports
* Excel exports
* Mobile application
* Offline data collection
* SMS notifications
* WhatsApp notifications
* Advanced M&E
* KoboToolbox integration
* Excel import
* External partner access
* Multi-organisation support
* SaaS functionality
* Additional modules approved by ERA

Future features shall not be treated as MVP requirements without formal approval.

# 29. Requirements Traceability and Change Control

Each major requirement shall be traceable to the relevant project documentation and implementation component.

Requirements should be identified using stable identifiers such as:

* FR-xxx for functional requirements
* NFR-xxx for non-functional requirements

Changes to requirements shall be:

1. Documented.
2. Reviewed.
3. Checked for contradictions with existing project documents.
4. Approved where organisational approval is required.
5. Reflected in affected design documents.
6. Reflected in the development log.
7. Implemented only after the documentation baseline is sufficiently aligned.

# 30. Relationship to Subsequent Design

This SRS establishes what ERA-IPMS is required to accomplish.

The following documents shall translate these requirements into implementation specifications:

1. User Roles and Permissions
2. System Workflows
3. Database Entity Design
4. ERD
5. Database Schema
6. Interface and UI Design
7. Backend implementation
8. Testing documentation

The database and application architecture shall not introduce functionality that contradicts this requirements baseline without an approved requirements change.

# 31. Conclusion

This Software Requirements Specification defines the current functional and non-functional requirements baseline for ERA-IPMS.

The SRS establishes the approved initial scope, user-access model, operational requirements, security direction, technology direction, MVP requirements, and acceptance criteria.

The initial system uses five approved titles:

* Admin
* Director
* Programme Coordinator
* Finance
* Member

Titles, permissions, and operational responsibilities are separate concepts.

The SRS also establishes record-level access, referral approval, beneficiary archiving, poultry and farm operational tracking, farm-to-poultry transfers, and basic financial management as important requirements.

Detailed permissions, workflows, database structures, and interface behaviour shall be developed in subsequent documentation while remaining consistent with this requirements baseline.
