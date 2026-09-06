-- ERA-IPMS approved baseline responsibilities
-- Step 13.4B: Responsibility definitions only.
-- No user-responsibility assignments are made in this script.

INSERT INTO responsibilities (
    responsibility_code,
    responsibility_name,
    description
)
SELECT
    v.responsibility_code,
    v.responsibility_name,
    v.description
FROM (
    SELECT
        'DISABILITY_SERVICES' AS responsibility_code,
        'Disability Services' AS responsibility_name,
        'Operational responsibility for authorised disability service activities.' AS description

    UNION ALL
    SELECT
        'BENEFICIARY_REGISTRATION',
        'Beneficiary Registration',
        'Operational responsibility for authorised beneficiary registration activities.'

    UNION ALL
    SELECT
        'DISABILITY_ASSESSMENT',
        'Disability Assessment',
        'Operational responsibility for authorised disability assessment activities.'

    UNION ALL
    SELECT
        'HOME_VISITS',
        'Home Visits',
        'Operational responsibility for authorised home visit activities.'

    UNION ALL
    SELECT
        'REFERRALS_FOLLOW_UP',
        'Referrals and Follow-Up',
        'Operational responsibility for authorised referrals and follow-up activities.'

    UNION ALL
    SELECT
        'COMMUNITY_AWARENESS',
        'Community Awareness',
        'Operational responsibility for authorised community awareness activities.'

    UNION ALL
    SELECT
        'PROJECT_ACTIVITIES',
        'Project Activities',
        'Operational responsibility for authorised project and activity operations.'

    UNION ALL
    SELECT
        'POULTRY_OPERATIONS',
        'Poultry Operations',
        'Operational responsibility for authorised poultry operations.'

    UNION ALL
    SELECT
        'FARM_OPERATIONS',
        'Farm Operations',
        'Operational responsibility for authorised farm operations.'

    UNION ALL
    SELECT
        'PROJECT_COORDINATION',
        'Project Coordination',
        'Operational responsibility for authorised project coordination activities.'

    UNION ALL
    SELECT
        'FINANCIAL_OPERATIONS',
        'Financial Operations',
        'Operational responsibility for authorised financial operations.'

    UNION ALL
    SELECT
        'MONITORING_EVALUATION',
        'Monitoring and Evaluation',
        'Operational responsibility for authorised monitoring and evaluation activities.'
) AS v
WHERE NOT EXISTS (
    SELECT 1
    FROM responsibilities r
    WHERE r.responsibility_code = v.responsibility_code
);