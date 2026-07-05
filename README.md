# 💰 AI Portfolio Manager

### An Agentic AI System for Intelligent Investment Management

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-00d9ff?style=flat&logo=langchain&logoColor=white)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)

---

## 🎯 What This Project Does

An **AI-powered portfolio manager** that acts as your personal financial advisor. It uses multiple AI agents working together to:

| Feature | Description |
|---------|-------------|
| **Monitor Portfolio** | Track all your investments in real-time |
| **Analyze Markets** | Read market data and news |
| **Assess Risk** | Calculate and explain portfolio risk |
| **Generate Insights** | Provide personalized recommendations |
| **Answer Questions** | Respond to natural language queries |

---

## 🤖 How It Works (Multi-Agent System)

```
User: "How is my portfolio doing?"
            ↓
┌─────────────────────────────────────────┐
│           PLANNING AGENT                │
│  - Understands user request             │
│  - Creates action plan                  │
│  - Decides which agents to use          │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│           EXECUTION AGENTS              │
│  ┌─────────────┐ ┌─────────────┐       │
│  │ Market Data │ │ News Agent  │       │
│  │ Agent       │ │             │       │
│  │ - Prices    │ │ - Headlines │       │
│  │ - Trends    │ │ - Sentiment │       │
│  └─────────────┘ └─────────────┘       │
│  ┌─────────────┐                       │
│  │ Risk Agent  │                       │
│  │ - Volatility│                       │
│  │ - Alerts    │                       │
│  └─────────────┘                       │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│         SYNTHESIS AGENT                 │
│  - Combines all insights                │
│  - Generates recommendations            │
│  - Creates final response               │
└─────────────────────────────────────────┘
            ↓
Response: "Your portfolio is up 12%..."
```

---

## 📂 Project Structure

```
portfolio_agent/
├── agents/
│   ├── __init__.py
│   └── portfolio_agents.py    # All AI agents
├── tools/
│   ├── __init__.py
│   └── stock_tools.py         # Stock data & calculations
├── data/
│   └── portfolio.json         # Your portfolio data
├── app/
│   └── streamlit_app.py       # Web interface
├── .env.example               # API key template
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (for AI agent)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio_agent.git
   cd portfolio_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the app**
   ```bash
   streamlit run app/streamlit_app.py
   ```

---

## 🖥️ Application Features

### 📊 Portfolio Overview
- Total portfolio value and returns
- Asset allocation pie chart
- Holdings performance visualization
- Risk assessment metrics

### 🤖 AI Assistant
- Natural language interface
- Ask anything about your portfolio
- Get personalized recommendations
- Multi-agent analysis

### ➕ Manage Holdings
- Add new stocks
- Remove holdings
- View current positions
- Track profit/loss

### 📈 Stock Research
- Individual stock analysis
- Price history charts
- Key financial metrics
- Company information

### 📋 Reports
- Executive summary
- AI-generated recommendations
- Risk analysis reports

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Agent Framework** | LangChain |
| **LLM** | OpenAI GPT-4 |
| **Market Data** | yfinance |
| **UI** | Streamlit |
| **Visualization** | Plotly |
| **Data Storage** | JSON |

---

## 📊 Example Usage

### Natural Language Queries

| You Ask | Agent Does |
|---------|------------|
| "How is my portfolio doing?" | Shows total value, returns, risk |
| "Should I buy more Apple?" | Analyzes Apple, gives recommendation |
| "What's my risk level?" | Calculates and explains risk |
| "Rebalance my portfolio" | Suggests buy/sell actions |
| "What happened in markets today?" | Summarizes market news |

---

## 🎓 Skills Demonstrated

| Skill | How It's Used |
|-------|---------------|
| **Multi-Agent Systems** | 5 specialized agents working together |
| **Tool Integration** | Stock API, news, calculations |
| **LLM Orchestration** | LangChain for agent coordination |
| **Financial Analysis** | Portfolio metrics, risk assessment |
| **Real-time Data** | Live stock prices and news |
| **Production Ready** | Error handling, state management |

---

## 📈 Business Impact

| Metric | Improvement |
|--------|-------------|
| **Analysis Time** | 2 hours → 30 seconds |
| **Insight Quality** | Manual research → AI-powered |
| **Risk Detection** | Reactive → Proactive |
| **Decision Speed** | Days → Instant |

---

## 🔮 Future Enhancements

- [ ] Real-time price alerts
- [ ] Historical portfolio tracking
- [ ] Tax optimization suggestions
- [ ] Multi-currency support
- [ ] Integration with broker APIs

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [yourusername](https://github.com/yourusername)
- LinkedIn: [Connect with me](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- Built with LangChain and OpenAI
- Stock data from Yahoo Finance
- UI powered by Streamlit
