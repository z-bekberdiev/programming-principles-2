-- READ CONTACT
CREATE OR REPLACE FUNCTION read_contact(
    reverse_data BOOLEAN,
    reverse_column VARCHAR,
    filter_data BOOLEAN,
    filter_column VARCHAR,
    filter_pattern VARCHAR
)
RETURNS TABLE (
    contact_id UUID,
    contact_name VARCHAR,
    contact_email VARCHAR,
    contact_birthday VARCHAR,
    contact_phones JSON,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $function$
DECLARE
    order_direction TEXT;
    sql_query TEXT;
    order_column TEXT;
BEGIN
    -- Determine order direction
    IF reverse_data THEN
        order_direction := 'DESC';
    ELSE
        order_direction := 'ASC';
    END IF;

    -- Map the column name to a fully qualified column
    CASE reverse_column
        WHEN 'contact_id' THEN order_column := 'contacts.contact_id';
        WHEN 'contact_name' THEN order_column := 'contacts.contact_name';
        WHEN 'contact_email' THEN order_column := 'contacts.contact_email';
        WHEN 'contact_birthday' THEN order_column := 'contacts.contact_birthday';
        WHEN 'group_name' THEN order_column := 'groups.group_name';
        ELSE
            RAISE NOTICE 'FAILURE: Unknown reverse column: %', reverse_column;
            order_column := 'contacts.contact_name'; -- Default fallback
    END CASE;

    -- Build dynamic SQL
    sql_query := '
        SELECT 
            contacts.contact_id,
            contacts.contact_name,
            contacts.contact_email,
            contacts.contact_birthday::VARCHAR,
            COALESCE(
                json_agg(
                    json_build_object(
                        ''phone_type'', phones.phone_type,
                        ''phone_number'', phones.phone_number
                    )
                ) FILTER (WHERE phones.phone_id IS NOT NULL),
                ''[]''::JSON
            ) AS contact_phones,
            groups.group_name
        FROM contacts
        LEFT JOIN phones ON contacts.contact_id = phones.contact_id
        LEFT JOIN groups ON contacts.group_id = groups.group_id
    ';

    -- Add filtering if requested
    IF filter_data THEN
        sql_query := sql_query || ' WHERE ' || quote_ident(filter_column) || ' LIKE ' || quote_literal(filter_pattern);
    END IF;

    -- Group by contact and group
    sql_query := sql_query || ' GROUP BY contacts.contact_id, groups.group_name';

    -- Add ordering
    sql_query := sql_query || ' ORDER BY ' || order_column || ' ' || order_direction;

    -- Execute dynamic SQL
    RETURN QUERY EXECUTE sql_query;
END;
$function$;

-- SEARCH CONTACT
CREATE OR REPLACE FUNCTION public.search_contact(
    search_column VARCHAR,
    search_pattern VARCHAR
)
RETURNS TABLE (
    contact_id UUID,
    contact_name VARCHAR,
    contact_email VARCHAR,
    contact_birthday VARCHAR,
    contact_phones JSON,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $function$
DECLARE
    sql_query TEXT;
    valid_columns TEXT[] := ARRAY[
        'contact_id',
        'contact_name',
        'contact_email',
        'contact_birthday',
        'phone_number',
        'phone_type',
        'group_name'
    ];
    result_count INT;
BEGIN
    -- Validate the input column
    IF NOT search_column = ANY(valid_columns) THEN
        RAISE NOTICE 'FAILURE: Valid columns: %', valid_columns;
        RETURN;
    END IF;

    -- Build base dynamic SQL
    sql_query := '
        SELECT
            contacts.contact_id,
            contacts.contact_name,
            contacts.contact_email,
            contacts.contact_birthday::VARCHAR,
            COALESCE(
                json_agg(
                    json_build_object(
                        ''phone_type'', phones.phone_type,
                        ''phone_number'', phones.phone_number
                    )
                ) FILTER (WHERE phones.phone_id IS NOT NULL),
                ''[]''::JSON
            ) AS contact_phones,
            groups.group_name
        FROM contacts
        LEFT JOIN groups ON contacts.group_id = groups.group_id
        LEFT JOIN phones ON contacts.contact_id = phones.contact_id
        WHERE ';

    -- Determine table prefix for the column
    IF search_column = 'contact_id' THEN
        sql_query := sql_query || 'contacts.' || quote_ident(search_column) || ' = ' || quote_literal(search_pattern::UUID);
    ELSEIF search_column IN ('contact_name', 'contact_email', 'contact_birthday') THEN
        sql_query := sql_query || 'contacts.' || quote_ident(search_column) || ' ILIKE ' || quote_literal('%' || search_pattern || '%');
    ELSEIF search_column IN ('phone_number', 'phone_type') THEN
        sql_query := sql_query || 'phones.' || quote_ident(search_column) || ' ILIKE ' || quote_literal('%' || search_pattern || '%');
    ELSEIF search_column = 'group_name' THEN
        sql_query := sql_query || 'groups.group_name ILIKE ' || quote_literal('%' || search_pattern || '%');
    END IF;

    -- Add additional OR conditions for phones and group
    sql_query := sql_query || '
        GROUP BY contacts.contact_id, groups.group_name
    ';

    -- Execute dynamic SQL into a temporary table
    EXECUTE 'CREATE TEMP TABLE temp_result AS ' || sql_query;

    -- Count result
    SELECT COUNT(*) INTO result_count FROM temp_result;

    IF result_count = 0 THEN
        RAISE NOTICE 'FAILURE: No contacts found matching the search pattern "%"', search_pattern;
    ELSE
        RAISE NOTICE 'SUCCESS: % contacts found matching the search pattern "%"', result_count, search_pattern;
    END IF;

    -- Return the result
    RETURN QUERY SELECT * FROM temp_result;

    -- Drop temp table
    DROP TABLE temp_result;
END;
$function$;