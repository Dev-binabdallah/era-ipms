# ERA Integrated Project Management System (ERA-IPMS)

# System Workflows

## Document Information

**Project:** ERA Integrated Project Management System (ERA-IPMS)
**Document Type:** System Workflow Design
**Version:** 1.0
**Date:** September 2026
**Prepared By:** Abdullahi Abdi Mohamed

# 1. Introduction

This document describes the main workflows of ERA-IPMS.

A workflow shows how information moves through the system from the beginning of an activity to the final outcome.

The workflows are based on ERA's current operations in:

* Disability services.
* Beneficiary support.
* Home visits.
* Referrals and follow-ups.
* Projects and activities.
* Poultry farming.
* Small-scale agriculture.
* Finance.
* Monitoring and evaluation.
* Reporting.

The workflows will guide the database design and software development.

# 2. Overall ERA-IPMS Workflow

The overall system can be represented as:

```text
                    ERA-IPMS
                       |
        +--------------+--------------+
        |              |              |
   Disability       Projects       Enterprise
    Services        & Activities    Activities
        |              |              |
        |              |        +-----+-----+
        |              |        |           |
    Beneficiary      Activities Poultry    Farm
        |                         |           |
   Assessment                     |           |
        |                         +-----+-----+
   Home Visit                           |
        |                              Data
    Referral                             |
        |                                |
   Follow-Up                             |
        +---------------+----------------+
                         |
                     Information
                         |
                    M&E / Dashboard
                         |
                      Reports
                         |
                    ERA Management
```

The system will bring information from different ERA activities into one central system.

# 3. User Login Workflow

All system users must authenticate before accessing ERA-IPMS.

```text
USER
  |
  v
Open ERA-IPMS
  |
  v
Enter Username / Email
  |
  v
Enter Password
  |
  v
System Validates Credentials
  |
  +-------- Invalid --------+
  |                         |
  v                         |
Display Error               |
  |                         |
  +------ Try Again <-------+
  |
 Valid
  |
  v
Identify User Role
  |
  v
Load Authorised Dashboard
  |
  v
Access Permitted Modules
```

## Expected Behaviour

If the credentials are correct, the user is authenticated.

The system identifies the user's role and provides access according to the permissions assigned to that role.

If the credentials are incorrect, the system should display an appropriate error message without revealing sensitive authentication information.

# 4. Beneficiary and Disability Service Workflow

This is one of the most important workflows in ERA-IPMS.

ERA currently identifies persons who need support through assessment documents.

The proposed digital workflow is:

```text
PERSON IDENTIFIED
       |
       v
BENEFICIARY SEARCH
       |
       +------ Existing ------+
       |                      |
       v                      |
Open Existing Record          |
       |                      |
       +----------+-----------+
                  |
                New
                  |
                  v
          REGISTER BENEFICIARY
                  |
                  v
          RECORD ASSESSMENT
                  |
                  v
          IDENTIFY NEEDS
                  |
                  v
       +----------+----------+
       |                     |
    Support Needed       Referral Needed
       |                     |
       v                     v
Provide Support          CREATE REFERRAL
       |                     |
       +----------+----------+
                  |
                  v
             HOME VISIT
          where required
                  |
                  v
             FOLLOW-UP
                  |
                  v
          RECORD OUTCOME
                  |
                  v
          CASE / SERVICE
             UPDATED
```

# 5. Beneficiary Registration Workflow

```text
FIELD STAFF / VOLUNTEER
          |
          v
Search Beneficiary
          |
     +----+----+
     |         |
  Found      Not Found
     |         |
     v         v
Open Record   Create Record
                 |
                 v
          Enter Required Data
                 |
                 v
          Validate Information
                 |
                 v
          Save Beneficiary
                 |
                 v
       Beneficiary ID Created
```

## Important Rule

Before creating a new beneficiary, the user should search for an existing beneficiary.

This helps reduce duplicate records.

# 6. Disability Assessment Workflow

```text
Beneficiary
    |
    v
Assessment Required
    |
    v
Field Staff / Volunteer
    |
    v
Collect Required Information
    |
    v
Record Assessment
    |
    v
Identify Needs
    |
    +------------------+
    |                  |
    v                  v
Direct Support      Referral
    |                  |
    v                  v
Record Support     Create Referral
                       |
                       v
                   Follow-Up
```

The assessment information should be stored against the beneficiary's record.

# 7. Home Visit Workflow

ERA currently records home visits manually.

The digital workflow will be:

```text
Home Visit Required
       |
       v
Assign / Conduct Visit
       |
       v
Field Staff / Volunteer
       |
       v
Open Beneficiary Record
       |
       v
Record Visit
       |
       +----------------------+
       |                      |
       v                      v
Support Provided        Further Action Needed
                              |
                              v
                         Create Action
                              |
                              v
                           Follow-Up
```

A home visit record should contain:

* Beneficiary.
* Visit date.
* Person conducting the visit.
* Purpose.
* Observations.
* Support provided.
* Follow-up required.
* Next action.

# 8. Referral Workflow

ERA currently makes referrals through written referrals, verbal communication, or accompanying a person to a service.

ERA-IPMS will create a formal digital record.

```text
Need Identified
      |
      v
Referral Required
      |
      v
Create Referral
      |
      v
Select / Enter Service
      |
      v
Record Reason
      |
      v
Referral Status = PENDING
      |
      v
Service / Referral Action
      |
      v
Field Staff / Volunteer Follow-Up
      |
      v
Record Outcome
      |
      +-------------------------+
      |                         |
      v                         v
Completed                 Not Completed
      |                         |
      v                         v
Close Referral           Further Follow-Up
                                |
                                v
                         Update Outcome
```

# 9. Referral Follow-Up Workflow

```text
Pending Referral
      |
      v
Follow-Up Due
      |
      v
Field Staff / Volunteer
      |
      v
Contact / Visit Beneficiary
      |
      v
Check Referral Status
      |
      +----------------------+------------------+
      |                      |                  |
      v                      v                  v
Service Received       Still Waiting       Unable to Access
      |                      |                  |
      v                      v                  v
Completed              Follow-Up Needed     Further Action
      |                      |                  |
      +-----------+----------+------------------+
                  |
                  v
            Record Outcome
```

The system should make it possible to identify referrals that remain pending.

# 10. Project Management Workflow

```text
PROJECT CREATED
      |
      v
Project Objectives Defined
      |
      v
Activities Planned
      |
      v
Activities Assigned
      |
      v
Activity Implemented
      |
      v
Activity Information Recorded
      |
      v
Activity Completed
      |
      v
Results Recorded
      |
      v
Project Monitoring
      |
      v
Project Report
```

# 11. Activity Workflow

```text
Activity Planned
      |
      v
Assign Responsible Person
      |
      v
Activity Date
      |
      v
Activity Conducted
      |
      v
Record Participants
      |
      v
Record Activity Details
      |
      v
Record Results
      |
      v
Activity Status = COMPLETED
```

Activities may also remain:

```text
PLANNED
ONGOING
PENDING
COMPLETED
CANCELLED
```

# 12. Poultry Management Workflow

ERA currently has approximately 10 local and Kienyeji chickens.

The poultry project currently focuses mainly on eggs, with future plans for meat and breeding.

The proposed workflow is:

```text
POULTRY PROJECT
       |
       v
Record Opening Stock
       |
       v
Purchase / Receive Chickens
       |
       v
Update Poultry Numbers
       |
       +------------------+
       |                  |
       v                  v
Feed Management       Poultry Health
       |                  |
       v                  +------+
Feed Used                     |
       |                      v
       |                 Illness / Death
       |                      |
       +----------+-----------+
                  |
                  v
             Egg Production
                  |
                  v
              Egg Record
                  |
                  v
           Poultry Summary
                  |
                  v
                Report
```

# 13. Poultry Stock Workflow

The system should calculate the current poultry stock.

Basic calculation:

```text
Current Stock =
Opening Stock
+ Chickens Purchased
+ Chickens Received
- Chickens Sold
- Poultry Deaths
```

Example:

```text
Opening stock       = 10
Purchased           = 20
Sold                = 3
Deaths              = 2

Current stock       = 10 + 20 - 3 - 2
                    = 25 chickens
```

This calculation reduces the need for manual counting and helps management monitor poultry numbers.

# 14. Egg Production Workflow

```text
Chickens
   |
   v
Eggs Produced
   |
   v
Record Production Date
   |
   v
Enter Number of Eggs
   |
   +------------------------+
   |                        |
   v                        v
Eggs Used                Eggs Sold
   |                        |
   +-----------+------------+
               |
               v
          Eggs Remaining
               |
               v
        Production Report
```

The system should allow ERA to monitor egg production over time.

# 15. Poultry Feed Workflow

ERA's poultry feed comes from:

* Produce from the small farm.
* Locally purchased feeds.

The workflow will be:

```text
Feed Source
    |
    +------------------+
    |                  |
    v                  v
Small Farm        Local Purchase
    |                  |
    +--------+---------+
             |
             v
        Feed Received
             |
             v
        Feed Used
             |
             v
       Feed Balance
             |
             v
       Feed Report
```

Where applicable, the system should record the cost of purchased feed.

# 16. Poultry Health Workflow

```text
Poultry Health Check
        |
        v
    Condition
        |
   +----+----+
   |         |
 Healthy   Problem
             |
       +-----+-----+
       |           |
    Illness       Death
       |           |
       v           v
Record Case   Record Death
       |           |
       +-----+-----+
             |
             v
       Update Poultry
          Numbers
```

# 17. Small Farm Workflow

ERA operates a small farm approximately 20–30 metres long and 3–5 metres wide.

The farm currently grows:

* Bananas.
* Natural/local vegetables.
* Sukuma wiki.

The proposed digital workflow is:

```text
FARM
 |
 v
Prepare Land
 |
 v
Plant Crops
 |
 v
Water
 |
 v
Weed
 |
 v
Maintain Crops
 |
 v
Harvest
 |
 v
Record Harvest
 |
 +--------------------+
 |                    |
 v                    v
Used for Poultry   Other Use
 |                    |
 v                    v
Poultry Feed       ERA Use / Future Sale
```

# 18. Farm Activity Workflow

```text
Farm Activity
      |
      v
Select Crop
      |
      v
Select Activity
      |
      +-----------------------------+
      |             |               |
      v             v               v
Planting        Watering        Weeding
      |             |               |
      +-------------+---------------+
                    |
                    v
                Harvest
                    |
                    v
             Record Quantity
                    |
                    v
              Record Usage
```

# 19. Farm Expense Workflow

ERA currently has farm expenses such as seeds, tools, and other inputs. Water and labour are currently not recorded as expenses.

The proposed workflow is:

```text
Farm Expense Occurs
       |
       v
Finance / Authorised User
       |
       v
Record Expense
       |
       v
Select Category
       |
       v
Enter Amount
       |
       v
Enter Description
       |
       v
Save Expense
       |
       v
Financial Record
       |
       v
Farm Expense Report
```

# 20. Poultry and Farm Relationship

The farm and poultry project are connected.

The system should therefore make it possible to record when farm produce is used to support poultry.

```text
             SMALL FARM
                 |
                 v
             Harvest
                 |
        +--------+--------+
        |                 |
        v                 v
Used by Poultry       Other Use
        |
        v
      Feed
        |
        v
     POULTRY
        |
        v
Egg Production
        |
        v
Potential Revenue
```

This relationship will help ERA understand how the farm contributes to the poultry project.

# 21. Finance Workflow

```text
Expense Occurs
      |
      v
Identify Expense Category
      |
      v
Record Expense
      |
      v
Enter Amount
      |
      v
Link to Project / Farm / Poultry
      |
      v
Save Transaction
      |
      v
Financial Summary
      |
      v
Financial Report
```

Possible categories include:

* Project.
* Poultry.
* Farm.
* Office.
* Transport.
* Equipment.
* Other.

# 22. Staff and Volunteer Workflow

```text
Person Joins ERA
      |
      v
Create Staff / Volunteer Record
      |
      v
Assign Role
      |
      v
Assign Responsibilities
      |
      v
Record Status
      |
      v
Update When Necessary
```

For system users, the authorised administrator will create the corresponding login account and assign the appropriate ERA-IPMS role.

# 23. Monitoring and Evaluation Workflow

M&E will bring information from different modules together.

```text
Beneficiary Data
       |
       v
Disability Data
       |
       +----------------+
       |                |
       v                v
Home Visits        Referrals
       |                |
       +-------+--------+
               |
               v
         Project Activities
               |
        +------+------+
        |             |
        v             v
     Poultry         Farm
        |             |
        +------+------+
               |
               v
          M&E Dashboard
               |
               v
           Indicators
               |
               v
            Reports
```

# 24. Dashboard Workflow

The dashboard will convert stored information into useful summaries.

```text
DATABASE
    |
    +-------------------+
    |                   |
    v                   v
Operational Data     Financial Data
    |                   |
    +---------+---------+
              |
              v
        System Processing
              |
              v
           Dashboard
              |
      +-------+-------+
      |       |       |
      v       v       v
 Disability Poultry  Farm
      |       |       |
      +-------+-------+
              |
              v
          Management
```

# 25. Reporting Workflow

```text
DATABASE
   |
   v
Select Report Type
   |
   v
Select Date / Filters
   |
   v
System Retrieves Data
   |
   v
Generate Report
   |
   +------------------+
   |                  |
   v                  v
View Report       Export Report
                       |
                +------+------+
                |             |
                v             v
              PDF           Excel
```

PDF and Excel export may be implemented after the initial MVP.

# 26. Information Flow

The overall information flow can be summarised as:

```text
DATA COLLECTION
      |
      v
DATABASE
      |
      v
DATA VALIDATION
      |
      v
DATA PROCESSING
      |
      v
DASHBOARD
      |
      v
MONITORING
      |
      v
REPORTING
      |
      v
DECISION-MAKING
```

# 27. Error and Correction Workflow

Users may make mistakes when entering information.

The system should provide a controlled correction process.

```text
Record Created
      |
      v
Information Reviewed
      |
   +--+--+
   |     |
 Correct Error
   |     |
   v     v
Keep   Edit Record
         |
         v
      Save Change
         |
         v
    Updated Record
```

Important records should maintain information about who created or modified them.

# 28. Data Validation

The system should validate important information before saving it.

Examples:

* Required fields cannot be empty.
* Dates must be valid.
* Numbers must contain valid numeric values.
* Expense amounts should not contain invalid text.
* Poultry numbers should not become negative.
* Egg quantities should not be negative.
* Duplicate beneficiaries should be identified where possible.

Example:

```text
Egg Production = -20
       |
       v
Invalid
       |
       v
Display Error
       |
       v
User Corrects Value
```

# 29. End-to-End ERA-IPMS Workflow

The complete system can be viewed as:

```text
                         ERA-IPMS
                            |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
   DISABILITY           PROJECTS          FARM & POULTRY
     SERVICES           & ACTIVITIES          |
        |                   |            +------+------+
        |                   |            |             |
 Beneficiary             Activities    Farm         Poultry
        |                   |            |             |
 Assessment                Results     Harvest       Eggs
        |                   |            |             |
 Home Visit                Reports      Feed          Feed
        |                                |             |
 Referral                               Expenses      Health
        |                                  \           /
 Follow-Up                                 \         /
        |                                   \       /
        +-------------------+----------------+-------+
                            |
                            v
                         DATABASE
                            |
                            v
                     M&E / DASHBOARD
                            |
                            v
                         REPORTS
                            |
                            v
                       MANAGEMENT
                            |
                            v
                    DECISION-MAKING
```

# 30. Workflow Design Principles

The ERA-IPMS workflows should follow these principles:

## 30.1 Simple

Users should not be required to complete unnecessary steps.

## 30.2 Accurate

The system should validate important information.

## 30.3 Traceable

Important records should identify who created or modified them.

## 30.4 Secure

Users should only access information appropriate to their roles.

## 30.5 Practical

The workflows should reflect how ERA actually operates rather than forcing ERA to follow unnecessarily complicated procedures.

## 30.6 Expandable

The workflows should allow future features to be added without redesigning the entire system.

# 31. Conclusion

The workflow design provides a practical model for how ERA-IPMS will operate.

The system will connect ERA's disability services, projects, poultry, small farm, finance, M&E, and reporting activities through a central database.

The workflows will be used as a direct input into the next stage of development: **database design**.

Before database tables are created, the workflows should be reviewed by ERA and adjusted where they do not accurately reflect actual organisational procedures.