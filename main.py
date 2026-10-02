from graph.agent import create_agent
from graph.state import AgentState

def main():
    print("=" * 50)
    print("I4Twins Multi-Skill Agent")
    print("Skills: Summarizer | Translator | Calculator | General Chat")
    print("Type 'exit' or 'quit' to stop")
    print("=" * 50)

    agent = create_agent()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
                
            if not user_input:
                continue

            # Initial state
            initial_state: AgentState = {
                "user_input": user_input,
                "detected_skills": [],
                "reasoning": "",
                "skill_results": {},
                "final_response": None,
            }

            # Run the agent
            result = agent.invoke(initial_state)

            print("\nAgent:", result.get("final_response", "No response generated."))

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()