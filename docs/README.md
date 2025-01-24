# MooMoo Investment Assistant Tool (Backend)

## Introduction

The MooMoo Investment Assistant Tool is a backend system designed to assist individual investors with investment decisions and automated trading using the MooMoo Open APIs.

## Features

- **Company Feedback**: Provides Buy/Sell/Hold recommendations based on comprehensive stock analysis.
- **Stock Recommendation**: Recommends stocks based on predefined investment preferences.
- **Today's Sentiment**: Analyzes market sentiment for the day using financial news and market data.
- **Automated Trading**: Executes automated trading strategies based on user-defined goals.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/MooMoo-Investment-Assistant.git
   cd MooMoo-Investment-Assistant
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**

   Update the `src/config/secrets.yaml` file with your MooMoo API keys.

4. **Run the Application**

   ```bash
   python src/main.py
   ```

## Testing

Run the test suite using:

```bash
python -m unittest discover tests
```

## Documentation

Refer to `docs/prd.md` for the detailed Product Requirements Document.

## License

MIT License 