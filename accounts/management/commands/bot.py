from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        from discord.ext import commands
        from accounts.models import User
        
        print(User.objects.all())

        TOKEN = "ODE3NDQzNjIzMTEzMDY0NDY5.YEJlsw.KISnB2oN3Eyz4jHMj4LH6xmId1c"
        prefix = "!"

        bot = commands.Bot(command_prefix=prefix)

        @bot.event
        async def on_ready():
            print("Everything's all ready to go~")

        @bot.command()
        async def ping(ctx):
            await ctx.send("Pong!")

        bot.run(TOKEN)  # Where 'TOKEN' is your bot token