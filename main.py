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

# Comando de Slash

@bot.tree.command(name="ola_mundo", description="Ola Querido Mundo!")
async def olamundo(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Ola {interaction.user.mention}!"
    )

# Novo membro
@bot.event
async def on_member_join(member: discord.Member):
    canal_bemvindo = bot.get_channel(1477821288436334644)
    canal_regras = bot.get_channel(1477396107339370576)
    cargo = member.guild.get_role(1477447780979970058)

    if cargo:
        await member.add_roles(cargo)

    if canal_bemvindo and canal_regras:
        await canal_bemvindo.send(
            f"Bem Vindo {member.mention} ao Servidor, "
            f"Leia as regras {canal_regras.mention}!"
        )

#Saida de Membro
@bot.event
async def on_member_remove(member: discord.Member):
    canal_bemvindo = bot.get_channel(1477821288436334644)

    if canal_bemvindo:
        await canal_bemvindo.send(
            f"{member.mention} saiu do servidor!"
        )

# Token correta via variável de ambiente
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN não encontrada no arquivo .env")

bot.run(TOKEN)