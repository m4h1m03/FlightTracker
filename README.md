# Flight Tracker

A personal data project to practice the full data analyst pipeline end-to-end: ingest live data from a public API, store it in a relational database, transform it with SQL, and visualise it on a dashboard. Flight data was chosen as there are a vast number of insights that can be drawn from it.

**[View the live dashboard →](https://datastudio.google.com/reporting/cfddb713-c4b2-48b8-b097-c5efb68bf7d1)**

---

## Why I Built It

Mainly to understand what to expect in an ETL pipeline and what goes into building one from the backend up. I also wanted to practice analysing real data and driving meaningful insights from it through visualisation tools.

---

## How It Works

### Stack

- **Language:** Python
- **Database:** PostgreSQL (Supabase)
- **Data source:** OpenSky Network API (free, real-time flight positions)
- **Dashboard:** Looker Studio (free, browser-based, free PostgreSQL connection)
- **Keepalive:** GitHub Actions scheduled workflow (daily) that queries the database so the Supabase Free project does not pause

A Python script fetches live flight data by calling the OpenSky Network API. The data is stored in a cloud-hosted PostgreSQL database (Supabase), where it is joined across three tables using SQL. Looker Studio connects directly to Supabase via a PostgreSQL connector to power the dashboard.

---

## Key Decisions

**1. Setting up a virtual environment**
A virtual environment was created to isolate the project's packages and dependencies, ensuring they remained separate from other Python projects on the machine and that the environment could be reproduced cleanly if needed.

**2. Protecting sensitive credentials**
A `.env` file was used to store sensitive details such as database credentials, keeping them out of the codebase and ensuring they would not be exposed if the project was shared publicly.

**3. Structuring the SQL schema**
Considerable thought went into how to structure the database — how many tables to create, how to categorise the data across them, and how to define primary keys, composite keys, and foreign key relationships to maintain data integrity.

**4. Automating the script**
The script needed to run automatically at regular intervals without manual intervention. `cron` was initially explored but proved unreliable due to macOS sleep behaviour. `launchd` was used instead as the more appropriate macOS-native solution.

**5. Choosing a visualisation tool**
Looker Studio was chosen based on its ability to handle the volume of data without straining local computational resources, its browser-based interface, and the availability of a free PostgreSQL connector that allows it to query Supabase directly.

**6. Keeping the free database awake**
Supabase's Free plan pauses a project after about a week of low activity, and mine kept pausing, which broke the dashboard. I considered upgrading to a paid plan, making the dashboard independent of Supabase, and keeping the database active with a small daily query. I tried the second option first, copying the data into a Looker Studio extract, but the charts' calculated metrics depend on Looker's internal Record Count fields for each data source, so switching the source broke them and I could not match the original dashboard. I reverted that and went with a scheduled GitHub Actions workflow that runs a short Python script (`src/keepalive.py`) once a day. Because the repository is public, the database credentials are stored as repository secrets rather than in the code. This is separate from the ETL script, which still runs on my Mac via `launchd`.

---

## What I Learned

**1. The value of APIs**
APIs open up access to real-world, live data that would otherwise be impossible to collect manually. Working with the OpenSky Network API highlighted how powerful they are as a data collection tool and how central they are to modern data pipelines.

**2. The importance of .env and virtual environments**
Both are essential housekeeping for any serious project. A virtual environment keeps dependencies isolated and reproducible, while a `.env` file ensures sensitive credentials never end up in the codebase — habits that matter especially when sharing work publicly.

**3. Designing a database schema**
Building the schema from scratch — deciding on tables, data types, primary keys, composite keys, and foreign key relationships — gave me a much deeper appreciation of how relational databases are structured and why those design decisions matter for querying and data integrity downstream.

**4. Scheduling and automation**
Automating a script to run without manual intervention introduced me to `cron` and `launchd`. `cron` is widely known but has limitations on macOS, particularly around system sleep. `launchd` is the more robust native alternative, though it comes with a steeper configuration curve.

**5. The role of visualisation in data storytelling**
A dashboard is not just a collection of charts — every design decision (what to include, what to exclude, how to label things) shapes the story the data tells. Looker Studio reinforced how much thought goes into translating raw data into meaningful, readable insights.

**6. Scheduled jobs need an off-switch**
A scheduled job keeps running until it is properly stopped. Unloading my launchd job was not enough to stop it for good: it appears to have restarted with my Mac and quietly kept collecting data from late July. `launchctl disable` is the persistent way to switch a job off, and a collection job should have an end date built in.

**7. Free-tier limits are real constraints**
Supabase's Free plan caps the database at 500 MB. Going over it slowed the dashboard and put the project at risk of going read-only. Monitoring usage and trimming data deliberately are part of running a pipeline. `TRUNCATE` returns disk space immediately, whereas `DELETE` on its own does not.

**8. Dashboard measures must match the grain of the data**
`flight_count` is a per-snapshot value repeated on every observation row, so summing or averaging it overstates results. It inflated my map weights and my average card (10,458 against the true 10,181); counting records fixed both. Rounding map points to a coarser grid also cut the map from roughly 247,000 points to around 5,500, which made it load far faster.

**9. Scheduled workflows, secrets and CI networking**
GitHub Actions can run a script on a cron schedule (in UTC) or manually through `workflow_dispatch`, which is useful for testing before waiting for the schedule. Repository secrets keep credentials out of a public repo and are passed to the script as environment variables. GitHub's runners only support IPv4, so the job connects through Supabase's session pooler instead of the direct (IPv6-only) connection. I also practised making a script fail loudly with a non-zero exit code and testing that failure path before relying on it.

---

## What I Built

A fully functioning ETL pipeline that can be run manually or scheduled to execute automatically without manual intervention. The pipeline fetches live global flight data from the OpenSky Network API, stores it across a structured three-table PostgreSQL database, and transforms it using SQL joins for analysis.

The project culminates in a fully interactive two-page Looker Studio dashboard. Page 1 provides a global overview of air traffic patterns — including a heatmap of flight density, flight count over time, and average velocity across snapshots. Page 2 focuses on a non-US breakdown, exploring aircraft observations, airborne vs on-ground ratios, altitude comparisons, and the relationship between altitude and velocity across origin countries. The dataset covers 25 snapshots collected on 25 May 2026 between 10:30 and 22:30 BST, totalling 254,525 observations.

The dashboard deliberately shows this single day. After the planned collection finished, the scheduled launchd job stayed set up on my Mac and quietly kept adding snapshots from late July to early October. That grew the database to around 5.3 million rows (1,043 MB) and past Supabase's 500 MB Free plan limit, which left the dashboard slow to load. I disabled the job and trimmed the database back to the original day (now around 70 MB), so the dashboard loads in seconds and every figure on it matches the dataset described above.

---

## Improvements

**1. More data**
25 snapshots collected over a single day is still a limited dataset. Running the pipeline continuously over several days or weeks would produce richer insights and reveal stronger patterns — particularly around time-of-day and day-of-week trends. Doing this properly would need a plan for storage: an end date or retention limit, and either a paid tier or pre-aggregated older data, because the Supabase Free plan's 500 MB limit only holds a couple of hundred snapshots of this size.

**2. Error logging**
Adding more robust logging to the ETL script would make it easier to diagnose failures and monitor the pipeline's health over time.

**3. Data validation**
Adding checks in the Python script to flag or handle unexpected values from the API before they reach the database would improve data quality and reduce the risk of corrupt records downstream.

**4. Guard rails on scheduled collection**
The pipeline should stop itself, for example after a set number of snapshots or an end date, and check the database size before inserting so it cannot silently outgrow its plan.

**5. Timeouts and failure handling**
The ETL script's network and database calls have no timeouts. One stalled run stayed open for almost three days, which stopped launchd from starting any later runs. Adding timeouts and clearer failure handling would prevent this.

**6. Pre-aggregated dashboard data**
Pointing Looker Studio at the full three-table join means every chart re-scans every observation. A pre-aggregated table or materialised view would keep the dashboard fast as the data grows.

**7. Keepalive limits and alerts**
GitHub disables scheduled workflows on a public repository after 60 days without any repository activity, so the keepalive is not completely set-and-forget. It also only covers this one Supabase project. Adding a failure alert, such as an email when a run fails, would show a problem straight away instead of after the project has already paused.
