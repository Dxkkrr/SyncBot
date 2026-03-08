import discord
from discord.ext import commands

class Comandos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ola_mundo", description="Ola Querido Mundo!")
    async def olamundo(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            f"Ola {interaction.user.mention}!"
        )

async def setup(bot):
    await bot.add_cog(Comandos(bot))