# 🚖 Ride Demand Forecasting — Urban Mobility Capstone

## Task 3: Probability Distribution of Ride Requests

This notebook analyzes the probability distributions of key ride request variables as part of the Urban Ride Demand Forecasting capstone project. The goal is to identify the statistical distributions that best describe demand patterns, forming the foundation for the forecasting model.

---

## 📁 Files

```
├── probability_distribution.ipynb          # Main analysis notebook
├── rideBookings_preprocessed1.xlsx         # Preprocessed dataset (1,48,767 bookings)
├── probability_distribution_insights.docx  # Written summary of findings
├── requirements.txt                        # Python dependencies
└── README.md
```

---

## 📊 What's Analyzed

| Variable | Best-fit Distribution | Key Parameters |
|---|---|---|
| Hourly ride counts | Poisson (overdispersed) | λ = 17.07, Dispersion Index = 6.11 |
| Booking value (fare) | Log-Normal | μ = ₹492, σ = ₹332, Skew = 0.94, KS = 0.046 |
| Ride distance | Uniform | a = 2 km, b = 50 km, KS = 0.0024, Bin CV = 0.014 |
| Booking outcome | Multinomial | P(Completed) = 62.01%, Chi-sq p = 0.26 |

---

## 🔍 Key Findings

- **Hourly demand is Poisson but overdispersed** (Dispersion Index = 6.11). The arrival rate spikes at 8h and 17–20h, making time-segmented forecasting essential.
- **Booking value follows Log-Normal** (KS = 0.046 vs 0.108 for Normal). Mean fare ₹492 exceeds median ₹414 due to a premium-ride tail. Fare modelling should work on the log scale.
- **Ride distance is Uniform across [2, 50] km** — every trip length is equally probable (KS = 0.0024, Bin CV = 0.014). Corroborated by EDA: Distance vs Booking Value R² = 0.001, so distance carries no predictive signal for demand.
- **Booking outcomes are Multinomial** with stable probabilities across all 7 vehicle types (Chi-Square p = 0.26). A single ~62% completion rate applies fleet-wide. Driver cancellations (18%) are the main lever to improve service rate.

---

## ⚙️ Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ride-demand-forecasting.git
cd ride-demand-forecasting
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the notebook
```bash
jupyter notebook probability_distribution.ipynb
```

> Make sure `rideBookings_preprocessed1.xlsx` is in the same directory as the notebook before running.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| pandas | 3.0.2 | Data loading and manipulation |
| numpy | 2.4.4 | Numerical computation |
| scipy | 1.17.1 | Distribution fitting, KS tests, Chi-Square |
| matplotlib | 3.10.8 | Plotting |
| seaborn | 0.13.2 | Statistical visualizations |
| openpyxl | 3.1.5 | Reading .xlsx files |
| jupyter / notebook | 1.1.1 / 7.4.2 | Running the notebook |

---

## 📖 Notebook Sections

1. **Hourly Demand — Poisson Distribution**
   Bar chart by hour with peak highlights (8h, 17–20h), Poisson PMF overlay, dispersion index analysis.

2. **Booking Value — Log-Normal Distribution**
   PDF fit comparison (Log-Normal vs Normal), Q-Q plot of log(fare), ECDF with percentile markers.

3. **Ride Distance — Uniform Distribution**
   PDF comparison across four distributions, bin-count flatness chart, ECDF vs Uniform CDF.

4. **Booking Outcome — Multinomial Distribution**
   Donut chart, probability bar chart, completion rate by vehicle type, Chi-Square independence test.

---

## 🗂️ Dataset

- **File:** `rideBookings_preprocessed1.xlsx`
- **Records:** 1,48,767 ride bookings
- **Period:** 2024
- **Vehicle types:** Auto, Bike, eBike, Go Mini, Go Sedan, Premier Sedan, Uber XL
- **Booking statuses:** Completed, Cancelled by Driver, Cancelled by Customer, No Driver Found, Incomplete
- **Key columns:** `Datetime`, `Booking Status`, `Vehicle Type`, `Booking Value`, `Ride Distance`, `Hour`, `DayOfWeek`, `IsWeekend`

---

## 👤 Author

**Rashika Joshi**
Capstone Project — Ride Demand Forecasting (Urban Mobility)

---

## 📚 References

- Scipy Stats — Distribution fitting, KS test, Chi-Square:
  https://docs.scipy.org/doc/scipy/reference/stats.html

- Poisson Distribution (Wikipedia):
  https://en.wikipedia.org/wiki/Poisson_distribution

- Log-Normal Distribution (Wikipedia):
  https://en.wikipedia.org/wiki/Log-normal_distribution

- Uniform Distribution (Wikipedia):
  https://en.wikipedia.org/wiki/Continuous_uniform_distribution

- Multinomial Distribution (Wikipedia):
  https://en.wikipedia.org/wiki/Multinomial_distribution

- Kolmogorov–Smirnov Test (Wikipedia):
  https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test

- Pandas Documentation:
  https://pandas.pydata.org/docs/

- Matplotlib Documentation:
  https://matplotlib.org/stable/index.html

- Seaborn Documentation:
  https://seaborn.pydata.org/
