SELECT count(*)
FROM nodes;

SELECT count(*) 
FROM nodes_tags;

SELECT count(*) 
FROM ways;

SELECT count(*) 
FROM ways_nodes;

SELECT count(*) 
FROM ways_tags;

SELECT value, count(*) as search_amount 
FROM nodes_tags
WHERE value = 'cafe';

SELECT value, count(*) as search_amount 
FROM ways_tags
WHERE value = 'cafe';

SELECT *
FROM ways_tags
WHERE value = 'abandoned';

SELECT *
FROM nodes
WHERE user = 'NO_USER';

SELECT user, count(*) AS contributions
FROM nodes 
GROUP BY user
ORDER BY contributions DESC
LIMIT 10;

SELECT user, count(*) AS contributions
FROM ways 
GROUP BY user
ORDER BY contributions DESC
LIMIT 10;

SELECT key, value
FROM nodes_tags
WHERE type = 'name';

SELECT key, value
FROM ways_tags
WHERE type = 'name';

SELECT key, value
FROM nodes_tags
WHERE type = 'fixme';

SELECT key, value
FROM ways_tags
WHERE type = 'fixme';

SELECT key, value
FROM nodes_tags
WHERE key = 'FIXME';

SELECT key, value
FROM ways_tags
WHERE key = 'FIXME';