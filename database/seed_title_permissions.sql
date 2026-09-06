-- ERA-IPMS approved baseline title-permission assignments
-- Step 13.3C: Title-level permission seed.
-- Uses title names and permission codes rather than hardcoded IDs.
-- Does not replace record-level authorization rules.

INSERT INTO title_permissions (
    title_id,
    permission_id
)
SELECT
    t.title_id,
    p.permission_id
FROM titles t
JOIN permissions p
WHERE
    (
        (t.title_name = 'Admin' AND p.permission_code IN (
            'VIEW',
            'ADD',
            'EDIT',
            'DELETE',
            'APPROVE',
            'EXPORT',
            'MANAGE',
            'ADMINISTER'
        ))
        OR
        (t.title_name = 'Director' AND p.permission_code IN (
            'VIEW',
            'APPROVE',
            'EXPORT',
            'MANAGE'
        ))
        OR
        (t.title_name = 'Programme Coordinator' AND p.permission_code IN (
            'VIEW',
            'ADD',
            'EDIT',
            'EXPORT',
            'MANAGE'
        ))
        OR
        (t.title_name = 'Finance' AND p.permission_code IN (
            'VIEW',
            'ADD',
            'EDIT',
            'EXPORT',
            'MANAGE'
        ))
        OR
        (t.title_name = 'Member' AND p.permission_code IN (
            'VIEW',
            'ADD',
            'EDIT'
        ))
    )
    AND NOT EXISTS (
        SELECT 1
        FROM title_permissions tp
        WHERE tp.title_id = t.title_id
          AND tp.permission_id = p.permission_id
    );