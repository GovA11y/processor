-- app/database/postgres/queries/clothe_domains.sql
-- Creates url entry
UPDATE targets.domains d
SET home_url = :home_url
WHERE id = :domain_id
RETURNING id;
