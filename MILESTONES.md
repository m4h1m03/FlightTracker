# Project Journal

---

## What the Project Is

A personal data project to practice the full data analyst pipeline end-to-end: ingest live data from a public API, store it in a relational database, transform it with SQL, and visualise it on a dashboard. Flight data was chosen as there are a vast number of insights that can be drawn from it.

---

## Why I Built It

Mainly to understand what to expect in an ETL pipeline and what goes into building one from the backend up. I also wanted to practice analysing real data and driving meaningful insights from it through visualisation tools.

---

## How It Works

### Stack

- **Language:** Python
- **Database:** PostgreSQL (local install via Postgres.app)
- **DB GUI:** DBeaver
- **Data source:** OpenSky Network API (free, real-time flight positions)
- **Dashboard:** Looker Studio (free, browser-based, native Mac, free Postgres connector)

A Python script fetches live flight data by calling the OpenSky Network API. The data is then stored in PostgreSQL, where it is joined across tables using SQL and exported as a CSV. The CSV is imported into Google Sheets, which serves as the data source connection to Looker Studio for visualisation.

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
Looker Studio was chosen based on its ability to handle the volume of data without straining local computational resources, its native browser-based interface, and the availability of a free Google Sheets connector.

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

---

## What I Built

A fully functioning ETL pipeline that can be run manually or scheduled to execute automatically without manual intervention. The pipeline fetches live global flight data from the OpenSky Network API, stores it across a structured three-table PostgreSQL database, and transforms it using SQL joins for analysis.

The project culminates in a fully interactive two-page Looker Studio dashboard. Page 1 provides a global overview of air traffic patterns — including a heatmap of flight density, flight count over time, and average velocity across snapshots. Page 2 focuses on a non-US breakdown, exploring aircraft observations, airborne vs on-ground ratios, altitude comparisons, and the relationship between altitude and velocity across origin countries.

---

## Improvements

**1. Refactoring the ETL script**
The script could be restructured to improve readability and simplicity — breaking it into smaller, more focused functions would make it easier to maintain and debug.

**2. Database connection**
A cloud-hosted PostgreSQL database (such as Supabase or Neon) connected directly to Looker Studio would eliminate the CSV/Google Sheets intermediary step, resulting in faster dashboard rendering and a more streamlined pipeline.

**3. More data**
16 snapshots collected over a single afternoon is a limited dataset. Running the pipeline continuously over several days or weeks would produce richer insights and reveal stronger patterns — particularly around time-of-day and day-of-week trends.

**4. Better scheduling**
Replacing `StartInterval` with `StartCalendarInterval` in the launchd plist would make the scheduling more reliable, particularly after the Mac wakes from sleep.

**5. Error logging**
Adding more robust logging to the ETL script would make it easier to diagnose failures and monitor the pipeline's health over time.

**6. Data validation**
Adding checks in the Python script to flag or handle unexpected values from the API before they reach the database would improve data quality and reduce the risk of corrupt records downstream.
