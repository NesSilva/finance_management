# Finance Management

> Personal finance management system built with **Django**.  
> Track **incomes**, **expenses**, and **categories** per user, with dashboards and monthly summaries.  
> The project will evolve with **AI features** for insights, anomaly detection, forecasts, and budgeting suggestions.

---

## ✨ Features

- User authentication (login/register)
- Income & expense tracking
- Categories per user
- Dashboard with totals (Income / Expense / Balance)
- Monthly filtering (current month/year)

---

## 🧠 AI Roadmap (planned)

The next updates will focus on adding AI-driven features:

- [x] Income/Expense CRUD with categories
- [x] Monthly totals + dashboard
- [ ] **Rule-based savings insights** (alerts & suggestions)
  - expense > income → warning
  - Food > 30% of income → suggestion
  - savings < 10% → improvement tips
- [ ] **Spending forecast** (next month prediction)
  - Time Series: ARIMA / Prophet
- [ ] **Anomaly detection**
  - Z-score / Isolation Forest
  - “This expense is 3× higher than your usual”
- [ ] **Personal finance chat assistant**
  - “Can I spend 150€ this weekend?”
  - Uses user data + OpenAI API for responses
- [ ] **Auto budget planner**
  - category limits, goals, monthly plan

---

## 💻 Requirements

Before starting, ensure you have:

- Python **3.11+**
- Pip + Virtualenv
- Git
- OS: Windows / Linux / macOS

---

## 🚀 Installation

### Linux and macOS

```bash
git clone https://github.com/NesSilva/finance_management.git
cd finance_management
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate


### Windows
git clone https://github.com/NesSilva/finance_management.git
cd finance_management
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate

