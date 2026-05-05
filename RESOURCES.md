# Resources

Curated learning resources for this project. Don't try to read all of these
before starting - skim, build, look things up as you hit them.

## PostgreSQL

- **postgresqltutorial.com** - the de facto best free tutorial site. Skim the
  basics (you know SQL from the IBM cert) and focus on Postgres-specific bits:
  data types, JSON support, window functions, `RETURNING` clauses.
- **pgexercises.com** - free interactive SQL exercises against a sample database.
  Great for muscle memory.
- **PostgreSQL official docs** (postgresql.org/docs) - reference material, not
  a tutorial. Bookmark, don't read front-to-back.

## Python + Postgres

- **psycopg documentation** (psycopg.org/psycopg3/docs/) - official docs for the
  Python Postgres driver. Read the "basic module usage" page first.
- **SQLAlchemy** (sqlalchemy.org) - higher-level ORM/toolkit. Optional. Worth
  learning eventually if you keep building with databases.
- **python-dotenv** - tiny library for loading secrets from a `.env` file.

## OpenSky Network API

- **opensky-network.org/apidoc/** - the official API documentation
- Look up: `/states/all` endpoint, rate limits, anonymous vs registered access,
  the meaning of each field in a state vector

## Looker Studio

- **support.google.com/looker-studio** - official help center
- Search specifically for: "PostgreSQL connector", "calculated fields",
  "date range control", "publish a report"

## Database hosting (free tiers, for milestone 8)

- **Supabase** (supabase.com) - generous free Postgres + nice web UI. Probably the easiest.
- **Neon** (neon.tech) - serverless Postgres, free tier
- **Railway** / **Render** - both have free Postgres options with limits

## Scheduling (for milestone 6, only if you go beyond manual)

- `man cron` and `man launchd` in your terminal - actual man pages
- crontab.guru - pastes a cron expression and tells you in plain English when it runs

## SQL practice (general)

- **DataLemur** (datalemur.com) - SQL interview-style questions, free tier
- **HackerRank SQL track** - more practice problems
- **Mode Analytics SQL Tutorial** (mode.com/sql-tutorial) - free, well-written

## Dashboard design

- **storytellingwithdata.com** - blog and book, gold standard for thinking
  about how to present data well
- Look at examples on Tableau Public's gallery and Looker Studio's gallery
  to see what good dashboards look like

## Git / GitHub (for milestone 9)

- **The Git Book** (git-scm.com/book) - free, official, comprehensive
- For just enough to publish a project: learn `git init`, `git add`, `git commit`,
  `git push`, `.gitignore`, and how to create a GitHub repo from the website
