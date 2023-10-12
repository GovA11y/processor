-- app/database/postgres/queries/get_naked_domains.sql
SELECT
  id AS "domain_id",
  "domain"
FROM targets.domains d
WHERE (home_url IS NULL OR home_url = '')
  AND active = TRUE
  AND "valid" = TRUE
LIMIT 1;

