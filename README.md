# RAMN

RAMN is a public personal AI website with account registration, chat, and an owner moderation panel. It also retains the original iPhone/a-Shell Python assistant in \`ramn.py\`.

## Deploy on Render

Create a Python Web Service from this GitHub repository:

- Build command: \`pip install -r requirements.txt\`
- Start command: \`gunicorn app:app\`
- Health check path: \`/health\`
- Region: Frankfurt is recommended for European visitors.

Set these environment variables in Render:

- \`RAMN_SECRET_KEY\`: a long random secret
- \`RAMN_OWNER_PASSWORD\`: a strong private owner password
- \`OPENAI_API_KEY\`: an OpenAI API key (required for AI chat; API usage may cost money)
- Optional: \`RAMN_CHAT_MODEL\` (defaults to \`gpt-4.1-mini\`)

Never put these secrets in GitHub. ChatGPT subscriptions and API billing are separate.

## Owner moderation

Open \`/owner/login\` and enter the value of \`RAMN_OWNER_PASSWORD\`.
The owner panel lists registered accounts and lets the owner ban or unban them.
Banned accounts are blocked server-side at login and on authenticated routes.

## Database persistence

The app uses SQLite. On Render's free web-service filesystem, local files can be reset during redeploys, restarts, or instance replacement. For durable accounts and bans, attach a persistent disk at \`/var/data\` and set \`RAMN_DB_PATH=/var/data/ramn.sqlite3\`, or migrate to a managed PostgreSQL database. Persistent disks may require a paid Render plan.

## Security and limitations

- Passwords are stored as salted PBKDF2 hashes.
- Owner access is controlled by a private Render environment variable.
- Use HTTPS (Render provides it).
- This starter app has basic session-based chat history and account management.
- Add CSRF protection, login throttling, database backups and a managed database before treating it as a large public production service.
- The browser chat uses the server-side OpenAI key; visitors do not see the key.
- Do not send sensitive personal information to the assistant.

## Local run

\`\`\`sh
pip install -r requirements.txt
export RAMN_SECRET_KEY="change-this-local-secret"
export RAMN_OWNER_PASSWORD="change-this-owner-password"
export OPENAI_API_KEY="your-api-key"
python app.py
\`\`\`

The original iPhone terminal assistant is in \`ramn.py\`.
