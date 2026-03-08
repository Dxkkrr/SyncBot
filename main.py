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
        await atualizar_painel(guild)


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

    await atualizar_painel(member.guild)


# Invite tracking
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

    await atualizar_painel(member.guild)

#Contador de membros
canal_contador = "1479641366689485011"
mensagens_stats = None

# Busca ou cria a mensagem do painel de estatísticas
async def pegar_painel(canal):
    async for msg in canal.history(limit=10):
        if msg.author == canal.guild.me and msg.embeds:
            return msg
        
    return await canal.send("Carregando estatísticas...")

# Atualiza o painel de estatísticas do servidor
async def atualizar_painel(guild):
    global mensagens_stats

    canal = bot.get_channel(int(canal_contador))

    total_membros = guild.member_count
    bots = len([m for m in guild.members if m.bot])
    membros = total_membros - bots
    online = len([m for m in guild.members if m.status != discord.Status.offline])
    offline = total_membros - online
    em_voz = len([m for m in guild.members if m.voice])
    boosters = guild.premium_subscription_count

# Atualiza o nome do canal com o número total de membros
    await canal.edit(name=f"📊 membros-{total_membros}")

    embed = discord.Embed(
        title="📊 Estatísticas do Servidor",
        color=discord.Color.blue()
    )
    embed.add_field(name="👥 Total", value=f"{total_membros}", inline=True)
    embed.add_field(name="🧑 Usuários", value=f"{membros}", inline=True)
    embed.add_field(name="🤖 Bots", value=f"{bots}", inline=True)
    embed.add_field(name="🟢 Online", value=f"{online}", inline=True)
    embed.add_field(name="🔴 Offline", value=f"{offline}", inline=True)
    embed.add_field(name="🔊 Em Voz", value=f"{em_voz}", inline=True)
    embed.add_field(name="💎 Boosters", value=f"{boosters}", inline=True)

    embed.set_footer(text=f"Servidor: {guild.name}")
    
    painel = await pegar_painel(canal)
    await painel.edit(content=None, embed=embed)

    if mensagens_stats is None:
        msg = await canal.send(embed=embed)
        mensagens_stats = msg.id
    else:
        msg = await canal.fetch_message(mensagens_stats)
        await msg.edit(embed=embed)


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