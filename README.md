# AI-Powered Portfolio Intelligence System

An AI-powered portfolio management system that uses multi-agent architecture to analyze stocks, assess risk, and provide investment recommendations.

## Features

- **Portfolio Overview** - Track holdings, asset allocation, and performance with interactive charts
- **AI Assistant** - Chat with an AI financial advisor powered by Llama 3.3
- **Stock Research** - Analyze individual stocks with price history and key metrics
- **Stock Comparison** - Compare multiple stocks side-by-side with category winners
- **Sentiment Analysis** - Analyze news sentiment for your holdings
- **Technical Analysis** - RSI, MACD, moving averages, and support/resistance levels
- **Tax Optimization** - Identify tax-loss harvesting opportunities
- **Price Alerts** - Set and monitor price alerts for target stocks
- **Reports** - Generate comprehensive portfolio reports

## Architecture

```
portfolio_agent/
├── agents/           # AI agents for different analysis tasks
│   ├── portfolio_agents.py   # Core agents (Planner, Market, News, Risk, Synthesizer)
│   └── extra_agents.py       # Additional agents (Sentiment, Technical, Tax, Alert, Compare)
├── tools/            # Data fetching and calculation tools
│   └── stock_tools.py        # StockDataTool, NewsTool, CalculatorTool, PortfolioManager
├── api/              # FastAPI backend
│   └── main.py               # REST API endpoints
├── app/              # Streamlit alternative UI
│   └── streamlit_app.py      # Single-page Streamlit application
├── frontend/         # Next.js frontend
│   └── src/                  # React components and pages
└── data/             # Portfolio and alerts data storage
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq (Llama 3.3 70B) |
| Backend API | FastAPI |
| Frontend | Next.js 14, React, TypeScript |
| Alternative UI | Streamlit |
| Stock Data | yfinance |
| Charts | Plotly, Recharts |
| Styling | Tailwind CSS |

## Prerequisites

- Python 3.10+
- Node.js 18+
- Groq API key

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd portfolio_agent
```

### 2. Set up Python environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Application

### Option 1: Full Stack (Recommended)

Start both the API and frontend:

```bash
chmod +x start.sh
./start.sh
```

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Streamlit Only

```bash
make run
```

Or:

```bash
streamlit run app/streamlit_app.py
```

### Option 3: API Only

```bash
python api/main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/portfolio` | Get portfolio summary |
| POST | `/api/portfolio/holdings` | Add a holding |
| DELETE | `/api/portfolio/holdings/{symbol}` | Remove a holding |
| GET | `/api/stock/{symbol}` | Get stock info |
| GET | `/api/stock/{symbol}/history` | Get stock history |
| POST | `/api/compare` | Compare multiple stocks |
| GET | `/api/sentiment/{symbol}` | Analyze sentiment |
| GET | `/api/technical/{symbol}` | Get technical analysis |
| POST | `/api/tax/analyze` | Analyze tax opportunities |
| GET | `/api/alerts` | Get all alerts |
| POST | `/api/alerts` | Add a price alert |
| DELETE | `/api/alerts/{alert_id}` | Remove an alert |
| POST | `/api/alerts/check` | Check triggered alerts |
| POST | `/api/ai/analyze` | Chat with AI assistant |

## AI Agents

The system uses a multi-agent architecture:

| Agent | Purpose |
|-------|---------|
| **Planner** | Analyzes user queries and creates analysis plans |
| **Market Analyst** | Fetches and analyzes market data using yfinance |
| **News Analyst** | Analyzes financial news sentiment |
| **Risk Analyst** | Assesses portfolio risk and diversification |
| **Synthesizer** | Combines all analysis into actionable recommendations |
| **Sentiment** | Deep sentiment analysis for individual stocks |
| **Technical** | RSI, MACD, moving averages analysis |
| **Tax** | Tax-loss harvesting opportunity detection |
| **Alert** | Price alert monitoring |
| **Compare** | Multi-stock comparison with category winners |

## Make Commands

```bash
make setup    # Install Python dependencies
make run      # Start Streamlit app
make clean    # Clean generated files
```

## License

MIT
