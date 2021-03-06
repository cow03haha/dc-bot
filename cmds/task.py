import asyncio
import datetime
import json

import discord
import pytz

from cores.classes import Cog_Extension


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        '''
        async def interval():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(741685158335479950)
            while not self.bot.is_closed():
                await self.channel.send('loop test')
                await asyncio.sleep(5)
            
        self.bg_task = self.bot.loop.create_task(interval())
        '''

        # self.counter = 0

        async def daily_check():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%H%M%S')

                if now_time == "000000":
                    guild = self.bot.get_guild(743292989790748812)

                    channel = self.bot.get_channel(743768856853479525)
                    notice = await channel.send("結算中...")

                    channel = self.bot.get_channel(753543338006806528)
                    role = guild.get_role(743292989790748812)
                    msg = await channel.send("結算中...")
                    await channel.set_permissions(role, send_messages=False)

                    with open('members.json', 'r', encoding='utf8') as bcfile:
                        bcdata = json.load(bcfile)

                    for i in bcdata["member_id"]:
                        if not bcdata[f'{i}']["today"]:
                            bcdata[f'{i}']["total"] = 0
                            with open('members.json', 'w', encoding='utf8') as bcfile:
                                json.dump(bcdata, bcfile, indent=4)
                        else:
                            bcdata[f'{i}']["today"] = False
                            with open('members.json', 'w', encoding='utf8') as bcfile:
                                json.dump(bcdata, bcfile, indent=4)

                        if bcdata[f'{i}']["total"] < 3 and bcdata[f'{i}']["custom_role"] \
                                and not bcdata[f'{i}']["remain"]:
                            member = guild.get_member(i)
                            role = guild.get_role(bcdata[f'{i}']["custom_role"])
                            await member.remove_roles(role)
                        elif bcdata[f'{i}']["total"] >= 3 and bcdata[f'{i}']["custom_role"]:
                            member = guild.get_member(i)
                            role = guild.get_role(bcdata[f'{i}']["custom_role"])
                            await member.add_roles(role)

                        if bcdata[f'{i}']["total"] >= 14:
                            bcdata[f'{i}']["remain"] = True
                            with open('members.json', 'w', encoding='utf8') as bcfile:
                                json.dump(bcdata, bcfile, indent=4)

                    await msg.delete()
                    role = guild.get_role(743292989790748812)
                    await channel.set_permissions(role, send_messages=None)

                    await notice.edit(content="結算成功!", delete_after=60)

                    await asyncio.sleep(60)
                else:
                    await asyncio.sleep(1)
                    pass

        self.bg_task = self.bot.loop.create_task(daily_check())

        async def reminder():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%H%M%S')

                with open('members.json', 'r', encoding='utf8') as bcfile:
                    bcdata = json.load(bcfile)

                if now_time in bcdata["remind_time"]:
                    for i in bcdata["member_id"]:
                        if "remind_list" in bcdata[f'{i}']:
                            user = self.bot.get_user(i)
                            cow = self.bot.get_user(315414910689476609)
                            tw = pytz.timezone('Asia/Taipei')
                            k = 0
                            embed = discord.Embed(title="備忘錄", color=0xf5ed00, timestamp=datetime.datetime.now(tz=tw))
                            embed.set_author(name=cow.name, icon_url=str(cow.avatar_url))
                            embed.set_thumbnail(url=str(self.bot.user.avatar_url))

                            for j in bcdata[f'{i}']["remind_list"]:
                                k += 1
                                embed.add_field(name=str(k), value=j, inline=True)

                            await user.send(embed=embed)

                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    pass

        self.bg_task = self.bot.loop.create_task(reminder())

        '''
        async def fight_task():
            await self.bot.wait_until_ready()

            with open('settings.json', 'r', encoding='utf8') as bcfile:
                bcdata =json.load(bcfile)
            self.guild = self.bot.get_guild(int(bcdata['fight_guild']))
            self.channel = self.guild.get_channel(int(bcdata['fight_channel']))
            self.role = self.guild.get_role(743668426383294495)
            
            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%m%d%H%M')
                
                with open('settings.json', 'r', encoding='utf8') as bcfile:
                    bcdata = json.load(bcfile)
                
                if now_time == bcdata['end_time'] and bcdata['fight_counter'] == '0':
                    now_time = datetime.datetime.now().strftime('%m-%d %H:%M')
                    await self.channel.send(f'內戰已於{now_time}截止報名')

                    with open('settings.json', 'r', encoding='utf8') as bcfile:
                        bcdata =json.load(bcfile)
                    bcdata['fight_counter'] = '1'
                    bcdata['fight_process'] = '0'
                    bcdata['end_time'] = '0'
                    with open('settings.json', 'w', encoding='utf8') as bcfile:
                        json.dump(bcdata, bcfile, indent=4)

                    await self.channel.send('開始隨機分組...')

                    with open('settings.json', 'r', encoding='utf8') as bcfile:
                        bcdata =json.load(bcfile)
                    users = self.role.members
                    bcdata['fight_users'] = str(users.id)
                    with open('settings.json', 'w', encoding='utf8') as bcfile:
                        json.dump(bcdata, bcfile, indent=4)

                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    pass

            self.bg_task = self.bot.loop.create_task(fight_task())
        '''

    '''
    @commands.command()
    async def set_channel(self, ctx, ch: int):
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f'{self.channel.mention} 的排程設定成功')
    
    @commands.command()
    async def set_time(self,ctx ,time):
        self.counter = 0
 
        with open('settings.json', 'r', encoding='utf8') as bcfile:
            bcdata =json.load(bcfile)

        bcdata['task_time'] = time

        with open('settings.json', 'w', encoding='utf8') as bcfile:
            json.dump(bcdata, bcfile, indent=4)
    '''


def setup(bot):
    bot.add_cog(Task(bot))
