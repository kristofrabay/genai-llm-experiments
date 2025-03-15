import dotenv
dotenv.load_dotenv()

import os
import requests

from datetime import datetime
import time

from slack_sdk import WebClient


channel_id = os.getenv("SLACK_CHANNEL_ID")
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def send_message_and_get_ts(message):
    response = client.chat_postMessage(channel=channel_id, text=message)
    return response["ts"]

def poll_for_feedback(channel_id, thread_ts, timeout=60):

    start_time = time.time()

    while time.time() - start_time < timeout:

        response = client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = response.get("messages", [])
        
        for msg in messages:
            # Skip the original message (which has the same ts as thread_ts)
            if msg.get("ts") == thread_ts:
                continue
                
            # If we found any reply message that's not the original, return it
            return msg.get("text")
            
        # No reply found yet, wait and try again
        time.sleep(5)
        
    return None

def slack_communication(message, require_feedback=False, timeout=60, image_url=None, image_path=None):
    """
    Send a message to Slack and optionally wait for human feedback.
    
    Args:
        message (str): The message to send to Slack
        require_feedback (bool): Whether to wait for human feedback
        timeout (int): Maximum time to wait for feedback in seconds
        image_url (str): Optional URL of an image to attach (for remote images)
        image_path (str): Optional file path to a local image to upload
        
    Returns:
        str: Human feedback if require_feedback=True, otherwise confirmation message
    """
    try:
        thread_ts = None
        
        # Handle local image upload if provided
        if image_path:
            # Upload the file first
            upload_response = client.files_upload_v2(
                channel=channel_id,
                file=image_path,
                initial_comment=message
            )
            # For local images, we need to send a follow-up message to get the thread_ts
            if require_feedback:
                if require_feedback:

                    thread_ts = None #upload_response.get('file', {}).get('timestamp', {})

                    if not thread_ts:
                        # Fallback if we can't get thread_ts from file upload
                        response = client.chat_postMessage(channel=channel_id, text="Respond to the last image here:")
                        
                        thread_ts = response["ts"]

            else:
                return f"Message and local image posted successfully: {message[:50]}..." if len(message) > 50 else message
        
        # Handle remote image URL
        elif image_url:
            # Prepare blocks for message with image URL
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Image"
                }
            ]
            
            response = client.chat_postMessage(
                channel=channel_id, 
                text=message,
                blocks=blocks
            )
            if require_feedback:
                thread_ts = response["ts"]

            else:
                return f"Message with remote image posted successfully: {message[:50]}..." if len(message) > 50 else message
        
        # Text-only message
        else:
            response = client.chat_postMessage(
                channel=channel_id, 
                text=message
            )
            if require_feedback:
                thread_ts = response["ts"]
                
            else:
                return f"Message posted successfully: {message[:50]}..." if len(message) > 50 else message
        
        # Wait for feedback if required
        if require_feedback and thread_ts:
            print(f"Message sent, waiting for feedback (timeout: {timeout}s)...")
            feedback = poll_for_feedback(channel_id, thread_ts, timeout)
            
            if feedback:
                return feedback
            else:
                return "No feedback received within the timeout period."
        
    except Exception as e:
        return f"Error sending message: {str(e)}"
