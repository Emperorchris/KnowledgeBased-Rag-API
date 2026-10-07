# CHRIS AJULUCHUKWU OKEKE
**PHP / Laravel Engineer | Backend & SaaS Architect**

Lagos, Nigeria (UTC+1 — overlaps EU and US East) | Open to remote
emperorchris36@gmail.com | +234 703 948 7884 | linkedin.com/in/chris-okeke | github.com/Emperorchris

---

## SUMMARY

PHP and Laravel engineer with 4+ years shipping production SaaS, EdTech and B2B systems. Rebuilt the university portal at Qverse serving 50,000+ students across 5 institutions, cutting p95 response time from ~4.2s to ~380ms. Currently one of two backend engineers on a B2B car-rental CRM deployed as an isolated instance per client for 20+ rental companies, the largest carrying 100,000+ registered users — where I also built the LLM document-extraction pipeline behind vehicle inspection intake. Depth in multi-tenant architecture, query and cache optimisation, queue-based decoupling, and payment integrations that hold under real production load.

---

## TECHNICAL SKILLS

- **Core Backend:** PHP 8.x, Laravel 10/11, REST API design and versioning, MVC, queue-driven architecture, CodeIgniter
- **Laravel Ecosystem:** Eloquent ORM, Sanctum, Queues and Jobs, Horizon, Task Scheduler, Events and Listeners, Pest and PHPUnit (TDD), Livewire, Inertia.js, Blade, Composer
- **System Design:** Multi-tenant architecture (instance-per-tenant and scoped single-database), database query optimisation and indexing, Redis caching strategies, idempotent webhook handling, RBAC and access-control design, API rate limiting
- **Frontend & Full-Stack:** Vue.js, TypeScript, Next.js, Tailwind CSS, Alpine.js
- **Data & DevOps:** MySQL, PostgreSQL, Redis (caching and queues), Docker, AWS, DigitalOcean, CI/CD with GitHub Actions, Git, Jira, Asana
- **Quality & Observability:** Laravel Telescope, Horizon dashboards, PHPStan / Larastan, Laravel Pint

---

## PROFESSIONAL EXPERIENCE

### Fullstack PHP Developer — CarCheck, Jerusalem, Israel (Remote)
**Sep 2025 – Present**

B2B car-rental CRM vendor deploying a separate instance per client company, used by 20+ rental companies including one with 100,000+ registered users.

- Built the AI document-extraction pipeline behind vehicle inspection intake using Google Gemini, parsing driver's licences and inspection reports at 2,500+ per month with 94% field-level accuracy and human review routing on low-confidence fields, removing 3 minutes of manual entry per inspection
- Cut rental agreement page load time from ~3.1s to ~420ms by eliminating N+1 queries in Eloquent, adding composite indexes on `rentals`, `vehicles` and `customers`, and caching read paths in Redis
- Own production incidents end to end across 20+ tenant instances — helpdesk ticket, log and server investigation with server logs, fix, deploy — sustaining 99.9% uptime through bi-weekly rollouts
- Redesigned the vehicle inspection intake flow, lifting inspection completion rate from 68% to 91% as measured by submitted vs. started inspections over a 30-day window

### Backend Engineer, NestJS (Contract) — Sonichoice Logistics (Remote)
**Jun 2026 – Jul 2026** | inventory.sonichoicelogistics.com

Node/NestJS inventory platform holding 5,000+ products and tracking stock movement across branches.

- Delivered real-time stock visibility and low-stock alerting across branches, with scheduled PDF and Excel reporting behind a live analytics dashboard
- Enforced four permission tiers with custom RBAC guards and JWT auth with refresh-token rotation

### Backend Engineer, Laravel — Qverse (Remote)
**May 2025 – Jun 2026**

Education software vendor running student portals for Nigerian universities, live across 5+ institutions with fee collection built in. One of two backend engineers on a four-person team.

- Cut response times on a portal serving 50,000+ registered students (peaking at 3,000+ concurrent during registration windows) from ~4.2s to ~380ms, by rewriting hot Eloquent queries and putting Redis in front of the read paths
- Integrated Paystack, Flutterwave and Interswitch for 3 universities with idempotent webhook handling and automated reconciliation, settling 15,000+ transactions per semester at 99% success rate
- Designed granular RBAC on Laravel Sanctum, scoping students, lecturers and administrators to their own records
- Mentored two junior developers on Laravel practice, code review standards and TDD

### Backend Engineer — AfrikDish Inc., Toronto, Canada (Remote)
**Oct 2024 – Oct 2025**

Food-tech marketplace connecting African and Caribbean restaurants and grocers with customers across Canada, each vendor running on its own isolated tenant.

- Cut vendor onboarding from ~45 minutes to under 10 minutes with a stancl/tenancy multi-tenant architecture enforcing strict data isolation
- Scaled Stripe integration for global transactions to 98% payment success, including webhook retries with exponential back-off, automated vendor payout splits and multi-currency handling (CAD/USD)
- Led TDD adoption with Pest, taking test coverage from 12% to 74% and cutting production error volume by 60% within three months

### Software Developer (Contract) — Selfany Ltd. (Remote)
**Mar 2024 – Jul 2024**

- Moved email notifications and media processing onto Laravel Queues, cutting server load 70% and page-load time from ~2.6s to ~450ms
- Built a digital marketplace with multi-format content delivery and custom affiliate tracking, lifting referral sales 40%

### Software Developer — 3rd Inventories (On-site)
**Aug 2023 – Dec 2023**

- Built inventory management features on Laravel and Vue.js, with REST APIs for stock tracking, order processing and reporting, delivered in agile sprints

### Software Development Intern — Digital Dreams Tech Hub (On-site)
**Jan 2023 – Jun 2023**

---

## SELECTED PROJECTS

### ESUT Open Distance Learning (ESUT ODL) LMS
PHP, Laravel, Laravel Sanctum, MySQL 

Virtual learning platform for distance-learning students and faculty.

- Supported 200+ registered users, with automated Laravel jobs cutting grade-processing time from ~25 minutes to under 3 minutes
- Secured student and faculty resources across distinct permission tiers with RBAC on Laravel Sanctum


---

## EDUCATION & RECOGNITION

**B.Sc. Computer Science, Enugu State University of Science and Technology (ESUT)** — Nov 2022 – Aug 2026, Second Class Upper (2:1)

**Diploma in Fullstack Development (Distinction), Digital Dreams ICT** — Feb 2022 – Jun 2023
Best Graduating Student and elected student president of the cohort

**Best Tech Personnel of the Year**, Nigeria Association of Computing Students (NACOS), 2024