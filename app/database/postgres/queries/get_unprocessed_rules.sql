-- app/database/postgres/queries/get_unprocessed_rules.sql

SELECT id as rule_id
FROM axe.rules
WHERE imported = false
ORDER BY id
LIMIT %s OFFSET %s
