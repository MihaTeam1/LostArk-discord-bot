import discord
import time
import datetime
from discord.ext import commands
import events

TOKEN = 'NjYyMzgwOTUyMTk4MTg0OTk3.Xg5IeA.HH5MzC7D0jqbVrzcW401ZPc-yto'
bot = commands.Bot(command_prefix='!')
DEBUG_MODE = True

msg = {
	"1":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["monday"]
	],
	"2":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["tuesday"]
	],
	"3":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["wednesday"]
	],
	"4":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["thursday"]
	],
	"5":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["friday"]
	],
	"6":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["saturday"]
	],
	"7":[
		[datetime.time(hour=t[0], minute=t[1], second=0, microsecond=0), msg, True]
		for t, msg in events.events["sunday"]
	],
}

def time_comp(obj, now, subt=0):
	cond = datetime.datetime.combine(datetime.date(now.year,now.month,now.day), obj) >= now
	obj = datetime.datetime.combine(datetime.date(now.year,now.month,now.day), obj) - datetime.timedelta(minutes=subt)
	return obj <= now and cond

def week(day):
	if day == 8:
		return 1
	else:
		return day

@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def start(ctx):  # создаем асинхронную фунцию бота
	templates = []
	flag = True
	while True:

		now = datetime.datetime.today().now()
		now = datetime.datetime(
				now.year,
				now.month,
				now.day,
				now.hour,
				now.minute,
			)

		if flag:
			now_day = (now.day, datetime.datetime.today().isoweekday())

		if now.day != now_day[0]:
			flag = False
			for i in msg[now_day[1]]:
				i[2] = True
		now_day = (now.day, datetime.datetime.today().isoweekday())


		for i in msg[str(datetime.datetime.today().isoweekday())]:
			if time_comp(i[0], now, 20):
				if i not in templates and i[2]:
					i[2] = False
					templates.append(i)
					await ctx.send("Через {} будет доступно {} {}".format(
						datetime.datetime.combine(datetime.date(now.year,now.month,now.day), i[0]) -  now,
						i[1][0],
						i[1][1]))

		if datetime.datetime.today().now().time() >= datetime.time(hour=23,minute=50):
			for i in msg[str(week(datetime.datetime.today().isoweekday()+1))]:
				if i[0][0] == 0:
					if time_comp(i[0], now, 20):
						if i not in templates and i[2]:
							i[2] = False
							templates.append(i)
							await ctx.send("{} осталось до {} {}".format(
								datetime.datetime.combine(datetime.date(now.year,now.month,now.day), i[0]) -  now,
								i[1][0], i[1][1]))


		for i in templates:
			if time_comp(i[0], now):
				templates.remove(i)
				await ctx.send("{} сейчас доступнен {}".format(i[1][0], i[1][1]))
		time.sleep(10)




bot.run(TOKEN)
