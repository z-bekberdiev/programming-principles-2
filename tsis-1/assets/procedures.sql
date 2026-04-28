-- CREATE CONTACT
CREATE OR REPLACE PROCEDURE public.create_contact(contact_credentials JSON)
LANGUAGE plpgsql
AS $procedure$
DECLARE
    group_uuid UUID;
    contact_uuid UUID;
    contact_phone JSON;
    contact_credential JSON;
BEGIN
    FOR contact_credential IN 
        SELECT * FROM json_array_elements(contact_credentials) 
    LOOP
        -- Insert group if it doesn't exist
        INSERT INTO groups (group_name)
        VALUES (contact_credential->>'group_name')
        ON CONFLICT (group_name) DO NOTHING
        RETURNING group_id INTO group_uuid;

        IF group_uuid IS NULL THEN
            SELECT group_id 
            INTO group_uuid
            FROM groups
            WHERE group_name = contact_credential->>'group_name';
        END IF;

        -- Insert contact if email doesn't exist
        IF NOT EXISTS (
            SELECT 1 
            FROM contacts
            WHERE contact_email = contact_credential->>'contact_email'
        ) THEN
            INSERT INTO contacts (contact_name, contact_email, contact_birthday, group_id)
            VALUES (
                contact_credential->>'contact_name',
                contact_credential->>'contact_email',
                (contact_credential->>'contact_birthday')::DATE,
                group_uuid
            )
            RETURNING contact_id INTO contact_uuid;

            -- Insert phones to contact
            FOR contact_phone IN 
                SELECT * FROM json_array_elements(contact_credential->'contact_phones') 
            LOOP
                IF NOT EXISTS (
                    SELECT 1 
                    FROM phones 
                    WHERE phone_number = contact_phone->>'phone_number'
                ) THEN
                    INSERT INTO phones (phone_number, phone_type, contact_id)
                    VALUES (
                        contact_phone->>'phone_number', 
                        contact_phone->>'phone_type', 
                        contact_uuid
                    );
                    RAISE NOTICE 'SUCCESS: Phone number "%" added to the contact "%"', 
                        contact_phone->>'phone_number', 
                        contact_credential->>'contact_name';
                ELSE
                    RAISE NOTICE 'FAILURE: Phone number "%" already exists', 
                        contact_phone->>'phone_number';
                END IF;
            END LOOP;

            RAISE NOTICE 'SUCCESS: Contact "%" created', 
                contact_credential->>'contact_name';
        ELSE
            RAISE NOTICE 'FAILURE: Contact with an email "%" already exists', 
                contact_credential->>'contact_email';
        END IF;
    END LOOP;
END;
$procedure$;

-- UPDATE CONTACT
CREATE OR REPLACE PROCEDURE public.update_contact(contact_credentials JSON)
LANGUAGE plpgsql
AS $procedure$
DECLARE
    group_uuid UUID;
    contact_uuid UUID;
    contact_phone JSON;
BEGIN
    -- Get the contact ID from JSON
    contact_uuid := (contact_credentials->>'contact_id')::UUID;

    -- Check if contact exists
    IF NOT EXISTS (
        SELECT 1 
        FROM contacts
        WHERE contact_id = contact_uuid
    ) THEN
        RAISE NOTICE 'FAILURE: Contact with an ID "%" does not exist', contact_uuid;
        RETURN;
    END IF;

    -- Get group ID, insert if it doesn't exist
    SELECT group_id 
    INTO group_uuid
    FROM groups
    WHERE group_name = contact_credentials->>'group_name';

    IF group_uuid IS NULL THEN
        INSERT INTO groups (group_name)
        VALUES (contact_credentials->>'group_name')
        RETURNING group_id INTO group_uuid;

        RAISE NOTICE 'SUCCESS: Group "%" created', contact_credentials->>'group_name';
    END IF;

    -- Update contact information
    UPDATE contacts
    SET contact_name = contact_credentials->>'contact_name',
        contact_email = contact_credentials->>'contact_email',
        contact_birthday = (contact_credentials->>'contact_birthday')::DATE,
        group_id = group_uuid
    WHERE contact_id = contact_uuid;

    -- Remove existing phones
    DELETE FROM phones 
    WHERE contact_id = contact_uuid;

    -- Add updated phones
    FOR contact_phone IN 
        SELECT * FROM json_array_elements(contact_credentials->'contact_phones') 
    LOOP
        INSERT INTO phones (phone_number, phone_type, contact_id)
        VALUES (
            contact_phone->>'phone_number', 
            contact_phone->>'phone_type', 
            contact_uuid
        );

        RAISE NOTICE 'SUCCESS: Phone number "%" updated/added to the contact with an ID "%"', 
            contact_phone->>'phone_number', 
            contact_uuid;
    END LOOP;

    RAISE NOTICE 'SUCCESS: Contact with an ID "%" updated', contact_uuid;
END;
$procedure$;

-- DELETE CONTACT
CREATE OR REPLACE PROCEDURE public.delete_contact(contact_uuid UUID)
LANGUAGE plpgsql
AS $procedure$
BEGIN
    -- Check if contact exists
    IF NOT EXISTS (
        SELECT 1 
        FROM contacts
        WHERE contact_id = contact_uuid
    ) THEN
        RAISE NOTICE 'FAILURE: Contact with an ID "%" does not exist', contact_uuid;
        RETURN;
    END IF;

    -- Delete the contact (phones automatically deleted via ON DELETE CASCADE)
    DELETE FROM contacts
    WHERE contact_id = contact_uuid;

    RAISE NOTICE 'SUCCESS: Contact with an ID "%" deleted', contact_uuid;
END;
$procedure$;

-- ADD PHONE TO CONTACT
CREATE OR REPLACE PROCEDURE public.add_phone_to_contact(
    temp_contact_id VARCHAR,
    temp_phone_number VARCHAR,
    temp_phone_type VARCHAR
)
LANGUAGE plpgsql
AS $procedure$
DECLARE
    contact_uuid UUID;
BEGIN
    -- Convert input contact_id to UUID
    contact_uuid := temp_contact_id::UUID;

    -- Check if contact exists
    IF NOT EXISTS (
        SELECT 1 
        FROM contacts
        WHERE contact_id = contact_uuid
    ) THEN
        RAISE NOTICE 'FAILURE: Contact with an ID "%" does not exist', temp_contact_id;
        RETURN;
    END IF;

    -- Check if phone number already exists
    IF EXISTS (
        SELECT 1 
        FROM phones 
        WHERE phone_number = temp_phone_number
    ) THEN
        RAISE NOTICE 'FAILURE: Phone number "%" already exists', temp_phone_number;
        RETURN;
    END IF;

    -- Insert the new phone
    INSERT INTO phones (phone_number, phone_type, contact_id)
    VALUES (temp_phone_number, temp_phone_type, contact_uuid);

    RAISE NOTICE 'SUCCESS: Phone number "%" added to the contact with an ID "%"', temp_phone_number, temp_contact_id;
END;
$procedure$;

-- MOVE CONTACT TO GROUP
CREATE OR REPLACE PROCEDURE public.move_contact_to_group(
    temp_contact_id VARCHAR,
    temp_group_name VARCHAR
)
LANGUAGE plpgsql
AS $procedure$
DECLARE
    group_uuid UUID;
    contact_uuid UUID;
BEGIN
    -- Convert input contact_id to UUID
    contact_uuid := temp_contact_id::UUID;

    -- Check if contact exists
    IF NOT EXISTS (
        SELECT 1 
        FROM contacts
        WHERE contact_id = contact_uuid
    ) THEN
        RAISE NOTICE 'FAILURE: Contact with an ID "%" does not exist', temp_contact_id;
        RETURN;
    END IF;

    -- Check if group exists
    SELECT group_id 
    INTO group_uuid
    FROM groups
    WHERE group_name = temp_group_name;

    -- If group doesn't exist, create it
    IF group_uuid IS NULL THEN
        INSERT INTO groups (group_name) 
        VALUES (temp_group_name)
        RETURNING group_id INTO group_uuid;

        RAISE NOTICE 'SUCCESS: Group "%" created', temp_group_name;
    END IF;

    -- Update contact's group
    UPDATE contacts
    SET group_id = group_uuid
    WHERE contact_id = contact_uuid;

    RAISE NOTICE 'SUCCESS: Contact with an ID "%" moved to the group "%"', temp_contact_id, temp_group_name;
END;
$procedure$;