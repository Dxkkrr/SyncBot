import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

invites = {}

class SyncBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="$",
            intents=intents
        )

    async def setup_hook(self):
        await self.tree.sync()

bot = SyncBot()

# Bot pronto
@bot.event
async def on_ready():
    print(f"O Bot {bot.user} está Ligado.")

    for guild in bot.guilds:
        invites[guild.id] = await guild.invites()


# Novo membro
@bot.event
async def on_member_join(member: discord.Member):

    canal_bemvindo = bot.get_channel(1477821288436334644)
    canal_regras = bot.get_channel(1477396107339370576)
    canal_invites = bot.get_channel(1477703820703170570)

    cargo = member.guild.get_role(1477447780979970058)

    if cargo:
        await member.add_roles(cargo)

    if canal_bemvindo and canal_regras:
        await canal_bemvindo.send(
            f"Bem Vindo {member.mention} ao Servidor, "
            f"Leia as regras {canal_regras.mention}!"
        )

    guild = member.guild
    new_invites = await guild.invites()

    inviter = None

    for invite in new_invites:
        for old_invite in invites[guild.id]:
            if invite.code == old_invite.code and invite.uses > old_invite.uses:
                inviter = invite.inviter

    invites[guild.id] = new_invites

    if canal_invites:
        await canal_invites.send(
            f"Bem vindo {member.mention}!\n"
            f"Convidado por: {inviter.mention if inviter else 'Desconhecido'}\n"
            f"Leia as regras {canal_regras.mention}"
        )


# Saída de membro
@bot.event
async def on_member_remove(member: discord.Member):
    canal_bemvindo = bot.get_channel(1477821288436334644)

    if canal_bemvindo:
        await canal_bemvindo.send(
            f"{member.mention} saiu do servidor!"
        )


# Comando
@bot.tree.command(name="ola_mundo", description="Ola Querido Mundo!")
async def olamundo(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Ola {interaction.user.mention}!"
    )


TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN não encontrada no arquivo .env")

bot.run(TOKEN)