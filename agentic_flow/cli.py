from agent import StrategistAgent
import argparse

def main():
    parser = argparse.ArgumentParser(description="Card Game Strategist Agent")
    parser.add_argument("--query", type=str, help="User query")
    args = parser.parse_args()
    
    agent = StrategistAgent()
    
    if args.query:
        # Process a single query
        response = agent.process_query(args.query)
        print(f"Response: {response['answer']}")
    else:
        # Interactive mode
        print("Magic the Gathering agent (type 'exit' to quit, 'reset' to clear history)")
        while True:
            query = input("\nUser: ")
            if query.lower() == "exit":
                break
            if query.lower() == "reset":
                agent.reset_conversation()
                print("Conversation history reset.")
                continue
                
            response = agent.process_query(query)
            print(f"\nStrategist: {response['answer']}")

if __name__ == "__main__":
    main()