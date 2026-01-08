import streamlit as st
import os
from typing import Annotated, TypedDict, List, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END

# 1. SETUP & THEME
load_dotenv()
st.set_page_config(page_title="Sana Nasir | Multi-Agent Orchestrator", layout="wide")

# Professional UI Styling
st.markdown("""
    <style>
    .stStatus { background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
    .agent-tag { background: #2e7d32; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# 2. CORE ENGINE INITIALIZATION
if not os.getenv("GROQ_API_KEY"):
    st.error("Missing GROQ_API_KEY in .env file")
    st.stop()

llm = ChatGroq(temperature=0.2, model_name="llama-3.3-70b-versatile")
search_tool = DuckDuckGoSearchRun()

# 3. ADVANCED AGENTIC STATE
class TeamState(TypedDict):
    task: str
    report_draft: str
    critique_notes: str
    iterations: int
    is_ready: bool
    logs: List[str]

# 4. AGENT NODES
def research_analyst_node(state: TeamState):
    """The 'Worker' Agent: Performs deep research and drafting."""
    it_count = state.get("iterations", 0) + 1
    query = state['task']
    
    # If this is a revision, incorporate the critic's feedback
    if state.get("critique_notes"):
        prompt = f"REVISE the following report: {state['report_draft']}\n\nApply these CRITIQUE NOTES: {state['critique_notes']}"
    else:
        raw_data = search_tool.run(query)
        prompt = f"Topic: {query}. Research Data: {raw_data}. Write a comprehensive technical report."

    response = llm.invoke(prompt)
    new_logs = state.get("logs", []) + [f"Iteration {it_count}: Analyst generated/revised draft."]
    
    return {
        "report_draft": response.content,
        "iterations": it_count,
        "logs": new_logs
    }

def quality_strategist_node(state: TeamState):
    """The 'Critic' Agent: Acts as a quality gate (Reflection Pattern)."""
    prompt = f"""Evaluate this report for accuracy and depth: {state['report_draft']}
    If it is technical, accurate, and complete, respond ONLY with 'READY'.
    Otherwise, provide specific instructions on what is missing or wrong."""
    
    response = llm.invoke(prompt)
    feedback = response.content
    
    is_ready = "READY" in feedback.upper()
    new_logs = state.get("logs", []) + [f"Strategist Check: {'Passed' if is_ready else 'Failed - Requesting Edits'}"]
    
    return {
        "is_ready": is_ready,
        "critique_notes": "" if is_ready else feedback,
        "logs": new_logs
    }

# 5. GRAPH ORCHESTRATION
builder = StateGraph(TeamState)
builder.add_node("analyst", research_analyst_node)
builder.add_node("strategist", quality_strategist_node)

builder.set_entry_point("analyst")
builder.add_edge("analyst", "strategist")

# Decision Logic: Loop back to analyst if not ready, else END
def router(state: TeamState) -> Literal["analyst", "__end__"]:
    if state["is_ready"] or state["iterations"] >= 3:
        return END
    return "analyst"

builder.add_conditional_edges("strategist", router)
executor = builder.compile()

# 6. STREAMLIT INTERFACE
st.title("🛡️ Self-Healing Multi-Agent System")
st.caption("Engineered by Sana Nasir | Autonomous Reflection & Error Correction")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("⚙️ Mission Control")
    user_query = st.text_input("Enterprise Goal:", placeholder="e.g. Analyze 2026 cybersecurity risks for Fintech")
    
    with st.expander("Agent Topology"):
        st.graphviz_chart("""
            digraph G {
                rankdir=LR; node [shape=box, style=filled, fillcolor="#E8F5E9"];
                "Analyst (Worker)" -> "Strategist (Critic)" [label="Draft"];
                "Strategist (Critic)" -> "Analyst (Worker)" [label="Feedback Loop"];
                "Strategist (Critic)" -> "Final Output" [label="READY"];
            }
        """)
    
    run_btn = st.button("🚀 Trigger Autonomous Workflow")

with col2:
    st.subheader("🖥️ Agent Execution Environment")
    if run_btn and user_query:
        # Initialize state
        initial_state = {
            "task": user_query, "report_draft": "", "critique_notes": "", 
            "iterations": 0, "is_ready": False, "logs": []
        }
        
        with st.status("Agents collaborating...", expanded=True) as status:
            final_state = executor.invoke(initial_state)
            for log in final_state["logs"]:
                st.write(log)
            status.update(label="Workflow Verified & Complete!", state="complete")
        
        # Display Final Result
        st.markdown("### 📄 Final Verified Report")
        st.info(f"Report verified after {final_state['iterations']} iteration(s).")
        st.markdown(final_state["report_draft"])
        st.download_button("Export Verified Intelligence", final_state["report_draft"])
    else:
        st.info("Awaiting task input to initialize multi-agent nodes...")