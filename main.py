import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

class SyncBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="$",
            intents=intents
        )

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"O Bot {self.user} está Ligado.")

bot = SyncBot()

@bot.tree.command(name="ola_mundo", description="Ola Querido Mundo!")
async def olamundo(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Ola {interaction.user.mention}!"
    )

# Evento de novo membro
@bot.event
async def on_member_join(member: discord.Member):
    canal_bemvindo = bot.get_channel(1477821288436334644)
    canal_regras = bot.get_channel(1477396107339370576)

    if canal_bemvindo and canal_regras:
        await canal_bemvindo.send(
            f"Bem Vindo {member.mention} ao Servidor, "
            f"Leia as regras {canal_regras.mention}!"
        )

# Token correta via variável de ambiente
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN não encontrada no arquivo .env")

bot.run(TOKEN)