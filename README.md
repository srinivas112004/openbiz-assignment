# openbiz_full_docker_setup_final

This final scaffold includes:
- Playwright scraper (Step 1 & 2) that writes schema.json and screenshots to /data.
- FastAPI backend that validates and stores submissions to PostgreSQL.
- Next.js frontend (mobile-first) that renders dynamic form, shows progress tracker (Steps 1 & 2),
  and provides a PIN -> City/State offline autofill using a local JSON map.
- Admin view to list submissions.
- Pytest tests for validators.
- Docker Compose to run everything (Postgres, scraper, backend, frontend).
- infra/init.sql preloads sample submissions.

## Quick start
1. Install Docker Desktop and open it.
2. Unzip the provided zip and open the folder in VS Code.
3. Run:
   ```
   docker-compose up --build
   ```
4. Visit:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs
   - Admin: http://localhost:3000/admin

## Notes
- PIN -> City/State uses `infra/pin_map.json` (offline), used by frontend for autofill.
- If the Playwright scraper fails due to site protections, check logs:
  ```
  docker-compose logs -f scraper
  ```
- To run backend tests:
  ```
  docker-compose run backend pytest
  ```
