import discord
from discord.ext import commands
import re

class AntiLink(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # cargos que podem enviar links
        self.cargos_permitidos = [
            1477420560223830081, #Idfc
            1477420737072730244, #Founder
            1477488180424081550, #Dono
            1478041134902018099, #Dev
            1477488029370159217, #Admin
            
            # ID do cargo staff
        ]

        # domínios permitidos
        self.dominios_permitidos = [
            "youtube.com",
            "youtu.be",
            "github.com"
        ]

        # regex para detectar links
        self.link_regex = re.compile(
            r"(https?://|www\.|discord\.gg/|discord\.com/invite/|bit\.ly|tinyurl|t\.co)",
            re.IGNORECASE
        )

        self.canal_logs = 1477454537907372202  # ID do canal de logs

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not self.link_regex.search(message.content):
            return

        # verificar whitelist de cargos
        for cargo in message.author.roles:
            if cargo.id in self.cargos_permitidos:
                return

        # verificar domínios permitidos
        for dominio in self.dominios_permitidos:
            if dominio in message.content.lower():
                return

        try:
            await message.delete()
        except:
            pass

        try:
            await message.channel.send(
                f"{message.author.mention} links não são permitidos neste servidor.",
                delete_after=5
            )
        except:
            pass

        canal_logs = self.bot.get_channel(self.canal_logs)

        if canal_logs:
            embed = discord.Embed(
                title="🚫 Link bloqueado",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Usuário",
                value=message.author.mention
            )

            embed.add_field(
                name="Canal",
                value=message.channel.mention
            )

            embed.add_field(
                name="Mensagem",
                value=message.content[:1000],
                inline=False
            )

            await canal_logs.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntiLink(bot))