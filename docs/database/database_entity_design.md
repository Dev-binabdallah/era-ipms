# ERA Integrated Project Management System (ERA-IPMS)

# Database Entity Design

## Document Information

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** Database Design Specification
**Version:** 1.1
**Date:** September 2026
**Status:** Draft
**Prepared By:** Abdullahi Abdi Mohamed

# 1. Introduction

This document defines the database entities and relationships required to support the approved ERA-IPMS requirements and workflows.

An entity represents an important type of information that the system must store.

The database design provides the structural bridge between:

* Software Requirements Specification.
* User Roles and Permissions.
* System Workflows.
* Entity Relationship Diagram.
* Database schema.
* Django application models.

The database shall support:

* Authentication and users.
* Dynamic titles.
* Fixed application permissions.
* User responsibilities.
* Project and activity assignments.
* Beneficiary services.
* Referrals and follow-ups.
* Projects and activities.
* Poultry operations.
* Small farm operations.
* Farm-to-poultry transfers.
* Basic finance.
* Monitoring and evaluation.
* Audit information.
* Record-level access.

This document defines the logical entity design. It does not yet constitute the final SQL implementation.

# 2. Database Design Principles

The database shall follow these principles:

1. Every important business entity must have a clear purpose.
2. Relationships must represent actual ERA business processes.
3. Primary keys must uniquely identify records.
4. Foreign keys must preserve referential integrity.
5. Sensitive records must support access-control decisions.
6. Important records must identify the responsible user where appropriate.
7. Operational quantities must remain distinguishable from financial transactions.
8. Beneficiary records should be archived rather than physically deleted.
9. Controlled values should be used for statuses and transaction types.
10. Historical information should not be unnecessarily overwritten.
11. The design should support future expansion without unnecessary duplication.
12. The final schema must remain consistent with the approved workflows.

# 3. Naming Standards

The database shall use:

* Lowercase table names.
* Snake_case for multiple words.
* Plural table names where appropriate.
* `table_name_id` for primary keys.
* `<entity>_id` for foreign keys.
* `created_at` for record creation timestamps.
* `updated_at` where records can be modified.
* `DATE` where only a calendar date is required.
* `DATETIME` where date and time are required.
* `DECIMAL` for monetary values.
* Appropriate integer or decimal types for quantities.
* Controlled values for statuses and transaction types.

Examples:

```text
users
beneficiaries
disability_assessments
referral_follow_ups
project_id
beneficiary_id
created_at
updated_at
```

# 4. Core Entity Inventory

The proposed initial database contains the following entities.

## Access and Organisation

1. `users`
2. `titles`
3. `permissions`
4. `title_permissions`
5. `responsibilities`
6. `user_responsibilities`
7. `staff_members`
8. `user_project_assignments`

## Beneficiary Services

9. `beneficiaries`
10. `disability_assessments`
11. `home_visits`
12. `referrals`
13. `referral_follow_ups`

## Projects and Activities

14. `projects`
15. `activities`
16. `activity_assignments`
17. `activity_participants`

## Poultry

18. `poultry_groups`
19. `poultry_stock_movements`
20. `egg_production`
21. `feed_records`
22. `poultry_health_records`
23. `poultry_sales`

## Farm

24. `farm_crops`
25. `farm_activities`
26. `harvests`
27. `farm_poultry_transfers`

## Finance

28. `financial_transactions`

## Monitoring and Evaluation

29. `me_indicators`
30. `me_indicator_records`

## System Accountability

31. `audit_events`

The final entity list may change only after validation against the requirements, workflows, ERD, and schema.

# 5. Users Entity

## Table Name

`users`

## Purpose

Stores system authentication accounts.

## Main Fields

| Field           | Type         | Description               |
| --------------- | ------------ | ------------------------- |
| `user_id`       | BIGINT       | Unique user identifier    |
| `username`      | VARCHAR(100) | Login username            |
| `email`         | VARCHAR(150) | Login email               |
| `password_hash` | VARCHAR(255) | Hashed password           |
| `title_id`      | BIGINT       | User's current title      |
| `is_active`     | BOOLEAN      | Whether account is active |
| `last_login`    | DATETIME     | Last successful login     |
| `created_at`    | DATETIME     | Account creation time     |
| `updated_at`    | DATETIME     | Last account update       |

## Primary Key

`user_id`

## Foreign Key

`title_id` → `titles.title_id`

## Rules

* `username` must be unique.
* Email should be unique where provided.
* Passwords must never be stored as plain text.
* Inactive users cannot authenticate.
* A user has one current title.
* A title may be assigned to many users.

# 6. Titles Entity

## Table Name

`titles`

## Purpose

Stores organisational system titles.

Titles identify the user's organisational position or system title. They do not directly represent individual permissions or responsibilities.

## Main Fields

| Field         | Type         | Description                |
| ------------- | ------------ | -------------------------- |
| `title_id`    | BIGINT       | Unique title identifier    |
| `title_name`  | VARCHAR(100) | Title name                 |
| `description` | TEXT         | Title description          |
| `is_active`   | BOOLEAN      | Whether title is available |
| `created_at`  | DATETIME     | Creation time              |
| `updated_at`  | DATETIME     | Last update                |

## Initial Titles

1. Admin
2. Director
3. Programme Coordinator
4. Finance
5. Member

Administrators may create additional titles in the future.

# 7. Permissions Entity

## Table Name

`permissions`

## Purpose

Stores fixed application permissions.

Examples:

* View.
* Add.
* Edit.
* Delete.
* Approve.
* Export.
* Manage.
* Administer.

Permissions represent actions that the application can enforce.

They are distinct from titles and responsibilities.

## Main Fields

| Field             | Type         | Description                  |
| ----------------- | ------------ | ---------------------------- |
| `permission_id`   | BIGINT       | Unique permission identifier |
| `permission_code` | VARCHAR(100) | Machine-readable permission  |
| `permission_name` | VARCHAR(100) | Human-readable name          |
| `description`     | TEXT         | Permission description       |

The application controls the available permission definitions.

# 8. Title Permissions Entity

## Table Name

`title_permissions`

## Purpose

Connects titles to permissions.

This allows permissions to be assigned to titles without treating titles themselves as permissions.

## Main Fields

| Field                 | Type   | Description        |
| --------------------- | ------ | ------------------ |
| `title_permission_id` | BIGINT | Unique identifier  |
| `title_id`            | BIGINT | Related title      |
| `permission_id`       | BIGINT | Related permission |

## Relationships

```text
TITLES 1 ─────< TITLE_PERMISSIONS >───── 1 PERMISSIONS
```

A title can have multiple permissions.

A permission can apply to multiple titles.

# 9. Responsibilities Entity

## Table Name

`responsibilities`

## Purpose

Stores functional responsibilities that may be assigned to users.

Examples:

* Disability services.
* Beneficiary assessment.
* Home visits.
* Referrals.
* Referral follow-up.
* Project coordination.
* Poultry operations.
* Farm operations.
* Finance.
* M&E.
* Reporting.

Responsibilities are separate from permissions.

# 10. User Responsibilities Entity

## Table Name

`user_responsibilities`

## Purpose

Assigns one or more responsibilities to individual users.

## Main Fields

| Field                    | Type     | Description                       |
| ------------------------ | -------- | --------------------------------- |
| `user_responsibility_id` | BIGINT   | Unique identifier                 |
| `user_id`                | BIGINT   | Assigned user                     |
| `responsibility_id`      | BIGINT   | Assigned responsibility           |
| `assigned_by`            | BIGINT   | User making assignment            |
| `assigned_at`            | DATETIME | Assignment time                   |
| `is_active`              | BOOLEAN  | Whether assignment remains active |

## Relationship

```text
USERS 1 ─────< USER_RESPONSIBILITIES >───── 1 RESPONSIBILITIES
```

# 11. Staff Members Entity

## Table Name

`staff_members`

## Purpose

Stores organisational information about ERA staff and Members separately from their authentication account.

A person may have an organisational record without requiring a system account.

## Main Fields

| Field             | Type         | Description                            |
| ----------------- | ------------ | -------------------------------------- |
| `staff_member_id` | BIGINT       | Unique identifier                      |
| `user_id`         | BIGINT       | Linked system account where applicable |
| `full_name`       | VARCHAR(150) | Full name                              |
| `phone`           | VARCHAR(30)  | Contact number                         |
| `email`           | VARCHAR(150) | Contact email                          |
| `start_date`      | DATE         | Start date                             |
| `status`          | VARCHAR(30)  | Active or inactive                     |
| `created_at`      | DATETIME     | Creation time                          |
| `updated_at`      | DATETIME     | Last update                            |

If `user_id` is present, it should identify the corresponding authentication account.

# 12. User Project Assignments Entity

## Table Name

`user_project_assignments`

## Purpose

Records which users are assigned to which projects.

This supports project-level access control.

## Main Fields

| Field           | Type     | Description            |
| --------------- | -------- | ---------------------- |
| `assignment_id` | BIGINT   | Unique identifier      |
| `user_id`       | BIGINT   | Assigned user          |
| `project_id`    | BIGINT   | Assigned project       |
| `assigned_by`   | BIGINT   | User making assignment |
| `assigned_at`   | DATETIME | Assignment time        |
| `is_active`     | BOOLEAN  | Assignment status      |

## Relationship

```text
USERS 1 ─────< USER_PROJECT_ASSIGNMENTS >───── 1 PROJECTS
```

# 13. Beneficiaries Entity

## Table Name

`beneficiaries`

## Purpose

Stores people supported by ERA.

## Main Fields

| Field               | Type         | Description                   |
| ------------------- | ------------ | ----------------------------- |
| `beneficiary_id`    | BIGINT       | Unique identifier             |
| `beneficiary_code`  | VARCHAR(50)  | Unique beneficiary reference  |
| `first_name`        | VARCHAR(100) | First name                    |
| `last_name`         | VARCHAR(100) | Last name                     |
| `date_of_birth`     | DATE         | Date of birth where known     |
| `sex`               | VARCHAR(20)  | Sex                           |
| `location`          | VARCHAR(150) | General location              |
| `phone`             | VARCHAR(30)  | Contact information           |
| `registration_date` | DATE         | Registration date             |
| `status`            | VARCHAR(30)  | Active, inactive, or archived |
| `created_by`        | BIGINT       | User who registered record    |
| `created_at`        | DATETIME     | Creation time                 |
| `updated_at`        | DATETIME     | Last update                   |

## Rules

* `beneficiary_code` must be unique.
* Users should search before creating a beneficiary.
* Duplicate detection should be performed where practical.
* Physical deletion should normally not be used.

# 14. Disability Assessments Entity

## Table Name

`disability_assessments`

## Purpose

Stores disability assessment information.

## Main Fields

| Field              | Type         | Description         |
| ------------------ | ------------ | ------------------- |
| `assessment_id`    | BIGINT       | Unique identifier   |
| `beneficiary_id`   | BIGINT       | Beneficiary         |
| `assessment_date`  | DATE         | Assessment date     |
| `assessment_type`  | VARCHAR(100) | Assessment category |
| `disability_type`  | VARCHAR(150) | Disability type     |
| `needs`            | TEXT         | Identified needs    |
| `assessment_notes` | TEXT         | Additional notes    |
| `assessed_by`      | BIGINT       | Assessing user      |
| `created_at`       | DATETIME     | Creation time       |

## Relationships

```text
BENEFICIARIES 1 ─────< DISABILITY_ASSESSMENTS
USERS 1 ─────< DISABILITY_ASSESSMENTS
```

# 15. Home Visits Entity

## Table Name

`home_visits`

## Purpose

Stores beneficiary home visits.

## Main Fields

| Field                | Type         | Description                   |
| -------------------- | ------------ | ----------------------------- |
| `home_visit_id`      | BIGINT       | Unique identifier             |
| `beneficiary_id`     | BIGINT       | Beneficiary visited           |
| `visit_date`         | DATE         | Visit date                    |
| `conducted_by`       | BIGINT       | User conducting visit         |
| `purpose`            | VARCHAR(255) | Visit purpose                 |
| `observations`       | TEXT         | Observations                  |
| `support_provided`   | TEXT         | Support provided              |
| `follow_up_required` | BOOLEAN      | Whether follow-up is required |
| `next_action`        | TEXT         | Next action                   |
| `created_at`         | DATETIME     | Creation time                 |

# 16. Referrals Entity

## Table Name

`referrals`

## Purpose

Stores beneficiary referrals.

## Main Fields

| Field                    | Type         | Description                      |
| ------------------------ | ------------ | -------------------------------- |
| `referral_id`            | BIGINT       | Unique identifier                |
| `beneficiary_id`         | BIGINT       | Beneficiary                      |
| `referral_date`          | DATE         | Referral date                    |
| `destination`   | VARCHAR(200) | Service or organisation          |
| `reason`                 | TEXT         | Referral reason                  |
| `supporting_information` | TEXT         | Relevant information             |
| `referred_by`            | BIGINT       | User creating referral           |
| `status`                 | VARCHAR(50)  | Referral status                  |
| `approved_by`            | BIGINT       | Approving user where applicable  |
| `approved_at`            | DATETIME     | Approval time where applicable   |
| `decision_reason`        | TEXT         | Approval/return/rejection reason |
| `created_at`             | DATETIME     | Creation time                    |
| `updated_at`             | DATETIME     | Last update                      |

Referral creation and approval must remain separate actions.

# 17. Referral Follow-Ups Entity

## Table Name

`referral_follow_ups`

## Purpose

Stores follow-up activities related to referrals.

## Main Fields

| Field              | Type     | Description                  |
| ------------------ | -------- | ---------------------------- |
| `follow_up_id`     | BIGINT   | Unique identifier            |
| `referral_id`      | BIGINT   | Related referral             |
| `follow_up_date`   | DATE     | Follow-up date               |
| `conducted_by`     | BIGINT   | Responsible user             |
| `outcome`          | TEXT     | Follow-up outcome            |
| `service_received` | BOOLEAN  | Whether service was received |
| `remaining_needs`  | TEXT     | Remaining needs              |
| `next_action`      | TEXT     | Next action                  |
| `created_at`       | DATETIME | Creation time                |

# 18. Projects Entity

## Table Name

`projects`

## Purpose

Stores ERA projects.

## Main Fields

| Field                 | Type         | Description       |
| --------------------- | ------------ | ----------------- |
| `project_id`          | BIGINT       | Unique identifier |
| `project_name`        | VARCHAR(200) | Project name      |
| `description`         | TEXT         | Description       |
| `start_date`          | DATE         | Start date        |
| `end_date`            | DATE         | End date          |
| `objectives`          | TEXT         | Objectives        |
| `status`              | VARCHAR(30)  | Project status    |
| `responsible_user_id` | BIGINT       | Responsible user  |
| `created_by`          | BIGINT       | Creating user     |
| `created_at`          | DATETIME     | Creation time     |
| `updated_at`          | DATETIME     | Last update       |

Project creation is initially authorised for Admin and Director according to their assigned permissions.

# 19. Activities Entity

## Table Name

`activities`

## Purpose

Stores activities belonging to projects.

## Main Fields

| Field           | Type         | Description          |
| --------------- | ------------ | -------------------- |
| `activity_id`   | BIGINT       | Unique identifier    |
| `project_id`    | BIGINT       | Related project      |
| `activity_name` | VARCHAR(200) | Activity name        |
| `activity_date` | DATE         | Activity date        |
| `location`      | VARCHAR(150) | Activity location    |
| `description`   | TEXT         | Activity description |
| `status`        | VARCHAR(30)  | Activity status      |
| `results`       | TEXT         | Results              |
| `created_by`    | BIGINT       | Creating user        |
| `created_at`    | DATETIME     | Creation time        |
| `updated_at`    | DATETIME     | Last update          |

# 20. Activity Assignments Entity

## Table Name

`activity_assignments`

## Purpose

Records users assigned to perform activities.

This is separate from activity participants.

```text
ACTIVITY ASSIGNMENT = WHO IS RESPONSIBLE FOR THE WORK

ACTIVITY PARTICIPANT = WHO PARTICIPATED IN THE ACTIVITY
```

## Main Fields

| Field           | Type        | Description       |
| --------------- | ----------- | ----------------- |
| `assignment_id` | BIGINT      | Unique identifier |
| `activity_id`   | BIGINT      | Activity          |
| `user_id`       | BIGINT      | Assigned user     |
| `assigned_by`   | BIGINT      | Assigning user    |
| `assigned_at`   | DATETIME    | Assignment time   |
| `status`        | VARCHAR(30) | Assignment status |

# 21. Activity Participants Entity

## Table Name

`activity_participants`

## Purpose

Records beneficiaries and other participants associated with activities.

## Main Fields

| Field              | Type         | Description                                         |
| ------------------ | ------------ | --------------------------------------------------- |
| `participant_id`   | BIGINT       | Unique identifier                                   |
| `activity_id`      | BIGINT       | Activity                                            |
| `beneficiary_id`   | BIGINT       | Beneficiary where applicable                        |
| `participant_name` | VARCHAR(150) | Participant name where no beneficiary record exists |
| `participant_type` | VARCHAR(50)  | Beneficiary, Staff, Member, Volunteer, Other        |
| `created_at`       | DATETIME     | Creation time                                       |

# 22. Poultry Groups Entity

## Table Name

`poultry_groups`

## Purpose

Represents identifiable poultry groups or batches.

This allows poultry records to be separated by category or group rather than maintaining only one organisation-wide quantity.

## Main Fields

| Field              | Type         | Description       |
| ------------------ | ------------ | ----------------- |
| `poultry_group_id` | BIGINT       | Unique identifier |
| `group_name`       | VARCHAR(150) | Group name        |
| `poultry_category` | VARCHAR(100) | Poultry category  |
| `start_date`       | DATE         | Group start date  |
| `status`           | VARCHAR(30)  | Group status      |
| `description`      | TEXT         | Group information |
| `created_by`       | BIGINT       | Creating user     |
| `created_at`       | DATETIME     | Creation time     |

Initial categories include local chickens and Kienyeji chickens.

# 23. Poultry Stock Movements Entity

## Table Name

`poultry_stock_movements`

## Purpose

Records every movement that changes poultry stock.

Examples:

* Opening stock.
* Purchase.
* Receipt.
* Sale.
* Death.
* Positive adjustment.
* Negative adjustment.

## Main Fields

| Field               | Type        | Description       |
| ------------------- | ----------- | ----------------- |
| `stock_movement_id` | BIGINT      | Unique identifier |
| `poultry_group_id`  | BIGINT      | Poultry group     |
| `movement_date`     | DATE        | Movement date     |
| `movement_type`     | VARCHAR(50) | Movement type     |
| `quantity`          | INT         | Quantity          |
| `description`       | TEXT        | Details           |
| `recorded_by`       | BIGINT      | Recording user    |
| `created_at`        | DATETIME    | Creation time     |

The stock balance should be calculated from movements.

```text
Current Stock =
Opening Stock
+ Purchases
+ Receipts
+ Positive Adjustments
- Sales
- Deaths
- Negative Adjustments
```

# 24. Egg Production Entity

## Table Name

`egg_production`

## Purpose

Stores egg production records.

## Main Fields

| Field               | Type     | Description            |
| ------------------- | -------- | ---------------------- |
| `egg_production_id` | BIGINT   | Unique identifier      |
| `poultry_group_id`  | BIGINT   | Producing group        |
| `production_date`   | DATE     | Production date        |
| `eggs_produced`     | INT      | Eggs produced          |
| `eggs_used`         | INT      | Eggs used              |
| `eggs_sold`         | INT      | Eggs sold              |
| `notes`             | TEXT     | Additional information |
| `recorded_by`       | BIGINT   | Recording user         |
| `created_at`        | DATETIME | Creation time          |

`eggs_remaining` should preferably be calculated from recorded quantities rather than manually maintained as an independent value.

# 25. Feed Records Entity

## Table Name

`feed_records`

## Purpose

Records poultry feed received, transferred, and used.

## Main Fields

| Field              | Type          | Description                    |
| ------------------ | ------------- | ------------------------------ |
| `feed_record_id`   | BIGINT        | Unique identifier              |
| `poultry_group_id` | BIGINT        | Poultry group where applicable |
| `record_date`      | DATE          | Record date                    |
| `feed_type`        | VARCHAR(100)  | Feed type                      |
| `feed_source`      | VARCHAR(100)  | Farm, Purchase, Other          |
| `quantity`         | DECIMAL(10,2) | Quantity                       |
| `unit`             | VARCHAR(30)   | Unit                           |
| `usage_type`       | VARCHAR(50)   | Received, Used, Adjustment     |
| `cost`             | DECIMAL(12,2) | Cost where applicable          |
| `recorded_by`      | BIGINT        | Recording user                 |
| `created_at`       | DATETIME      | Creation time                  |

Farm-originated feed must be traceable to a farm-to-poultry transfer where applicable.

# 26. Poultry Health Records Entity

## Table Name

`poultry_health_records`

## Purpose

Stores poultry health events.

## Main Fields

| Field              | Type        | Description            |
| ------------------ | ----------- | ---------------------- |
| `health_record_id` | BIGINT      | Unique identifier      |
| `poultry_group_id` | BIGINT      | Affected group         |
| `record_date`      | DATE        | Event date             |
| `condition_type`   | VARCHAR(50) | Illness, injury, other |
| `number_affected`  | INT         | Number affected        |
| `description`      | TEXT        | Condition              |
| `action_taken`     | TEXT        | Action taken           |
| `outcome`          | TEXT        | Outcome                |
| `recorded_by`      | BIGINT      | Recording user         |
| `created_at`       | DATETIME    | Creation time          |

Deaths that change stock must also be represented through `poultry_stock_movements`.

# 27. Poultry Sales Entity

## Table Name

`poultry_sales`

## Purpose

Stores operational details of poultry or egg sales.

## Main Fields

| Field              | Type          | Description                 |
| ------------------ | ------------- | --------------------------- |
| `poultry_sale_id`  | BIGINT        | Unique identifier           |
| `poultry_group_id` | BIGINT        | Related poultry group       |
| `sale_date`        | DATE          | Sale date                   |
| `sale_type`        | VARCHAR(50)   | Poultry or Eggs             |
| `quantity`         | DECIMAL(10,2) | Quantity sold               |
| `unit`             | VARCHAR(30)   | Unit                        |
| `unit_price`       | DECIMAL(12,2) | Unit price where applicable |
| `total_amount`     | DECIMAL(12,2) | Sale value                  |
| `recorded_by`      | BIGINT        | Recording user              |
| `created_at`       | DATETIME      | Creation time               |

A corresponding financial transaction should be created or linked where required.

# 28. Farm Crops Entity

## Table Name

`farm_crops`

## Purpose

Represents crop production units managed by ERA.

## Main Fields

| Field           | Type         | Description       |
| --------------- | ------------ | ----------------- |
| `crop_id`       | BIGINT       | Unique identifier |
| `crop_name`     | VARCHAR(100) | Crop name         |
| `description`   | TEXT         | Crop information  |
| `planting_date` | DATE         | Planting date     |
| `status`        | VARCHAR(30)  | Crop status       |
| `recorded_by`   | BIGINT       | Recording user    |
| `created_at`    | DATETIME     | Creation time     |
| `updated_at`    | DATETIME     | Last update       |

Initial examples include:

* Bananas.
* Local/natural vegetables.
* Sukuma wiki.

# 29. Farm Activities Entity

## Table Name

`farm_activities`

## Purpose

Stores activities performed on farm crops.

Examples:

* Planting.
* Watering.
* Weeding.
* Fertilising.
* Maintenance.
* Harvesting.

## Main Fields

| Field              | Type         | Description       |
| ------------------ | ------------ | ----------------- |
| `farm_activity_id` | BIGINT       | Unique identifier |
| `crop_id`          | BIGINT       | Related crop      |
| `activity_date`    | DATE         | Activity date     |
| `activity_type`    | VARCHAR(100) | Activity type     |
| `description`      | TEXT         | Activity details  |
| `conducted_by`     | BIGINT       | Responsible user  |
| `created_at`       | DATETIME     | Creation time     |

# 30. Harvests Entity

## Table Name

`harvests`

## Purpose

Stores farm harvest records.

## Main Fields

| Field                | Type          | Description              |
| -------------------- | ------------- | ------------------------ |
| `harvest_id`         | BIGINT        | Unique identifier        |
| `crop_id`            | BIGINT        | Harvested crop           |
| `harvest_date`       | DATE          | Harvest date             |
| `quantity`           | DECIMAL(10,2) | Harvest quantity         |
| `unit`               | VARCHAR(30)   | Quantity unit            |
| `available_quantity` | DECIMAL(10,2) | Quantity still available |
| `notes`              | TEXT          | Additional information   |
| `recorded_by`        | BIGINT        | Recording user           |
| `created_at`         | DATETIME      | Creation time            |

The available quantity must not become negative.

# 31. Farm-to-Poultry Transfers Entity

## Table Name

`farm_poultry_transfers`

## Purpose

Records farm produce transferred for poultry feed.

This entity provides traceability between the farm harvest and poultry feed.

## Main Fields

| Field              | Type          | Description             |
| ------------------ | ------------- | ----------------------- |
| `transfer_id`      | BIGINT        | Unique identifier       |
| `harvest_id`       | BIGINT        | Source harvest          |
| `poultry_group_id` | BIGINT        | Receiving poultry group |
| `transfer_date`    | DATE          | Transfer date           |
| `quantity`         | DECIMAL(10,2) | Quantity transferred    |
| `unit`             | VARCHAR(30)   | Unit                    |
| `recorded_by`      | BIGINT        | Recording user          |
| `notes`            | TEXT          | Additional information  |
| `created_at`       | DATETIME      | Creation time           |

Relationship:

```text
FARM_CROPS
    |
    v
HARVESTS
    |
    v
FARM_POULTRY_TRANSFERS
    |
    v
POULTRY_GROUPS
```

This makes the transfer traceable from source to destination.

# 32. Financial Transactions Entity

## Table Name

`financial_transactions`

## Purpose

Stores basic financial transactions.

The initial system supports basic financial management, not full accounting.

The entity must support both income and expenses.

## Main Fields

| Field                      | Type          | Description                           |
| -------------------------- | ------------- | ------------------------------------- |
| `financial_transaction_id` | BIGINT        | Unique identifier                     |
| `transaction_date`         | DATE          | Transaction date                      |
| `transaction_type`         | VARCHAR(30)   | Income or Expense                     |
| `category`                 | VARCHAR(100)  | Financial category                    |
| `amount`                   | DECIMAL(12,2) | Transaction amount                    |
| `description`              | TEXT          | Description                           |
| `project_id`               | BIGINT        | Related project where applicable      |
| `poultry_sale_id`          | BIGINT        | Related poultry sale where applicable |
| `expense_area`             | VARCHAR(50)   | Organisation, Project, Poultry, Farm  |
| `payment_method`           | VARCHAR(50)   | Cash, Bank, Mobile Money, etc.        |
| `status`                   | VARCHAR(30)   | Status                                |
| `recorded_by`              | BIGINT        | Recording user                        |
| `approved_by`              | BIGINT        | Approving user where applicable       |
| `approved_at`              | DATETIME      | Approval time where applicable        |
| `created_at`               | DATETIME      | Creation time                         |
| `updated_at`               | DATETIME      | Last update                           |

Operational records and financial transactions remain logically separate.

# 33. Monitoring and Evaluation Indicators Entity

## Table Name

`me_indicators`

## Purpose

Defines indicators used to monitor projects and programme performance.

## Main Fields

| Field            | Type          | Description                      |
| ---------------- | ------------- | -------------------------------- |
| `indicator_id`   | BIGINT        | Unique identifier                |
| `project_id`     | BIGINT        | Related project where applicable |
| `indicator_name` | VARCHAR(200)  | Indicator name                   |
| `description`    | TEXT          | Description                      |
| `target_value`   | DECIMAL(12,2) | Target                           |
| `unit`           | VARCHAR(50)   | Measurement unit                 |
| `start_date`     | DATE          | Measurement period start         |
| `end_date`       | DATE          | Measurement period end           |
| `recorded_by`    | BIGINT        | User defining indicator          |
| `created_at`     | DATETIME      | Creation time                    |

# 34. M&E Indicator Records Entity

## Table Name

`me_indicator_records`

## Purpose

Stores periodic measurements against an M&E indicator.

Separating indicator definition from indicator measurements allows historical values to be retained.

## Main Fields

| Field                 | Type          | Description       |
| --------------------- | ------------- | ----------------- |
| `indicator_record_id` | BIGINT        | Unique identifier |
| `indicator_id`        | BIGINT        | Related indicator |
| `measurement_date`    | DATE          | Measurement date  |
| `value`               | DECIMAL(12,2) | Recorded value    |
| `notes`               | TEXT          | Measurement notes |
| `recorded_by`         | BIGINT        | Recording user    |
| `created_at`          | DATETIME      | Creation time     |

Relationship:

```text
ME_INDICATORS 1 ─────< ME_INDICATOR_RECORDS
```

# 35. Audit Events Entity

## Table Name

`audit_events`

## Purpose

Stores important system actions for accountability and traceability.

## Main Fields

| Field            | Type         | Description                            |
| ---------------- | ------------ | -------------------------------------- |
| `audit_event_id` | BIGINT       | Unique identifier                      |
| `user_id`        | BIGINT       | User performing action                 |
| `action`         | VARCHAR(50)  | Create, Edit, Approve, Archive, etc.   |
| `module`         | VARCHAR(100) | System module                          |
| `record_type`    | VARCHAR(100) | Entity affected                        |
| `record_id`      | BIGINT       | Affected record identifier             |
| `old_values`     | TEXT         | Previous information where appropriate |
| `new_values`     | TEXT         | New information where appropriate      |
| `event_time`     | DATETIME     | Date and time                          |
| `description`    | TEXT         | Additional information                 |

Audit events should cover important administrative, approval, archive, create, and edit operations.

# 36. Core Relationship Model

The overall logical structure is:

```text
                         TITLES
                           |
                           | 1
                           v
                         USERS
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
 USER_RESPONSIBILITIES  PROJECTS      BENEFICIARIES
          |                |                |
          |                |                +----< DISABILITY_ASSESSMENTS
          |                |                +----< HOME_VISITS
          |                |                +----< REFERRALS
          |                |                           |
          |                |                           +----< FOLLOW_UPS
          |                |
          |                +----< ACTIVITIES
          |                           |
          |                           +----< ACTIVITY_ASSIGNMENTS
          |                           +----< ACTIVITY_PARTICIPANTS
          |
          +---- RESPONSIBILITIES

PROJECTS
   |
   +----< USER_PROJECT_ASSIGNMENTS
   +----< ACTIVITIES
   +----< ME_INDICATORS
   +----< FINANCIAL_TRANSACTIONS

FARM_CROPS
   |
   +----< FARM_ACTIVITIES
   +----< HARVESTS
              |
              +----< FARM_POULTRY_TRANSFERS
                              |
                              v
                        POULTRY_GROUPS
                              |
              +---------------+----------------+
              |               |                |
              v               v                v
       STOCK_MOVEMENTS   EGG_PRODUCTION    FEED_RECORDS
              |
              +----< POULTRY_SALES
              |
              +----< HEALTH_RECORDS

FINANCIAL_TRANSACTIONS
        |
        v
     REPORTING / M&E
```

# 37. Key Relationship Rules

## Users and Titles

```text
TITLES 1 ─────< USERS
```

One title may be assigned to many users.

## Titles and Permissions

```text
TITLES >────< PERMISSIONS
```

Implemented through `title_permissions`.

## Users and Responsibilities

```text
USERS >────< RESPONSIBILITIES
```

Implemented through `user_responsibilities`.

## Beneficiaries and Services

```text
BENEFICIARIES 1 ─────< DISABILITY_ASSESSMENTS
BENEFICIARIES 1 ─────< HOME_VISITS
BENEFICIARIES 1 ─────< REFERRALS
```

## Referrals

```text
REFERRALS 1 ─────< REFERRAL_FOLLOW_UPS
```

## Projects and Activities

```text
PROJECTS 1 ─────< ACTIVITIES
```

## Activities and Users

```text
ACTIVITIES >────< USERS
```

Implemented through `activity_assignments`.

## Activities and Beneficiaries

```text
ACTIVITIES >────< BENEFICIARIES
```

Implemented through `activity_participants`.

## Farm

```text
FARM_CROPS 1 ─────< FARM_ACTIVITIES
FARM_CROPS 1 ─────< HARVESTS
```

## Farm-to-Poultry

```text
HARVESTS 1 ─────< FARM_POULTRY_TRANSFERS >───── 1 POULTRY_GROUPS
```

## Poultry

```text
POULTRY_GROUPS 1 ─────< POULTRY_STOCK_MOVEMENTS
POULTRY_GROUPS 1 ─────< EGG_PRODUCTION
POULTRY_GROUPS 1 ─────< FEED_RECORDS
POULTRY_GROUPS 1 ─────< POULTRY_HEALTH_RECORDS
POULTRY_GROUPS 1 ─────< POULTRY_SALES
```

## Monitoring and Evaluation

```text
PROJECTS 1 ─────< ME_INDICATORS
ME_INDICATORS 1 ─────< ME_INDICATOR_RECORDS
```

# 38. Record-Level Access Support

The database must provide sufficient relationships for the application to enforce record-level access.

For example, a Member's beneficiary access may be derived from relationships such as:

```text
BENEFICIARY
    |
    +---- created_by
    |
    +---- assessments.assessed_by
    |
    +---- home_visits.conducted_by
    |
    +---- referrals.referred_by
```

Project access may be derived from:

```text
USER
 |
 v
USER_PROJECT_ASSIGNMENTS
 |
 v
PROJECT
 |
 v
ACTIVITIES
```

The final access implementation remains an application responsibility and must also be enforced on the backend.

# 39. Audit and Accountability Relationships

Important operational entities should identify the user responsible for creating, recording, conducting, approving, or modifying information.

Common relationships include:

```text
USERS 1 ─────< BENEFICIARIES
USERS 1 ─────< DISABILITY_ASSESSMENTS
USERS 1 ─────< HOME_VISITS
USERS 1 ─────< REFERRALS
USERS 1 ─────< REFERRAL_FOLLOW_UPS
USERS 1 ─────< PROJECTS
USERS 1 ─────< ACTIVITIES
USERS 1 ─────< POULTRY_STOCK_MOVEMENTS
USERS 1 ─────< EGG_PRODUCTION
USERS 1 ─────< FEED_RECORDS
USERS 1 ─────< POULTRY_HEALTH_RECORDS
USERS 1 ─────< FARM_CROPS
USERS 1 ─────< FARM_ACTIVITIES
USERS 1 ─────< HARVESTS
USERS 1 ─────< FINANCIAL_TRANSACTIONS
USERS 1 ─────< ME_INDICATORS
USERS 1 ─────< AUDIT_EVENTS
```

# 40. Important Data Rules

## Users

* Username must be unique.
* Email should be unique where provided.
* Password hashes must never contain plain-text passwords.
* Inactive users must not authenticate.

## Titles

* Title names should be unique.
* Titles may be added or deactivated by authorised administrators.
* Titles must not be treated as permission definitions.

## Permissions

* Permission definitions are controlled by the application.
* A permission must have a unique code.

## Beneficiaries

* Beneficiary codes must be unique.
* Required information must be validated.
* Duplicate detection should be performed.
* Archived beneficiaries remain in the database.

## Referrals

* Every referral must belong to a beneficiary.
* Referral status must use controlled values.
* Referral approval must be separately authorised.

## Poultry

* Quantities must not be negative.
* Stock movements must use controlled movement types.
* Sales and deaths must reduce stock.
* Poultry groups must provide sufficient separation for operational records.

## Eggs

* Production quantities cannot be negative.
* Used or sold quantities must not exceed available quantities.

## Farm

* Harvest quantities cannot be negative.
* Transfers cannot exceed available harvest quantity.
* Farm-to-poultry transfers must identify both source and destination.

## Finance

* Financial amounts must be greater than zero unless a specific adjustment process permits otherwise.
* Income and expense transactions must be distinguishable.
* Financial transactions must identify the responsible user.
* Approval requirements must be enforced where applicable.

# 41. Delete and Archive Rules

Physical deletion should be restricted.

For beneficiary records:

```text
ACTIVE
   |
   v
ARCHIVE / INACTIVE
   |
   v
RETAIN RECORD
```

The database should preserve historical relationships wherever practical.

Administrative deletion of records, where permitted, must be controlled and auditable.

# 42. Referential Integrity

Foreign keys should be used to prevent orphaned records.

Examples:

```text
disability_assessments.beneficiary_id
    → beneficiaries.beneficiary_id
```

```text
referral_follow_ups.referral_id
    → referrals.referral_id
```

```text
activities.project_id
    → projects.project_id
```

```text
farm_poultry_transfers.harvest_id
    → harvests.harvest_id
```

```text
farm_poultry_transfers.poultry_group_id
    → poultry_groups.poultry_group_id
```

Foreign-key delete and update behaviour must be explicitly decided before the final SQL schema is created.

# 43. Indexing Considerations

The final schema should consider indexes for:

* `users.username`
* `users.email`
* `beneficiaries.beneficiary_code`
* `beneficiaries.created_by`
* Foreign-key columns.
* Frequently searched statuses.
* Project assignments.
* Referral statuses.
* Poultry group identifiers.
* Transaction dates.
* Financial transaction dates.
* Audit event dates.

Indexes should be confirmed during SQL schema design rather than added indiscriminately.

# 44. Data Protection

ERA-IPMS will contain sensitive beneficiary and organisational information.

The database and application must support:

* Authentication.
* Password hashing.
* Backend access control.
* Record-level access.
* Audit information.
* Controlled updates.
* Archiving.
* Database backups.
* Secure production credentials.

Real beneficiary information must not be committed to the public GitHub repository.

Development and testing must use fictional or appropriately anonymised data.

# 45. Outstanding Validation Points

The following items remain requirements-validation issues:

1. Exact referral approval authority.
2. Exact project approval authority.
3. Exact financial approval rules.
4. Final referral status values.
5. Final project status values.
6. Final activity status values.
7. Exact M&E indicators.
8. Final MVP report list.
9. Notification priority.
10. Detailed project assignment rules.
11. Detailed activity assignment rules.
12. Post-submission editing rules.
13. Beneficiary archive and restoration authority.
14. Whether all poultry groups require separate operational tracking.
15. Exact financial categories and payment methods.

These items must not be silently invented in the final application.

# 46. Relationship to the ERD

The entities and relationships defined here will be represented visually in the Entity Relationship Diagram.

The ERD must show:

* Entities.
* Primary keys.
* Foreign keys.
* One-to-many relationships.
* Many-to-many relationships through junction entities.
* Major access-control relationships.
* Farm-to-poultry traceability.
* Finance relationships.
* Audit relationships.

The ERD must be generated from this approved logical design and should not introduce unrelated entities.

# 47. Relationship to SQL Schema

The final `database/schema.sql` must be derived from this entity design.

The implementation stage must define:

* Exact column types.
* Nullability.
* Defaults.
* Primary keys.
* Foreign keys.
* Unique constraints.
* Check constraints where supported.
* Indexes.
* Delete/update behaviour.
* Initial controlled values where appropriate.

SQL implementation must not precede agreement on the entity structure.

# 48. Relationship to Django Models

After the database design and SQL schema are approved, Django models should represent the approved database structure.

The application should not introduce undocumented database entities simply for programming convenience.

Where Django-specific technical tables are required by the framework, they should be distinguished from ERA business entities.

# 49. MVP Entity Scope

The MVP database should prioritise:

1. Users.
2. Titles.
3. Permissions.
4. Title permissions.
5. Responsibilities.
6. User responsibilities.
7. Staff Members.
8. User project assignments.
9. Beneficiaries.
10. Disability assessments.
11. Home visits.
12. Referrals.
13. Referral follow-ups.
14. Projects.
15. Activities.
16. Activity assignments.
17. Activity participants.
18. Poultry groups.
19. Poultry stock movements.
20. Egg production.
21. Feed records.
22. Poultry health records.
23. Poultry sales.
24. Farm crops.
25. Farm activities.
26. Harvests.
27. Farm-to-poultry transfers.
28. Financial transactions.
29. M&E indicators.
30. M&E indicator records.
31. Audit events.

# 50. Conclusion

The ERA-IPMS database entity design is based on the approved requirements and workflow architecture.

The design explicitly separates:

```text
TITLE
    ≠
PERMISSION
    ≠
RESPONSIBILITY
```

It also separates:

```text
OPERATIONAL RECORD
    ≠
FINANCIAL TRANSACTION
```

and:

```text
ACTIVITY ASSIGNMENT
    ≠
ACTIVITY PARTICIPATION
```

The design provides traceability across:

```text
FARM
  ↓
HARVEST
  ↓
FARM-TO-POULTRY TRANSFER
  ↓
POULTRY FEED
  ↓
POULTRY
  ↓
SALES / HEALTH / PRODUCTION
  ↓
FINANCE
```

and:

```text
BENEFICIARY
  ↓
ASSESSMENT
  ↓
HOME VISIT
  ↓
REFERRAL
  ↓
FOLLOW-UP
  ↓
OUTCOME
```

This document is the logical database baseline for the next stages:

1. ERD documentation.
2. ERD visual design.
3. SQL schema design.
4. Django model alignment.

No production database migration or application implementation should be performed until this entity design has been reviewed and committed as the approved Step 8 baseline.
