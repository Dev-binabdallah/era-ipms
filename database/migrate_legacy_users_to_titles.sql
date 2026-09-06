-- ERA-IPMS Phase A
-- Migrate legacy users.role_id to approved users.title_id model.
-- Permissions and title-permission assignments are intentionally NOT seeded here.
-- Legacy roles table is intentionally retained for post-migration verification.

SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------
-- 1. Create the five approved organizational titles
-- ------------------------------------------------------------

INSERT INTO titles
    (title_name, description, is_active)
VALUES
    ('Admin', 'System Administration', 1),
    ('Director', 'Programme Oversight and Monitoring and Evaluation', 1),
    ('Programme Coordinator', 'Programme and Project Coordination', 1),
    ('Finance', 'Sales, Expenses, and Financial Records', 1),
    ('Member', 'Assigned Programme Responsibilities', 1)
ON DUPLICATE KEY UPDATE
    description = VALUES(description),
    is_active = VALUES(is_active);

-- ------------------------------------------------------------
-- 2. Add the new title_id column temporarily as nullable
-- ------------------------------------------------------------

ALTER TABLE users
    ADD COLUMN title_id BIGINT UNSIGNED NULL
    AFTER user_id;

-- ------------------------------------------------------------
-- 3. Map the existing legacy System Administrator account
--    to the approved Admin title.
-- ------------------------------------------------------------

UPDATE users u
JOIN titles t
    ON t.title_name = 'Admin'
SET u.title_id = t.title_id
WHERE u.role_id = 1;

-- ------------------------------------------------------------
-- 4. Safety check: every existing user must now have a title.
--    This deliberately fails before destructive changes if
--    any legacy role cannot be mapped.
-- ------------------------------------------------------------

SET @unmapped_users := (
    SELECT COUNT(*)
    FROM users
    WHERE title_id IS NULL
);

SELECT
    @unmapped_users AS unmapped_users;

-- The current database has only user_id=1 / role_id=1,
-- so this should return 0.

-- ------------------------------------------------------------
-- 5. Remove the legacy users -> roles foreign key
-- ------------------------------------------------------------

ALTER TABLE users
    DROP FOREIGN KEY users_ibfk_1;

-- ------------------------------------------------------------
-- 6. Remove the legacy role_id index
-- ------------------------------------------------------------

ALTER TABLE users
    DROP INDEX role_id;

-- ------------------------------------------------------------
-- 7. Align users.title_id with the approved schema
-- ------------------------------------------------------------

ALTER TABLE users
    MODIFY COLUMN title_id BIGINT UNSIGNED NOT NULL;

-- ------------------------------------------------------------
-- 8. Add missing approved users fields
-- ------------------------------------------------------------

ALTER TABLE users
    ADD COLUMN last_login DATETIME NULL
    AFTER is_active;

ALTER TABLE users
    ADD COLUMN updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
    AFTER created_at;

-- ------------------------------------------------------------
-- 9. Align created_at with the approved schema
-- ------------------------------------------------------------

ALTER TABLE users
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

-- ------------------------------------------------------------
-- 10. Align users table character set/collation
-- ------------------------------------------------------------

ALTER TABLE users
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 11. Add approved title index and foreign key
-- ------------------------------------------------------------

ALTER TABLE users
    ADD KEY idx_users_title (title_id);

ALTER TABLE users
    ADD CONSTRAINT fk_users_title
        FOREIGN KEY (title_id)
        REFERENCES titles (title_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;

-- ------------------------------------------------------------
-- 12. Remove legacy role_id
-- ------------------------------------------------------------

ALTER TABLE users
    DROP COLUMN role_id;

-- ------------------------------------------------------------
-- End Phase A
-- ------------------------------------------------------------
