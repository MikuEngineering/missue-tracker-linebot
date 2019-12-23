# missue-tracker-linebot

## Requirements

- Python 3.6+
- Poetry
- MariaDB

## Usage

1. Install dependencies.
```bash
poetry install
```

2. Set environment variables.
```bash
export FLASK_RUN_PORT=3001
export LINE_BOT_DB_HOSTNAME=localhost
export LINE_BOT_DB_DATABASE=missue_tracker_linebot
export LINE_BOT_DB_USERNAME=miku
export LINE_BOT_DB_PASSWORD=mtpassword
export LINE_CHANNEL_ACCESS_TOKEN=xxxxxx
export LINE_CHANNEL_SECRET=xxxxxx
```

3. Run!
```bash
poetry run flask run
```
