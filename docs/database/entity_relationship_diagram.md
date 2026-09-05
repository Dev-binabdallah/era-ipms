# ERA Integrated Project Management System (ERA-IPMS)

## Entity Relationship Diagram Specification

**Project:** ERA Integrated Project Management System (ERA-IPMS)  
**Document Type:** Entity Relationship Diagram Specification  
**Version:** 1.1  
**Date:** September 2026  
**Status:** Baseline for database schema derivation  

## 1. Purpose

This document defines the visual and logical ERD baseline derived from the approved Database Entity Design v1.1.

The ERD is the bridge between the entity design and the MariaDB/MySQL schema. It must show the approved entities, primary keys, foreign keys, and cardinality relationships without introducing application features that are not in the approved design.

## 2. Important v1.1 Model Rules

The ERD preserves these distinctions:

1. **Title is not Permission.**
2. **Permission is not Responsibility.**
3. Titles are expandable by administrators; permissions are application-defined.
4. Beneficiary access is record-level and is supported by accountable user relationships.
5. Beneficiary deletion is an archive/inactivation operation rather than routine physical deletion.
6. Activity assignment and activity participation are separate concepts.
7. Poultry stock is movement-based.
8. Farm harvests can be transferred to poultry through an explicit transfer record.
9. Operational records and financial transactions remain separate.
10. Audit events provide system accountability.

## 3. Approved Entities

The v1.1 ERD contains **31 entities**:

1. `users`
2. `titles`
3. `permissions`
4. `title_permissions`
5. `responsibilities`
6. `user_responsibilities`
7. `staff_members`
8. `user_project_assignments`
9. `beneficiaries`
10. `disability_assessments`
11. `home_visits`
12. `referrals`
13. `referral_follow_ups`
14. `projects`
15. `activities`
16. `activity_assignments`
17. `activity_participants`
18. `poultry_groups`
19. `poultry_stock_movements`
20. `egg_production`
21. `feed_records`
22. `poultry_health_records`
23. `poultry_sales`
24. `farm_crops`
25. `farm_activities`
26. `harvests`
27. `farm_poultry_transfers`
28. `financial_transactions`
29. `me_indicators`
30. `me_indicator_records`
31. `audit_events`

## 4. Relationship Diagram

The following Mermaid diagram is the source representation of the logical ERD. The Draw.io file in `docs/database/erd/` is the editable visual representation.

```mermaid
erDiagram
    TITLES ||--o{ USERS : assigned_to
    TITLES ||--o{ TITLE_PERMISSIONS : has
    PERMISSIONS ||--o{ TITLE_PERMISSIONS : grants
    USERS ||--o{ USER_RESPONSIBILITIES : has
    RESPONSIBILITIES ||--o{ USER_RESPONSIBILITIES : assigned
    USERS ||--o{ STAFF_MEMBERS : profile
    USERS ||--o{ USER_PROJECT_ASSIGNMENTS : assigned
    PROJECTS ||--o{ USER_PROJECT_ASSIGNMENTS : includes
    USERS ||--o{ BENEFICIARIES : creates
    BENEFICIARIES ||--o{ DISABILITY_ASSESSMENTS : has
    USERS ||--o{ DISABILITY_ASSESSMENTS : assesses
    BENEFICIARIES ||--o{ HOME_VISITS : receives
    USERS ||--o{ HOME_VISITS : conducts
    BENEFICIARIES ||--o{ REFERRALS : has
    USERS ||--o{ REFERRALS : creates
    REFERRALS ||--o{ REFERRAL_FOLLOW_UPS : has
    USERS ||--o{ REFERRAL_FOLLOW_UPS : conducts
    USERS ||--o{ PROJECTS : creates
    PROJECTS ||--o{ ACTIVITIES : contains
    USERS ||--o{ ACTIVITIES : responsible
    ACTIVITIES ||--o{ ACTIVITY_ASSIGNMENTS : has
    USERS ||--o{ ACTIVITY_ASSIGNMENTS : assigned
    ACTIVITIES ||--o{ ACTIVITY_PARTICIPANTS : has
    BENEFICIARIES ||--o{ ACTIVITY_PARTICIPANTS : participates
    PROJECTS ||--o{ POULTRY_GROUPS : contains
    POULTRY_GROUPS ||--o{ POULTRY_STOCK_MOVEMENTS : has
    USERS ||--o{ POULTRY_STOCK_MOVEMENTS : records
    POULTRY_GROUPS ||--o{ EGG_PRODUCTION : has
    USERS ||--o{ EGG_PRODUCTION : records
    POULTRY_GROUPS ||--o{ FEED_RECORDS : has
    USERS ||--o{ FEED_RECORDS : records
    POULTRY_GROUPS ||--o{ POULTRY_HEALTH_RECORDS : has
    USERS ||--o{ POULTRY_HEALTH_RECORDS : records
    POULTRY_GROUPS ||--o{ POULTRY_SALES : has
    USERS ||--o{ POULTRY_SALES : records
    PROJECTS ||--o{ FARM_CROPS : contains
    FARM_CROPS ||--o{ FARM_ACTIVITIES : has
    USERS ||--o{ FARM_ACTIVITIES : records
    FARM_CROPS ||--o{ HARVESTS : produces
    USERS ||--o{ HARVESTS : records
    HARVESTS ||--o{ FARM_POULTRY_TRANSFERS : source
    POULTRY_GROUPS ||--o{ FARM_POULTRY_TRANSFERS : receives
    USERS ||--o{ FARM_POULTRY_TRANSFERS : records
    PROJECTS ||--o{ FINANCIAL_TRANSACTIONS : has
    USERS ||--o{ FINANCIAL_TRANSACTIONS : records
    PROJECTS ||--o{ ME_INDICATORS : defines
    ME_INDICATORS ||--o{ ME_INDICATOR_RECORDS : records
    USERS ||--o{ ME_INDICATOR_RECORDS : records
    USERS ||--o{ AUDIT_EVENTS : generates

    USERS {
        user_id PK
    }
    TITLES {
        title_id PK
    }
    PERMISSIONS {
        permission_id PK
    }
    TITLE_PERMISSIONS {
        title_permission_id PK
        title_id FK
        permission_id FK
    }
    RESPONSIBILITIES {
        responsibility_id PK
    }
    USER_RESPONSIBILITIES {
        user_responsibility_id PK
        user_id FK
        responsibility_id FK
    }
    STAFF_MEMBERS {
        staff_member_id PK
        user_id FK
    }
    USER_PROJECT_ASSIGNMENTS {
        assignment_id PK
        user_id FK
        project_id FK
    }
    BENEFICIARIES {
        beneficiary_id PK
        created_by FK
    }
    DISABILITY_ASSESSMENTS {
        assessment_id PK
        beneficiary_id FK
        assessed_by FK
    }
    HOME_VISITS {
        home_visit_id PK
        beneficiary_id FK
        conducted_by FK
    }
    REFERRALS {
        referral_id PK
        beneficiary_id FK
        referred_by FK
    }
    REFERRAL_FOLLOW_UPS {
        follow_up_id PK
        referral_id FK
        conducted_by FK
    }
    PROJECTS {
        project_id PK
        created_by FK
    }
    ACTIVITIES {
        activity_id PK
        project_id FK
        responsible_user_id FK
    }
    ACTIVITY_ASSIGNMENTS {
        activity_assignment_id PK
        activity_id FK
        user_id FK
    }
    ACTIVITY_PARTICIPANTS {
        participant_id PK
        activity_id FK
        beneficiary_id FK
    }
    POULTRY_GROUPS {
        poultry_group_id PK
        project_id FK
    }
    POULTRY_STOCK_MOVEMENTS {
        movement_id PK
        poultry_group_id FK
        recorded_by FK
    }
    EGG_PRODUCTION {
        egg_production_id PK
        poultry_group_id FK
        recorded_by FK
    }
    FEED_RECORDS {
        feed_record_id PK
        poultry_group_id FK
        recorded_by FK
    }
    POULTRY_HEALTH_RECORDS {
        health_record_id PK
        poultry_group_id FK
        recorded_by FK
    }
    POULTRY_SALES {
        poultry_sale_id PK
        poultry_group_id FK
        recorded_by FK
    }
    FARM_CROPS {
        crop_id PK
        project_id FK
        recorded_by FK
    }
    FARM_ACTIVITIES {
        farm_activity_id PK
        crop_id FK
        recorded_by FK
    }
    HARVESTS {
        harvest_id PK
        crop_id FK
        recorded_by FK
    }
    FARM_POULTRY_TRANSFERS {
        transfer_id PK
        harvest_id FK
        poultry_group_id FK
        recorded_by FK
    }
    FINANCIAL_TRANSACTIONS {
        transaction_id PK
        project_id FK
        recorded_by FK
    }
    ME_INDICATORS {
        indicator_id PK
        project_id FK
    }
    ME_INDICATOR_RECORDS {
        indicator_record_id PK
        indicator_id FK
        recorded_by FK
    }
    AUDIT_EVENTS {
        audit_event_id PK
        user_id FK
    }
```

## 5. Relationship Groups

### 5.1 Access and Identity

- `titles` 1-to-many `users`
- `titles` 1-to-many `title_permissions`
- `permissions` 1-to-many `title_permissions`
- `users` 1-to-many `user_responsibilities`
- `responsibilities` 1-to-many `user_responsibilities`
- `users` 1-to-0/1 `staff_members`
- `users` and `projects` are linked through `user_project_assignments`

### 5.2 Beneficiary and Service Delivery

- `beneficiaries` 1-to-many `disability_assessments`
- `beneficiaries` 1-to-many `home_visits`
- `beneficiaries` 1-to-many `referrals`
- `referrals` 1-to-many `referral_follow_ups`
- `beneficiaries` and `activities` are linked through `activity_participants`
- User foreign keys identify who created, assessed, conducted, or referred.

### 5.3 Project and Activity Management

- `projects` 1-to-many `activities`
- `activities` 1-to-many `activity_assignments`
- `activities` 1-to-many `activity_participants`
- `users` are linked to projects and activities for accountability and access control.

### 5.4 Poultry

- `projects` 1-to-many `poultry_groups`
- `poultry_groups` 1-to-many `poultry_stock_movements`
- `poultry_groups` 1-to-many `egg_production`
- `poultry_groups` 1-to-many `feed_records`
- `poultry_groups` 1-to-many `poultry_health_records`
- `poultry_groups` 1-to-many `poultry_sales`

Stock is derived from movement records rather than maintained only as a manually edited balance.

### 5.5 Farm

- `projects` 1-to-many `farm_crops`
- `farm_crops` 1-to-many `farm_activities`
- `farm_crops` 1-to-many `harvests`
- `harvests` 1-to-many `farm_poultry_transfers`
- `poultry_groups` 1-to-many `farm_poultry_transfers`

This preserves traceability from crop production to harvest and, where applicable, poultry feed transfer.

### 5.6 Finance

- `projects` 1-to-many `financial_transactions`
- Financial transactions are separate from operational poultry and farm records.
- The initial finance scope is basic income and expense management, not full accounting.

### 5.7 Monitoring and Evaluation

- `projects` 1-to-many `me_indicators`
- `me_indicators` 1-to-many `me_indicator_records`

### 5.8 Audit

- `users` 1-to-many `audit_events`

## 6. Visual ERD Layout

The visual ERD is arranged in logical zones to reduce line crossings:

1. Access and identity
2. Beneficiary and service delivery
3. Projects and activities
4. Poultry
5. Farm
6. Finance
7. Monitoring and evaluation
8. Audit

The editable Draw.io source should remain the master visual artifact. PNG and PDF are presentation/export artifacts.

## 7. Validation Before SQL

Before creating `database/schema.sql`, confirm:

- Every v1.1 entity appears exactly once.
- Every PK appears in its entity.
- Every FK shown in the ERD exists in the referenced entity.
- Relationship cardinalities match the Database Entity Design.
- No legacy `roles` table remains.
- No legacy `staff_volunteers` table remains.
- No legacy `poultry_transactions` table remains.
- `poultry_groups` and movement-based stock are represented.
- `farm_poultry_transfers` is represented.
- `financial_transactions` replaces the legacy generic `expenses` design.
- `me_indicator_records` is represented.
- `audit_events` is represented.
- Activity assignments are separate from participants.

## 8. Legacy ERD Audit Result

The supplied previous ERD is not suitable as the v1.1 baseline. It visibly contains the old `ROLES`, `STAFF_VOLUNTEERS`, and legacy poultry/finance structures. The old Draw.io source also contains the older role-based model.

The v1.1 ERD therefore replaces the previous visual model rather than extending it incrementally.

## 9. Next Step

After the ERD baseline is reviewed and committed, proceed to **Step 10: `database/schema.sql`**.

No Django model migration or production database change is authorized by this document alone.
