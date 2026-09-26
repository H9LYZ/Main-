# Ticket Bot 🎫 Made By Vexis/H9LYZ

A Python-based Discord bot featuring a ticket management system with interactive buttons, custom category placement, and owner/admin toggle controls.

---

## 🛠️ Features
- **📩 Dynamic Ticket Panels:** Post a support panel in any channel with a single command.
- **📁 Custom Categories:** Direct newly opened tickets to any target category.
- **🔒 Private Channels:** Automatic permission setup restricting view access strictly to the user and staff.
- **🛑 Admin Toggle Controls:** Instantly disable or re-enable ticket creation (`/down_ticket` and `/online_ticket`).
- **🛡️ Secure Token Storage:** Uses `.env` files to prevent secret token leaks.

---

## ⚙️ Commands

| Command | Permission | Description |
| :--- | :--- | :--- |
| `/ticket_setup [category]` | Administrator | Posts the support panel and links ticket creation to the selected category. |
| `/down_ticket` | Administrator | Takes ticket creation offline. |
| `/online_ticket` | Administrator | Brings ticket creation back online. |

---

## 🚀 Setup & Installation

### 1. Requirements
Ensure you have Python 3.8+ installed, then install the dependencies:
```bash
pip install -r requirements.txt
