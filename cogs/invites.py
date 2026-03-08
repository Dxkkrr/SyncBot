import discord
from discord.ext import commands

invites = {}

class Invites(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        for guild in self.bot.guilds:
            invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        canal_invites = self.bot.get_channel(1477703820703170570)
        canal_regras = self.bot.get_channel(1477396107339370576)

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

async def setup(bot):
    await bot.add_cog(Invites(bot))