# College Decision Tool

An interactive, web-based decision matrix application designed to help evaluate and rank colleges based on custom-weighted criteria, detailed qualitative insights, and side-by-side comparisons.

---

## 🚀 Project Overview

The College Decision Tool is built as a single-page web application featuring dynamic layout controls, live score calculations, and contextual data drawers. It loads its dataset dynamically from external CSV files, making it easy to update school evaluations, metrics, and weight configurations without touching application code.

---

## 🗂️ Data Files Structure

The project relies on two core comma-separated values (`.csv`) files:

### 1. `data.csv`

Contains the core institutional data, location information, enrollment numbers, and a series of **Score** and **Details** columns for each evaluated metric.

* **Columns Structure:**
* `School`: The full official name of the university.
* `Short_Name`: A concise abbreviation or identifier used for compact table headers.
* `Location`: City and state of the campus.
* `Enrollment`: Total student population.
* **Metric Columns (e.g., `Cost_Score`, `Cost_Details`, `Biology_Score`, `Biology_Details`, etc.):** Each metric features a grade letter (`A`, `B`, `C`, `D`, `F`) and a detailed text evaluation explaining the reasoning behind the grade.



### 2. `metrics.csv`

Defines the qualitative breakdown and definitions for each evaluation metric shown across the tool.

* **Columns Structure:**
* `Metric / Display Name`: The title of the evaluation category (e.g., Cost, Difficulty, Biology, etc.).
* `Description`: A descriptive text block providing deeper context on what the metric measures, which appears in the metric configuration drawer when clicked.



---

## 🛠️ Key Features & How They Work

* **School Comparison Matrix:** Displays a side-by-side breakdown of all active schools and categories.
* **Axis Flipping:** Easily toggle the matrix layout between *Metrics on Y-Axis* and *Schools on Y-Axis* using the **Flip Axes** button.
* **School Management:** Use the **Manage Schools** dropdown filter in the toolbar to check or uncheck specific schools instantly. Hidden schools are dynamically removed from both the comparison table and the live ranking calculations.


* **Interactive Spotlight & Detailed Drawers:**
* **School Spotlight:** Clicking any school header opens a top drawer detailing its current calculated ranking, score percentage, location, enrollment, and automatically sorted lists of key strengths (A/B grades) and areas of concern (D/F grades).
* **Metric Customization:** Clicking any metric header opens its configuration drawer where you can adjust its importance weight multiplier (*Not Factored, Not Important, Somewhat, Very Important, Dealbreaker*) or reverse the grade scale ($A \leftrightarrow F$).
* **Grade Insights:** Clicking any grade letter inside the table opens a detail drawer showing the specific qualitative analysis for that school and metric.


* **Live Weighted Rankings:** Automatically recomputes overall scores and percentage grades whenever weights, grade reversals, or school visibility filters are updated, featuring smooth transition highlights.
* **School Profile Tab:** Switch to the second tab to view a dedicated campus overview, location stats, and major selection views for any institution.

---

## 💻 Getting Started & Development

1. Ensure `index.html`, `data.csv`, and `metrics.csv` are hosted together in the same local directory or web server root.
2. Because the application fetches external CSV data asynchronously via the JavaScript `fetch` API, running it locally requires a simple local development server (such as VS Code's **Live Server** extension or Python's built-in HTTP server: `python3 -m http.server`) to prevent browser CORS restrictions.
3. Open `http://localhost:8000` (or your local server address) in any modern browser to run the tool.