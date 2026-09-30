# Ticket Bot 🎫 Made By Vexis/H9LYZ

A Python-based Discord bot featuring a ticket management system with interactive buttons, custom category placement, and owner/admin toggle controls.

🛠️ Features
- 📩 Dynamic Ticket Panels: Post a support panel in any channel with a single command.
- 📁 Custom Categories: Direct newly opened tickets to any target category.
- 🔒 Private Channels: Automatic permission setup restricting view access strictly to the user and staff.
- 🛑 Admin Toggle Controls: Instantly disable or re-enable ticket creation (/down_ticket and /online_ticket).
- 🛡️ Secure Token Storage: Uses .env files to prevent secret token leaks.

⚙️ Commands
| Command | Permission | Description |
| --- | --- | --- |
| /ticket_setup [category] | Administrator | Posts the support panel and links ticket creation to the selected category. |
| /down_ticket | Administrator | Takes ticket creation offline. |
| /online_ticket | Administrator | Brings ticket creation back online. |

🚀 Setup & Installation

1. Clone the repository and navigate into the folder:

~~~bash
git clone https://github.com/H9LYZ/Ticket-Tool-Sleepy
cd Ticket-Tool-Sleepy
~~~

2. Delete the original README.md file inside the directory:

~~~bash
rm README.md
~~~

3. Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

4. Create a .env file and add your Discord bot token:

~~~env
DISCORD_TOKEN=your_discord_bot_token_here
~~~

5. Run the bot:

~~~bash
python main.py
~~~
