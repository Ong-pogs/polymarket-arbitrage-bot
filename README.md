# Polymarket Arbitrage Bot with the Predictefy API

A Python arbitrage scanner and historical price-study dashboard from the **How to Build a $500/Day Polymarket Arbitrage Bot** tutorial. Inspect cross-platform YES/NO assessments, costs, fees and available size, then explore Polymarket and Kalshi hourly price data.

Built with the [Predictefy Prediction Market API](https://predictefy.com/en/prediction-market-api?utm_source=github&utm_medium=repo&utm_campaign=polymarket-arbitrage-bot&utm_content=readme-top). Get an [API key](https://predictefy.com/en/build/get-started?utm_source=github&utm_medium=repo&utm_campaign=polymarket-arbitrage-bot&utm_content=setup) and check [plans and pricing](https://predictefy.com/en/pricing?utm_source=github&utm_medium=repo&utm_campaign=polymarket-arbitrage-bot&utm_content=pricing) for the endpoints you need.

**Current capabilities:** scanning and analysis. This project does not sign transactions or submit orders. The $500/day figure is an objective investigated in the video, not demonstrated earnings.

## Quick start

Requires Python 3.10 or newer. No third-party packages are required.

```bash
git clone https://github.com/Ong-pogs/polymarket-arbitrage-bot.git
cd polymarket-arbitrage-bot
python server.py
```

Open **http://127.0.0.1:8862**. The dashboard loads the included dated example and historical data without an API key.

For a fresh scan:

1. Sign in to [Predictefy Build](https://predictefy.com/en/build/get-started?utm_source=github&utm_medium=repo&utm_campaign=polymarket-arbitrage-bot&utm_content=setup) and create your own API key.
2. Copy `.env.example` to `.env` and set `PREDICTEFY_API_KEY` locally. An environment variable works too.
3. Use **Refresh live** in the Scanner tab. This requests an assessment; it does not place an order.

The arbitrage feed and historical replay used in the recording required Pro or above at recording time. Check the current plan features before purchasing.

The key is read by Python and never embedded in the browser. Only `public/` is served; `.env` is outside that directory and ignored by Git. The app binds to your local machine. To use another port, set the `PORT` environment variable before starting it.

## Dashboard views

| View | What it shows |
| --- | --- |
| Scanner | Included dated assessments or a fresh Predictefy response |
| Opportunity | Both legs, walked costs, fees, available size and assessment time |
| History / Replay | Matched hourly Polymarket YES and Kalshi NO closes |
| Capacity | Capital and turnover scenarios for a chosen daily objective |
| Setup | The editable build prompt and local launch command |
| Terminal | Recomputed historical counts from the included dataset |

The fresh request uses `/api/router/fetchArbitrage?contracts=100&executableOnly=true&limit=50`. `executableOnly` is an API assessment filter, not a guarantee that an order will fill at the same price later. Inspect current books, fees, resolution conditions and capital requirements before acting.

## Reproduce the historical study

```bash
python tools/analyze.py
```

The dataset contains **939 matched hourly observations** for Republican control of the US House in 2026, pairing Polymarket YES with Kalshi NO. It spans July 19 through October 28, 2026, with gaps. Timestamps are matched without filling missing hours. The chronological split uses the first 704 rows for development and the final 235 for the later comparison.

| Period | Matched observations | Close-price spread strictly above 1 cent |
| --- | ---: | ---: |
| Earlier | 704 | 368 |
| Later | 235 | 45 |

Prices are trade-derived hourly closes, not synchronized executable asks. The study does not model fills, slippage, fees or realized P&L. Its results do not establish a profitable strategy or $500/day income. The capacity worksheet is a scenario calculator, not a forecast.

`public/study.json` contains the matched public market observations and study metadata. `public/scan.json` contains the dated API example used in the tutorial. Fresh scan results are saved to ignored `public/latest-scan.json`; they are not committed automatically. These snapshots are historical, not current recommendations.

## Build prompt

Use [build-prompt.txt](build-prompt.txt) with your preferred coding assistant. Keep API keys and wallet credentials out of prompts and public files. The prompt specifies research and alerts rather than automatic order submission.

## Predictefy API and SDK resources

- [Prediction Market API](https://predictefy.com/en/prediction-market-api?utm_source=github&utm_medium=repo&utm_campaign=polymarket-arbitrage-bot&utm_content=resources): market data and cross-platform tooling.
- [API quickstart](https://docs.predictefy.com/quickstart/): authentication and first requests.
- [Arbitrage API reference](https://docs.predictefy.com/api/operations/fetcharbitrage/): request and response fields.
- [Historical data guide](https://docs.predictefy.com/guides/history/): data access and limitations.
- [Python SDK](https://docs.predictefy.com/guides/python-sdk/) and [TypeScript SDK](https://docs.predictefy.com/guides/sdk/): alternative integration options. This project uses Python's standard-library HTTP client directly.

## License and attribution

Project code is MIT licensed. Included public-data snapshots remain subject to the relevant providers' terms. Predictefy and Polymarket logos identify their respective services and are not covered by the code license. This is an independent tutorial project, not an official product of either service.

Educational purposes only; not financial advice.
