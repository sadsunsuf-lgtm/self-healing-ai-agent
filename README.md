# 🛡️ Autonomous Self-Healing Multi-Agent System (MAS)
**Enterprise-Grade Orchestration for Intelligent Decision Making**

---

## 🏛️ Project Vision
In the 2026 AI landscape, simple LLM prompts are no longer enough. This project demonstrates a **Self-Healing Agentic Workflow** built on **LangGraph**. It replaces linear AI responses with an autonomous team structure that uses **Reflection Patterns** to audit, critique, and refine its own output before final delivery.

> **Key Achievement:** Achieved a zero-human-intervention pipeline for technical reporting by implementing an autonomous quality-gate (Critic) that forces revisions on suboptimal drafts.

---

## 🧠 Cognitive Architecture
The system is modeled as a **Stateful Graph**, ensuring that context is never lost and errors are corrected in real-time.

### 1. The Analyst Node (Execution)
The "Worker" agent responsible for high-speed research and synthesis.
* **Capabilities:** Real-time web-scraping (DuckDuckGo), multi-source data fusion.
* **Context Awareness:** Injected with previous "Critique Notes" during revision cycles.

### 2. The Strategist Node (Supervision)
The "Critic" agent acting as a high-level quality guardrail.
* **Logic:** Evaluates the Analyst's output against strict enterprise metrics (Depth, Technical Accuracy, Bias).
* **Decision Gate:** Implements a binary pass/fail logic. If `fail`, it generates a "Refinement Plan" for the Analyst.

### 3. The Self-Healing Loop (Reflection)
Instead of a straight path, the graph uses **Conditional Edges**. If the Strategist identifies a hallucination or data gap, the workflow automatically "heals" by rerouting the state back to the Analyst for a targeted rewrite.

---

## 🛠️ Tech Stack & Engineering Primitives
* **Orchestration:** LangGraph (Stateful Workflow Management)
* **Reasoning Engine:** Llama-3.3-70B (via Groq for sub-second inference)
* **State Persistence:** Python `TypedDict` for real-time memory tracking
* **Deployment Architecture:** Streamlit Cloud with Secrets Management

---

## 📊 System Execution Flow
```mermaid
graph TD
    A[User Input] --> B[Analyst Node]
    B --> C{Strategist Critique}
    C -- "Suboptimal" --> D[Generate Feedback]
    D --> B
    C -- "Ready" --> E[Final Intelligence Report]
    
    style C fill:#f96,stroke:#333,stroke-width:2px
    style E fill:#00ff00,stroke:#333,stroke-width:2px