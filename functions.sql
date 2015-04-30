CREATE OR REPLACE FUNCTION parse_numeric(numeric_str text) RETURNS NUMERIC LANGUAGE plpgsql AS $$
	BEGIN
		RETURN numeric_str::NUMERIC;
	EXCEPTION WHEN OTHERS THEN
		RETURN NULL;
	END
$$ IMMUTABLE;

-- https://github.com/fhirbase/fhirbase/blob/60d7480523649078e2f44a5d16dbed783038f12e/src/fhirbase_date_idx.sql

CREATE OR REPLACE FUNCTION parse_date_to_lower(date_str text) RETURNS timestamptz LANGUAGE sql AS $$
	SELECT CASE
	WHEN date_str IS NULL THEN
		NULL
	WHEN date_str ~ '^\d\d\d\d$' THEN
		(date_str || '-01-01 00:00:00')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d$' THEN
		(date_str || '-01 00:00:00')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d$' THEN
		(date_str || ' 00:00:00')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d( |T)\d\d$' THEN
		(date_str || ':00:00')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d( |T)\d\d:\d\d$' THEN
		(date_str || ':00')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d( |T)\d\d:\d\d:\d\d(\.\d+)?((\+|\-)\d\d:\d\d)?$' THEN -- full date
		date_str::timestamptz
	ELSE
		NULL
	END
$$ IMMUTABLE;

CREATE OR REPLACE FUNCTION parse_date_to_upper(date_str text) RETURNS timestamptz LANGUAGE sql AS $$
	SELECT CASE
	WHEN date_str IS NULL THEN
		NULL
	WHEN date_str ~ '^\d\d\d\d$' THEN
		(date_str || '-01-01 00:00:00')::timestamptz + interval '1 year' - interval '1 second'
	WHEN date_str ~ '^\d\d\d\d-\d\d$' THEN
		(date_str || '-01 00:00:00')::timestamptz + interval '1 month' - interval '1 second'
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d$' THEN
		(date_str || ' 23:59:59')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d( |T)\d\d$' THEN
		(date_str || ':59:59')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d( |T)\d\d:\d\d$' THEN
		(date_str || ':59')::timestamptz
	WHEN date_str ~ '^\d\d\d\d-\d\d-\d\d( |T)\d\d:\d\d:\d\d(\.\d+)?((\+|\-)\d\d:\d\d)?$' THEN -- full date
		date_str::timestamptz
	ELSE
		NULL
	END
$$ IMMUTABLE;