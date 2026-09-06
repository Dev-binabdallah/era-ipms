-- ERA-IPMS approved baseline permissions
-- Step 13.2: Permission definitions only.
-- No title-permission assignments are made in this script.

INSERT INTO permissions (
    permission_code,
    permission_name,
    description
)
VALUES
    (
        'VIEW',
        'View',
        'View authorised records and information.'
    ),
    (
        'ADD',
        'Add',
        'Create new authorised records.'
    ),
    (
        'EDIT',
        'Edit',
        'Modify authorised records.'
    ),
    (
        'DELETE',
        'Delete',
        'Delete or otherwise remove records where deletion is authorised.'
    ),
    (
        'APPROVE',
        'Approve',
        'Approve records, actions, or decisions where approval authority is assigned.'
    ),
    (
        'EXPORT',
        'Export',
        'Export authorised records or reports.'
    ),
    (
        'MANAGE',
        'Manage',
        'Manage authorised operational or system resources.'
    ),
        (
        'ADMINISTER',
        'Administer',
        'Perform system-level administrative operations.'
    );