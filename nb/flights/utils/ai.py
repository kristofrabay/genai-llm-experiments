from dotenv import load_dotenv
load_dotenv()

from agents import Agent, Runner, function_tool, WebSearchTool
from openai.types.responses import ResponseTextDeltaEvent, ResponseWebSearchCallInProgressEvent, ResponseWebSearchCallCompletedEvent

from typing import List
from IPython.display import display, Markdown
from datetime import datetime
import asyncio

async def ai(
        question: str, 
        agent_name: str,
        system_message: str,
        user_message_template: str,
        tools: List[function_tool], 
        stream: bool = False, 
        model: str = "gpt-4.1",
        format_to_md: bool = False
    ):
    
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    agent = Agent(
        name=agent_name,
        instructions=system_message,
        model=model,
        tools=tools,
    )
    
    formatted_question = user_message_template.format(
        question=question,
        current_datetime=current_datetime
    )
    
    if stream:
        result = Runner.run_streamed(agent, formatted_question)

        #print("=== Run starting ===")
        if format_to_md:
            md_display = display(Markdown(""), display_id=True)
            text_chunks = []

        async for event in result.stream_events():

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if format_to_md:
                    text_chunks.append(event.data.delta)
                    md_display.update(Markdown("".join(text_chunks)))
                else:
                    print(event.data.delta, end="", flush=True)

            elif event.type == "raw_response_event" and isinstance(event.data, ResponseWebSearchCallInProgressEvent):
                print(f"Web search call in progress: {event.data.item_id}")

            elif event.type == "raw_response_event" and isinstance(event.data, ResponseWebSearchCallCompletedEvent):
                print(f"Web search call completed: {event.data.item_id}")

            elif event.type == "agent_updated_stream_event":
                #print(f"Agent updated: {event.new_agent.name}")
                continue

            elif event.type == "run_item_stream_event" and event.item.type == "tool_call_item":
                try:
                    tool_name = event.item.raw_item.name
                except Exception as e:
                    tool_name = event.item.raw_item.type
                try:
                    tool_args = event.item.raw_item.arguments
                    print(f"Tool {tool_name} called with arguments: {tool_args}")
                except Exception as e:
                    continue
                    
            elif event.type == "run_item_stream_event" and event.item.type == "tool_call_output_item":
                tool_name = event.item.raw_item['call_id'].split('_')[1]
                tool_output = str(event.item.output)[:250]
                print(f"Tool call {tool_name} returned with results: {tool_output}")

                #elif event.item.type == "message_output_item":
                #    print("------ Agent output ------")
                #    print(f"{ItemHelpers.text_message_output(event.item)}")
                #    print("------ / Agent output ------")

            else:
                pass  # Ignore other event types

        #print("=== Run complete ===")

        return result
    
    else:
        result = await Runner.run(agent, formatted_question)
        return result

async def conversation(payload: dict):
    conversation_history = []
    
    while True:
        q = input("\n\nHuman input: ")
        # Clear the "Human input: " prompt after user enters text
        print("\033[A\033[K", end="")  # Move up one line and clear it
        
        print("\n=== Human ===")
        print(q)
        
        if q.lower() == "quit":
            break
            
        print("\n=== AI ===")
        
        if not conversation_history:
            # First turn
            a = await ai(q, **payload)
            conversation_history = a.to_input_list()
        else:
            # Subsequent turns
            new_input = conversation_history + [{"role": "user", "content": q}]
            a = await ai(new_input, **payload)
            conversation_history = a.to_input_list()

if __name__ == "__main__":

    from tools import get_flights_to_destinations_tool, add_tool
    from prompts import system_message, user_message_template
    
    default_payload = {
        "agent_name": "Flight Assistant",
        "system_message": system_message,
        "user_message_template": user_message_template,
        "tools": [get_flights_to_destinations_tool, add_tool, WebSearchTool()],
        "stream": True,
        "model": "gpt-4.1",
        "format_to_md": False
    }
    
    # Run the conversation function instead of a single query
    asyncio.run(conversation(payload=default_payload))