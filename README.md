# RAMN — Personal AI Assistant

RAMN is a small online AI assistant designed to run in **a-Shell on iPhone**.
It uses the OpenAI API for chat and text-to-speech. It requires no pip packages.

## Features

- Online chat using the OpenAI Chat Completions API
- Natural male-style spoken replies using the OpenAI text-to-speech API
- Conversation history saved locally
- Local notes, time and safe arithmetic commands
- API key stored locally, never included in this repository
- Python standard library only

## Requirements

- iPhone with a-Shell
- Internet connection
- OpenAI API key with API billing enabled

ChatGPT subscriptions and API billing are separate. API usage may incur charges.
Check your API pricing and set a usage limit before using RAMN. If you are under
18, ask a parent or guardian to help set up API access and billing.

## Install on iPhone

1. Install **a-Shell** from the App Store.
2. Open a-Shell.
3. Run:

   \`\`\`sh
   cd ~/Documents
   \`\`\`

4. Download the source file from this repository, or copy \`jarvis.py\` into
   the a-Shell Documents folder and rename it to \`ramn.py\`.
5. Run:

   \`\`\`sh
   python3 ramn.py
   \`\`\`

6. On first launch, enter your OpenAI API key. RAMN stores it in
   \`ramn_config.json\` in the local Documents folder.

If you downloaded the file with the name \`jarvis.py\`, either run
\`python3 jarvis.py\` or rename it to \`ramn.py\`.

## Commands

| Command | Action |
|---|---|
| \`/help\` | Show commands |
| \`/time\` | Show device-local time |
| \`/note TEXT\` | Save a note |
| \`/notes\` | List saved notes |
| \`/calc EXPR\` | Calculate basic arithmetic |
| \`/voice on\` | Enable voice replies |
| \`/voice off\` | Disable voice replies |
| \`/forget\` | Clear conversation history |
| \`/exit\` | Quit RAMN |

All other text is sent to the online AI. Generated speech is saved as
\`ramn_voice.mp3\` in the current folder. Open that file from a-Shell's
Documents folder to listen. Automatic background playback and always-on
microphone access are not provided by this command-line version.

## Local files

These files are created on your device and are excluded by \`.gitignore\`:

- \`ramn_config.json\` — API key
- \`ramn_memory.json\` — recent conversation
- \`ramn_notes.json\` — saved notes
- \`ramn_voice.mp3\` — latest generated voice reply

**Never commit or share your API key or personal conversation files.**

## Configuration

Optional environment variables:

- \`RAMN_CHAT_MODEL\` — defaults to \`gpt-4.1-mini\`
- \`RAMN_TTS_MODEL\` — defaults to \`gpt-4o-mini-tts\`
- \`RAMN_VOICE\` — defaults to \`onyx\`

Model and voice availability can change. See the OpenAI API documentation.

## Privacy and safety

RAMN sends prompts to the OpenAI API to generate responses and speech.
Do not send passwords, payment details, private keys or sensitive personal data.
RAMN does not control iOS settings, send messages, access arbitrary apps,
or execute arbitrary shell commands. Review code before running it.

## License

MIT
