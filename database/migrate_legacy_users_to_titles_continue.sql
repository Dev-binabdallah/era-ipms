-- ERA-IPMS Phase A continuation
-- Completes the partially applied users -> titles migration.

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Confirm every user has a title
SELECT
    COUNT(*) AS users_missing_title
FROM users
WHERE title_id IS NULL;

-- Expected: 0

-- 2. Confirm created_at contains no NULL values
SELECT
    COUNT(*) AS users_missing_created_at
FROM users
WHERE created_at IS NULL;

-- Expected: 0

-- 3. Convert created_at to approved DATETIME definition
ALTER TABLE users
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

-- 4. Align is_active with approved schema
UPDATE users
SET is_active = 1
WHERE is_active IS NULL;

ALTER TABLE users
    MODIFY COLUMN is_active TINYINT(1) NOT NULL
        DEFAULT 1;

-- 5. Align table character set/collation
ALTER TABLE users
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 6. Add approved title index
ALTER TABLE users
    ADD KEY idx_users_title (title_id);

-- 7. Add approved title foreign key
ALTER TABLE users
    ADD CONSTRAINT fk_users_title
        FOREIGN KEY (title_id)
        REFERENCES titles (title_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;

-- 8. Replace legacy username/email index names
ALTER TABLE users
    DROP INDEX username,
    DROP INDEX email,
    ADD UNIQUE KEY uq_users_username (username),
    ADD UNIQUE KEY uq_users_email (email);

-- 9. Remove legacy role_id
ALTER TABLE users
    DROP COLUMN role_id;
