from agents import Agent, Runner, function_tool, ModelSettings, WebSearchTool
from openai.types.responses import ResponseTextDeltaEvent
from typing import List
from datetime import datetime

async def ai(
        question: str, 
        agent_name: str,
        system_message: str,
        user_message_template: str,
        tools: List[function_tool], 
        stream: bool = False, 
        model: str = "gpt-4.1"
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
        async for event in result.stream_events():

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

            elif event.type == "agent_updated_stream_event":
                #print(f"Agent updated: {event.new_agent.name}")
                continue

            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    tool_name = event.item.raw_item.name
                    tool_args = event.item.raw_item.arguments
                    print(f"Tool {tool_name} called with arguments: {tool_args}")

                elif event.item.type == "tool_call_output_item":
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