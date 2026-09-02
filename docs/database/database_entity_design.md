# ERA Integrated Project Management System (ERA-IPMS)

# Database Entity Design

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** Database Design Specification
**Version:** 1.0
**Date:** September 2026
**Status:** Draft
**Prepared By:** Abdullahi Abdi Mohamed

# 1. Introduction

This document defines the main database entities for the ERA Integrated Project Management System (ERA-IPMS).

An entity represents an important type of information that the system needs to store.

For example:

* A beneficiary is an entity.
* A project is an entity.
* A home visit is an entity.
* A referral is an entity.

In the MySQL database, each entity will normally become a table.

This document defines:

* Database tables.
* Main fields.
* Primary keys.
* Foreign keys.
* Relationships.
* Important data rules.

The design is based on ERA's current operations and the approved system requirements and workflows.

# 2. Database Naming Standards

The database will follow these naming rules:

* Table names will use lowercase letters.
* Multiple words will use underscores.
* Table names will use plural nouns where appropriate.
* Primary keys will normally use the format `table_name_id`.
* Foreign keys will use the name of the referenced entity followed by `_id`.
* Dates will use the `DATE` data type where time is not required.
* Monetary values will use `DECIMAL`.
* Status values will use controlled values where appropriate.

Examples:

```text
beneficiaries
home_visits
referral_follow_ups
project_id
beneficiary_id
created_at
```

# 3. Entity Overview

The initial ERA-IPMS database will contain the following entities:

1. `roles`
2. `users`
3. `staff_volunteers`
4. `beneficiaries`
5. `disability_assessments`
6. `home_visits`
7. `referrals`
8. `referral_follow_ups`
9. `projects`
10. `activities`
11. `activity_participants`
12. `poultry_transactions`
13. `egg_production`
14. `feed_records`
15. `poultry_health_records`
16. `farm_crops`
17. `farm_activities`
18. `harvests`
19. `expenses`
20. `me_indicators`

# 4. Roles Entity

## Table Name

`roles`

## Purpose

Stores the different ERA-IPMS user roles.

## Fields

| Field         | Type         | Description                          |
| ------------- | ------------ | ------------------------------------ |
| `role_id`     | BIGINT       | Unique role identifier               |
| `role_name`   | VARCHAR(100) | Name of the role                     |
| `description` | TEXT         | Description of responsibilities      |
| `created_at`  | DATETIME     | Date and time the record was created |

## Primary Key

`role_id`

## Example Roles

* System Administrator
* ERA Management
* Programme / Project Coordinator
* Field Staff / Volunteer
* Farm Personnel
* Finance Personnel
* Monitoring & Evaluation Personnel

---

# 5. Users Entity

## Table Name

`users`

## Purpose

Stores system login accounts.

## Fields

| Field           | Type         | Description                             |
| --------------- | ------------ | --------------------------------------- |
| `user_id`       | BIGINT       | Unique user identifier                  |
| `role_id`       | BIGINT       | Assigned system role                    |
| `username`      | VARCHAR(100) | Login username                          |
| `email`         | VARCHAR(150) | User email                              |
| `password_hash` | VARCHAR(255) | Encrypted password                      |
| `is_active`     | BOOLEAN      | Indicates whether the account is active |
| `last_login`    | DATETIME     | Last login date and time                |
| `created_at`    | DATETIME     | Account creation date                   |

## Primary Key

`user_id`

## Foreign Key

`role_id` → `roles.role_id`

## Relationship

One role can be assigned to many users.

```text
roles
  1
  |
  |------ many
  |
users
```

# 6. Staff and Volunteers Entity

## Table Name

`staff_volunteers`

## Purpose

Stores information about ERA staff members and volunteers.

## Fields

| Field                | Type         | Description                         |
| -------------------- | ------------ | ----------------------------------- |
| `staff_volunteer_id` | BIGINT       | Unique identifier                   |
| `user_id`            | BIGINT       | Linked system user where applicable |
| `full_name`          | VARCHAR(150) | Full name                           |
| `person_type`        | VARCHAR(20)  | Staff or Volunteer                  |
| `phone`              | VARCHAR(30)  | Contact number                      |
| `email`              | VARCHAR(150) | Email address                       |
| `start_date`         | DATE         | Start date                          |
| `status`             | VARCHAR(30)  | Active or Inactive                  |
| `created_at`         | DATETIME     | Record creation date                |

## Primary Key

`staff_volunteer_id`

## Foreign Key

`user_id` → `users.user_id`

A staff or volunteer record may exist without a system account.

# 7. Beneficiaries Entity

## Table Name

`beneficiaries`

## Purpose

Stores information about people supported by ERA.

## Fields

| Field               | Type         | Description                           |
| ------------------- | ------------ | ------------------------------------- |
| `beneficiary_id`    | BIGINT       | Unique identifier                     |
| `beneficiary_code`  | VARCHAR(50)  | Unique beneficiary reference          |
| `first_name`        | VARCHAR(100) | First name                            |
| `last_name`         | VARCHAR(100) | Last name                             |
| `date_of_birth`     | DATE         | Date of birth                         |
| `sex`               | VARCHAR(20)  | Sex                                   |
| `location`          | VARCHAR(150) | General location                      |
| `phone`             | VARCHAR(30)  | Contact information where appropriate |
| `registration_date` | DATE         | Date registered                       |
| `status`            | VARCHAR(30)  | Active or Inactive                    |
| `created_by`        | BIGINT       | User who created the record           |
| `created_at`        | DATETIME     | Record creation date                  |
| `updated_at`        | DATETIME     | Last update                           |

## Primary Key

`beneficiary_id`

## Foreign Key

`created_by` → `users.user_id`

# 8. Disability Assessments Entity

## Table Name

`disability_assessments`

## Purpose

Stores assessment information for beneficiaries who require disability-related support.

## Fields

| Field              | Type         | Description                    |
| ------------------ | ------------ | ------------------------------ |
| `assessment_id`    | BIGINT       | Unique assessment identifier   |
| `beneficiary_id`   | BIGINT       | Beneficiary being assessed     |
| `assessment_date`  | DATE         | Assessment date                |
| `assessment_type`  | VARCHAR(100) | Type or category of assessment |
| `disability_type`  | VARCHAR(150) | Type of disability             |
| `needs`            | TEXT         | Identified needs               |
| `assessment_notes` | TEXT         | Additional notes               |
| `assessed_by`      | BIGINT       | User conducting assessment     |
| `created_at`       | DATETIME     | Record creation date           |

## Primary Key

`assessment_id`

## Foreign Keys

`beneficiary_id` → `beneficiaries.beneficiary_id`

`assessed_by` → `users.user_id`

## Relationship

One beneficiary may have multiple assessments.

# 9. Home Visits Entity

## Table Name

`home_visits`

## Purpose

Stores records of home visits conducted for beneficiaries.

## Fields

| Field                | Type         | Description                   |
| -------------------- | ------------ | ----------------------------- |
| `home_visit_id`      | BIGINT       | Unique visit identifier       |
| `beneficiary_id`     | BIGINT       | Beneficiary visited           |
| `visit_date`         | DATE         | Date of visit                 |
| `conducted_by`       | BIGINT       | User conducting visit         |
| `purpose`            | VARCHAR(255) | Purpose of visit              |
| `observations`       | TEXT         | Visit observations            |
| `support_provided`   | TEXT         | Support provided              |
| `follow_up_required` | BOOLEAN      | Whether follow-up is required |
| `next_action`        | TEXT         | Required next action          |
| `created_at`         | DATETIME     | Record creation date          |

## Primary Key

`home_visit_id`

## Foreign Keys

`beneficiary_id` → `beneficiaries.beneficiary_id`

`conducted_by` → `users.user_id`

# 10. Referrals Entity

## Table Name

`referrals`

## Purpose

Stores referrals made for beneficiaries.

## Fields

| Field                  | Type         | Description                |
| ---------------------- | ------------ | -------------------------- |
| `referral_id`          | BIGINT       | Unique referral identifier |
| `beneficiary_id`       | BIGINT       | Beneficiary being referred |
| `referral_date`        | DATE         | Referral date              |
| `referral_destination` | VARCHAR(200) | Organisation or service    |
| `reason`               | TEXT         | Reason for referral        |
| `referred_by`          | BIGINT       | User making referral       |
| `status`               | VARCHAR(50)  | Current referral status    |
| `created_at`           | DATETIME     | Record creation date       |

## Primary Key

`referral_id`

## Foreign Keys

`beneficiary_id` → `beneficiaries.beneficiary_id`

`referred_by` → `users.user_id`

## Suggested Statuses

* Pending
* Follow-up Required
* Completed
* Not Completed
* Cancelled

# 11. Referral Follow-Ups Entity

## Table Name

`referral_follow_ups`

## Purpose

Stores follow-up information for referrals.

## Fields

| Field              | Type     | Description                  |
| ------------------ | -------- | ---------------------------- |
| `follow_up_id`     | BIGINT   | Unique follow-up identifier  |
| `referral_id`      | BIGINT   | Referral being followed up   |
| `follow_up_date`   | DATE     | Follow-up date               |
| `conducted_by`     | BIGINT   | User conducting follow-up    |
| `outcome`          | TEXT     | Outcome of follow-up         |
| `service_received` | BOOLEAN  | Whether service was received |
| `remaining_needs`  | TEXT     | Remaining needs              |
| `next_action`      | TEXT     | Next action                  |
| `created_at`       | DATETIME | Record creation date         |

## Primary Key

`follow_up_id`

## Foreign Keys

`referral_id` → `referrals.referral_id`

`conducted_by` → `users.user_id`

One referral may have multiple follow-ups.

# 12. Projects Entity

## Table Name

`projects`

## Purpose

Stores ERA projects.

## Fields

| Field                 | Type         | Description               |
| --------------------- | ------------ | ------------------------- |
| `project_id`          | BIGINT       | Unique project identifier |
| `project_name`        | VARCHAR(200) | Project name              |
| `description`         | TEXT         | Project description       |
| `start_date`          | DATE         | Project start date        |
| `end_date`            | DATE         | Project end date          |
| `objectives`          | TEXT         | Project objectives        |
| `status`              | VARCHAR(30)  | Project status            |
| `responsible_user_id` | BIGINT       | Responsible user          |
| `created_at`          | DATETIME     | Record creation date      |

## Primary Key

`project_id`

## Foreign Key

`responsible_user_id` → `users.user_id`

# 13. Activities Entity

## Table Name

`activities`

## Purpose

Stores project and organisational activities.

## Fields

| Field                 | Type         | Description                |
| --------------------- | ------------ | -------------------------- |
| `activity_id`         | BIGINT       | Unique activity identifier |
| `project_id`          | BIGINT       | Related project            |
| `activity_name`       | VARCHAR(200) | Name of activity           |
| `activity_date`       | DATE         | Activity date              |
| `location`            | VARCHAR(150) | Activity location          |
| `responsible_user_id` | BIGINT       | Responsible user           |
| `description`         | TEXT         | Activity description       |
| `status`              | VARCHAR(30)  | Activity status            |
| `results`             | TEXT         | Activity results           |
| `created_at`          | DATETIME     | Record creation date       |

## Primary Key

`activity_id`

## Foreign Keys

`project_id` → `projects.project_id`

`responsible_user_id` → `users.user_id`

One project may have many activities.

# 14. Activity Participants Entity

## Table Name

`activity_participants`

## Purpose

Stores participant information for activities.

## Fields

| Field              | Type         | Description                              |
| ------------------ | ------------ | ---------------------------------------- |
| `participant_id`   | BIGINT       | Unique identifier                        |
| `activity_id`      | BIGINT       | Related activity                         |
| `beneficiary_id`   | BIGINT       | Beneficiary participant where applicable |
| `participant_name` | VARCHAR(150) | Participant name                         |
| `participant_type` | VARCHAR(50)  | Beneficiary, Staff, Volunteer, or Other  |
| `created_at`       | DATETIME     | Record creation date                     |

## Primary Key

`participant_id`

## Foreign Keys

`activity_id` → `activities.activity_id`

`beneficiary_id` → `beneficiaries.beneficiary_id`

# 15. Poultry Transactions Entity

## Table Name

`poultry_transactions`

## Purpose

Records all changes to poultry stock.

## Fields

| Field                    | Type         | Description                                                |
| ------------------------ | ------------ | ---------------------------------------------------------- |
| `poultry_transaction_id` | BIGINT       | Unique identifier                                          |
| `transaction_date`       | DATE         | Transaction date                                           |
| `transaction_type`       | VARCHAR(50)  | Opening Stock, Purchase, Received, Sale, Death, Adjustment |
| `quantity`               | INT          | Number of chickens                                         |
| `chicken_type`           | VARCHAR(100) | Local, Kienyeji, or other                                  |
| `description`            | TEXT         | Additional details                                         |
| `recorded_by`            | BIGINT       | User recording transaction                                 |
| `created_at`             | DATETIME     | Record creation date                                       |

## Primary Key

`poultry_transaction_id`

## Foreign Key

`recorded_by` → `users.user_id`

# 16. Egg Production Entity

## Table Name

`egg_production`

## Purpose

Stores egg production information.

## Fields

| Field               | Type     | Description          |
| ------------------- | -------- | -------------------- |
| `egg_production_id` | BIGINT   | Unique identifier    |
| `production_date`   | DATE     | Production date      |
| `eggs_produced`     | INT      | Total eggs produced  |
| `eggs_used`         | INT      | Eggs used            |
| `eggs_sold`         | INT      | Eggs sold            |
| `eggs_remaining`    | INT      | Remaining eggs       |
| `recorded_by`       | BIGINT   | User recording data  |
| `created_at`        | DATETIME | Record creation date |

## Primary Key

`egg_production_id`

## Foreign Key

`recorded_by` → `users.user_id`

# 17. Feed Records Entity

## Table Name

`feed_records`

## Purpose

Stores poultry feed information.

## Fields

| Field              | Type          | Description              |
| ------------------ | ------------- | ------------------------ |
| `feed_record_id`   | BIGINT        | Unique identifier        |
| `record_date`      | DATE          | Record date              |
| `feed_source`      | VARCHAR(100)  | Farm, Purchase, or Other |
| `feed_description` | VARCHAR(200)  | Description of feed      |
| `quantity`         | DECIMAL(10,2) | Feed quantity            |
| `unit`             | VARCHAR(30)   | Kilograms, bags, etc.    |
| `cost`             | DECIMAL(12,2) | Cost where applicable    |
| `recorded_by`      | BIGINT        | User recording data      |
| `created_at`       | DATETIME      | Record creation date     |

## Primary Key

`feed_record_id`

## Foreign Key

`recorded_by` → `users.user_id`

# 18. Poultry Health Records Entity

## Table Name

`poultry_health_records`

## Purpose

Stores poultry illness and health information.

## Fields

| Field              | Type        | Description                 |
| ------------------ | ----------- | --------------------------- |
| `health_record_id` | BIGINT      | Unique identifier           |
| `record_date`      | DATE        | Date problem identified     |
| `condition_type`   | VARCHAR(50) | Illness or Other            |
| `number_affected`  | INT         | Number of chickens affected |
| `description`      | TEXT        | Condition description       |
| `action_taken`     | TEXT        | Action taken                |
| `outcome`          | TEXT        | Outcome                     |
| `recorded_by`      | BIGINT      | User recording information  |
| `created_at`       | DATETIME    | Record creation date        |

## Primary Key

`health_record_id`

## Foreign Key

`recorded_by` → `users.user_id`

Poultry deaths will primarily be recorded in `poultry_transactions` because deaths affect stock numbers.

# 19. Farm Crops Entity

## Table Name

`farm_crops`

## Purpose

Stores crops grown on the ERA farm.

## Fields

| Field           | Type         | Description                |
| --------------- | ------------ | -------------------------- |
| `crop_id`       | BIGINT       | Unique crop identifier     |
| `crop_name`     | VARCHAR(100) | Name of crop               |
| `description`   | TEXT         | Additional details         |
| `planting_date` | DATE         | Date planted               |
| `status`        | VARCHAR(30)  | Growing, Harvested, etc.   |
| `recorded_by`   | BIGINT       | User recording information |
| `created_at`    | DATETIME     | Record creation date       |

## Primary Key

`crop_id`

## Foreign Key

`recorded_by` → `users.user_id`

# 20. Farm Activities Entity

## Table Name

`farm_activities`

## Purpose

Stores farm activities.

## Fields

| Field              | Type         | Description                                   |
| ------------------ | ------------ | --------------------------------------------- |
| `farm_activity_id` | BIGINT       | Unique identifier                             |
| `crop_id`          | BIGINT       | Related crop                                  |
| `activity_date`    | DATE         | Date of activity                              |
| `activity_type`    | VARCHAR(100) | Planting, Watering, Weeding, Harvesting, etc. |
| `description`      | TEXT         | Activity details                              |
| `conducted_by`     | BIGINT       | User responsible                              |
| `created_at`       | DATETIME     | Record creation date                          |

## Primary Key

`farm_activity_id`

## Foreign Keys

`crop_id` → `farm_crops.crop_id`

`conducted_by` → `users.user_id`

# 21. Harvests Entity

## Table Name

`harvests`

## Purpose

Stores farm harvest information.

## Fields

| Field          | Type          | Description                      |
| -------------- | ------------- | -------------------------------- |
| `harvest_id`   | BIGINT        | Unique harvest identifier        |
| `crop_id`      | BIGINT        | Crop harvested                   |
| `harvest_date` | DATE          | Harvest date                     |
| `quantity`     | DECIMAL(10,2) | Harvest quantity                 |
| `unit`         | VARCHAR(30)   | Kilograms, pieces, bunches, etc. |
| `usage`        | VARCHAR(100)  | Poultry, ERA use, Sale, Other    |
| `notes`        | TEXT          | Additional information           |
| `recorded_by`  | BIGINT        | User recording information       |
| `created_at`   | DATETIME      | Record creation date             |

## Primary Key

`harvest_id`

## Foreign Keys

`crop_id` → `farm_crops.crop_id`

`recorded_by` → `users.user_id`

# 22. Expenses Entity

## Table Name

`expenses`

## Purpose

Stores organisational, project, farm, and poultry expenses.

## Fields

| Field            | Type          | Description                          |
| ---------------- | ------------- | ------------------------------------ |
| `expense_id`     | BIGINT        | Unique expense identifier            |
| `expense_date`   | DATE          | Date of expense                      |
| `category`       | VARCHAR(100)  | Expense category                     |
| `amount`         | DECIMAL(12,2) | Expense amount                       |
| `description`    | TEXT          | Expense description                  |
| `project_id`     | BIGINT        | Related project where applicable     |
| `expense_area`   | VARCHAR(50)   | Organisation, Poultry, Farm, Project |
| `payment_method` | VARCHAR(50)   | Cash, Bank, Mobile Money, etc.       |
| `recorded_by`    | BIGINT        | User recording expense               |
| `created_at`     | DATETIME      | Record creation date                 |

## Primary Key

`expense_id`

## Foreign Keys

`project_id` → `projects.project_id`

`recorded_by` → `users.user_id`

# 23. Monitoring and Evaluation Indicators Entity

## Table Name

`me_indicators`

## Purpose

Stores key indicators used for monitoring projects and organisational performance.

## Fields

| Field            | Type          | Description                        |
| ---------------- | ------------- | ---------------------------------- |
| `indicator_id`   | BIGINT        | Unique indicator identifier        |
| `project_id`     | BIGINT        | Related project where applicable   |
| `indicator_name` | VARCHAR(200)  | Name of indicator                  |
| `description`    | TEXT          | Indicator description              |
| `target_value`   | DECIMAL(12,2) | Target                             |
| `current_value`  | DECIMAL(12,2) | Current value                      |
| `unit`           | VARCHAR(50)   | People, Activities, Chickens, etc. |
| `start_date`     | DATE          | Measurement start                  |
| `end_date`       | DATE          | Measurement end                    |
| `recorded_by`    | BIGINT        | User recording indicator           |
| `created_at`     | DATETIME      | Record creation date               |

## Primary Key

`indicator_id`

## Foreign Keys

`project_id` → `projects.project_id`

`recorded_by` → `users.user_id`

# 24. Summary of Main Relationships

The main database relationships are:

```text
roles
  |
  └──< users
         |
         ├──< beneficiaries
         ├──< disability_assessments
         ├──< home_visits
         ├──< referrals
         ├──< referral_follow_ups
         ├──< projects
         ├──< activities
         ├──< poultry_transactions
         ├──< egg_production
         ├──< feed_records
         ├──< poultry_health_records
         ├──< farm_crops
         ├──< farm_activities
         ├──< harvests
         ├──< expenses
         └──< me_indicators


beneficiaries
  |
  ├──< disability_assessments
  ├──< home_visits
  ├──< referrals
  └──< activity_participants


referrals
  |
  └──< referral_follow_ups


projects
  |
  ├──< activities
  ├──< expenses
  └──< me_indicators


activities
  |
  └──< activity_participants


farm_crops
  |
  ├──< farm_activities
  └──< harvests
```

# 25. Important Data Rules

The following rules should apply to the database.

## Beneficiaries

* `beneficiary_code` must be unique.
* Required identification fields should not be empty.
* Duplicate beneficiaries should be avoided.

## Users

* `username` must be unique.
* `email` should be unique where provided.
* Passwords must never be stored as plain text.

## Poultry

* Quantities must not be negative.
* Transaction types should use controlled values.
* Deaths and sales must reduce poultry stock.

## Eggs

* Egg quantities must not be negative.
* Eggs used and sold should not exceed available eggs.

## Finance

* Expense amounts must be greater than zero.
* Expenses should have a valid date.
* Users should only record expenses they are authorised to manage.

## Referrals

* Every referral must belong to a beneficiary.
* A referral should have a status.
* Follow-ups must belong to an existing referral.

# 26. Data Protection Considerations

ERA-IPMS will contain sensitive beneficiary information.

The database design should therefore support:

* Role-based access.
* User authentication.
* Password hashing.
* Restricted access to sensitive records.
* Database backups.
* Controlled data updates.
* Audit information such as record creator and creation date.

Real beneficiary data must not be uploaded to the public GitHub repository.

Development and testing should use fictional data.