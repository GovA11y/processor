SELECT
  id AS "domain_id",
  "domain"
FROM targets.domains d
WHERE home_url IS NULL
  AND active = TRUE
  AND "valid" = TRUE
LIMIT 1;
