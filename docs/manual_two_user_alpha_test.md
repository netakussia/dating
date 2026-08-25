# Manual two-user ALPHA E2E test checklist

Purpose: Step-by-step manual end-to-end checklist for verifying basic functionality and resilience of the dating bot with two test users (User A and User B). Follow each step and mark ACTUAL and PASS/FAIL.

Usage: run the checklist while two test Telegram accounts are available. For destructive cleanup between runs use the tools/reset_test_data.py utility (development only).

| STEP | ACTION | EXPECTED | ACTUAL | PASS/FAIL | NOTES |
|------|--------|----------|--------|----------|-------|
| 1 | User A: /start | Bot prompts to create a profile or continue registration | | | |
| 2 | User A: complete registration (name/age/district/institution/interests/bio) | Profile draft created; preview shown | | | |
| 3 | User A: Upload first photo (photo 1) | Photo uploaded and accepted by UI | | | |
| 4 | User A: Upload second photo (photo 2) | Photo uploaded and shown as second | | | |
| 5 | User A: Upload third photo (photo 3) | Photo uploaded and shown as third | | | |
| 6 | User A: Check photo order in profile preview | Photos appear in the expected order (1,2,3) | | | |
| 7 | User A: Publish profile | Profile visible (is_visible=True) and claim success message | | | |
| 8 | Repeat steps 1–7 for User B | User B has published profile | | | |
| 9 | User A: Open "Знакомства" / recommendations | User B appears in recommendation card for User A (unless filtered by eligibility) | | | |
| 10 | User B: Open recommendations | User A appears in recommendation card for User B | | | |
| 11 | Inspect match percentage shown on cards | A numeric compatibility/score is displayed and within 0..100 or documented range | | | |
| 12 | User A: Press LIKE for User B | Like recorded; User B receives in-chat notification of like | | | |
| 13 | User B: Verify like notification | Notification received (inline or direct) | | | |
| 14 | User B: Press LIKE for User A | Like recorded and mutual match created | | | |
| 15 | Check that Match event triggers contact exchange (username or contact message) | Both users see contact / username shown or instructions to contact | | | |
| 16 | Check "Симпатии" (sent likes) lists | Each user's sent likes includes the other | | | |
| 17 | Press old inline like/match buttons again (replay callbacks) | Actions are idempotent: no duplicate likes/matches or errors | | | |
| 18 | Verify no duplicate matches in database / UI | Only single Match record exists | | | |
| 19 | User A: Press DISLIKE on User B | Dislike recorded; User B not notified by default | | | |
| 20 | User A: Block User B | Block recorded; User B cannot see User A in recommendations anymore | | | |
| 21 | User A: Send REPORT against User B | Report recorded and report_count incremented; if threshold reached moderation_case may be created | | | |
| 22 | User A: Send another REPORT against User B (duplicate) | Duplicate report from same reporter is prevented (duplicate report policy) | | | |
| 23 | Verify blocked profile is hidden from recommendations for blocker and blocked | Blocked pair no longer returns in recommendations | | | |
| 24 | User A: Edit profile text/bio | Changes saved and visible in preview | | | |
| 25 | User A: Replace a photo in profile | New photo replaces old one, moderation flow triggered if necessary | | | |
| 26 | User A: Delete a photo | Photo removed from profile and UI updates | | | |
| 27 | Trigger stale photo callbacks (simulate or retry stale) | Old inline/photo moderation callback handlers do not crash; UI remains consistent | | | |
| 28 | Attempt to upload 4th photo (beyond allowed limit) | Upload refused with clear message; no silent acceptance | | | |
| 29 | Force ML to mark photo UNDER_REVIEW (simulate provider error or use test hook) | Profile moderation status becomes UNDER_REVIEW and is_visible=False; moderation_locked=True | | | |
| 30 | Run `python -m tools.reset_test_data --user <id_A>` | The profile and all related rows are removed for that user; Redis cleaned for that user | | | |
| 31 | After reset: try to view the deleted profile via recommendations | Profile not present; handlers return user-friendly message or not found handling | | | |
| 32 | Re-register User A from scratch | New profile can be created with same telegram id and functions as expected | | | |
| 33 | Rapid double-click test: quickly press like/dislike twice | Server handles idempotency and no duplicate DB records/errors | | | |
| 34 | Press stale callback for removed/archived profile | Handlers are resilient and do not raise uncaught exceptions | | | |
| 35 | Final sanity: Open recommendations for both users and perform a short happy-path session | No exceptions, correct counts, no duplicated cards or crashes | | | |


## Infrastructure resilience checks (additional manual steps)

| STEP | ACTION | EXPECTED | ACTUAL | PASS/FAIL | NOTES |
|------|--------|----------|--------|----------|-------|
| R1 | While a user session is active, restart Redis server | Bot remains responsive; in-flight operations either succeed or fail gracefully; recommendation queue recovers | | | |
| R2 | Restart bot process (docker compose restart bot) during active session | Bot reconnects; no stuck transactions; no duplicate matches created | | | |
| R3 | Restart PostgreSQL during active session | Long-running transactions handled; system returns to consistent state after DB comes back | | | |
| R4 | Replay old inline callback data (expired/replayed) | Handlers tolerate stale callback data and do not crash; user sees a helpful message | | | |
| R5 | Rapid double-click (like/skip) | No duplicate entries or unhandled exceptions | | | |
| R6 | Request a non-existent or deleted profile via direct link or callback | Handler responds with not-found message; no stack-trace visible to user | | | |


Notes:
- Keep two separate Telegram client sessions; prefer one mobile and one desktop client to simulate realistic timing.
- Use tools/reset_test_data.py for cleanups between runs (development-only). Do NOT run tool in production.
- If you need to publish Redis locally for GUI debugging, copy docker-compose.override.yml.example -> docker-compose.override.yml (this file is gitignored by default) and run docker compose up -d.


Seeding test data (mass profiles):

- To generate a batch of fake test profiles and warm up recommendation queues run inside the bot container (development only):

  export ENV=development
  docker compose exec -T bot /bin/sh -lc "python -m tools.seed_test_profiles --count 50"

- The tool will create users with IDs starting at 200000 and fill Redis recommendation queues by invoking RecommendationService.rebuild_queue for each created user.
