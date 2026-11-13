-- Lab 5 Part F: write your queries for the assistant database here.
-- Q1 requests per intent

-- Q2 average latency per intent

-- Q3 topics with the most thumbs-down (JOIN feedback with interaction)

-- H2 (Dang Xuan Phat - 25125062): Backup/degraded path share, latency impact, unresolved rate, and negative feedback across intents & handbook topics
-- Question: What share of answers used the degraded/backup path overall and per (intent, topic), and how does degraded execution correlate with latency and thumbs-down feedback?
-- Quick CLI execution:
--   python3 -c "import sqlite3; con = sqlite3.connect('assistant.db'); print(con.execute(open('sql/my_queries.sql', encoding='utf-8').read()).fetchall())"
-- Or via sqlite3 CLI:
--   sqlite3 -header -column assistant.db < sql/my_queries.sql
WITH fb_summary AS (
    SELECT
        request_id,
        COUNT(*) AS feedback_count,
        SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) AS thumbs_down_count
    FROM feedback
    GROUP BY request_id
),
levels AS (
    SELECT 0 AS sort_group
    UNION ALL
    SELECT 1 AS sort_group
)
SELECT
    CASE WHEN l.sort_group = 1 THEN 'ALL' ELSE i.intent END AS intent,
    CASE WHEN l.sort_group = 1 THEN '(all)' ELSE COALESCE(i.topic, '(none)') END AS topic,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN i.degraded = 1 THEN 1 ELSE 0 END) AS degraded_requests,
    ROUND(100.0 * SUM(CASE WHEN i.degraded = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS degraded_pct,
    ROUND(AVG(CASE WHEN i.degraded = 0 THEN i.latency_ms END), 1) AS avg_normal_ms,
    ROUND(AVG(CASE WHEN i.degraded = 1 THEN i.latency_ms END), 1) AS avg_degraded_ms,
    SUM(CASE WHEN i.resolved = 0 THEN 1 ELSE 0 END) AS unresolved_requests,
    COALESCE(SUM(f.feedback_count), 0) AS feedback_count,
    COALESCE(SUM(f.thumbs_down_count), 0) AS thumbs_down_count,
    COALESCE(
        ROUND(100.0 * SUM(f.thumbs_down_count) / NULLIF(SUM(f.feedback_count), 0), 1),
        0.0
    ) AS thumbs_down_pct
FROM interaction i
LEFT JOIN fb_summary f ON f.request_id = i.request_id
CROSS JOIN levels l
GROUP BY
    l.sort_group,
    CASE WHEN l.sort_group = 1 THEN 'ALL' ELSE i.intent END,
    CASE WHEN l.sort_group = 1 THEN '(all)' ELSE COALESCE(i.topic, '(none)') END
ORDER BY l.sort_group, degraded_pct DESC, thumbs_down_count DESC, intent, topic;

-- Executed on seeded assistant.db (300 interactions, 59 sessions, 96 feedback entries, random.seed(7)):
-- intent   | topic   | total_requests | degraded_requests | degraded_pct | avg_normal_ms | avg_degraded_ms | unresolved_requests | feedback_count | thumbs_down_count | thumbs_down_pct
-- ---------+---------+----------------+-------------------+--------------+---------------+-----------------+---------------------+----------------+-------------------+----------------
-- rule     | H26-7.2 | 11             | 4                 | 36.36        | 64.7          | 236.3           | 0                   | 3              | 2                 | 66.7
-- rule     | H26-4.2 | 45             | 11                | 24.44        | 46.3          | 184.2           | 0                   | 16             | 8                 | 50.0
-- rule     | H26-5.3 | 84             | 19                | 22.62        | 39.4          | 163.4           | 0                   | 28             | 8                 | 28.6
-- greeting | (none)  | 26             | 2                 | 7.69         | 1.9           | 7.8             | 0                   | 7              | 2                 | 28.6
-- office   | (none)  | 47             | 1                 | 2.13         | 3.2           | 12.1            | 0                   | 13             | 3                 | 23.1
-- fee      | (none)  | 61             | 1                 | 1.64         | 4.8           | 21.2            | 0                   | 21             | 4                 | 19.0
-- unknown  | (none)  | 26             | 0                 | 0.0          | 8.1           | NULL            | 26                  | 8              | 8                 | 100.0
-- ALL      | (all)   | 300            | 38                | 12.67        | 20.2          | 161.2           | 26                  | 96             | 35                | 36.5
