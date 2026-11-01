# Task T2: Feedback POST Endpoint — Developer Guide & Presentation

**Course:** CSC10014 - Computational Thinking  
**Project:** Smart Virtual Assistant (`assistant_core_lab`)  
**Lab:** Lab 04 — Web Service & API Design  
**Author:** Lý Tuấn Kiệt (MSSV: `25125022`, GitHub: `@kiethm07`)  
**Cross-Reviewer:** Trần Thành Lợi  

---

## 1. Overview & Architectural Role

The `POST /v1/feedback` endpoint fulfills task **T2** of the Lab 4 backend web service. Its primary responsibility is to capture user sentiment and qualitative feedback regarding specific assistant chat interactions.

### Workflow Sequence
```
┌─────────┐                ┌──────────────────┐               ┌────────────────┐
│ Client  │                │  FastAPI Server  │               │ In-Memory DB   │
│ (UI)    │                │ (assistant_api)  │               │(feedback_store)│
└────┬────┘                └────────┬─────────┘               └───────┬────────┘
     │                              │                                 │
     │ 1. POST /v1/feedback         │                                 │
     │    {request_id, rating, ..}  │                                 │
     │─────────────────────────────>│                                 │
     │                              │ 2. Validate payload             │
     │                              │    against FeedbackIn schema    │
     │                              │                                 │
     │                              │ 3. Assign ID and UTC timestamp  │
     │                              │ 4. Append to feedback_store     │
     │                              │────────────────────────────────>│
     │                              │                                 │
     │ 5. HTTP 201 Created          │                                 │
     │    FeedbackOut payload       │                                 │
     │<─────────────────────────────│                                 │
```

1. A client initiates a chat query via `POST /v1/chat` and receives an answer along with a unique `request_id`.
2. The user reacts to the response (thumbs up, neutral, or thumbs down) and optionally leaves a comment.
3. The client submits this data via `POST /v1/feedback`.
4. The backend validates the payload, assigns a sequential `id` and current UTC `created_at` timestamp, and stores the record.
5. In Lab 4, records are kept in an in-memory storage array (`feedback_store`). In Lab 5, this will be transitioned to a persistent database (e.g., SQLite / PostgreSQL).

---

## 2. API Contract & Data Schemas

### Route Details
- **Method:** `POST`
- **Path:** `/v1/feedback`
- **Request Headers:** `Content-Type: application/json`
- **Authentication:** Public (no API key required)

### Request Schema (`FeedbackIn`)
| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| `request_id` | `str` | Yes | 1 to 64 characters | Trace ID of the assistant response being rated |
| `rating` | `int` | Yes | `-1`, `0`, or `1` | `-1` = thumbs down, `0` = neutral, `1` = thumbs up |
| `comment` | `str` | No | Max 500 characters | Optional textual commentary or reason |

### Success Response (`FeedbackOut`)
- **Status Code:** `201 Created`
- **Response Headers:** `Content-Type: application/json`
- **Body Example:**
```json
{
  "request_id": "req-98f24a1b02",
  "rating": 1,
  "comment": "Accurate tuition fee calculation with exact source citations.",
  "id": 1,
  "created_at": "2026-11-01T07:45:00.123456Z"
}
```

### Error Responses
All errors adhere to the project's unified error envelope: `{"error": {"code": "...", "message": "..."}}`.
- **Status Code:** `422 Unprocessable Entity`
  - **Error Code:** `invalid_request`
  - **Causes:** Missing required fields (`request_id` or `rating`), rating out of range (e.g. `rating: 5`), or comment exceeding 500 characters.
  - **Example:**
```json
{
  "error": {
    "code": "invalid_request",
    "message": "body.rating: Input should be less than or equal to 1"
  }
}
```

---

## 3. Implementation Details

Located in `lab04/starter/src/assistant_api/main.py`:

```python
@app.post("/v1/feedback", response_model=FeedbackOut, status_code=201, tags=["feedback"])
def add_feedback(fb: FeedbackIn) -> FeedbackOut:
    # T2: Record user feedback with an auto-incremented ID and current UTC timestamp
    item = FeedbackOut(
        **fb.model_dump(),
        id=len(feedback_store) + 1,
        created_at=datetime.now(timezone.utc),
    )
    feedback_store.append(item)
    return item
```

Key engineering decisions:
- **Pydantic Validation:** Payload validation is automatically enforced by FastAPI using the typed `FeedbackIn` Pydantic model.
- **Auto-increment ID:** `id=len(feedback_store) + 1` guarantees incremental integer identifiers starting from 1.
- **Timezone-aware Timestamps:** Always explicitly use `datetime.now(timezone.utc)` to prevent local machine timezone drift and ensure ISO-8601 compliance.
- **State Exposure:** `app.state.feedback_store = feedback_store` enables direct state inspection and deterministic testing.

---

## 4. User & Developer Guide

### 4.1 Running the API Server Locally
```bash
# Navigate to the starter package directory
cd lab04/starter

# Launch Uvicorn development server with hot-reload enabled
uvicorn assistant_api.main:create_app --factory --reload
```
The server will start at `http://127.0.0.1:8000`.

### 4.2 Interactive Swagger UI Walkthrough
1. Open your browser and navigate to `http://127.0.0.1:8000/docs`.
2. Locate the **feedback** section and expand `POST /v1/feedback`.
3. Click **Try it out**.
4. Paste the following JSON into the **Request body**:
   ```json
   {
     "request_id": "demo-request-001",
     "rating": 1,
     "comment": "Quick and helpful answers!"
   }
   ```
5. Click **Execute** and observe the `201 Created` response.

### 4.3 Manual Testing with `curl`

#### Case 1: Successful Feedback (Thumbs Up with Comment)
```bash
curl -X POST "http://127.0.0.1:8000/v1/feedback" \
     -H "Content-Type: application/json" \
     -d '{"request_id": "req-101", "rating": 1, "comment": "Clear tuition breakdown."}'
```
**Expected Response:** HTTP 201 with `id: 1` and populated `created_at`.

#### Case 2: Minimal Feedback (Thumbs Down, No Comment)
```bash
curl -X POST "http://127.0.0.1:8000/v1/feedback" \
     -H "Content-Type: application/json" \
     -d '{"request_id": "req-102", "rating": -1}'
```
**Expected Response:** HTTP 201 with `comment: null`.

#### Case 3: Validation Failure (Invalid Rating)
```bash
curl -X POST "http://127.0.0.1:8000/v1/feedback" \
     -H "Content-Type: application/json" \
     -d '{"request_id": "req-103", "rating": 5}'
```
**Expected Response:** HTTP 422 with `{"error": {"code": "invalid_request", ...}}`.

---

## 5. Automated Verification

Dedicated unit tests are implemented in `lab04/starter/tests/test_feedback_post.py`.

Run the automated test suite:
```bash
python -m pytest lab04/starter/tests/test_feedback_post.py -v
```

### Verified Test Cases:
- `test_post_feedback_success_minimal`: Checks valid feedback without comment returns HTTP 201 and `id == 1`.
- `test_post_feedback_success_with_comment`: Checks valid feedback with user comments.
- `test_post_feedback_id_auto_increment`: Verifies sequential `id` generation (`1, 2, 3...`) across multiple calls.
- `test_post_feedback_valid_ratings`: Verifies acceptance of all valid ratings (`-1`, `0`, `1`).
- `test_post_feedback_invalid_rating_range`: Verifies HTTP 422 on ratings outside `[-1, 1]` (`-5`, `2`, `5`, etc.).
- `test_post_feedback_missing_required_fields`: Verifies HTTP 422 when `rating` or `request_id` is missing.
- `test_post_feedback_empty_request_id`: Verifies rejection of empty `request_id`.
- `test_post_feedback_request_id_too_long`: Verifies rejection of `request_id` > 64 chars.
- `test_post_feedback_comment_too_long`: Verifies rejection of comment > 500 chars.

---

## 6. Presentation & Demonstration Script

### Slide 1: Introduction & Scope
- **Presenter:** Lý Tuấn Kiệt (MSSV: 25125022)
- **Feature:** T2 — Feedback POST Endpoint (`POST /v1/feedback`)
- **Objective:** Provide a standardized, validated HTTP API for clients to record feedback on AI responses.

### Slide 2: API Contract Design
- Explain the `FeedbackIn` schema: `request_id` (1–64 chars), constrained `rating` (`-1`, `0`, `1`), and optional `comment` (max 500 chars).
- Explain the `FeedbackOut` response: returns HTTP 201 with auto-incremented integer `id` and ISO-8601 UTC timestamp.
- Explain the error contract: standardized `422 invalid_request` envelope.

### Slide 3: Code Implementation & Clean Design
- Walk through the 3-line implementation in `add_feedback()`.
- Emphasize adherence to Clean Code: clear variable naming, timezone-aware UTC handling, and separation of concerns.

### Slide 4: Live Demonstration
- Open Swagger UI (`/docs`).
- Submit valid thumbs-up feedback -> Show HTTP 201 Created.
- Submit invalid payload (`rating: 5`) -> Show HTTP 422 error response.
- Execute Pytest suite in terminal -> Show all 15 automated tests passing.

### Slide 5: Future Integration (Lab 5)
- Explain the migration path: replacing the in-memory array (`feedback_store`) with SQL repository pattern and database transactions.

---

## 7. Cross-Review Checklist (For Trần Thành Lợi)

Please verify the following criteria when reviewing this pull request:

- [ ] **Functionality:** `POST /v1/feedback` returns HTTP 201 Created with valid `id` and UTC `created_at`.
- [ ] **Validation:** Pydantic rejects invalid ratings (e.g. `2`, `-5`), missing IDs, and comments > 500 chars with HTTP 422.
- [ ] **Tests:** All unit tests in `lab04/starter/tests/test_feedback_post.py` pass without errors or warnings.
- [ ] **Lint & Format:** Code strictly passes `ruff check .` with zero errors.
- [ ] **Language & Comments:** All code comments, docstrings, and documentation files are 100% in English.

