# ERA Integrated Project Management System (ERA-IPMS)

## User Roles and Permissions

### Document Information

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** User Roles and Permissions
**Version:** 1.0
**Date:** September 2026
**Prepared By:** Abdullahi Abdi Mohamed

# 1. Introduction

ERA-IPMS will be used by different people with different responsibilities within Emergency Response Aid (ERA).

Because the system will contain beneficiary, disability, project, poultry, farm, financial, staff, volunteer, and organisational information, users must not automatically have access to everything in the system.

The system will use **role-based access control (RBAC)**. Each user will be assigned a role, and the role will determine which parts of the system the user can access and what actions they can perform.

ERA-IPMS will initially have seven user roles:

1. System Administrator
2. ERA Management
3. Programme / Project Coordinator
4. Field Staff / Volunteer
5. Farm Personnel
6. Finance Personnel
7. Monitoring & Evaluation Personnel

# 2. Purpose

The purpose of this document is to:

* Define the official ERA-IPMS user roles.
* Define the responsibilities of each role.
* Define what information each role can access.
* Define what actions each role can perform.
* Protect confidential information.
* Prevent unauthorised access.
* Provide a foundation for implementing authentication and permissions.

# 3. Permission Types

ERA-IPMS will use the following basic permission types.

| Permission | Meaning                                           |
| ---------- | ------------------------------------------------- |
| View       | User can view authorised information              |
| Add        | User can create new records                       |
| Edit       | User can modify authorised records                |
| Delete     | User can delete records where permitted           |
| Approve    | User can approve authorised records or activities |
| Export     | User can export authorised information            |
| Manage     | User has broader control over a module            |
| Administer | User can manage system-level functions            |

Permissions will be assigned according to the user's role and responsibilities.

# 4. Role 1 - System Administrator

## 4.1 Purpose

The System Administrator is responsible for the technical and administrative operation of ERA-IPMS.

This role is primarily concerned with managing the system itself rather than managing individual programme activities.

## 4.2 Main Responsibilities

The System Administrator may:

* Manage user accounts.
* Create user accounts.
* Disable or activate user accounts.
* Assign user roles.
* Reset user passwords.
* Manage system settings.
* Maintain system configuration.
* Monitor system operation.
* Support troubleshooting.
* Manage authorised technical functions.
* Support backups and system maintenance.
* Monitor system security.

## 4.3 Access

The System Administrator has the highest technical access level.

The System Administrator can:

* View system modules.
* Manage users.
* Manage roles and permissions.
* Access system settings.
* View system records where technically required.
* Maintain the database and application.

However, technical access must not be interpreted as unrestricted permission to use beneficiary or financial information for purposes outside ERA's authorised operations.

## 4.4 Main Permissions

| Function           | Permission  |
| ------------------ | ----------- |
| Manage Users       | Manage      |
| Manage Roles       | Manage      |
| System Settings    | Manage      |
| Beneficiaries      | Manage      |
| Disability Records | Manage      |
| Home Visits        | Manage      |
| Referrals          | Manage      |
| Follow-Ups         | Manage      |
| Projects           | Manage      |
| Activities         | Manage      |
| Poultry            | Manage      |
| Farm               | Manage      |
| Finance            | Manage      |
| Reports            | Manage      |
| Dashboard          | Full Access |

# 5. Role 2 - ERA Management

## 5.1 Purpose

ERA Management uses ERA-IPMS to monitor organisational performance, review activities, support decision-making, and access management information.

## 5.2 Main Responsibilities

Management should be able to:

* Monitor organisational activities.
* Review beneficiary information and statistics.
* Monitor disability services.
* Review referrals and follow-ups.
* Monitor poultry performance.
* Monitor farm activities.
* Review financial information.
* Review staff and volunteer information.
* Review project performance.
* Review reports.
* Monitor upcoming and pending activities.

## 5.3 Dashboard Access

Management should have access to a comprehensive dashboard showing:

* Total beneficiaries.
* Home visits.
* Referrals.
* Completed follow-ups.
* Pending follow-ups.
* Current chickens.
* Egg production.
* Feed information.
* Poultry deaths and illnesses.
* Farm crops.
* Harvests.
* Farm expenses.
* Project expenses.
* Organisational expenses.
* Number of activities.
* Staff and volunteer numbers.
* Upcoming activities.
* Pending activities.

## 5.4 Main Permissions

| Function             | Permission                      |
| -------------------- | ------------------------------- |
| Dashboard            | Full View                       |
| Beneficiaries        | View                            |
| Disability Records   | View                            |
| Home Visits          | View                            |
| Referrals            | View                            |
| Follow-Ups           | View                            |
| Projects             | View                            |
| Activities           | View / Approve where authorised |
| Poultry              | View                            |
| Farm                 | View                            |
| Finance              | View / Approve where authorised |
| Staff and Volunteers | View                            |
| Reports              | View / Generate                 |
| Export Reports       | Export                          |
| User Management      | No                              |
| System Settings      | No                              |

Management should generally review information rather than directly edit operational records.

# 6. Role 3 - Programme / Project Coordinator

## 6.1 Purpose

The Programme / Project Coordinator manages ERA projects, activities, implementation processes, and programme information.

## 6.2 Main Responsibilities

The Programme / Project Coordinator may:

* Create projects.
* Update project information.
* Plan activities.
* Record activities.
* Monitor activity implementation.
* Assign activities to staff or volunteers.
* Review beneficiary services.
* Review home visits.
* Monitor referrals.
* Monitor follow-ups.
* Prepare project reports.
* Track project progress.

## 6.3 Main Permissions

| Function             | Permission                       |
| -------------------- | -------------------------------- |
| Dashboard            | View                             |
| Beneficiaries        | View / Add / Edit                |
| Disability Records   | View / Add / Edit                |
| Home Visits          | View / Add / Edit                |
| Referrals            | View / Add / Edit                |
| Follow-Ups           | View / Add / Edit                |
| Projects             | Manage                           |
| Activities           | Manage                           |
| Poultry              | View                             |
| Farm                 | View                             |
| Finance              | View authorised project expenses |
| Staff and Volunteers | View / Assign Activities         |
| Reports              | Generate                         |
| Export Reports       | Export                           |
| User Management      | No                               |
| System Settings      | No                               |

# 7. Role 4 - Field Staff / Volunteer

## 7.1 Purpose

Field Staff and Volunteers will have the **same system role and access level**.

They support ERA's community and field activities.

Their work may include beneficiary registration, assessments, home visits, referrals, follow-ups, community awareness, and other assigned activities.

## 7.2 Main Responsibilities

Field Staff / Volunteers may:

* Register beneficiaries.
* Record disability assessments.
* Record home visits.
* Create referrals.
* Follow up referrals.
* Record follow-up outcomes.
* Participate in community activities.
* Record assigned activities.
* Update authorised beneficiary information.
* Report field information.

## 7.3 Access Principle

Field Staff / Volunteers should have access to the information required to perform their assigned responsibilities.

They should not automatically have access to:

* Financial records.
* System administration.
* All organisational records.
* Unrelated project information.

## 7.4 Main Permissions

| Function             | Permission                           |
| -------------------- | ------------------------------------ |
| Dashboard            | Limited View                         |
| Beneficiaries        | Add / View / Edit authorised records |
| Disability Records   | Add / View / Edit                    |
| Home Visits          | Add / View / Edit                    |
| Referrals            | Add / View / Edit                    |
| Follow-Ups           | Add / View / Edit                    |
| Projects             | View assigned projects               |
| Activities           | View / Update assigned activities    |
| Poultry              | No                                   |
| Farm                 | No                                   |
| Finance              | No                                   |
| Staff and Volunteers | No                                   |
| Reports              | Limited View                         |
| Export               | No                                   |
| User Management      | No                                   |
| System Settings      | No                                   |

# 8. Role 5 - Farm Personnel

## 8.1 Purpose

Farm Personnel manage and record ERA's small farm and poultry-related operational activities.

This role is designed for persons assigned responsibility for farming and poultry operations.

## 8.2 Main Responsibilities

Farm Personnel may:

* Record crops.
* Record planting.
* Record watering.
* Record weeding.
* Record harvesting.
* Record farm activities.
* Record harvest quantities.
* Record produce transferred to poultry.
* Record poultry numbers.
* Record chicken purchases.
* Record egg production.
* Record feed usage.
* Record feed purchases.
* Record poultry illnesses.
* Record poultry deaths.
* Record poultry-related activities.

## 8.3 Farm Access

Farm Personnel should be able to manage farm information but should not automatically access beneficiary or confidential disability records.

## 8.4 Main Permissions

| Function             | Permission                                      |
| -------------------- | ----------------------------------------------- |
| Dashboard            | Farm / Poultry View                             |
| Beneficiaries        | No                                              |
| Disability Records   | No                                              |
| Home Visits          | No                                              |
| Referrals            | No                                              |
| Follow-Ups           | No                                              |
| Projects             | View relevant projects                          |
| Activities           | View / Update assigned activities               |
| Poultry              | Manage                                          |
| Farm                 | Manage                                          |
| Finance              | Add / View authorised farm and poultry expenses |
| Staff and Volunteers | No                                              |
| Reports              | Farm / Poultry Reports                          |
| Export               | Authorised                                      |
| User Management      | No                                              |
| System Settings      | No                                              |

# 9. Role 6 - Finance Personnel

## 9.1 Purpose

Finance Personnel manage authorised financial information within ERA-IPMS.

## 9.2 Main Responsibilities

Finance Personnel may:

* Record expenses.
* Categorise expenses.
* Record project expenses.
* Record poultry expenses.
* Record farm expenses.
* Maintain financial records.
* Review financial transactions.
* Prepare financial summaries.
* Generate financial reports.

## 9.3 Main Permissions

| Function             | Permission                          |
| -------------------- | ----------------------------------- |
| Dashboard            | Financial View                      |
| Beneficiaries        | No                                  |
| Disability Records   | No                                  |
| Home Visits          | No                                  |
| Referrals            | No                                  |
| Follow-Ups           | No                                  |
| Projects             | View relevant project information   |
| Activities           | View relevant information           |
| Poultry              | View authorised expense information |
| Farm                 | View authorised expense information |
| Finance              | Manage                              |
| Staff and Volunteers | No                                  |
| Reports              | Financial Reports                   |
| Export               | Export authorised financial reports |
| User Management      | No                                  |
| System Settings      | No                                  |

Financial records should only be accessible to authorised personnel.

# 10. Role 7 - Monitoring & Evaluation Personnel

## 10.1 Purpose

Monitoring & Evaluation (M&E) Personnel use ERA-IPMS to monitor programme performance, analyse information, track indicators, and prepare reports.

## 10.2 Main Responsibilities

M&E Personnel may:

* Monitor beneficiary information.
* Monitor disability services.
* Monitor home visits.
* Monitor referrals.
* Monitor follow-ups.
* Monitor project activities.
* Monitor poultry information.
* Monitor farm information.
* Analyse programme information.
* Track indicators.
* Generate reports.
* Export authorised reports.
* Support management decision-making through evidence.

## 10.3 Main Permissions

| Function             | Permission                          |
| -------------------- | ----------------------------------- |
| Dashboard            | Full Monitoring View                |
| Beneficiaries        | View                                |
| Disability Records   | View authorised information         |
| Home Visits          | View                                |
| Referrals            | View                                |
| Follow-Ups           | View                                |
| Projects             | View                                |
| Activities           | View                                |
| Poultry              | View                                |
| Farm                 | View                                |
| Finance              | View authorised summary information |
| Staff and Volunteers | View summary                        |
| Reports              | Generate                            |
| Export Reports       | Export                              |
| User Management      | No                                  |
| System Settings      | No                                  |

M&E Personnel should normally analyse and report information rather than change the original operational records unless specifically authorised.

# 11. Final Permission Matrix

The following matrix provides the initial overall access model.

| Function              | Admin  | Management   | Coordinator  | Field Staff / Volunteer | Farm Personnel | Finance      | M&E        |
| --------------------- | ------ | ------------ | ------------ | ----------------------- | -------------- | ------------ | ---------- |
| User Management       | Manage | No           | No           | No                      | No             | No           | No         |
| System Settings       | Manage | No           | No           | No                      | No             | No           | No         |
| Dashboard             | Full   | Full         | View         | Limited                 | Farm/Poultry   | Finance      | Monitoring |
| Beneficiaries         | Manage | View         | Add/Edit     | Add/Edit                | No             | No           | View       |
| Disability Assessment | Manage | View         | Add/Edit     | Add/Edit                | No             | No           | View       |
| Home Visits           | Manage | View         | Add/Edit     | Add/Edit                | No             | No           | View       |
| Referrals             | Manage | View         | Add/Edit     | Add/Edit                | No             | No           | View       |
| Follow-Ups            | Manage | View         | Add/Edit     | Add/Edit                | No             | No           | View       |
| Projects              | Manage | View         | Manage       | Assigned                | Relevant       | Relevant     | View       |
| Activities            | Manage | View/Approve | Manage       | Assigned                | Assigned       | View         | View       |
| Poultry               | Manage | View         | View         | No                      | Manage         | Expense View | View       |
| Farm                  | Manage | View         | View         | No                      | Manage         | Expense View | View       |
| Finance               | Manage | View/Approve | Project View | No                      | Limited        | Manage       | Summary    |
| Staff/Volunteers      | Manage | View         | View/Assign  | No                      | No             | No           | View       |
| Reports               | Manage | Generate     | Generate     | Limited                 | Farm/Poultry   | Financial    | Generate   |
| PDF/Excel Export      | Yes    | Yes          | Yes          | No                      | Authorised     | Yes          | Yes        |

# 12. Role Assignment

Each ERA-IPMS user should have one primary role.

Example:

```text
User
  ↓
Assigned Role
  ↓
Role Permissions
  ↓
Authorised Modules
  ↓
Allowed Actions
```

For example:

```text
Field Staff / Volunteer
        ↓
Beneficiary Module
        ↓
Add Beneficiary
Record Assessment
Record Home Visit
Create Referral
Record Follow-Up
```

Another example:

```text
Farm Personnel
        ↓
Farm & Poultry Modules
        ↓
Record Crop
Record Harvest
Record Chicken
Record Eggs
Record Feed
Record Illness
Record Death
```

# 13. Data Access Principle

ERA-IPMS should follow the principle of **least privilege**.

This means users should receive only the access necessary to perform their responsibilities.

For example, a Field Staff / Volunteer user working on beneficiary follow-up should not be able to view ERA's financial records.

Similarly, Finance Personnel should not need access to detailed disability information to perform financial responsibilities.

# 14. Confidentiality

ERA-IPMS may contain personal and potentially sensitive information about persons receiving ERA services.

Therefore:

* Users must authenticate before accessing the system.
* Access must be controlled by role.
* Users should only access authorised records.
* Passwords must not be stored as plain text.
* Confidential information must not be included in the public GitHub repository.
* Test data should be fictional or appropriately anonymised.
* System activity should be recorded where appropriate.

# 15. Audit Trail

For important records, ERA-IPMS should eventually record:

* User who created the record.
* Date and time the record was created.
* User who last modified the record.
* Date and time of the last modification.
* Important changes made to the record.

This will improve accountability and help identify errors or unauthorised changes.

# 16. Future Permission Improvements

The initial seven roles provide a practical starting point for ERA.

As ERA-IPMS develops, more detailed permissions may be introduced.

For example:

* View only.
* Add only.
* Add and edit.
* Approve.
* Export.
* Delete.
* Module-specific permissions.
* Project-specific permissions.
* Assignment-based access.

The system should be designed so that permissions can be expanded without requiring a complete redesign.

# 17. Conclusion

ERA-IPMS will use seven initial user roles:

1. **System Administrator**
2. **ERA Management**
3. **Programme / Project Coordinator**
4. **Field Staff / Volunteer**
5. **Farm Personnel**
6. **Finance Personnel**
7. **Monitoring & Evaluation Personnel**

Field Staff and Volunteers will intentionally use the same role and permissions because their current responsibilities and required system access are the same.

The role-based access model will help ERA organise responsibilities, protect confidential information, reduce unauthorised access, and ensure that each user can perform the functions required for their work.

This document will be used as a foundation for designing the authentication system, database user relationships, application permissions, and system workflows.