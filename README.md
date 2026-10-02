# Multi-Skill AI Agent

Early prototype of a multi-skill agent built with **LangGraph**.  
The agent receives a free-form prompt (English or Persian), detects the relevant skill(s), and generates a response.

## AI Usage Disclosure

This project was developed with the assistance of an AI coding assistant (Grok).  
The assistant helped with:

- Project structure
- LangGraph graph design
- Prompt engineering
- Debugging routing loops
- Writing documentation

All final code and design decisions were reviewed and understood by the author.

## Evaluation

A set of 15 varied prompts (clear, ambiguous, multi-skill, Persian) was tested.

**Skill Detection Accuracy: 100%**

See `evaluation.md` for the full table.


## Skills

| Skill | Description |
|-------|-------------|
| **Summarizer** | Summarizes the input text |
| **Translator** | Translates the input text |
| **Calculator** | Performs real mathematical calculations (uses a safe evaluation tool) |
| **General Chat** | Handles greetings, small talk, and general questions |

Supports up to **2 skills simultaneously**.

---

## How to Run

### Prerequisites
- Python 3.10+
- Groq API key (free tier)

### Installation

```bash
git clone <your-repo-url>
cd i4twins-ai-agent
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt