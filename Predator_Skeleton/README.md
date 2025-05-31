# File Structure

quote_scraper_project/
├── docker-compose.yml
├── scraper_orchestrator/
│   ├── orchestrator.py
│   ├── scrapers/
│   │   ├── site1_scraper.py
│   │   ├── site2_scraper.py
│   │   └── ...
│   └── requirements.txt
├── consumer_service/
│   ├── consumer.py
│   ├── models.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── requirements.txt
└── .env

# Execution

Build and start services:

```bash
$ docker-compose up --build
```

Access the frontend:

Navigate to http://localhost:5000 to view the scraped quotes.