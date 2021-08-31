
import discord
from captcha.image import ImageCaptcha
from discord.ext import commands
import string, asyncio, random
from discord.utils import get

class captch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def captch(self, message):
        if message.content == "!인증":
            Image_Captcha = ImageCaptcha()
            a = ""
            for i in range(6):
                a += str(random.randint(0, 9))

            name = str(message.author.id) + ".captcha.png"
            Image_Captcha.write(a, name)

            embed = discord.Embed(description=f"{message.author.mention}님, 아래 인증번호 6자리를 숫자로만 60초 이내 입력해 주세요!")
            embed.set_image(url="https://cdn.discordapp.com/attachments/840193854447550484/{message.author.id}.captcha.png")
            await message.channel.send(embed=embed)

            await message.channel.send(file=discord.File(name))
            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)

            except: #시간 초과
                embed = discord.Embed(description="<:outage:844070172675538945> 인증 시간이 초과되어, 인증이 취소 되었습니다.", color=0xFCB801)
                await message.channel.send(embed=embed)
                return

            if msg.content == a: #인증 완료
                embed = discord.Embed(description="<a:Success_gif:833555731101909002> 인증이 완료 되었습니다. 5초뒤에 역할을 지급 합니다.", color=0x43B481)
                await message.channel.send(embed=embed)

                await asyncio.sleep(5)
                await message.author.add_roles(get(message.author.guild.roles, name="CaptchaVerified"))

            else: #인증 실패
                embed = discord.Embed(description="<a:Error_gif:833555812156309525> 인증 번호 6자리가 일치하지 않습니다. `!인증` 다시시도 해주세요!", color=0xF04947)
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(captch(bot))
    print('cogs - `captch` is loaded')
