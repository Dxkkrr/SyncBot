import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Comandos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

# Comando de Teste do Bot
    @app_commands.command(name="ola_mundo", description="Ola Querido Mundo!")

    async def olamundo(self, interaction: discord.Interaction):

        # ALTERAÇÃO: evitar erro "Aplicativo não respondeu"
        await interaction.response.defer()

        await interaction.followup.send(
            f"Ola {interaction.user.mention}!"
        )
# Mute
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

        await interaction.response.defer()

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return


        # PermaMute
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

            await interaction.followup.send(
                f"🔇 | {membro.mention} foi silenciado permanentemente.\nMotivo: {motivo}"
            )


        # Mute Temporário
        else:

            duracao = timedelta(minutes=tempo)

            await membro.timeout(duracao, reason=motivo)

            await interaction.followup.send(
                f"🔇 | {membro.mention} foi silenciado por **{tempo} minutos**.\nMotivo: {motivo}"
            )

# Desmutar
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

        await interaction.followup.send(
            f"🔊 | {membro.mention} foi desmutado."
        )

# Ban
    @app_commands.command(name="ban", description="Banir membro")

    async def ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):

        await interaction.response.defer()

        if not interaction.user.guild_permissions.ban_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        await membro.ban(reason=motivo)

        await interaction.followup.send(
            f"🔨 | {membro.mention} foi banido.\nMotivo: {motivo}"
        )
        
# Kick
    @app_commands.command(name="kick", description="Expulsar membro")

    async def kick(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):

        await interaction.response.defer()

        if not interaction.user.guild_permissions.kick_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        await membro.kick(reason=motivo)

        await interaction.followup.send(
            f"👢 | {membro.mention} foi expulso.\nMotivo: {motivo}"
        )

# Warn
    @app_commands.command(name="warn", description="Advertir membro")

    async def warn(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo"):

        await interaction.response.defer()

        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        try:
            await membro.send(
                f"⚠️ Você recebeu um aviso no servidor **{interaction.guild.name}**.\nMotivo: {motivo}"
            )
        except:
            pass

        await interaction.followup.send(
            f"⚠️ {membro.mention} recebeu um aviso.\nMotivo: {motivo}"
        )

# Clear ( Mensagens )
    @app_commands.command(name="clear", description="Apagar mensagens")
    @app_commands.describe(amount="Quantidade de mensagens (1-100)")

    async def clear(self, interaction: discord.Interaction, amount: int):

        await interaction.response.defer(ephemeral=True)

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.followup.send("❌ | Sem permissão.")
            return

        if amount < 1 or amount > 100:
            await interaction.followup.send("⚠️ Quantidade inválida (1-100).")
            return

        await interaction.channel.purge(limit=amount)

        await interaction.followup.send(
            f"🧹 | {amount} mensagens apagadas."
        )

# Lock ( Mensagens )
    @app_commands.command(name="lock", description="Bloquear chat")

    async def lock(self, interaction: discord.Interaction):

        await interaction.response.defer()

        if not interaction.user.guild_permissions.manage_channels:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=False
        )

        await interaction.followup.send("🔒 | Chat bloqueado.")

# Unlock ( Mensagens )
    @app_commands.command(name="unlock", description="Desbloquear chat")

    async def unlock(self, interaction: discord.Interaction):

        await interaction.response.defer()

        if not interaction.user.guild_permissions.manage_channels:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=True
        )

        await interaction.followup.send("🔓 | Chat desbloqueado.")

# Avisos & Anuncios
    @app_commands.command(name="anunciar", description="Enviar anúncio")

    @app_commands.describe(
        tipo="Tipo do anúncio",
        mensagem="Mensagem do anúncio"
    )

    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Lives", value="lives"),
            app_commands.Choice(name="Anuncio Comum", value="comum"),
            app_commands.Choice(name="Servidor Parceiro", value="parceiro")
        ]
    )

    async def anunciar(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str],
        mensagem: str
    ):

        await interaction.response.defer()

        if not interaction.user.guild_permissions.manage_messages:
            await interaction.followup.send("❌ | Sem permissão.", ephemeral=True)
            return


        if tipo.value == "lives":

            await interaction.channel.send(
                f"@everyone 🔴 **LIVE AGORA**\n{mensagem}"
            )


        elif tipo.value == "comum":

            await interaction.channel.send(
                f"@everyone\n📢 **MENSAGEM ENVIADA POR:** {interaction.user.mention}\n\n{mensagem}"
            )


        elif tipo.value == "parceiro":

            await interaction.channel.send(mensagem)


        await interaction.followup.send("✅ | Anúncio enviado.", ephemeral=True)
        
# Adição de Cargos Pelo comando

    @app_commands.command(name="addcargo", description="Adicionar Cargo")
    @app_commands.describe(membro="Usuario", cargo="Cargo que vai ser adicionado")
    
    async def addcargo(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        cargo: discord.Role
    ):
        await interaction.response.defer(ephemeral=True)
        
#Permissão do Usuário
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.followup.send("❌ | Você não tem permissão para gerenciar cargos", ephemeral=True)
            return
        
# Permissão do Bot
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.followup.send("❌ | Eu não tenho permissão para gerenciar cargos", ephemeral=True)
            return
        
# Hierarquia do Bot
        if cargo >= interaction.guild.me.top_role:
            await interaction.followup.send("❌ | Não posso adicionar este cargo ( Ele está acima do meu )", ephemeral=True)
            return
        
# Hierarquia do usuário
        if cargo >= interaction.user.top_role:
            await interaction.followup.send("❌ | Você não pode adicionar um cargo maior ou igual ao seu")
            return
        
        try:
            await membro.add_roles(cargo)
            
            await interaction.followup.send(f"✅ | Cargo {cargo.mention} adicionado a {membro.mention}.")
        
        except Exception as e:
            await interaction.followup.send(f"❌ | Erro ao adicionar cargo: {e}")

async def setup(bot):
    await bot.add_cog(Comandos(bot))