import os
import re
import shutil
from config import NARRATOR_NICKNAME, DOCS_DIR, BUILT_DOCS_DIR
from pathlib import Path

def transform_zii_block(content):
    lines = content.split("\n")
    chatbox = '<div class="chatbox">\n'

    for line in lines:
        line = line.strip()
        if not line:
            continue

        timestamp_match = re.match(r"^\[(\d{2}:\d{2})\]\s*", line)
        timestamp = timestamp_match.group(1) if timestamp_match else None
        line = re.sub(r"^\[\d{2}:\d{2}\]\s*", "", line)

        nickname_match = re.match(r"^([^:]+):\s*(.*)", line)
        nickname = nickname_match.group(1).strip() if nickname_match else None
        message_text = nickname_match.group(2).strip() if nickname_match else line.strip()

        message_type = "chat-message"  # Default type
        if nickname:
            if nickname.startswith('"'):
                nickname = nickname.replace('"', f"{NARRATOR_NICKNAME}->", 1)
                message_type = "private-message"
            elif nickname.endswith('"'):
                nickname = nickname.replace('"', f"->{NARRATOR_NICKNAME}", 1)
                message_type = "private-message"
            elif nickname.startswith("!"):
                message_type = "shout-message"
            elif nickname.startswith("+"):
                message_type = "trade-message"
            elif nickname.startswith("#"):
                message_type = "party-message"
            elif nickname.startswith("@"):
                message_type = "clan-message"
            elif nickname.startswith("$"):
                message_type = "alliance-message"
            elif nickname.startswith("{"):
                nickname = nickname.replace("{", "")
                message_type = "system-message"
            elif nickname.startswith("}"):
                nickname = nickname.replace("}", "")
                message_type = "combat-message"
            elif nickname.startswith("·"):
                nickname = nickname.replace("·", "")
                message_type = "warning-message"

        message = f'<div class="message {message_type}">\n'
        if timestamp:
            message += f'<span class="timestamp">[{timestamp}]</span>\n'
        if nickname:
            message += f'<strong>{nickname}:</strong>\n'
        message += f'<span>{message_text}</span>\n'
        message += '</div>\n'

        chatbox += message

    chatbox += '</div>'
    return chatbox

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    transformed_content = re.sub(
        r"```zii([\s\S]*?)```",
        lambda match: transform_zii_block(match.group(1)),
        content,
    )
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(transformed_content)

    print(f"Processed: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                process_file(file_path)

# Main script
if __name__ == "__main__":
    pages_dir = Path(DOCS_DIR)
    build_dir = Path(BUILT_DOCS_DIR)
    if not pages_dir.exists():
        raise FileNotFoundError(f"The directory '{pages_dir}' does not exist.")

    # Copy files to the temporary directory
    if build_dir.exists():
        shutil.rmtree(build_dir)
    shutil.copytree(pages_dir, build_dir)

    print("Transforming zii code blocks in Markdown files...")
    process_directory(build_dir)
    print("Transformation complete!")