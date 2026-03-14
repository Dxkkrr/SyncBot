import discord 
from discord.ext import commands
from cogs.status import atualizar_painel

class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

# Entrada de Membro no Servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):
        global entradas
        entradas += 1
        
        canal_bemvindo = self.bot.get_channel(1482274529098076250) #ID Bem-Vindos
        canal_regras = self.bot.get_channel(1477396107339370576) #ID Regras

        cargo = member.guild.get_role(1477447780979970058) #ID cargo Membro

        if cargo:
            await member.add_roles(cargo)

        if canal_bemvindo and canal_regras:
            await canal_bemvindo.send(f"👋 Bem Vindo {member.mention} ao Servidor! 👋\n"
                                    f"📖 Leia as regras no canal {canal_regras.mention} para evitar punições! 📖\n"
                                    f"👥 Atualmente temos **{member.guild.member_count}** de Membros no servidor 👥")
        
        await atualizar_painel(self.bot, member.guild)
        
        
# Saida de Membro do Servidor
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        
        canal_bemvindo = self.bot.get_channel(1482450659977592852) #ID Saídas
        if canal_bemvindo:
            await canal_bemvindo.send(f"{member.mention} saiu do servidor.")
            
        await atualizar_painel(self.bot, member.guild)
        
async def setup(bot):
    await bot.add_cog(Welcome(bot))