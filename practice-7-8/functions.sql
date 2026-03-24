-- Read contacts
CREATE OR REPLACE FUNCTION public.read_contacts(with_filter boolean, search_column character varying, search_pattern character varying, with_reverse boolean, with_pagination boolean, page_number integer, page_size integer)
 RETURNS SETOF phonebook
 LANGUAGE plpgsql
AS $function$
DECLARE
    vertical_offset integer;
BEGIN
    vertical_offset := (page_number - 1) * page_size;
    IF (with_filter) THEN
        IF (with_pagination) THEN
            IF (with_reverse) THEN      
                RETURN QUERY EXECUTE format('SELECT * FROM phonebook WHERE %I LIKE %L ORDER BY firstname DESC, lastname DESC LIMIT %L OFFSET %L;', search_column, search_pattern, page_size, vertical_offset);
            ELSE
                RETURN QUERY EXECUTE format('SELECT * FROM phonebook WHERE %I LIKE %L ORDER BY firstname ASC, lastname ASC LIMIT %L OFFSET %L;', search_column, search_pattern, page_size, vertical_offset);
            END IF;
        ELSE
            IF (with_reverse) THEN
                RETURN QUERY EXECUTE format('SELECT * FROM phonebook WHERE %I LIKE %L ORDER BY firstname DESC, lastname DESC;', search_column, search_pattern);
            ELSE
                RETURN QUERY EXECUTE format('SELECT * FROM phonebook WHERE %I LIKE %L ORDER BY firstname ASC, lastname ASC;', search_column, search_pattern);
            END IF;
        END IF;
    ELSE
        IF (with_pagination) THEN
            IF (with_reverse) THEN      
                RETURN QUERY SELECT * FROM phonebook ORDER BY firstname DESC, lastname DESC LIMIT page_size OFFSET vertical_offset;
            ELSE
                RETURN QUERY SELECT * FROM phonebook ORDER BY firstname ASC, lastname ASC LIMIT page_size OFFSET vertical_offset;
            END IF;
        ELSE
            IF (with_reverse) THEN
                RETURN QUERY SELECT * FROM phonebook ORDER BY firstname DESC, lastname DESC;
            ELSE
                RETURN QUERY SELECT * FROM phonebook ORDER BY firstname ASC, lastname ASC;
            END IF;
        END IF;
    END IF;
END;
$function$
