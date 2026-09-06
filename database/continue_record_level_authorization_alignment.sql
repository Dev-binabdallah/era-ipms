-- ============================================================
-- ERA-IPMS RECORD-LEVEL AUTHORIZATION SCHEMA ALIGNMENT
-- CONTINUATION / RECOVERY SCRIPT
--
-- This script continues from the partial execution of:
--   database/align_record_level_authorization_schema.sql
--
-- Pre-alignment backup:
--   backups/era_ipms_pre_record_level_alignment_20260906_202136.sql
--
-- IMPORTANT:
--   Do NOT execute the original alignment script again.
--
-- No INSERT, UPDATE, or DELETE statements are included.
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;


-- ============================================================
-- 7. EGG PRODUCTION
-- ============================================================
-- Required relationship:
--   POULTRY_GROUPS 1 ─────< EGG_PRODUCTION
--
-- Actual primary key:
--   egg_production_id
-- ============================================================

ALTER TABLE egg_production
    ADD COLUMN poultry_group_id BIGINT UNSIGNED NOT NULL
        AFTER egg_production_id;

ALTER TABLE egg_production
    ADD INDEX idx_ep_group (poultry_group_id);

ALTER TABLE egg_production
    ADD CONSTRAINT fk_ep_group
        FOREIGN KEY (poultry_group_id)
        REFERENCES poultry_groups(poultry_group_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE egg_production
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE egg_production
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 8. FEED RECORDS
-- ============================================================
-- Required relationship:
--   POULTRY_GROUPS 1 ─────< FEED_RECORDS
--
-- Actual primary key:
--   feed_record_id
-- ============================================================

ALTER TABLE feed_records
    ADD COLUMN poultry_group_id BIGINT UNSIGNED NOT NULL
        AFTER feed_record_id;

ALTER TABLE feed_records
    ADD INDEX idx_fr_group (poultry_group_id);

ALTER TABLE feed_records
    ADD CONSTRAINT fk_fr_group
        FOREIGN KEY (poultry_group_id)
        REFERENCES poultry_groups(poultry_group_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE feed_records
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE feed_records
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 9. POULTRY HEALTH RECORDS
-- ============================================================
-- Required relationship:
--   POULTRY_GROUPS 1 ─────< POULTRY_HEALTH_RECORDS
--
-- Actual primary key:
--   health_record_id
-- ============================================================

ALTER TABLE poultry_health_records
    ADD COLUMN poultry_group_id BIGINT UNSIGNED NOT NULL
        AFTER health_record_id;

ALTER TABLE poultry_health_records
    ADD INDEX idx_phr_group (poultry_group_id);

ALTER TABLE poultry_health_records
    ADD CONSTRAINT fk_phr_group
        FOREIGN KEY (poultry_group_id)
        REFERENCES poultry_groups(poultry_group_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE poultry_health_records
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE poultry_health_records
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 10. POULTRY SALES
-- ============================================================

ALTER TABLE poultry_sales
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 11. FINANCIAL TRANSACTIONS
-- ============================================================
-- project_id remains nullable.
-- NULL = organization/global financial record.
-- non-NULL = project-scoped financial record.
-- ============================================================

ALTER TABLE financial_transactions
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 12. M&E INDICATORS
-- ============================================================
-- Approved structure:
--   project_id nullable
--   created_by
--   status
--   updated_at
--
-- Existing live structure:
--   project_id NOT NULL
--   current_value
--   recorded_by
--   no status
--   no updated_at
-- ============================================================

ALTER TABLE me_indicators
    DROP FOREIGN KEY me_indicators_ibfk_1;

ALTER TABLE me_indicators
    MODIFY COLUMN project_id BIGINT UNSIGNED NULL;

ALTER TABLE me_indicators
    ADD CONSTRAINT fk_mei_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

ALTER TABLE me_indicators
    CHANGE COLUMN recorded_by
        created_by BIGINT UNSIGNED NOT NULL;

ALTER TABLE me_indicators
    MODIFY COLUMN target_value DECIMAL(14,2) NULL;

ALTER TABLE me_indicators
    ADD COLUMN status VARCHAR(50) NOT NULL
        DEFAULT 'active'
        AFTER end_date;

ALTER TABLE me_indicators
    ADD COLUMN updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE me_indicators
    DROP COLUMN current_value;

ALTER TABLE me_indicators
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 13. M&E INDICATOR RECORDS
-- ============================================================

ALTER TABLE me_indicator_records
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 14. REFERRALS
-- ============================================================
-- Approved structure adds:
--   destination
--   approved_by
--   approved_at
--   updated_at
-- ============================================================

ALTER TABLE referrals
    CHANGE COLUMN referral_destination
        destination VARCHAR(255) NOT NULL;

ALTER TABLE referrals
    ADD COLUMN approved_by BIGINT UNSIGNED NULL
        AFTER status,
    ADD COLUMN approved_at DATETIME NULL
        AFTER approved_by,
    ADD COLUMN updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE referrals
    ADD INDEX idx_ref_approved_by (approved_by);

ALTER TABLE referrals
    ADD CONSTRAINT fk_ref_approved_by
        FOREIGN KEY (approved_by)
        REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

ALTER TABLE referrals
    MODIFY COLUMN status VARCHAR(50) NOT NULL
        DEFAULT 'submitted';

ALTER TABLE referrals
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE referrals
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 15. REFERRAL FOLLOW-UPS
-- ============================================================

ALTER TABLE referral_follow_ups
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE referral_follow_ups
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- FINAL
-- ============================================================

SET FOREIGN_KEY_CHECKS = 1;

-- No INSERT, UPDATE, or DELETE statements are intentionally
-- included in this script.
-- ============================================================
