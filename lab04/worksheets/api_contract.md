# Lab 4 — API contract worksheet

Fill in one row per endpoint **before** you code it.

| Method | Path | Request body / params | Success (code + body) | Errors (code + error.code) | Who calls it |
|---|---|---|---|---|---|
| GET | /health | — | 200 {status, version} | — | ops, UI |
| POST | /v1/chat | | | | UI, tests |
| POST | /v1/feedback | `{"request_id": str (1–64), "rating": int (-1, 0, 1), "comment"?: str (≤500)}` | 201 `{"id": int, "request_id": str, "rating": int, "comment": str\|null, "created_at": datetime}` | 422 `{"error": {"code": "invalid_request", "message": "..."}}` | UI |
| GET | /v1/feedback | header X-API-Key | | | staff dashboard |
| GET | /v1/weather | — | | | UI |

Questions:
1. Which fields are required, and what are their limits?
   - `request_id` (str, required): min 1, max 64 characters. Identifies the specific assistant interaction.
   - `rating` (int, required): integer constrained between -1 and 1 (`-1` = thumbs down, `0` = neutral, `1` = thumbs up).
   - `comment` (str, optional): maximum 500 characters, defaults to `None`.
2. What does the UI show for each error code?
   - `422 Unprocessable Entity` (`invalid_request`): Display an inline user validation message (e.g., "Please select a valid rating" or "Comment cannot exceed 500 characters").
   - `500 Internal Server Error`: Display "An unexpected error occurred while saving feedback. Please try again later."
3. What changes would force a `/v2`?
   - Changing the rating format (e.g., changing from `[-1, 0, 1]` to a 1–5 star rating scale).
   - Making optional fields mandatory (e.g., requiring mandatory feedback comments or categories).
   - Renaming or removing existing response attributes (`id`, `request_id`, `created_at`).
   - Altering the standard error envelope structure `{"error": {"code": "...", "message": "..."}}`.
