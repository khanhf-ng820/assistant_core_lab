-- Lab 5 Part F: write your queries for the assistant database here.
-- Author: Lý Tuấn Kiệt (MSSV: 25125022, @kiethm07) - Developer
-- Reviewer: Nguyễn Minh Khang (MSSV: 25125018, @nmkhang_student) - QA/QC

-- Q1 requests per intent
SELECT
    intent,
    COUNT(*) AS total_requests
FROM interaction
GROUP BY intent
ORDER BY total_requests DESC, intent ASC;

-- Q2 average latency per intent
SELECT
    intent,
    ROUND(AVG(latency_ms), 2) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY avg_latency_ms DESC, intent ASC;

-- Q3 topics with the most thumbs-down (JOIN feedback with interaction)
SELECT
    i.topic,
    COUNT(*) AS thumbs_down_count
FROM feedback f
JOIN interaction i ON f.request_id = i.request_id
WHERE f.rating = -1
  AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_down_count DESC, i.topic ASC;
