import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Comandos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ola_mundo", description="Ola Querido Mundo!")
    async def olamundo(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            f"Ola {interaction.user.mention}!"
        )

    # MUTE
    @app_commands.command(name="mute", description="Silenciar um membro")
    @app_commands.describe(
        membro="Usuário que será silenciado",
        tempo="Tempo em minutos (0 = permanente)",
        motivo="Motivo do mute"
    )
    async def mute(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        tempo: int,
        motivo: str = "Nenhum motivo informado"
    ):

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ | Sem permissão.", ephemeral=True)
            return

        # PERMANENTE
        if tempo == 0:

            cargo_mute = discord.utils.get(interaction.guild.roles, name="Mutado")

            if cargo_mute is None:

                cargo_mute = await interaction.guild.create_role(name="Mutado")

                for canal in interaction.guild.channels:
                    await canal.set_permissions(
                        cargo_mute,
                        send_messages=False,
                        speak=False
                    )

            await membro.add_roles(cargo_mute)

            await interaction.response.send_message(
                f"🔇 | {membro.mention} foi silenciado permanentemente.\nMotivo: {motivo}"
            )

        # TEMPORÁRIO
        else:

            duracao = timedelta(minutes=tempo)

            await membro.timeout(duracao, reason=motivo)

            await interaction.response.send_message(
                f"🔇 | {membro.mention} foi silenciado por **{tempo} minutos**.\nMotivo: {motivo}"
            )

    # UNMUTE
    @app_commands.command(name="unmute", description="Unmute")
    async def unmute(self, interaction: discord.Interaction, membro: discord.Member):

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ | Sem permissão.", ephemeral=True)
            return

        cargo = discord.utils.get(interaction.guild.roles, name="Mutado")

        if cargo and cargo in membro.roles:
            await membro.remove_roles(cargo)

        await membro.timeout(None)

        await interaction.response.send_message(
            f"🔊 | {membro.mention} foi desmutado."
        )

    # BAN
    @app_commands.command(name="ban", description="Banir membro")
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ | Sem permissão.", ephemeral=True)
            return

        await membro.ban(reason=motivo)

        await interaction.response.send_message(
            f"🔨 | {membro.mention} foi banido.\nMotivo: {motivo}"
        )

    # KICK
    @app_commands.command(name="kick", description="Expulsar membro")
    async def kick(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):

        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ | Sem permissão.", ephemeral=True)
            return

        await membro.kick(reason=motivo)

        await interaction.response.send_message(
            f"👢 | {membro.mention} foi expulso.\nMotivo: {motivo}"
        )

    # WARN
    @app_commands.command(name="warn", description="Punir membro")
    async def warn(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ | Sem permissão.", ephemeral=True)
            return

        try:
            await membro.send(
                f"⚠️ Você recebeu um aviso no servidor **{interaction.guild.name}**.\nMotivo: {motivo}"
            )
        except:
            pass

        await interaction.response.send_message(
            f"⚠️ {membro.mention} recebeu um aviso.\nMotivo: {motivo}"
        )


async def setup(bot):
    await bot.add_cog(Comandos(bot))