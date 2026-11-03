# Lab 4 — Reflection Note (H2)

**Author:** Đặng Xuân Phát (MSSV: 25125062)  
**Role:** Member 6 — H1 & H2 (Offices API & Reflection)  
**Team:** 07 (`khanhf-ng820/assistant_core_lab`)

---

### Reflection Prompt
> *In your own words: what is the difference between calling `service.handle()` in Lab 3 and calling `POST /v1/chat` today? Why might a team prefer the HTTP version?*

### 5-Line Reflection

1. **Execution Boundary & Runtime Decoupling:** In Lab 3, `service.handle()` was an in-process Python call binding the caller and service to the same memory space, OS process, and Python virtual environment; `POST /v1/chat` decouples them over standard HTTP/JSON across any network boundary.
2. **Language & Platform Agnosticism:** The HTTP interface enables clients written in any language or platform (React, mobile SDKs, curl) to consume assistant capabilities without importing Python modules or maintaining Python runtime dependencies.
3. **Independent Lifecycle & Scalability:** An HTTP API server can be deployed, containerized, and scaled horizontally behind a load balancer independently from downstream consumers, avoiding caller redeployment during backend updates.
4. **Boundary Gateway for Cross-Cutting Concerns:** The HTTP boundary allows applying gateway policies before business logic executes; specifically, this app enables declarative Pydantic 422 request validation, endpoint-level `require_admin` API key enforcement on feedback, and 429 rate limiting on chat, while framework middleware (e.g., CORS) can be attached centrally as requirements grow.
5. **Contract Governance & Testability:** Exposing an HTTP service produces a standardized OpenAPI schema and interactive Swagger UI (`/docs`), giving multi-developer teams an explicit, versioned, and automatable test contract rather than implicit in-memory method contracts.
