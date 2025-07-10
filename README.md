<p align="center">
  <img src="https://envs.sh/232.jpg" alt="RMC-POST-SEARCH-BOT Logo">
</p>

<h1 align="center">
  RMC POST SEARCH BOT
</h1>

---

## 🔍 Fast Telegram Post Search Bot — Powered by RMCBACKUP

A powerful Telegram bot to search posts from connected channels, with advanced features like force subscription, pagination, owner login, web dashboard, retry system, and more.

---

## 🧩 Features

### 💬 Basic Commands

| Command | Description |
|--------|-------------|
| `/start` | Show welcome message with buttons |
| `/help` | Show how to use the bot |
| `/about` | Info about the bot & credits |
| `/id` | Get user ID, chat ID, replied user ID, etc. |
| `/stats` | Show total user and group count |
| `/login` / `/logout` | Owner-only session-based login/logout |

---

### 📡 Channel Connection System

| Command | Description |
|--------|-------------|
| `/connect` | Connect current group to a channel |
| `/disconnect` | Disconnect current channel |
| `/connections` | Show all connected channels |
| `/verify` | Group verification via log channel |

---

### 🔐 Force Subscription System

| Feature | Description |
|--------|-------------|
| `/fsub` / `/nofsub` | Enable or disable force-subscription |
| 🔁 Retry Button | Resume search after user joins required channel |
| ⏱ Auto Resume | If user joins later, previous search resumes |

---

### 🔍 Post Search System

| Feature | Description |
|--------|-------------|
| 🔎 Text Search | Fast keyword-based search from connected channels |
| 📄 Pagination | 5 results per page with ◀️ ▶️ inline navigation |
| 💾 Recent Memory | Saves last search to retry after join |
| 📩 Upload Request | If no result, user can request via button |

---

### 🧠 Inline Buttons & Callback Support

| Feature | Description |
|--------|-------------|
| `misc_help`, `misc_about` | Inline buttons for help/about |
| `⬅️ Back` Buttons | Navigation inside inline responses |
| Pagination Buttons | `page_<id>_<page>` to move pages |
| Upload Request | Sends message to admin log channel |

---

### 🔧 Admin & Owner Features

| Feature | Description |
|--------|-------------|
| 📢 Broadcast | Send messages to all users (owner only) |
| 🧪 Owner Login | Via phone + OTP (2FA supported) |
| 🧠 Session Saved | Owner session stored securely |
| `/adminpanel` | Feature toggles (inline, spell toggle etc.) |

---

### 🌐 Web Server & Hosting

| Feature | Description |
|--------|-------------|
| 🌐 Flask Server | Route `/` returns "🤖 Bot is running!" |
| ☁️ Render / Koyeb Ready | Deployable on Render (free) or Koyeb |
| 🔄 Prevent Idle | Flask keeps app container alive |

---

### 🧾 MongoDB Powered (Motor Async)

| Data | Stored In |
|------|-----------|
| 🧍 Users | Saved on `/start` |
| 👥 Groups | Saved when bot added |
| 🔐 Sessions | Owner login sessions |
| 🧷 Last Query | For retry-after-join |
| 📌 Connections | Group-to-channel maps |

---

### ✨ Other Features

- ✅ Modular plugin structure
- ✅ Fast async search system
- ✅ Auto delete bot replies after 50 seconds
- ✅ Fully compatible with Render deployments
- ✅ Branding: **BY RMCBACKUP** in all bot responses

---

## 📸 Demo

> [Click to open bot](https://t.me/YOUR_BOT_USERNAME)

> Replace `YOUR_BOT_USERNAME` with your bot's actual username.

---

## 🚀 Deployment

Bot is fully ready for deployment on:

- ✅ [Render](https://render.com/)
- ✅ [Koyeb](https://koyeb.com/)
- ✅ [Railway](https://railway.app/) *(optional)*

You only need to set:

```env
API_ID=
API_HASH=
BOT_TOKEN=
DATABASE_URI=
ADMIN=
LOG_CHANNEL=


---

### 🧾 Notes:
- Replace `YOUR_BOT_USERNAME` in the demo link section.
- You can also add a **badge section** if you want GitHub stars, forks, etc.
- This README is GitHub-optimized (Markdown format) and shows well on mobile and web.

---

Let me know if you want:
- 🧪 Badge for Render Deploy
- 🔗 Add license info
- 📂 Add folder structure diagram

Ready to package your repo 💯
