from langgraph.graph import StateGraph, END
from state import MarketMindState
from agents.price_agent import price_agent
from agents.sentiment_agent import sentiment_agent
from agents.onchain_agent import onchain_agent
from agents.macro_agent import macro_agent
from agents.risk_agent import risk_agent
from agents.synthesis_agent import synthesis_agent

def orchestrator(state: MarketMindState) -> dict:
    ticker = state["ticker"].upper().strip()
    crypto_tickers = {
        "BTC","ETH","SOL","BNB","DOGE","ADA",
        "AVAX","DOT","MATIC","LINK","XRP","LTC"
    }
    asset_type = "crypto" if ticker in crypto_tickers else "stock"
    return {"ticker": ticker, "asset_type": asset_type, "agent_signals": []}

def build_graph():
    builder = StateGraph(MarketMindState)

    builder.add_node("orchestrator", orchestrator)
    builder.add_node("price_agent", price_agent)
    builder.add_node("sentiment_agent", sentiment_agent)
    builder.add_node("onchain_agent", onchain_agent)
    builder.add_node("macro_agent", macro_agent)
    builder.add_node("risk_agent", risk_agent)
    builder.add_node("synthesis_agent", synthesis_agent)

    builder.set_entry_point("orchestrator")

    for agent in ["price_agent", "sentiment_agent", "onchain_agent", "macro_agent", "risk_agent"]:
        builder.add_edge("orchestrator", agent)
        builder.add_edge(agent, "synthesis_agent")

    builder.add_edge("synthesis_agent", END)

    return builder.compile()

graph = build_graph()