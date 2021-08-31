
import discord
import random
from captcha.image import ImageCaptcha
from discord.utils import get
import os

client = discord.Client()
token = ""
prefix = ""

@client.event
async def on_ready():
    print("=====================================\n봇이 로그인 및 실행 되었습니다.\n=====================================\n[봇정보]\nID : {}\nNAME : {}\n=====================================".format(client.user.id, client.user.name))
    await client.change_presence(status=discord.Status.online, activity=discord.Game("!help"))


@client.event #인증
async def on_message(message):
        if message.content.startswith("!인증"):
            Image_Captcha = ImageCaptcha()
            a = ""
            for i in range(6):
                a += str(random.randint(0, 9))

            name = str(message.author.id) + ".captcha.png"
            Image_Captcha.write(a, name)

            embed = discord.Embed(description="{}님, [**__숫자ㅣ6자리ㅣ60초__**]".format(message.author.mention), color=0x36393F)
            embed.set_author(name="{}님, 아래 인증번호 6자리를 숫자로만 60초 이내 입력해 주세요!".format(message.author), icon_url="https://cdn.discordapp.com/emojis/837825273793740832.gif?v=1")
            embed.set_image(url="https://cdn.discordapp.com/attachments/840193854447550484/{message.author.id}.captcha.png")
            await message.channel.send(embed=embed)

            await message.channel.send(file=discord.File(name))
            def check(msg):
                return msg.author == message.author and msg.channel == message.channel

            try:
                msg = await client.wait_for("message", timeout=60, check=check)

            except: #시간 초과
                embed = discord.Embed(description="<a:Load_gif:833555877402378260> 인증 시간이 초과되어, 인증이 취소 되었습니다.", color=0xFCB801)
                await message.channel.send(embed=embed)
                
                embed = discord.Embed(description="<a:Load_gif:833555877402378260> {}님, 인증에 실패 하였습니다. 다시시도 해주세요!".format(message.author.mention), color=0xFCB801)
                await message.author.send(embed=embed)

                return
            
            if msg.content == a: #인증 완료
                embed = discord.Embed(description="<a:Success_gif:833555731101909002> 인증이 완료 되었습니다. 5초뒤에 유저 역할을 지급 합니다.", color=0x43B481)
                await message.channel.send(embed=embed)



                embed = discord.Embed(description="<a:Success_gif:833555731101909002> {}님, 인증이 완료 되었습니다. 5초뒤에 유저 역할을 지급 합니다.".format(message.author.mention), color=0x43B481)
                await message.author.send(embed=embed)



                await asyncio.sleep(5)
                await message.author.add_roles(get(message.author.guild.roles, name="유저"))

            else: #인증 실패
                embed = discord.Embed(description="<a:Error_gif:833555812156309525> 인증 번호 6자리가 일치하지 않습니다. `!인증` 다시시도 해주세요!", color=0xF04947)
                await message.channel.send(embed=embed)

                embed = discord.Embed(description="<a:Error_gif:833555812156309525> {}님, 인증에 실패 하였습니다. 다시시도 해주세요!".format(message.author.mention), color=0xF04947)
                await message.author.send(embed=embed)
 
 
my_secret = os.environ['TOKEN']               
client.run(my_secret)