# IntelliCart — AI E-Commerce & Customer Intelligence

Ready-to-run Flask e-commerce project for a college DBMS/AI demo.

## Features
- 500 seeded products in SQLite
- Product search, category filter and sorting
- Login/register
- Cart and checkout/order flow
- Product recommendations
- Customer segmentation field
- Admin analytics dashboard
- JSON analytics API
- Responsive UI
- Gunicorn deployment configuration

## Run
```bash
pip install -r requirements.txt
python app.py
```

Production:
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```
