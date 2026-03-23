-- Create contacts
CREATE OR REPLACE PROCEDURE public.create_contacts(IN contacts character varying[])
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    contact character varying[];
BEGIN
    FOREACH contact SLICE 1 IN ARRAY contacts LOOP
        IF (SELECT contact[1] ~ '^[A-Z]{1}[a-z]{1,14}(\-[A-Z]{1}[a-z]{1,14})?$' AND contact[2] ~ '^[A-Z]{1}[a-z]{1,14}(\-[A-Z]{1}[a-z]{1,14})?$' AND contact[3] ~ '^\+[0-9]{1,2}\([0-9]{3,4}\)[0-9]{2,3}\-[0-9]{1,2}\-[0-9]{1,2}$' AND contact[4] ~ '^([0-9]+)(\ [a-zA-Z]+)+(\ (St|Rd|Ave|Blvd|Sq))$') THEN
            IF NOT EXISTS (SELECT 1 FROM phonebook WHERE number = contact[3]) THEN
                IF NOT EXISTS (SELECT 1 FROM phonebook WHERE firstname = contact[1] AND lastname = contact[2] AND address = contact[4]) THEN
                    INSERT INTO phonebook (firstname, lastname, number, address) VALUES (contact[1], contact[2], contact[3], contact[4]);
                    RAISE NOTICE 'success: the contact ("%", "%", "%", "%") was added to the phonebook', contact[1], contact[2], contact[3], contact[4];
                ELSE
                    UPDATE phonebook SET number = contact[3] WHERE firstname = contact[1] AND lastname = contact[2] AND address = contact[4];
                    RAISE NOTICE 'success: the contact ("%", "%", "%", "%") was updated in the phonebook', contact[1], contact[2], contact[3], contact[4];
                END IF;
            ELSE
                RAISE NOTICE 'failure: the contact with the number "%" already exists', contact[3];
            END IF;
        ELSE
            RAISE NOTICE 'failure: the contact ("%", "%", "%", "%") was not added to the phonebook because it failed a validation', contact[1], contact[2], contact[3], contact[4];
        END IF;
    END LOOP;
END;
$procedure$

-- Update contacts
CREATE OR REPLACE PROCEDURE public.update_contacts(IN contacts character varying[])
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    contact character varying[];
    result character varying;
BEGIN
    FOREACH contact SLICE 1 IN ARRAY contacts LOOP
        IF EXISTS (SELECT 1 FROM phonebook WHERE number = contact[1]) THEN
            IF (SELECT contact[3] ~ '^[A-Z]{1}[a-z]{1,14}(\-[A-Z]{1}[a-z]{1,14})?$' OR contact[3] ~ '^\+[0-9]{1,2}\([0-9]{3,4}\)[0-9]{2,3}\-[0-9]{1,2}\-[0-9]{1,2}$' OR contact[3] ~ '^([0-9]+)(\ [a-zA-Z]+)+(\ (St|Rd|Ave|Blvd|Sq))$') THEN
                EXECUTE format('SELECT %I FROM phonebook WHERE number = %L;', contact[2], contact[1]) INTO result;
                IF (contact[3] != result) THEN
                    EXECUTE format('UPDATE phonebook SET %I = %L WHERE number = %L;', contact[2], contact[3], contact[1]);
                    RAISE NOTICE 'success: % of the contact with the number "%" was updated to "%"', contact[2], contact[1], contact[3];
                ELSE
                    RAISE NOTICE 'failure: the % was not changed because it was similar to the existing one', contact[2];
                END IF;
            ELSE
                RAISE NOTICE 'failure: the % was not changed because it failed a validation', contact[2];
            END IF;
        ELSE
            RAISE NOTICE 'failure: the contact with the number "%" does not exist', contact[1];
        END IF;
    END LOOP;
END;
$procedure$

-- Delete contacts
CREATE OR REPLACE PROCEDURE public.delete_contacts(IN credentials character varying[])
 LANGUAGE plpgsql
AS $procedure$
DECLARE
    credential character varying;
BEGIN
    FOREACH credential SLICE 0 IN ARRAY credentials LOOP
        IF (SELECT credential ~ '^\+[0-9]{1,2}\([0-9]{3,4}\)[0-9]{2,3}\-[0-9]{1,2}\-[0-9]{1,2}$') THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE number = credential) THEN
                DELETE FROM phonebook WHERE number = credential;
                RAISE NOTICE 'success: the contact with the number "%" was deleted', credential;
            ELSE
                RAISE NOTICE 'failure: the contact with the number "%" does not exist', credential;
            END IF;
        ELSE
            RAISE NOTICE 'failure: the contact was not deleted because the number "%" failed a validation', credential;
        END IF;
    END LOOP;
END;
$procedure$
