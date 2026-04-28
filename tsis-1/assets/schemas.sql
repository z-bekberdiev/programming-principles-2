-- Enable pgcrypto extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================
-- Groups table
-- =========================
CREATE TABLE IF NOT EXISTS groups (
    group_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_name VARCHAR(16) UNIQUE NOT NULL
);

-- =========================
-- Contacts table
-- =========================
CREATE TABLE IF NOT EXISTS contacts (
    contact_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_name     VARCHAR(64) NOT NULL,
    contact_email    VARCHAR(64) UNIQUE NOT NULL,
    contact_birthday DATE NOT NULL,
    group_id         UUID NOT NULL,
    CONSTRAINT fk_contacts FOREIGN KEY (group_id)
        REFERENCES groups (group_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =========================
-- Phones table
-- =========================
CREATE TABLE IF NOT EXISTS phones (
    phone_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(16) UNIQUE NOT NULL,
    phone_type   VARCHAR(16) NOT NULL,
    contact_id   UUID NOT NULL,
    CONSTRAINT fk_phones FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);