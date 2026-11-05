#!/usr/bin/env python3
"""RAMN - a small online personal AI assistant for a-Shell on iPhone.

Uses only Python's standard library. API keys and personal data stay in local,
git-ignored files. Voice replies are saved as MP3 files in the current folder.
"""
import ast
import datetime as dt
import getpass
import json
import operator
import os
import sys
import urllib.error
import urllib.request

APP_NAME = "RAMN"
CONFIG_FILE = "ramn_config.json"
MEMORY_FILE = "ramn_memory.json"
NOTES_FILE = "ramn_notes.json"
AUDIO_FILE = "ramn_voice.mp3"

CHAT_MODEL = os.environ.get("RAMN_CHAT_MODEL", "gpt-4.1-mini")
TTS_MODEL = os.environ.get("RAMN_TTS_MODEL", "gpt-4o-mini-tts")
VOICE = os.environ.get("RAMN_VOICE", "onyx")

SYSTEM_PROMPT = """You are RAMN, a capable personal AI assistant.
Speak German by default and match the user's language when appropriate.
Your voice and personality are calm, intelligent, warm, concise and confident.
Be honest about your capabilities. Never claim you accessed a device, website,
file, account or service unless a tool in this program actually did so.
You can explain, plan, write code, brainstorm and help with everyday tasks.
Do not ask for passwords, API keys or other secrets in chat.
Ask for confirmation before sensitive or irreversible actions.
"""

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, ValueError, TypeError):
        return default

def save_json(path, value):
    temp = path + ".tmp"
    with open(temp, "w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
    os.replace(temp, path)

def get_api_key():
    config = load_json(CONFIG_FILE, {})
    key = config.get("api_key", "").strip()
    if key:
        return key

    print("\n[SETUP] OpenAI API key required.")
    print("The key is saved only in this local git-ignored config file.")
    try:
        key = getpass.getpass("API key (input hidden): ").strip()
    except (Exception,):
        key = input("API key: ").strip()

    if not key:
        print("No API key entered. Exiting.")
        raise SystemExit(1)

    save_json(CONFIG_FILE, {"api_key": key})
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except OSError:
        pass
    return key

API_KEY = get_api_key()
history = load_json(MEMORY_FILE, [])
notes = load_json(NOTES_FILE, [])
voice_enabled = True

def request_json(endpoint, payload):
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/" + endpoint,
        data=body,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except ValueError:
            pass
        raise RuntimeError("API error " + str(error.code) + ": " + str(detail))
    except urllib.error.URLError as error:
        raise RuntimeError("Network error: " + str(error.reason))

def ask_ram(message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-16:])
    messages.append({"role": "user", "content": message})
    result = request_json("chat/completions", {
        "model": CHAT_MODEL,
        "messages": messages,
        "temperature": 0.7,
    })
    answer = result["choices"][0]["message"]["content"]
    if isinstance(answer, list):
        answer = " ".join(
            part.get("text", "") for part in answer
            if isinstance(part, dict)
        )
    answer = str(answer).strip()
    if not answer:
        answer = "I could not generate a response."
    history.extend([
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ])
    del history[:-40]
    save_json(MEMORY_FILE, history)
    return answer

def make_voice(text):
    payload = json.dumps({
        "model": TTS_MODEL,
        "voice": VOICE,
        "input": text[:4000],
        "instructions": (
            "Speak in natural German with a deep, warm adult male voice. "
            "Calm, clear, confident and measured, like a polished AI assistant. "
            "Avoid robotic delivery."
        ),
        "response_format": "mp3",
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/audio/speech",
        data=payload,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            audio = response.read()
        with open(AUDIO_FILE, "wb") as file:
            file.write(audio)
        print("[VOICE] MP3 saved as " + os.path.abspath(AUDIO_FILE))
        print("[VOICE] Open the MP3 from the a-Shell Documents folder to listen.")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print("[VOICE ERROR] " + str(error.code) + " " + detail[:500])
    except (urllib.error.URLError, OSError) as error:
        print("[VOICE ERROR] " + str(error))

def safe_calculate(expression):
    allowed_ops = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
        ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](evaluate(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent too large.")
            return allowed_ops[type(node.op)](left, right)
        raise ValueError("Only basic arithmetic is allowed.")
    return evaluate(ast.parse(expression, mode="eval"))

def show_help():
    print("""
COMMANDS
  /help          Show this help
  /time          Show local device time
  /note TEXT     Save a note
  /notes         List saved notes
  /calc EXPR     Calculate basic arithmetic
  /voice on|off  Enable or disable spoken replies
  /forget        Clear conversation memory
  /exit          Close RAMN

Anything else is sent to the online AI.
Voice replies are saved as ramn_voice.mp3 in this folder.
""")

def handle_command(text):
    global voice_enabled, history
    if text == "/help":
        show_help()
    elif text == "/time":
        print("[RAMN] " + dt.datetime.now().astimezone().strftime("%A, %d %B %Y — %H:%M:%S %Z"))
    elif text.startswith("/note "):
        note = text[6:].strip()
        if note:
            notes.append({
                "text": note,
                "created": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            })
            save_json(NOTES_FILE, notes)
            print("[RAMN] Note saved.")
        else:
            print("Usage: /note your note")
    elif text == "/notes":
        if not notes:
            print("[RAMN] No notes saved.")
        else:
            for index, note in enumerate(notes, 1):
                print(str(index) + ". " + note["text"])
    elif text.startswith("/calc "):
        try:
            print("[RAMN] " + str(safe_calculate(text[6:].strip())))
        except Exception as error:
            print("[RAMN] Calculation error: " + str(error))
    elif text == "/voice on":
        voice_enabled = True
        print("[RAMN] Voice enabled.")
    elif text == "/voice off":
        voice_enabled = False
        print("[RAMN] Voice disabled.")
    elif text == "/forget":
        history = []
        save_json(MEMORY_FILE, history)
        print("[RAMN] Conversation memory cleared.")
    else:
        return False
    return True

def main():
    print("\n" + "=" * 48)
    print("  RAMN // PERSONAL AI SYSTEM")
    print("  ONLINE • VOICE: " + VOICE.upper())
    print("=" * 48)
    print("Type /help for commands. Type /exit to quit.\n")

    while True:
        try:
            user_text = input("YOU > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[RAMN] Shutting down.")
            break

        if not user_text:
            continue
        if user_text.lower() in ("/exit", "exit", "quit"):
            print("[RAMN] Goodbye.")
            break
        if handle_command(user_text):
            continue

        print("\n[RAMN] Thinking...\n")
        try:
            answer = ask_ram(user_text)
            print("RAMN > " + answer + "\n")
            if voice_enabled:
                make_voice(answer)
        except Exception as error:
            print("[RAMN ERROR] " + str(error))

if __name__ == "__main__":
    main()
