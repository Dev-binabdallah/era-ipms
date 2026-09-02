# ERA Integrated Project Management System (ERA-IPMS)

## Entity Relationship Diagram Specification

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** Entity Relationship Diagram Specification
**Version:** 1.0
**Date:** September 2026
**Status:** Draft
**Prepared By:** Abdullahi Abdi Mohamed

## 1. Purpose

This document defines the relationships between the database entities of the ERA Integrated Project Management System (ERA-IPMS).

It explains how the tables connect through primary keys and foreign keys.

This document will be used as the reference for creating the visual Entity Relationship Diagram (ERD) and the MySQL database schema.

## 2. Relationship Notation

The following notation is used:

```text
1 ─────< Many
```

This means one record in the first table can be related to many records in the second table.

For example:

```text
BENEFICIARIES 1 ─────< HOME_VISITS
```

This means one beneficiary can have many home visit records.

The foreign key is stored in the `home_visits` table:

```text
home_visits.beneficiary_id
```

This references:

```text
beneficiaries.beneficiary_id
```

# 3. User Management Relationships

## 3.1 Roles and Users

```text
ROLES 1 ─────< USERS
```

One role can be assigned to many users.

Each user must have one assigned role.

**Relationship:**

```text
roles.role_id
        │
        └──────< users.role_id
```

## 3.2 Users and Staff/Volunteers

```text
USERS 1 ───── 0..1 STAFF_VOLUNTEERS
```

A system user can be linked to one staff or volunteer record.

A staff or volunteer may exist in the system without having a user login account.

**Relationship:**

```text
users.user_id
        │
        └──────── staff_volunteers.user_id
```

# 4. Beneficiary and Disability Management Relationships

## 4.1 Beneficiaries and Disability Assessments

```text
BENEFICIARIES 1 ─────< DISABILITY_ASSESSMENTS
```

One beneficiary may have one or more disability assessments.

Each disability assessment belongs to one beneficiary.

**Foreign Key:**

```text
disability_assessments.beneficiary_id
→ beneficiaries.beneficiary_id
```

## 4.2 Beneficiaries and Home Visits

```text
BENEFICIARIES 1 ─────< HOME_VISITS
```

One beneficiary may receive multiple home visits.

Each home visit belongs to one beneficiary.

**Foreign Key:**

```text
home_visits.beneficiary_id
→ beneficiaries.beneficiary_id
```

## 4.3 Beneficiaries and Referrals

```text
BENEFICIARIES 1 ─────< REFERRALS
```

One beneficiary may receive multiple referrals.

Each referral belongs to one beneficiary.

**Foreign Key:**

```text
referrals.beneficiary_id
→ beneficiaries.beneficiary_id
```

## 4.4 Referrals and Referral Follow-Ups

```text
REFERRALS 1 ─────< REFERRAL_FOLLOW_UPS
```

One referral may have multiple follow-up records.

Each follow-up record belongs to one referral.

**Foreign Key:**

```text
referral_follow_ups.referral_id
→ referrals.referral_id
```

# 5. Project and Activity Management Relationships

## 5.1 Projects and Activities

```text
PROJECTS 1 ─────< ACTIVITIES
```

One project can have many activities.

Each activity belongs to one project.

**Foreign Key:**

```text
activities.project_id
→ projects.project_id
```

## 5.2 Activities and Activity Participants

```text
ACTIVITIES 1 ─────< ACTIVITY_PARTICIPANTS
```

One activity can have many participants.

Each participant record belongs to one activity.

**Foreign Key:**

```text
activity_participants.activity_id
→ activities.activity_id
```

## 5.3 Beneficiaries and Activity Participants

```text
BENEFICIARIES 1 ─────< ACTIVITY_PARTICIPANTS
```

A beneficiary may participate in multiple activities.

The `activity_participants` table connects beneficiaries to activities.

This creates a many-to-many relationship:

```text
BENEFICIARIES >────< ACTIVITIES
```

The relationship is implemented using:

```text
ACTIVITY_PARTICIPANTS
```

# 6. Poultry Management Relationships

The poultry module currently contains four operational tables:

```text
POULTRY_TRANSACTIONS
EGG_PRODUCTION
FEED_RECORDS
POULTRY_HEALTH_RECORDS
```

At the initial stage, these tables do not require direct foreign-key relationships with each other.

Each record is connected to the user who created it.

```text
USERS 1 ─────< POULTRY_TRANSACTIONS

USERS 1 ─────< EGG_PRODUCTION

USERS 1 ─────< FEED_RECORDS

USERS 1 ─────< POULTRY_HEALTH_RECORDS
```

Poultry deaths are recorded in `poultry_transactions` because they directly affect the total poultry stock.

The current poultry stock will be calculated from poultry transactions such as:

* Opening stock
* Purchase
* Received
* Sale
* Death
* Adjustment

# 7. Farm Management Relationships

## 7.1 Farm Crops and Farm Activities

```text
FARM_CROPS 1 ─────< FARM_ACTIVITIES
```

One crop can have many farm activities.

For example:

* Planting
* Watering
* Weeding
* Fertilising
* Harvesting

**Foreign Key:**

```text
farm_activities.crop_id
→ farm_crops.crop_id
```

## 7.2 Farm Crops and Harvests

```text
FARM_CROPS 1 ─────< HARVESTS
```

One crop may have multiple harvest records.

**Foreign Key:**

```text
harvests.crop_id
→ farm_crops.crop_id
```

The harvest can be recorded as being used for:

* Poultry feed
* ERA organisational use
* Sale
* Other purposes

# 8. Finance Relationships

## 8.1 Projects and Expenses

```text
PROJECTS 1 ─────< EXPENSES
```

One project may have many expenses.

An organisational, farm, or poultry expense may not always belong to a specific project.

Therefore, `expenses.project_id` may be optional.

**Foreign Key:**

```text
expenses.project_id
→ projects.project_id
```

# 9. Monitoring and Evaluation Relationships

## 9.1 Projects and M&E Indicators

```text
PROJECTS 1 ─────< ME_INDICATORS
```

One project may have multiple monitoring and evaluation indicators.

An organisational indicator may exist without being connected to a specific project.

Therefore, `me_indicators.project_id` may be optional.

**Foreign Key:**

```text
me_indicators.project_id
→ projects.project_id
```

# 10. User Audit Relationships

The `users` table is connected to many operational records because the system needs to know who created, conducted, or recorded an activity.

The following relationships apply:

```text
USERS 1 ─────< BENEFICIARIES
USERS 1 ─────< DISABILITY_ASSESSMENTS
USERS 1 ─────< HOME_VISITS
USERS 1 ─────< REFERRALS
USERS 1 ─────< REFERRAL_FOLLOW_UPS
USERS 1 ─────< PROJECTS
USERS 1 ─────< ACTIVITIES
USERS 1 ─────< POULTRY_TRANSACTIONS
USERS 1 ─────< EGG_PRODUCTION
USERS 1 ─────< FEED_RECORDS
USERS 1 ─────< POULTRY_HEALTH_RECORDS
USERS 1 ─────< FARM_CROPS
USERS 1 ─────< FARM_ACTIVITIES
USERS 1 ─────< HARVESTS
USERS 1 ─────< EXPENSES
USERS 1 ─────< ME_INDICATORS
```

These relationships provide basic accountability and help identify who created or managed a record.

# 11. Complete Relationship Summary

The main relationships in the ERA-IPMS database are:

```text
ROLES
  └────< USERS

USERS
  └──── STAFF_VOLUNTEERS

BENEFICIARIES
  ├────< DISABILITY_ASSESSMENTS
  ├────< HOME_VISITS
  ├────< REFERRALS
  └────< ACTIVITY_PARTICIPANTS

REFERRALS
  └────< REFERRAL_FOLLOW_UPS

PROJECTS
  ├────< ACTIVITIES
  ├────< EXPENSES
  └────< ME_INDICATORS

ACTIVITIES
  └────< ACTIVITY_PARTICIPANTS

FARM_CROPS
  ├────< FARM_ACTIVITIES
  └────< HARVESTS
```

In addition, the `users` table is connected to operational records through fields such as:

```text
created_by
assessed_by
conducted_by
referred_by
responsible_user_id
recorded_by
```

# 12. Core Database Relationship Model

The simplified structure of ERA-IPMS is:

```text
                         ROLES
                           │
                           │ 1
                           ▼
                         USERS
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
 STAFF_VOLUNTEERS    BENEFICIARIES        PROJECTS
                         │                   │
          ┌──────────────┼───────┐           │
          │              │       │           │
          ▼              ▼       ▼           ▼
    ASSESSMENTS    HOME_VISITS  REFERRALS  ACTIVITIES
                                  │           │
                                  ▼           ▼
                               FOLLOW-UPS  PARTICIPANTS
                                               ▲
                                               │
                                         BENEFICIARIES


FARM_CROPS
    │
    ├────< FARM_ACTIVITIES
    │
    └────< HARVESTS


PROJECTS
    │
    ├────< EXPENSES
    │
    └────< ME_INDICATORS


POULTRY MODULE
    │
    ├──── POULTRY_TRANSACTIONS
    ├──── EGG_PRODUCTION
    ├──── FEED_RECORDS
    └──── POULTRY_HEALTH_RECORDS
```

# 13. Design Decisions

The following design decisions have been made for Version 1 of ERA-IPMS:

1. Field Staff and Volunteers will share the same system access role.

2. Staff and volunteer information will be stored separately from user login accounts.

3. A beneficiary may have multiple assessments, home visits, and referrals.

4. A referral may have multiple follow-up records.

5. Beneficiaries and activities have a many-to-many relationship implemented through `activity_participants`.

6. Poultry stock will be calculated from transaction records rather than manually storing only one current stock number.

7. Farm harvests can be marked according to how they are used, including poultry feed.

8. Expenses may be connected to a project, poultry activities, farm activities, or general organisational operations.

9. M&E indicators may belong to a specific project or to ERA's general organisational monitoring.

10. The `users` table will provide accountability by recording which user created or managed operational records.

# 14. Next Step

After this relationship specification is reviewed, the next step is to create the visual Entity Relationship Diagram.

The visual ERD will:

* Show all database tables.
* Show primary keys.
* Show foreign keys.
* Display one-to-many relationships.
* Display the many-to-many relationship between beneficiaries and activities.
* Provide the final database blueprint before MySQL implementation.

The visual ERD will be created using Draw.io and stored in:

```text
docs/database/erd/
```

The completed ERD will then be used to create:

```text
database/schema.sql
```