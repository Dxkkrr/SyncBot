import discord

canal_contador = 1479641366689485011

async def pegar_painel(canal):

    async for msg in canal.history(limit=10):
        if msg.author == canal.guild.me and msg.embeds:
            return msg

    return await canal.send("Carregando estatísticas...")

async def atualizar_painel(bot, guild):

    canal = bot.get_channel(canal_contador)

    total_membros = guild.member_count
    bots = len([m for m in guild.members if m.bot])
    membros = total_membros - bots
    online = len([m for m in guild.members if m.status != discord.Status.offline])
    offline = total_membros - online
    em_voz = len([m for m in guild.members if m.voice])
    boosters = guild.premium_subscription_count

    await canal.edit(name=f"📊 membros-{total_membros}")

    embed = discord.Embed(
        title="📊 Estatísticas do Servidor",
        color=discord.Color.blue()
    )

    embed.add_field(name="👥 Total", value=total_membros)
    embed.add_field(name="🧑 Usuários", value=membros)
    embed.add_field(name="🤖 Bots", value=bots)
    embed.add_field(name="🟢 Online", value=online)
    embed.add_field(name="🔴 Offline", value=offline)
    embed.add_field(name="🔊 Em Voz", value=em_voz)
    embed.add_field(name="💎 Boosters", value=boosters)

    embed.set_footer(text=f"Servidor: {guild.name}")

    painel = await pegar_painel(canal)

    await painel.edit(content=None, embed=embed)