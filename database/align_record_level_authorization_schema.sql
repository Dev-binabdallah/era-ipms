-- ============================================================
-- ERA-IPMS
-- Step 13.13A — Record-Level Authorization Schema Alignment
--
-- PURPOSE:
--   Align the live domain-table structures with the approved
--   ERA-IPMS v1.1 schema so record-level authorization can safely
--   inherit project/activity/poultry-group relationships.
--
-- IMPORTANT:
--   REVIEW ONLY. DO NOT EXECUTE AGAINST THE LIVE DATABASE YET.
--
-- Preconditions verified:
--   All affected domain tables currently contain 0 rows.
--
-- Target database:
--   era_ipms
-- ============================================================

USE era_ipms;

SET FOREIGN_KEY_CHECKS = 0;


-- ============================================================
-- 1. FARM CROPS
-- ============================================================
-- Required relationship:
--   PROJECTS 1 ─────< FARM_CROPS
--
-- Required fields:
--   project_id
--   updated_at
-- ============================================================

ALTER TABLE farm_crops
    ADD COLUMN project_id BIGINT UNSIGNED NOT NULL AFTER crop_id,
    ADD COLUMN updated_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE farm_crops
    ADD INDEX idx_fc_project (project_id);

ALTER TABLE farm_crops
    ADD CONSTRAINT fk_fc_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE;


-- ============================================================
-- 2. FARM ACTIVITIES
-- ============================================================
-- Approved accountability field:
--   recorded_by
--
-- Existing live field:
--   conducted_by
-- ============================================================

ALTER TABLE farm_activities
    DROP FOREIGN KEY farm_activities_ibfk_2;

ALTER TABLE farm_activities
    DROP INDEX conducted_by;

ALTER TABLE farm_activities
    CHANGE COLUMN conducted_by
        recorded_by BIGINT UNSIGNED NOT NULL;

ALTER TABLE farm_activities
    ADD INDEX idx_fa_recorded_by (recorded_by);

ALTER TABLE farm_activities
    ADD CONSTRAINT fk_fa_recorded_by
        FOREIGN KEY (recorded_by)
        REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE;


-- ============================================================
-- 3. HARVESTS
-- ============================================================
-- Relationship already exists:
--   FARM_CROPS 1 ─────< HARVESTS
--
-- Normalize timestamp/collation through table conversion.
-- ============================================================

ALTER TABLE harvests
    MODIFY COLUMN created_at DATETIME NOT NULL
        DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE harvests
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 4. FARM POULTRY TRANSFERS
-- ============================================================
-- Relationship:
--   HARVESTS ─────< FARM_POULTRY_TRANSFERS >───── POULTRY_GROUPS
--
-- Structure is already substantially aligned.
-- Normalize table character set/collation.
-- ============================================================

ALTER TABLE farm_poultry_transfers
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 5. POULTRY GROUPS
-- ============================================================
-- Already aligned with approved project relationship.
-- ============================================================

ALTER TABLE poultry_groups
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 6. POULTRY STOCK MOVEMENTS
-- ============================================================
-- Already has poultry_group_id and recorded_by relationships.
-- ============================================================

ALTER TABLE poultry_stock_movements
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 7. EGG PRODUCTION
-- ============================================================
-- Required relationship:
--   POULTRY_GROUPS 1 ─────< EGG_PRODUCTION
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
-- Already aligned with poultry-group relationship.
-- ============================================================

ALTER TABLE poultry_sales
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 11. FINANCIAL TRANSACTIONS
-- ============================================================
-- project_id intentionally remains nullable:
--   NULL = organization/global financial record
--   non-NULL = project-scoped financial record
--
-- Existing structure is approved.
-- Normalize character set/collation only.
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
--   updated_at
--
-- Existing live structure contains:
--   project_id NOT NULL
--   current_value
--   recorded_by
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
        DEFAULT 'active';

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
-- Relationship:
--   ME_INDICATORS 1 ─────< ME_INDICATOR_RECORDS
--
-- Already aligned.
-- ============================================================

ALTER TABLE me_indicator_records
    CONVERT TO CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;


-- ============================================================
-- 14. REFERRALS
-- ============================================================
-- Approved structure adds:
--   approved_by
--   approved_at
--   updated_at
--
-- Existing beneficiary/referred_by relationships remain.
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
-- Relationship:
--   REFERRALS 1 ─────< REFERRAL_FOLLOW_UPS
--
-- Existing relationship is correct.
-- Normalize timestamp/collation.
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
-- included in this alignment script.
--
-- After execution, verify:
--   SHOW CREATE TABLE <table>;
--   SHOW ENGINE INNODB STATUS;
--   information_schema.KEY_COLUMN_USAGE;
--
-- Then re-run Django/database alignment checks.
-- ============================================================
