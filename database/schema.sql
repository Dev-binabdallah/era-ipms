-- ERA-IPMS Database Schema v1.1
-- MariaDB / MySQL
-- September 2026
--
-- PURPOSE:
--   Authoritative database schema baseline derived from the approved
--   Database Entity Design v1.1 and ERD v1.1.
--
-- SAFETY:
--   This file is a design/install baseline. It does NOT perform migrations
--   of the existing legacy database and contains no DROP TABLE statements.
--   Do not run it against an existing production database until a migration
--   plan has been reviewed and approved.
--
-- IMPORTANT:
--   Status/type/category values are intentionally VARCHAR where final
--   controlled vocabularies remain subject to validation.

CREATE DATABASE IF NOT EXISTS era_ipms
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE era_ipms;

SET NAMES utf8mb4;

-- ============================================================
-- 1. ACCESS AND IDENTITY
-- ============================================================

CREATE TABLE IF NOT EXISTS titles (
    title_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title_name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (title_id),
    UNIQUE KEY uq_titles_name (title_name),
    KEY idx_titles_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS permissions (
    permission_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    permission_code VARCHAR(100) NOT NULL,
    permission_name VARCHAR(150) NOT NULL,
    description TEXT NULL,
    PRIMARY KEY (permission_id),
    UNIQUE KEY uq_permissions_code (permission_code),
    UNIQUE KEY uq_permissions_name (permission_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS responsibilities (
    responsibility_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    responsibility_code VARCHAR(100) NOT NULL,
    responsibility_name VARCHAR(150) NOT NULL,
    description TEXT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (responsibility_id),
    UNIQUE KEY uq_responsibilities_code (responsibility_code),
    UNIQUE KEY uq_responsibilities_name (responsibility_name),
    KEY idx_responsibilities_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title_id BIGINT UNSIGNED NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(30) NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    last_login DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email),
    KEY idx_users_title (title_id),
    KEY idx_users_active (is_active),
    CONSTRAINT fk_users_title
        FOREIGN KEY (title_id) REFERENCES titles (title_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS title_permissions (
    title_permission_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title_id BIGINT UNSIGNED NOT NULL,
    permission_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (title_permission_id),
    UNIQUE KEY uq_title_permissions (title_id, permission_id),
    KEY idx_tp_permission (permission_id),
    CONSTRAINT fk_tp_title
        FOREIGN KEY (title_id) REFERENCES titles (title_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_tp_permission
        FOREIGN KEY (permission_id) REFERENCES permissions (permission_id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_responsibilities (
    user_responsibility_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    responsibility_id BIGINT UNSIGNED NOT NULL,
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by BIGINT UNSIGNED NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (user_responsibility_id),
    UNIQUE KEY uq_user_responsibility (user_id, responsibility_id),
    KEY idx_ur_responsibility (responsibility_id),
    KEY idx_ur_assigned_by (assigned_by),
    CONSTRAINT fk_ur_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ur_responsibility
        FOREIGN KEY (responsibility_id) REFERENCES responsibilities (responsibility_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ur_assigned_by
        FOREIGN KEY (assigned_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS staff_members (
    staff_member_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    person_type VARCHAR(100) NULL,
    phone VARCHAR(30) NULL,
    email VARCHAR(150) NULL,
    start_date DATE NULL,
    status VARCHAR(50) NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (staff_member_id),
    UNIQUE KEY uq_staff_user (user_id),
    KEY idx_staff_status (status),
    CONSTRAINT fk_staff_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 2. PROJECT AND ACCESS ASSIGNMENT
-- ============================================================

CREATE TABLE IF NOT EXISTS projects (
    project_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_name VARCHAR(200) NOT NULL,
    description TEXT NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    objectives TEXT NULL,
    status VARCHAR(50) NULL,
    created_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id),
    KEY idx_projects_status (status),
    KEY idx_projects_dates (start_date, end_date),
    KEY idx_projects_created_by (created_by),
    CONSTRAINT fk_projects_created_by
        FOREIGN KEY (created_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_project_assignments (
    assignment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    project_id BIGINT UNSIGNED NOT NULL,
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by BIGINT UNSIGNED NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (assignment_id),
    UNIQUE KEY uq_user_project (user_id, project_id),
    KEY idx_upa_project (project_id),
    KEY idx_upa_assigned_by (assigned_by),
    CONSTRAINT fk_upa_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_upa_project
        FOREIGN KEY (project_id) REFERENCES projects (project_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_upa_assigned_by
        FOREIGN KEY (assigned_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 3. BENEFICIARY AND SERVICE DELIVERY
-- ============================================================

CREATE TABLE IF NOT EXISTS beneficiaries (
    beneficiary_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    beneficiary_code VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NULL,
    sex VARCHAR(20) NULL,
    location VARCHAR(200) NULL,
    phone VARCHAR(30) NULL,
    registration_date DATE NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (beneficiary_id),
    UNIQUE KEY uq_beneficiary_code (beneficiary_code),
    KEY idx_beneficiaries_created_by (created_by),
    KEY idx_beneficiaries_status (status),
    KEY idx_beneficiaries_name (last_name, first_name),
    CONSTRAINT fk_beneficiaries_created_by
        FOREIGN KEY (created_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS disability_assessments (
    assessment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    beneficiary_id BIGINT UNSIGNED NOT NULL,
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(100) NULL,
    disability_type VARCHAR(100) NULL,
    needs TEXT NULL,
    assessment_notes TEXT NULL,
    assessed_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (assessment_id),
    KEY idx_da_beneficiary (beneficiary_id),
    KEY idx_da_assessed_by (assessed_by),
    KEY idx_da_date (assessment_date),
    CONSTRAINT fk_da_beneficiary
        FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries (beneficiary_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_da_assessed_by
        FOREIGN KEY (assessed_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS home_visits (
    home_visit_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    beneficiary_id BIGINT UNSIGNED NOT NULL,
    visit_date DATE NOT NULL,
    conducted_by BIGINT UNSIGNED NOT NULL,
    purpose VARCHAR(255) NULL,
    observations TEXT NULL,
    support_provided TEXT NULL,
    follow_up_required TINYINT(1) NOT NULL DEFAULT 0,
    next_action TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (home_visit_id),
    KEY idx_hv_beneficiary (beneficiary_id),
    KEY idx_hv_conducted_by (conducted_by),
    KEY idx_hv_date (visit_date),
    CONSTRAINT fk_hv_beneficiary
        FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries (beneficiary_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_hv_conducted_by
        FOREIGN KEY (conducted_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS referrals (
    referral_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    beneficiary_id BIGINT UNSIGNED NOT NULL,
    referral_date DATE NOT NULL,
    referral_destination VARCHAR(255) NOT NULL,
    reason TEXT NULL,
    referred_by BIGINT UNSIGNED NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'submitted',
    approved_by BIGINT UNSIGNED NULL,
    approved_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (referral_id),
    KEY idx_ref_beneficiary (beneficiary_id),
    KEY idx_ref_referred_by (referred_by),
    KEY idx_ref_approved_by (approved_by),
    KEY idx_ref_status (status),
    CONSTRAINT fk_ref_beneficiary
        FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries (beneficiary_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ref_referred_by
        FOREIGN KEY (referred_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ref_approved_by
        FOREIGN KEY (approved_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS referral_follow_ups (
    follow_up_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    referral_id BIGINT UNSIGNED NOT NULL,
    follow_up_date DATE NOT NULL,
    conducted_by BIGINT UNSIGNED NOT NULL,
    outcome TEXT NULL,
    service_received TINYINT(1) NOT NULL DEFAULT 0,
    remaining_needs TEXT NULL,
    next_action TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follow_up_id),
    KEY idx_rfu_referral (referral_id),
    KEY idx_rfu_conducted_by (conducted_by),
    KEY idx_rfu_date (follow_up_date),
    CONSTRAINT fk_rfu_referral
        FOREIGN KEY (referral_id) REFERENCES referrals (referral_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_rfu_conducted_by
        FOREIGN KEY (conducted_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 4. ACTIVITIES
-- ============================================================

CREATE TABLE IF NOT EXISTS activities (
    activity_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id BIGINT UNSIGNED NOT NULL,
    activity_name VARCHAR(200) NOT NULL,
    activity_date DATE NULL,
    location VARCHAR(200) NULL,
    responsible_user_id BIGINT UNSIGNED NOT NULL,
    description TEXT NULL,
    status VARCHAR(50) NULL,
    results TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (activity_id),
    KEY idx_activities_project (project_id),
    KEY idx_activities_responsible (responsible_user_id),
    KEY idx_activities_date (activity_date),
    KEY idx_activities_status (status),
    CONSTRAINT fk_activities_project
        FOREIGN KEY (project_id) REFERENCES projects (project_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_activities_responsible
        FOREIGN KEY (responsible_user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS activity_assignments (
    activity_assignment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    activity_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by BIGINT UNSIGNED NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'assigned',
    PRIMARY KEY (activity_assignment_id),
    UNIQUE KEY uq_activity_user_assignment (activity_id, user_id),
    KEY idx_aa_user (user_id),
    KEY idx_aa_assigned_by (assigned_by),
    CONSTRAINT fk_aa_activity
        FOREIGN KEY (activity_id) REFERENCES activities (activity_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_aa_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_aa_assigned_by
        FOREIGN KEY (assigned_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS activity_participants (
    participant_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    activity_id BIGINT UNSIGNED NOT NULL,
    beneficiary_id BIGINT UNSIGNED NOT NULL,
    participant_name VARCHAR(200) NULL,
    participant_type VARCHAR(100) NOT NULL DEFAULT 'beneficiary',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (participant_id),
    UNIQUE KEY uq_activity_beneficiary (activity_id, beneficiary_id),
    KEY idx_ap_beneficiary (beneficiary_id),
    CONSTRAINT fk_ap_activity
        FOREIGN KEY (activity_id) REFERENCES activities (activity_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ap_beneficiary
        FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries (beneficiary_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 5. POULTRY
-- ============================================================

CREATE TABLE IF NOT EXISTS poultry_groups (
    poultry_group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id BIGINT UNSIGNED NOT NULL,
    group_name VARCHAR(150) NOT NULL,
    poultry_category VARCHAR(100) NULL,
    breed_or_type VARCHAR(100) NULL,
    start_date DATE NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    description TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (poultry_group_id),
    UNIQUE KEY uq_poultry_group_project_name (project_id, group_name),
    KEY idx_pg_project (project_id),
    KEY idx_pg_status (status),
    CONSTRAINT fk_pg_project
        FOREIGN KEY (project_id) REFERENCES projects (project_id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS poultry_stock_movements (
    movement_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    poultry_group_id BIGINT UNSIGNED NOT NULL,
    movement_date DATE NOT NULL,
    movement_type VARCHAR(50) NOT NULL,
    quantity INT UNSIGNED NOT NULL,
    description TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (movement_id),
    KEY idx_psm_group (poultry_group_id),
    KEY idx_psm_date (movement_date),
    KEY idx_psm_type (movement_type),
    KEY idx_psm_recorded_by (recorded_by),
    CONSTRAINT fk_psm_group
        FOREIGN KEY (poultry_group_id) REFERENCES poultry_groups (poultry_group_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_psm_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS egg_production (
    egg_production_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    poultry_group_id BIGINT UNSIGNED NOT NULL,
    production_date DATE NOT NULL,
    eggs_produced INT UNSIGNED NOT NULL DEFAULT 0,
    eggs_used INT UNSIGNED NOT NULL DEFAULT 0,
    eggs_sold INT UNSIGNED NOT NULL DEFAULT 0,
    eggs_remaining INT UNSIGNED NOT NULL DEFAULT 0,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (egg_production_id),
    KEY idx_ep_group (poultry_group_id),
    KEY idx_ep_date (production_date),
    KEY idx_ep_recorded_by (recorded_by),
    CONSTRAINT fk_ep_group
        FOREIGN KEY (poultry_group_id) REFERENCES poultry_groups (poultry_group_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ep_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS feed_records (
    feed_record_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    poultry_group_id BIGINT UNSIGNED NOT NULL,
    record_date DATE NOT NULL,
    feed_source VARCHAR(200) NULL,
    feed_description TEXT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    unit VARCHAR(50) NULL,
    cost DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (feed_record_id),
    KEY idx_feed_group (poultry_group_id),
    KEY idx_feed_date (record_date),
    KEY idx_feed_recorded_by (recorded_by),
    CONSTRAINT fk_feed_group
        FOREIGN KEY (poultry_group_id) REFERENCES poultry_groups (poultry_group_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_feed_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_feed_quantity CHECK (quantity >= 0),
    CONSTRAINT chk_feed_cost CHECK (cost >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS poultry_health_records (
    health_record_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    poultry_group_id BIGINT UNSIGNED NOT NULL,
    record_date DATE NOT NULL,
    condition_type VARCHAR(100) NOT NULL,
    number_affected INT UNSIGNED NOT NULL DEFAULT 0,
    description TEXT NULL,
    action_taken TEXT NULL,
    outcome TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (health_record_id),
    KEY idx_phr_group (poultry_group_id),
    KEY idx_phr_date (record_date),
    KEY idx_phr_recorded_by (recorded_by),
    CONSTRAINT fk_phr_group
        FOREIGN KEY (poultry_group_id) REFERENCES poultry_groups (poultry_group_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_phr_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS poultry_sales (
    poultry_sale_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    poultry_group_id BIGINT UNSIGNED NOT NULL,
    sale_date DATE NOT NULL,
    quantity INT UNSIGNED NOT NULL,
    unit_price DECIMAL(12,2) NULL,
    total_amount DECIMAL(12,2) NULL,
    buyer_description VARCHAR(255) NULL,
    notes TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (poultry_sale_id),
    KEY idx_ps_group (poultry_group_id),
    KEY idx_ps_date (sale_date),
    KEY idx_ps_recorded_by (recorded_by),
    CONSTRAINT fk_ps_group
        FOREIGN KEY (poultry_group_id) REFERENCES poultry_groups (poultry_group_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ps_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_ps_unit_price CHECK (unit_price IS NULL OR unit_price >= 0),
    CONSTRAINT chk_ps_total_amount CHECK (total_amount IS NULL OR total_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 6. SMALL FARM
-- ============================================================

CREATE TABLE IF NOT EXISTS farm_crops (
    crop_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id BIGINT UNSIGNED NOT NULL,
    crop_name VARCHAR(200) NOT NULL,
    description TEXT NULL,
    planting_date DATE NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (crop_id),
    KEY idx_fc_project (project_id),
    KEY idx_fc_status (status),
    KEY idx_fc_recorded_by (recorded_by),
    CONSTRAINT fk_fc_project
        FOREIGN KEY (project_id) REFERENCES projects (project_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_fc_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS farm_activities (
    farm_activity_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    crop_id BIGINT UNSIGNED NOT NULL,
    activity_date DATE NOT NULL,
    activity_type VARCHAR(100) NOT NULL,
    description TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (farm_activity_id),
    KEY idx_fa_crop (crop_id),
    KEY idx_fa_date (activity_date),
    KEY idx_fa_recorded_by (recorded_by),
    CONSTRAINT fk_fa_crop
        FOREIGN KEY (crop_id) REFERENCES farm_crops (crop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_fa_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS harvests (
    harvest_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    crop_id BIGINT UNSIGNED NOT NULL,
    harvest_date DATE NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    unit VARCHAR(50) NULL,
    usage_type VARCHAR(100) NULL,
    notes TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (harvest_id),
    KEY idx_harvest_crop (crop_id),
    KEY idx_harvest_date (harvest_date),
    KEY idx_harvest_recorded_by (recorded_by),
    CONSTRAINT fk_harvest_crop
        FOREIGN KEY (crop_id) REFERENCES farm_crops (crop_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_harvest_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_harvest_quantity CHECK (quantity >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS farm_poultry_transfers (
    transfer_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    harvest_id BIGINT UNSIGNED NOT NULL,
    poultry_group_id BIGINT UNSIGNED NOT NULL,
    transfer_date DATE NOT NULL,
    quantity DECIMAL(12,2) NOT NULL,
    unit VARCHAR(50) NULL,
    notes TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transfer_id),
    KEY idx_fpt_harvest (harvest_id),
    KEY idx_fpt_group (poultry_group_id),
    KEY idx_fpt_date (transfer_date),
    KEY idx_fpt_recorded_by (recorded_by),
    CONSTRAINT fk_fpt_harvest
        FOREIGN KEY (harvest_id) REFERENCES harvests (harvest_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_fpt_group
        FOREIGN KEY (poultry_group_id) REFERENCES poultry_groups (poultry_group_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_fpt_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_fpt_quantity CHECK (quantity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 7. FINANCE
-- ============================================================

CREATE TABLE IF NOT EXISTS financial_transactions (
    transaction_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id BIGINT UNSIGNED NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(30) NOT NULL,
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(14,2) NOT NULL,
    description TEXT NULL,
    payment_method VARCHAR(50) NULL,
    reference_number VARCHAR(100) NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    approved_by BIGINT UNSIGNED NULL,
    approved_at DATETIME NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'recorded',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id),
    KEY idx_ft_project (project_id),
    KEY idx_ft_date (transaction_date),
    KEY idx_ft_type (transaction_type),
    KEY idx_ft_category (category),
    KEY idx_ft_recorded_by (recorded_by),
    KEY idx_ft_approved_by (approved_by),
    KEY idx_ft_status (status),
    CONSTRAINT fk_ft_project
        FOREIGN KEY (project_id) REFERENCES projects (project_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_ft_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ft_approved_by
        FOREIGN KEY (approved_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_ft_amount CHECK (amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 8. MONITORING AND EVALUATION
-- ============================================================

CREATE TABLE IF NOT EXISTS me_indicators (
    indicator_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id BIGINT UNSIGNED NULL,
    indicator_name VARCHAR(200) NOT NULL,
    description TEXT NULL,
    target_value DECIMAL(14,2) NULL,
    unit VARCHAR(50) NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (indicator_id),
    KEY idx_mei_project (project_id),
    KEY idx_mei_created_by (created_by),
    KEY idx_mei_status (status),
    CONSTRAINT fk_mei_project
        FOREIGN KEY (project_id) REFERENCES projects (project_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_mei_created_by
        FOREIGN KEY (created_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_mei_target CHECK (target_value IS NULL OR target_value >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS me_indicator_records (
    indicator_record_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    indicator_id BIGINT UNSIGNED NOT NULL,
    record_date DATE NOT NULL,
    recorded_value DECIMAL(14,2) NOT NULL,
    notes TEXT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (indicator_record_id),
    KEY idx_meir_indicator (indicator_id),
    KEY idx_meir_date (record_date),
    KEY idx_meir_recorded_by (recorded_by),
    CONSTRAINT fk_meir_indicator
        FOREIGN KEY (indicator_id) REFERENCES me_indicators (indicator_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_meir_recorded_by
        FOREIGN KEY (recorded_by) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 9. AUDIT
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_events (
    audit_event_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NULL,
    event_type VARCHAR(50) NOT NULL,
    entity_name VARCHAR(100) NULL,
    entity_id BIGINT UNSIGNED NULL,
    description TEXT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (audit_event_id),
    KEY idx_audit_user (user_id),
    KEY idx_audit_event_type (event_type),
    KEY idx_audit_entity (entity_name, entity_id),
    KEY idx_audit_created_at (created_at),
    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- 10. INITIAL APPLICATION DATA
-- ============================================================
-- Permission and title seed data should be inserted through a controlled
-- deployment/initialisation process after final permission and governance
-- validation. No production users or passwords are included here.

-- ============================================================
-- 11. DESIGN NOTES
-- ============================================================
-- 1. Poultry stock is derived from poultry_stock_movements.
-- 2. Poultry sales are operational records; related money is recorded in
--    financial_transactions.
-- 3. Farm harvests can be linked to poultry through farm_poultry_transfers.
-- 4. Beneficiaries are archived/inactivated rather than routinely deleted.
-- 5. Record-level access is implemented by application logic using the
--    accountable user relationships and project/activity assignments.
-- 6. Title, permission, and responsibility are intentionally separate.
-- 7. This schema is not a full accounting system.
-- 8. Controlled status/type values remain subject to final validation.
