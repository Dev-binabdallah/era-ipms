-- ERA-IPMS project/activity schema alignment
-- Step 13.5I
--
-- Purpose:
-- Align the live projects and activities tables with the approved
-- database/schema.sql baseline.
--
-- Preconditions verified:
--   - projects: 0 rows
--   - user_project_assignments: 0 rows
--   - activities: 0 rows
--   - activity_assignments: 0 rows
--   - current live indexes/foreign keys audited
--   - current database backup created before this migration
--
-- This is a targeted structural migration.
-- It does not seed project/activity data.

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- PROJECTS
-- ============================================================

ALTER TABLE projects
    DROP FOREIGN KEY projects_ibfk_1;

ALTER TABLE projects
    DROP INDEX responsible_user_id;

ALTER TABLE projects
    CHANGE COLUMN responsible_user_id created_by BIGINT UNSIGNED NOT NULL;

ALTER TABLE projects
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE projects
    ADD COLUMN updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE projects
    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE projects
    ADD KEY idx_projects_status (status),
    ADD KEY idx_projects_dates (start_date, end_date),
    ADD KEY idx_projects_created_by (created_by);

ALTER TABLE projects
    ADD CONSTRAINT fk_projects_created_by
        FOREIGN KEY (created_by)
        REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;

-- ============================================================
-- ACTIVITIES
-- ============================================================

ALTER TABLE activities
    DROP FOREIGN KEY activities_ibfk_1,
    DROP FOREIGN KEY activities_ibfk_2;

ALTER TABLE activities
    DROP INDEX project_id,
    DROP INDEX responsible_user_id;

ALTER TABLE activities
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE activities
    ADD COLUMN updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE activities
    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE activities
    ADD KEY idx_activities_project (project_id),
    ADD KEY idx_activities_responsible (responsible_user_id),
    ADD KEY idx_activities_date (activity_date),
    ADD KEY idx_activities_status (status);

ALTER TABLE activities
    ADD CONSTRAINT fk_activities_project
        FOREIGN KEY (project_id)
        REFERENCES projects (project_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE;

ALTER TABLE activities
    ADD CONSTRAINT fk_activities_responsible
        FOREIGN KEY (responsible_user_id)
        REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT;
