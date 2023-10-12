-- app/database/postgres/queries/upsert_url.sql
INSERT INTO targets.urls (url, domain_id)
VALUES (:home_url, :domain_id)
ON CONFLICT (url) DO UPDATE SET url = :home_url, domain_id = :domain_id
RETURNING id;
