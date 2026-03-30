import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Mute
    @app_commands.command(name="mute", description="Silenciar um membro")
    async def mute(self, interaction: discord.Interaction, membro: discord.Member, tempo: int, motivo: str = "Nenhum motivo informado"):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        if tempo == 0:
            cargo_mute = discord.utils.get(interaction.guild.roles, name="Mutado")

            if cargo_mute is None:
                cargo_mute = await interaction.guild.create_role(name="Mutado")
                for canal in interaction.guild.channels:
                    await canal.set_permissions(cargo_mute, send_messages=False, speak=False)

            await membro.add_roles(cargo_mute)
            await interaction.followup.send(f"🔇 | {membro.mention} foi silenciado permanentemente.\nMotivo: {motivo}")
        else:
            await membro.timeout(timedelta(minutes=tempo), reason=motivo)
            await interaction.followup.send(f"🔇 | {membro.mention} foi silenciado por {tempo} minutos.\nMotivo: {motivo}")

# Unmute
    @app_commands.command(name="unmute", description="Remover mute")
    async def unmute(self, interaction: discord.Interaction, membro: discord.Member):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        cargo = discord.utils.get(interaction.guild.roles, name="Mutado")

        if cargo and cargo in membro.roles:
            await membro.remove_roles(cargo)

        await membro.timeout(None)
        await interaction.followup.send(f"🔊 | {membro.mention} foi desmutado.")

# Ban
    @app_commands.command(name="ban", description="Banir membro")
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.ban_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        await membro.ban(reason=motivo)
        await interaction.followup.send(f"🔨 | {membro.mention} foi banido.\nMotivo: {motivo}")

# Kick
    @app_commands.command(name="kick", description="Expulsar membro")
    async def kick(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.kick_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        await membro.kick(reason=motivo)
        await interaction.followup.send(f"👢 | {membro.mention} foi expulso.\nMotivo: {motivo}")

# Warn
    @app_commands.command(name="warn", description="Advertir membro")
    async def warn(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):
        await interaction.response.defer()

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        try:
            await membro.send(f"⚠️ Você recebeu um aviso no servidor **{interaction.guild.name}**.\nMotivo: {motivo}")
        except:
            pass

        await interaction.followup.send(f"⚠️ {membro.mention} recebeu um aviso.\nMotivo: {motivo}")

async def setup(bot):
    await bot.add_cog(Moderacao(bot))