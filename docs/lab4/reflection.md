# Lab 4 — Reflection Note (H2)

**Author:** Đặng Xuân Phát (MSSV: 25125062)  
**Role:** Member 6 — H1 & H2 (Offices API & Reflection)  
**Team:** 07 (`khanhf-ng820/assistant_core_lab`)

---

### Reflection Prompt
> *In your own words: what is the difference between calling `service.handle()` in Lab 3 and calling `POST /v1/chat` today? Why might a team prefer the HTTP version?*

### 5-Line Reflection

1. **Execution Boundary & Runtime Coupling:** In Lab 3, `service.handle()` is an in-process Python function call requiring the caller and service to share the same memory space, OS process, and Python virtual environment; in contrast, `POST /v1/chat` exposes the service over HTTP/JSON across arbitrary network boundaries.
2. **Language & Platform Agnosticism:** The HTTP endpoint allows any client (React web app, Flutter/iOS/Android mobile clients, CLI, or microservices in Go/Java) to interact with the assistant without importing Python packages or knowing its internal classes.
3. **Independent Lifecycle & Scalability:** A networked backend can be containerized, horizontally auto-scaled behind a load balancer, and deployed independently without rebuilding or redeploying client frontends.
4. **Centralized Infrastructure Concerns:** The HTTP layer acts as a single gateway where authentication (API keys), rate limiting (429), input sanitization/validation (422), CORS, and structured telemetry are enforced uniformly before touching business logic.
5. **Standardized Contract Governance:** By using FastAPI, the team gains an automated, versioned OpenAPI specification and interactive Swagger documentation (`/docs`), creating an explicit, contract-driven interface that prevents tight in-memory coupling between team members.
