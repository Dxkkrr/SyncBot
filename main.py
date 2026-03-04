import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import yt_dlp
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(override=False)

TOKEN = os.getenv("TOKEN")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if TOKEN is None:
    raise ValueError("TOKEN não encontrada no arquivo .env")

# Configuração do Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}
FFMPEG_OPTIONS = {'options': '-vn'}

queue = {}

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

#Música
async def play_next(guild: discord.Guild):
    if guild.id not in queue or not queue[guild.id]:
        if guild.voice_client:
            await guild.voice_client.disconnect()
            return
        
    query = queue[guild.id].pop(0)

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        url = info['url']
    
    source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)

    guild.voice_client.play(
        source,
        after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next(guild),
            bot.loop
        )
    )

@bot.tree.command(name="play", description="Tocar uma música do YouTube ou Spotify na Call")
async def play(interaction: discord.Interaction, musica: str):
    await interaction.response.defer()

    if not interaction.user.voice:
        return await interaction.followup.send("Entre em um canal de voz primeiro!")
    
    canal = interaction.user.voice.channel

    if not interaction.guild.voice_client:
        await canal.connect()

    if interaction.guild.id not in queue:
        queue[interaction.guild.id] = []

#Se for música do Spotify
    if "spotify.com" in musica:
        track = sp.track(musica)
        musica = f"{track['name']} {track['artists'][0]['name']}"

    queue[interaction.guild.id].append(musica)

#Adicionando música à fila e colocando para tocar se não tiver nada tocando
    if not interaction.guild.voice_client.is_playing():
        await play_next(interaction.guild)

    await interaction.followup.send(f"Adicionado à fila: {musica}")


#Pulando Músicas
@bot.tree.command(name="skip", description="Pular a música atual")
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Música pulada!")


#Mostrando a fila de músicas
@bot.tree.command(name="queue", description="Mostrar a fila de músicas")
async def show_queue(interaction: discord.Interaction):
    if interaction.guild.id not in queue or not queue[interaction.guild.id]:
        return await interaction.response.send_message("A fila está vazia!")
    
    lista = "\n".join(queue[interaction.guild.id])
    await interaction.response.send_message(f"Fila de músicas:\n{lista}")

#Desconectando o Bot Automaticamente caso fique sozinho na Call
@bot.event
async def on_voice_state_update(member, before, after):
    voice = member.guild.voice_client
    if voice and len(voice.channel.members) == 1:
        await voice.disconnect()

#TOKEN .env do BOT
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN não encontrada no arquivo .env")

bot.run(TOKEN)