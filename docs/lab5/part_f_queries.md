# Lab 5 — Part F SQL Queries & Assistant Database Insights

**Author:** Lý Tuấn Kiệt (MSSV: 25125022, `@kiethm07`) — Developer  
**Reviewer:** Nguyễn Minh Khang (MSSV: 25125018, `@nmkhang_student`) — QA/QC  
**Branch:** `feat/part-f-queries`  
**Target Files:** `sql/my_queries.sql`, `lab05/starter/sql/my_queries.sql`  

---

## 1. Overview & Objective

Part F focuses on deriving operational insights from synthetic interaction and feedback records stored in SQLite (`assistant.db`). The goal is to monitor system health, detect performance bottlenecks, and identify topics causing user dissatisfaction.

All queries are executed against the standardized synthetic dataset generated via:
```bash
python scripts/migrate.py assistant.db
python scripts/seed.py assistant.db 300
```
- **Total interactions:** 300
- **Total chat sessions:** 59
- **Total feedback records:** 96 (35 negative / thumbs-down)

---

## 2. Query Specifications & Execution Results

### F1. Requests Per Intent (Q1)

Measures total interaction volume grouped by detected user intent.

#### SQL Query
```sql
SELECT
    intent,
    COUNT(*) AS total_requests
FROM interaction
GROUP BY intent
ORDER BY total_requests DESC, intent ASC;
```

#### Results on Seeded `assistant.db` (300 interactions)
| Intent | Total Requests | Percentage of Traffic |
| :--- | :---: | :---: |
| `rule` | 140 | 46.67% |
| `fee` | 61 | 20.33% |
| `office` | 47 | 15.67% |
| `greeting` | 26 | 8.67% |
| `unknown` | 26 | 8.67% |
| **Total** | **300** | **100.0%** |

#### Operational Insight
- The `rule` intent dominates system usage (~47%), indicating that handbook retrieval is the primary value proposition.
- `unknown` intent represents ~8.7% of all incoming requests, identifying traffic that fell completely outside the intent classifier scope.

---

### F2. Average Latency Per Intent (Q2)

Measures response processing latency in milliseconds (`latency_ms`) across each intent to evaluate performance and identify computational bottlenecks.

#### SQL Query
```sql
SELECT
    intent,
    ROUND(AVG(latency_ms), 2) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY avg_latency_ms DESC, intent ASC;
```

#### Results on Seeded `assistant.db`
| Intent | Average Latency (`ms`) | Observations |
| :--- | :---: | :--- |
| `rule` | **76.18** | High variance due to handbook text retrieval and degraded fallback paths (~161 ms when degraded). |
| `unknown` | **8.06** | Fast rejection path when classifier confidence is zero. |
| `fee` | **5.07** | Direct deterministic calculation from parsed credit load. |
| `office` | **3.40** | Fast CSV lookup in memory/table directory. |
| `greeting` | **2.40** | Static template response with minimal overhead. |

#### Operational Insight
- `rule` queries take significantly longer (~76 ms average) compared to simple static or lookup queries (2–5 ms). Optimizing handbook keyword retrieval and minimizing degraded path invocation will yield the highest user-perceived performance gains.

---

### F3. Handbook Topics With The Most Thumbs-Down (Q3)

Identifies which specific handbook knowledge topics receive the highest volume of negative feedback (`rating = -1`), joining the `feedback` table with `interaction`.

#### SQL Query
```sql
SELECT
    i.topic,
    COUNT(*) AS thumbs_down_count
FROM feedback f
JOIN interaction i ON f.request_id = i.request_id
WHERE f.rating = -1
  AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_down_count DESC, i.topic ASC;
```

#### Results on Seeded `assistant.db`
| Topic Code | Handbook Section Title | Negative Ratings (`-1`) | Notes |
| :---: | :--- | :---: | :--- |
| `H26-4.2` | Retaking a course | **8** | Equal top negative; retake credit charging confusion. |
| `H26-5.3` | Thesis registration | **8** | Equal top negative; 120 credit / 2.0 GPA threshold questions. |
| `H26-7.2` | Exam absence | **2** | High percentage thumbs-down (66.7% of its feedback). |

*Note on NULL Topics:* Interactions with `topic IS NULL` (such as `unknown` intent, `greeting`, `fee`, and `office`) account for 17 thumbs-down ratings (primarily `unknown` which has 100% negative feedback). The query intentionally filters for `i.topic IS NOT NULL` to isolate actionable student handbook knowledge gaps.

#### Operational Insight
- `H26-4.2` (Retaking a course) and `H26-5.3` (Thesis registration) should be reviewed first by the curriculum team to improve answer clarity and reduce ambiguous responses.

---

## 3. How to Run & Verify

Run all queries directly against `assistant.db` via Python CLI:
```bash
python3 -c "import sqlite3; con = sqlite3.connect('assistant.db'); print(con.execute('SELECT intent, COUNT(*) FROM interaction GROUP BY intent ORDER BY COUNT(*) DESC').fetchall())"
```

Or execute the complete SQL script via SQLite CLI:
```bash
sqlite3 -header -column assistant.db < sql/my_queries.sql
```

---

## 4. Quality & Regression Checklist

- [x] Query syntax verified on SQLite 3.3x+ without errors.
- [x] Markers `-- Q1`, `-- Q2`, `-- Q3` preserved intact in `sql/my_queries.sql`.
- [x] H2 query by Dang Xuan Phat preserved intact below Q3.
- [x] Root regression tests pass (`pytest -q`: `222 passed, 4 skipped`).
- [x] Code style and formatting clean (`ruff check .` clean).
