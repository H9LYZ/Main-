import datetime
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = None

tickets_enabled = True


class TicketBot(commands.Bot):

  def __init__(self):
    intents = discord.Intents.default()
    intents.guilds = True
    super().__init__(command_prefix="!", intents=intents)

  async def setup_hook(self):
    self.add_view(TicketSetupView())
    self.add_view(CloseTicketView())

    if GUILD_ID:
      guild = discord.Object(id=GUILD_ID)
      self.tree.copy_global_to(guild=guild)
      await self.tree.sync(guild=guild)
      print(f"Slash commands synced instantly to Guild ID: {GUILD_ID}")
    else:
      await self.tree.sync()
      print("Slash commands synced globally!")


bot = TicketBot()


class TicketSetupView(discord.ui.View):

  def __init__(self, category_id: int = None):
    super().__init__(timeout=None)
    self.category_id = category_id

  @discord.ui.button(
      label="Create Ticket",
      style=discord.ButtonStyle.green,
      emoji="🎫",
      custom_id="create_ticket_button",
  )
  async def create_ticket(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if not tickets_enabled:
      await interaction.response.send_message(
          "⚠️ Support tickets are currently **OFFLINE**. Please try again"
          " later!",
          ephemeral=True,
      )
      return

    guild = interaction.guild
    user = interaction.user

    category = (
        guild.get_channel(self.category_id)
        if self.category_id
        else interaction.channel.category
    )

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(
            read_messages=True, send_messages=True
        ),
        guild.me: discord.PermissionOverwrite(
            read_messages=True, send_messages=True, manage_channels=True
        ),
    }

    ticket_channel_name = f"ticket-{user.name.lower()}"

    ticket_channel = await guild.create_text_channel(
        name=ticket_channel_name,
        category=category,
        overwrites=overwrites,
        reason=f"Ticket opened by {user}",
    )

    embed = discord.Embed(
        title=f"Welcome {user.name}!",
        description=(
            "Staff will be with you shortly. Describe your issue below.\n\nClick"
            " **Close Ticket** when finished."
        ),
        color=0xFEE75C,
    )
    await ticket_channel.send(
        content=user.mention, embed=embed, view=CloseTicketView()
    )

    await interaction.response.send_message(
        f"✅ Your ticket has been created: {ticket_channel.mention}",
        ephemeral=True,
    )


class CloseTicketView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(
      label="Close Ticket",
      style=discord.ButtonStyle.red,
      emoji="🔒",
      custom_id="close_ticket_button",
  )
  async def close_ticket(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message("Deleting ticket in 5 seconds...")
    await discord.utils.sleep_until(
        discord.utils.utcnow() + datetime.timedelta(seconds=5)
    )
    await interaction.channel.delete(reason="Ticket closed by user/staff.")


@bot.tree.command(
    name="ticket_setup", description="Sets up the ticket panel in this channel."
)
@app_commands.describe(category="The category where tickets will be created")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_setup(
    interaction: discord.Interaction, category: discord.CategoryChannel
):
  embed = discord.Embed(
      title="📩 Support Tickets",
      description=(
          "Need help or have a question? Click the button below to open a"
          " private ticket with staff!"
      ),
      color=0xFEE75C,
  )

  view = TicketSetupView(category_id=category.id)
  await interaction.channel.send(embed=embed, view=view)

  await interaction.response.send_message(
      f"✅ Ticket panel initialized! Tickets will be created under:"
      f" **{category.name}**",
      ephemeral=True,
  )


@bot.tree.command(
    name="down_ticket", description="Take ticket creation offline (Admin Only)."
)
@app_commands.checks.has_permissions(administrator=True)
async def down_ticket(interaction: discord.Interaction):
  global tickets_enabled
  tickets_enabled = False
  await interaction.response.send_message(
      "🛑 Ticket creation system has been turned **OFFLINE**.", ephemeral=True
  )


@bot.tree.command(
    name="online_ticket",
    description="Bring ticket creation back online (Admin Only).",
)
@app_commands.checks.has_permissions(administrator=True)
async def online_ticket(interaction: discord.Interaction):
  global tickets_enabled
  tickets_enabled = True
  await interaction.response.send_message(
      "🟢 Ticket creation system is now **ONLINE**.", ephemeral=True
  )


@ticket_setup.error
@down_ticket.error
@online_ticket.error
async def admin_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
  if isinstance(error, app_commands.MissingPermissions):
    await interaction.response.send_message(
        "❌ Only Administrators can use this command.", ephemeral=True
    )


bot.run(TOKEN)
