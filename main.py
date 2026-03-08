import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

class SyncBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='$', intents=intents)

    async def setup_hook(self):
        print("Carregando cogs...")

        for arquivo in os.listdir('cogs'):
            if arquivo.endswith('.py') and arquivo != '__init__.py':
                try:
                    await self.load_extension(f'cogs.{arquivo[:-3]}')
                    print(f'Cog {arquivo} carregado')
                except Exception as e:
                    print(f'Erro ao carregar {arquivo}: {e}')

        await self.tree.sync()
        print("Comandos sincronizados!")

bot = SyncBot()

@bot.event
async def on_ready():
    print(f"O bot {bot.user} está Ligado!")

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("O token do bot não foi encontrado. Verifique a variável TOKEN no Railway ou no .env.")

bot.run(TOKEN)