# ERA Integrated Project Management System (ERA-IPMS)

## Software Requirements Specification (SRS)

### Document Information

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** Software Requirements Specification
**Version:** 1.0
**Date:** September 2026
**Status:** Draft
**Prepared By:** Abdullahi Abdi Mohamed

# 1. Introduction

## 1.1 Purpose

The ERA Integrated Project Management System (ERA-IPMS) is a web-based information management system proposed for Emergency Response Aid (ERA).

The system will help ERA move from mainly manual and paper-based documentation toward structured digital information management.

ERA-IPMS will bring together information relating to:

* Disability services.
* Beneficiaries.
* Home visits.
* Referrals and follow-ups.
* Projects.
* Activities.
* Poultry.
* Small-scale farming.
* Finance.
* Staff and volunteers.
* Monitoring and evaluation.
* Reporting.

The system will provide authorised users with a central location for recording, managing, searching, monitoring, and reporting organisational information.

# 2. Background

ERA is a community-based organisation working in areas including disability services, community advocacy and awareness, poultry farming, and small-scale agriculture.

ERA's disability activities include:

* Home visits.
* Assessments.
* Referrals.
* Follow-up.
* Capacity building.
* Advocacy.
* Awareness activities for persons with disabilities and vulnerable persons.

ERA also operates a small poultry project and a small vegetable farm.

The poultry project currently has approximately 10 local and Kienyeji chickens. Its main purpose is currently egg production, with plans for future expansion into meat production and breeding.

ERA's small farm grows crops including bananas, natural vegetables, and sukuma wiki. The farm supports the poultry project through farm produce that may be used as chicken feed. Local feeds are also purchased when necessary.

Much of ERA's information is currently maintained using paper forms and manual records.

# 3. Problem Statement

ERA currently faces several information management challenges.

These include:

* Difficulty finding old beneficiary records.
* Risk of losing or damaging paper records.
* Duplicate records.
* Time-consuming report preparation.
* Difficulty determining the total number of beneficiaries served.
* Difficulty tracking referrals and follow-ups.
* Difficulty monitoring poultry numbers.
* Difficulty monitoring egg production.
* Lack of structured feed records.
* Difficulty monitoring poultry illness and deaths.
* Lack of formal farm production records.
* Lack of formal harvest records.
* Difficulty consolidating farm expenses.
* Difficulty producing high-quality organisational and project reports.

ERA-IPMS is intended to address these problems through a structured digital information management system.

# 4. System Objectives

The main objectives of ERA-IPMS are to:

1. Digitise important ERA records.
2. Centralise organisational and project information.
3. Improve beneficiary information management.
4. Improve disability service tracking.
5. Improve referral and follow-up tracking.
6. Improve poultry monitoring.
7. Introduce structured farm records.
8. Improve financial record management.
9. Improve project and activity monitoring.
10. Provide useful management dashboards.
11. Improve report preparation.
12. Improve information retrieval.
13. Support evidence-based decision-making.

# 5. Scope of the System

## 5.1 In Scope

The initial ERA-IPMS will include:

* User authentication.
* User roles and permissions.
* Beneficiary management.
* Disability assessment records.
* Home visit records.
* Referral management.
* Referral follow-up.
* Project management.
* Activity management.
* Poultry management.
* Small farm management.
* Expense management.
* Staff and volunteer records.
* Dashboard.
* Monitoring and evaluation information.
* Basic reporting.

## 5.2 Future Scope

The following features may be considered in later versions:

* PDF exports.
* Excel exports.
* Mobile application.
* Offline data collection.
* SMS notifications.
* WhatsApp notifications.
* Advanced M&E indicators.
* Multi-organisation SaaS functionality.
* External partner access.
* Integration with KoboToolbox.
* Import from Excel.

These features are not required for the first MVP.

# 6. Target Users

ERA-IPMS will initially support seven user roles:

1. System Administrator.
2. ERA Management.
3. Programme / Project Coordinator.
4. Field Staff / Volunteer.
5. Farm Personnel.
6. Finance Personnel.
7. Monitoring & Evaluation Personnel.

Each role will have different permissions according to its responsibilities.

# 7. Functional Requirements

Functional requirements describe what the system must be able to do.

## FR-001: User Authentication

The system shall allow authorised users to log in using a username or email and password.

The system shall reject invalid login credentials.

The system shall allow authorised users to log out.

## FR-002: User Management

The System Administrator shall be able to:

* Create user accounts.
* Update user accounts.
* Activate user accounts.
* Deactivate user accounts.
* Assign user roles.
* Reset user passwords.

## FR-003: Role-Based Access Control

The system shall restrict access according to the user's assigned role.

For example:

* Finance Personnel shall access authorised financial information.
* Farm Personnel shall access farm and poultry information.
* Field Staff / Volunteers shall access authorised beneficiary and field information.
* System Administrators shall manage system-level functions.

# 8. Beneficiary Management

## FR-004: Beneficiary Registration

Authorised users shall be able to register beneficiaries.

The system should capture appropriate information such as:

* Beneficiary identification number.
* Name.
* Age.
* Sex.
* Location.
* Contact information where appropriate.
* Disability information where applicable.
* Date of registration.
* Service needs.
* Other relevant information.

Only necessary information should be collected.

## FR-005: Beneficiary Search

Authorised users shall be able to search for beneficiaries.

The system should support searches using appropriate fields such as:

* Beneficiary ID.
* Name.
* Location.
* Service status.

## FR-006: Beneficiary Update

Authorised users shall be able to update beneficiary information where they have permission.

The system should record when important information was updated.

# 9. Disability Services

## FR-007: Disability Assessment

Authorised Field Staff / Volunteers and Programme Coordinators shall be able to record disability assessment information.

The assessment record should capture relevant needs and service information.

## FR-008: Home Visits

Authorised users shall be able to record home visits.

A home visit record should include information such as:

* Beneficiary.
* Date of visit.
* Person conducting the visit.
* Purpose of visit.
* Key observations.
* Support provided.
* Follow-up required.
* Next action.

# 10. Referral Management

## FR-009: Create Referral

Authorised users shall be able to create referral records.

A referral should include:

* Beneficiary.
* Referral date.
* Referral destination or service.
* Reason for referral.
* Person making the referral.
* Referral status.

## FR-010: Referral Status

The system shall support referral statuses such as:

* Pending.
* Follow-up required.
* Completed.
* Not completed.
* Cancelled.

## FR-011: Referral Follow-Up

Authorised Field Staff / Volunteers shall be able to record follow-up activities.

The system should record:

* Follow-up date.
* Person conducting follow-up.
* Outcome.
* Service received.
* Remaining needs.
* Next action.

# 11. Project Management

## FR-012: Project Registration

Authorised Programme / Project Coordinators shall be able to create projects.

A project should contain:

* Project name.
* Description.
* Start date.
* End date.
* Objectives.
* Project status.
* Responsible person.

## FR-013: Activity Management

Authorised users shall be able to record project and organisational activities.

Activity information should include:

* Activity name.
* Project.
* Date.
* Location.
* Responsible person.
* Participants.
* Description.
* Status.
* Results or outcomes.

## FR-014: Activity Status

The system should support statuses such as:

* Planned.
* Ongoing.
* Completed.
* Pending.
* Cancelled.

# 12. Poultry Management

## FR-015: Poultry Records

Authorised Farm Personnel shall be able to record poultry information.

The system should support:

* Current chicken numbers.
* Chicken purchases.
* Chicken type.
* Egg production.
* Feed information.
* Poultry illness.
* Poultry deaths.
* Poultry sales.
* Other poultry activities.

## FR-016: Poultry Numbers

The system should allow authorised users to record changes in poultry numbers.

For example:

```text
Opening chickens: 10
New chicks purchased: 20
Deaths: 2
Sold: 3

Current chickens = 10 + 20 - 2 - 3
Current chickens = 25
```

The system should support accurate tracking of these changes.

## FR-017: Egg Production

The system shall allow Farm Personnel to record egg production.

Egg records should include:

* Date.
* Number of eggs produced.
* Eggs used.
* Eggs sold.
* Eggs remaining.

## FR-018: Feed Management

The system should allow authorised users to record:

* Feed purchased.
* Feed received from the farm.
* Feed used.
* Feed quantity.
* Feed cost where applicable.

## FR-019: Poultry Health

The system should allow authorised users to record:

* Illness.
* Date identified.
* Number affected.
* Action taken.
* Outcome.

Poultry deaths should also be recorded.

# 13. Small Farm Management

## FR-020: Crop Management

The system shall allow Farm Personnel to record crops grown by ERA.

Initial crops may include:

* Bananas.
* Natural/local vegetables.
* Sukuma wiki.

## FR-021: Farm Activities

The system should allow users to record:

* Planting.
* Watering.
* Weeding.
* Harvesting.
* Other farm activities.

## FR-022: Harvest Records

The system shall allow Farm Personnel to record harvests.

A harvest record should include:

* Crop.
* Date.
* Quantity.
* Unit.
* Use of produce.

Produce use may include:

* Used for poultry.
* Used by ERA.
* Sold in the future.
* Other authorised use.

## FR-023: Farm Expenses

The system shall allow authorised users to record farm expenses.

Examples include:

* Seeds.
* Tools.
* Farm inputs.
* Transport.
* Other relevant expenses.

# 14. Finance Management

## FR-024: Expense Recording

Authorised Finance Personnel shall be able to record organisational and project expenses.

An expense record should include:

* Date.
* Amount.
* Category.
* Description.
* Project where applicable.
* Payment method where appropriate.
* Person responsible.
* Supporting reference where applicable.

## FR-025: Expense Categories

The system should support categories such as:

* Project expenses.
* Poultry expenses.
* Farm expenses.
* Office expenses.
* Transport.
* Equipment.
* Other authorised expenses.

# 15. Staff and Volunteer Management

## FR-026: Staff Records

Authorised users shall be able to maintain staff records.

## FR-027: Volunteer Records

Authorised users shall be able to maintain volunteer records.

Records may include:

* Name.
* Role.
* Contact information.
* Start date.
* Status.
* Assigned responsibilities.

# 16. Dashboard

## FR-028: Management Dashboard

The system shall provide a dashboard containing key organisational indicators.

The dashboard should display:

* Total beneficiaries.
* Home visits.
* Referrals.
* Referral follow-ups.
* Current chickens.
* Eggs produced.
* Feed used or purchased.
* Poultry deaths and illnesses.
* Farm crops.
* Harvests.
* Farm expenses.
* Organisational expenses.
* Project expenses.
* Activities conducted.
* Staff and volunteers.
* Upcoming activities.
* Pending activities.

# 17. Monitoring and Evaluation

## FR-029: Indicator Monitoring

The system should support monitoring of selected organisational and project indicators.

Examples include:

* Number of beneficiaries served.
* Number of home visits.
* Number of referrals.
* Number of completed referrals.
* Number of activities.
* Poultry production.
* Farm production.

# 18. Reporting

## FR-030: Report Generation

Authorised users shall be able to generate reports.

Initial reports may include:

* Beneficiary report.
* Disability service report.
* Home visit report.
* Referral report.
* Project activity report.
* Poultry report.
* Egg production report.
* Farm report.
* Expense report.
* Management summary report.

# 19. Search and Filtering

## FR-031: Search

The system shall provide search functionality for authorised records.

Users should be able to filter information using relevant criteria.

Examples include:

* Date.
* Project.
* Beneficiary.
* Activity.
* Status.
* Crop.
* Poultry record.
* Expense category.

# 20. Non-Functional Requirements

Non-functional requirements describe how the system should perform.

## NFR-001: Usability

The system should have a simple and understandable interface.

The system should be usable by people with different levels of technical experience.

## NFR-002: Performance

The system should respond to normal user requests within a reasonable amount of time under expected usage.

## NFR-003: Security

The system shall require authentication.

The system shall implement role-based access control.

Passwords shall not be stored as plain text.

Unauthorised users shall not access restricted information.

## NFR-004: Data Protection

Beneficiary and organisational information should be protected against unauthorised access, modification, or disclosure.

Production information should not be stored in the public GitHub repository.

## NFR-005: Reliability

The system should minimise data loss.

Regular database backups should be implemented before production deployment.

## NFR-006: Maintainability

The source code should be organised into logical components.

The system should use clear naming conventions and documentation.

## NFR-007: Scalability

The system should be designed so that additional modules and users can be added in the future.

## NFR-008: Compatibility

The initial system should operate through modern web browsers on computers and other supported devices.

# 21. Technology Requirements

The initial development technology stack will be limited to the technologies selected for the project.

### Frontend

* HTML.
* CSS.
* JavaScript.

### Backend

* Python.

### Database

* MySQL.

### Version Control

* Git.
* GitHub.

Java may be used for future components where appropriate, but it is not required for the initial ERA-IPMS MVP.

# 22. Data Requirements

ERA-IPMS will need structured data for the following main entities:

* Users.
* Roles.
* Beneficiaries.
* Disability assessments.
* Home visits.
* Referrals.
* Referral follow-ups.
* Projects.
* Activities.
* Poultry records.
* Egg production.
* Feed records.
* Poultry health records.
* Farm crops.
* Farm activities.
* Harvests.
* Expenses.
* Staff.
* Volunteers.

These entities will be analysed in detail during database design.

# 23. System Constraints

The initial project has the following constraints:

1. Development will use HTML, CSS, JavaScript, Python, and MySQL.
2. The system will initially be developed for ERA.
3. Initial testing will use fictional or test data.
4. The first version will focus on essential functionality.
5. Advanced mobile and integration features will be developed later.
6. Internet availability may affect access to the web-based system.

# 24. Assumptions

The project assumes that:

* ERA will provide feedback during development.
* ERA users will participate in testing.
* Users will receive appropriate training before deployment.
* Data entered into the system will be reviewed for accuracy.
* Appropriate procedures will be established for protecting organisational and beneficiary information.
* The system will initially be used by authorised ERA personnel.

# 25. MVP Requirements

The first Minimum Viable Product should focus on the most important functions.

The MVP should include:

### Authentication

* Login.
* Logout.
* User roles.

### Disability

* Beneficiary registration.
* Disability assessment.
* Home visits.
* Referrals.
* Follow-ups.

### Projects

* Project registration.
* Activity registration.
* Activity status.

### Poultry

* Chicken records.
* Egg production.
* Feed records.
* Illness records.
* Death records.

### Farm

* Crop records.
* Farm activities.
* Harvest records.
* Farm expenses.

### Finance

* Expense records.
* Expense categories.

### Management

* Dashboard.
* Basic reports.

# 26. Acceptance Criteria

ERA-IPMS will be considered ready for initial deployment when:

1. Authorised users can log in securely.
2. Users receive access according to their assigned roles.
3. Beneficiaries can be registered.
4. Disability service information can be recorded.
5. Home visits can be recorded.
6. Referrals can be created and followed up.
7. Projects and activities can be recorded.
8. Poultry information can be recorded.
9. Egg production can be recorded.
10. Feed information can be recorded.
11. Poultry illnesses and deaths can be recorded.
12. Farm activities and harvests can be recorded.
13. Expenses can be recorded.
14. Management can view key indicators.
15. Basic reports can be generated.
16. Test data can be entered without major errors.
17. Unauthorised users cannot access restricted information.

# 27. Future Development

After successful implementation of the MVP, ERA-IPMS may be expanded to include:

* PDF reports.
* Excel reports.
* Mobile application.
* Offline data collection.
* SMS notifications.
* WhatsApp notifications.
* Advanced M&E.
* KoboToolbox integration.
* Excel import.
* Multi-organisation support.
* SaaS subscription functionality.

# 28. Conclusion

This Software Requirements Specification defines the initial functional and non-functional requirements for ERA-IPMS.

The document establishes what the system should accomplish before software development begins.

The requirements will be reviewed and validated by ERA before implementation. Approved requirements will guide the system workflow design, database design, interface development, backend development, testing, and deployment.

Future changes to the system should be documented and reviewed so that the project remains controlled and traceable.