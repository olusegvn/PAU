DO
$$
    DECLARE
        drop_statement text;
    BEGIN
        FOR drop_statement IN
            SELECT 'DROP TABLE IF EXISTS ' || quote_ident(schemaname) || '.' || quote_ident(tablename) || ' CASCADE;'
            FROM pg_tables
            WHERE schemaname = 'public'
            LOOP
                RAISE NOTICE 'Executing: %', drop_statement;
                EXECUTE drop_statement;
            END LOOP;
    END
$$;