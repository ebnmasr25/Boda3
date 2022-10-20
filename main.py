from pyrogram import *
from pyrogram.types import *
from yt_dlp import YoutubeDL
from requests import get
from youtube_search import YoutubeSearch
import os, wget
from pytube import YouTube
import yt_dlp
import asyncio
import re
from pyrogram.errors import *
import requests
import pyshorteners
from googlesearch import search
from pyshorteners.shorteners import tinyurl	
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
MONGO = "mongodb+srv://ebnmasr:Aaee1122##@clustering0.bew52zk.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(MONGO)
mongodb = mongo.bot
usersdb = mongodb.users
OWNER = 5701042002

async def is_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True
    
async def get_users() -> list:
 	users_list = []
 	async for user in usersdb.find({"user_id": {"$gt": 0}}):
 	  users_list.append(user)
 	return users_list
    
async def add_user(user_id: int):
    is_served = await is_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})   
    
NEW_MEMBER = """
♡• 
مرحبا بك دخل شخص جديد الي الروبوت .

- Name : {} 
- ID : {}

- Users : {} 

✦✧✦✧✦✧
"""
api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
token = os.environ.get("TOKEN")


app = Client(
	"ytui",
	api_id=api_id,
	api_hash=api_hash,
	bot_token=token
	)
app_token = token
CHANNEL = "pyth_on3"

photo = 'https://telegra.ph/file/3334192903ea1011165c8.jpg'

TEXT = """**مرحبا بك {} **

من خلال هذا البوت يمكنك تحميل الاغاني والفيديوهات بكل سهوله 

- كل ما عليك هو ارسال اسم الاغنيه او الفيديو  .

- يمكنك البحث عن طريق ( بحث + اسم الاغنيه )  .

- يمكنك التحميل بثلاث طرق ( اسم الاغنيه فقط / تحميل + اسم الاغنيه / رابط مقطع من يوتيوب ) .

- يمكنك البحث في جوجل عن طريق كتابه الامر ( جوجل + الي عاوز تبحث عنو ) .

- يمكنك البحث ايضاا والتحميل عن طريق الضغط علي الايي اسفل كل بحث .

**- Dev : {} **"""

@app.on_message(filters.command('start'))
async def st(client,message):
	m = message.chat.id
	user = message.from_user.mention
	if message.from_user.id != OWNER:
		user_id = message.from_user.id
		if not await is_user(user_id=user_id):
			await add_user(user_id=user_id)
			a = message.from_user.mention
			b = message.from_user.id
			c = len(await get_users())
			await app.send_message(
			OWNER,
			NEW_MEMBER.format(a,b,c)
			)
		await message.delete()
		x = (await app.get_users(5701042002)).mention
		await app.send_photo(message.chat.id,
		photo=photo,
		caption=TEXT.format(message.from_user.mention,x),
		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Channel",url="https://t.me/pyth_on3"),InlineKeyboardButton("- Dev ",user_id=5701042002)],]))
	
		
@app.on_message(filters.command(['نسخه','نسخة','نسخه احتياطيه','نسخة احتياطية','احتياطيه','احتياطية'],prefixes="")&filters.user(OWNER))
async def getl(client,message):
	m = await message.reply("**prossing...**")
	filename = "@U_X3a-users.txt"
	with open(filename, "w+", encoding="utf8") as out_file:
		out_file.write(str(await get_users()))
	stats = len(await get_users())
	await app.send_document(
	message.chat.id,
	document=filename,
	caption="**users Stats {}".format(stats)
	)
	await m.delete()
	os.remove(filename)

USERS_BROADCAST = filters.command("broadcast_users") & filters.user(OWNER)
USERS_BROADCAST2 = filters.regex("اذاعة") & filters.user(OWNER)
@app.on_message(USERS_BROADCAST)
@app.on_message(USERS_BROADCAST2)
async def broadcast(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.id
        y = message.chat.id
        sent = 0
        users = []
        hah = await get_users()
        for user in hah:
            users.append(int(user["user_id"]))
        for i in users:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"تمت الاذاعه الي  {sent} User ! ")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**استخدم الامر بجوار الرساله التي تريد اذاعتها او قم بالرد علي رساله**"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    users = []
    hah = await get_users()
    for user in hah:
        users.append(int(user["user_id"]))
    for i in users:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"تمت الاذاعه الي  {sent} User !")
    
	
							
@app.on_message(filters.command("تحميل",[".",""]))
async def soenload_song(_,message):
	await message.delete()
	query = " ".join(message.command[1:])
	if not query:
		await app.send_message(message.chat.id,"** 📮 ¦ اعطني شيئ للبحث عنه ..**")
		return
	m = await message.reply("**🔄 Searching.... {}**.".format(query))
	await app.send_message(
	-1001567683610,
	"**New Search From {} && Id Is : {}\n\nSearch - > {}".format(message.from_user.mention,message.from_user.id,query)
	)
	results = YoutubeSearch(query, max_results=1).to_dict()
	link = f"https://youtube.com{results[0]['url_suffix']}"
	yt = YouTube(link)
	photo = yt.thumbnail_url
	ti = yt.title
	jk = yt.embed_url
	await m.delete()
	x = (await app.get_users(5701042002)).mention
	await app.send_photo(
	message.chat.id,
	photo=photo,
	caption="- Title : {} \n\n** By : {} .\n\n- Link ¦ {}**".format(ti,x,jk),
	reply_markup=InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton("تحميل صوت 🔊",
			callback_data="audio"),
			InlineKeyboardButton("تحميل فيديو 🎥",
			callback_data='vedio')
		],
		[
			InlineKeyboardButton("اغلاق 🗑",
			callback_data='ex'
			)
		],
	]
))

@app.on_callback_query(filters.regex('audio'))
async def au(_,query:CallbackQuery):
	await query.edit_message_caption("**عزيزى {} \n\n♻️ ¦ جارى تحميل المقطع الصوتي ...**".format(query.from_user.mention),
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Channel ",
	url='https://t.me/pyth_on3')],]))
	try:
		url = query.message.caption.split("embed/",1)[1]
		with YoutubeDL(audio) as ytdl:
			ytdl_data = ytdl.extract_info(url, download=True)
			audio_file = ytdl.prepare_filename(ytdl_data)
			thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
	except Exception as e:
		x = (await app.get_users(5701042002)).mention
		await app.send_message(-1001567683610,"**{} \n\n هناك خطأ بالبوت ...\n\n {}".format(x,e))
		return await query.edit_message_caption("**حدث خطأ غير متوقع انتظر حل الخطأ ⚠️**")
	x3 = await query.edit_message_caption("**عزيزى {} \n\n♻️ ¦  جارى رفع المقطع الصوتي ...**".format(query.from_user.mention),
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Channel ",
	url='https://t.me/pyth_on3')],]))
	await app.send_audio(
	query.message.chat.id,
	audio=audio_file,
	duration=int(ytdl_data["duration"]),
      title=str(ytdl_data["title"]),
      performer=str(ytdl_data["uploader"]),
      file_name=str(ytdl_data["title"]),
      thumb=thumb,
      caption=f"[{ytdl_data['title']}]({url})",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Channel ",
	url='https://t.me/pyth_on3')],[InlineKeyboardButton("- Dev ",
	user_id=5701042002)],]))
	await x3.delete()
	

	
@app.on_callback_query(filters.regex('vedio'))
async def vidd(_,query:CallbackQuery):
	await query.edit_message_caption("**عزيزى {} \n\n♻️ ¦ جارى تحميل مقطع الفيديو **".format(query.from_user.mention),
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Channel ",
	url='https://t.me/pyth_on3')],]))
	try:
		url = query.message.caption.split("embed/",1)[1]
		with YoutubeDL(video) as ytdl:
			ytdl_data = ytdl.extract_info(url, download=True)
			video_file = ytdl.prepare_filename(ytdl_data)
	except Exception as e:
		x = (await app.get_users(5701042002)).mention
		await app.send_message(-1001567683610,"**{} \n\n هناك خطأ بالبوت ...\n\n {}".format(x,e))
		return await query.edit_message_caption("**حدث خطأ غير متوقع انتظر حل الخطأ ⚠️**")
	x3 = await query.edit_message_caption("**عزيزى {} \n\n ✅ ¦ جارى رفع مقطع الفيديو...**".format(query.from_user.mention),
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("- Channel ",
	url='https://t.me/pyth_on3')],]))
	await query.message.delete()
	await app.send_video(
	query.message.chat.id,
	video=video_file,
	duration=int(ytdl_data["duration"]),
	file_name=str(ytdl_data["title"]),
	supports_streaming=True,
	caption=f"- [{ytdl_data['title']}]({url})\n\n- By : **@pyth_on3**",
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Watch on youtube",url=f"https://www.youtube.com/watch?v={url}"),InlineKeyboardButton("- Channel",url='https://t.me/pyth_on3')],])
	)

@app.on_message(filters.command("بحث",[".",""]))
async def search(client,message):
	await message.delete()
	query = " ".join(message.command[1:])
	if not query:
		await app.send_message(message.chat.id,"** 📮 ¦ اعطني شيئ للبحث عنه ..**")
		return
	m = await message.reply("**🔄 Searching.... {}**.".format(query))
	results = YoutubeSearch(query,max_results=8).to_dict()
	i = 0
	text = ""
	while i < 8 :
		text += f"👤 {results[i]['title']}\n"
		text += f"🕑 {results[i]['duration']}\n"
		text += f"👁 {results[i]['views']}\n"
		text += f"🌐 {results[i]['channel']}\n"
		text += f"🔗 https://www.youtube.com{results[i]['url_suffix']}\n\n"
		text += f"📥 **Download : ** /{results[i]['id']}\n\n"
		text += f"**ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n\nــ**"
		i += 1
		await m.edit(text,disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اغلاق 🗑",
		callback_data='er')]]))
		

@app.on_callback_query(filters.regex('er'))
async def er(_,query:CallbackQuery):
	await query.message.delete()
	
@app.on_callback_query(filters.regex('ex'))
async def xr(_,query:CallbackQuery):
	await query.message.delete()
	
@app.on_message(filters.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
	msg = message.text
	await message.delete()
	await app.send_message(
	-1001567683610,
	"**New Search From {} && Id Is : {}\n\nSearch - > {}".format(message.from_user.mention,message.from_user.id,query)
	)
	await app.send_message(message.chat.id,"**📮 ¦ رابط المقطع ..\n\n{}".format(msg),reply_markup=InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton("تحميل صوت 🔊",
			callback_data="audio"),
			InlineKeyboardButton("تحميل فيديو 🎥",
			callback_data="vedio")
		],
		[
			InlineKeyboardButton("اغلاق 🗑",
			callback_data='ex'
			)
		],
		]
	),
	disable_web_page_preview=True
)

#@app.on_callback_query(filters.regex("aix"))
#async def aix(_,query:CallbackQuery):
#	
#	
@app.on_message(filters.command('جوجل',[".",""]))
async def google(client,message):
	await message.delete()
	msg = " ".join(message.command[1:])
	if not msg:
		await message.reply('**اعطني شيئ للبحث عنه ..**')
		return
		await app.send_message(
	-1001567683610,
	"**New Search From {} && Id Is : {}\n\nSearch - > {}".format(message.from_user.mention,message.from_user.id,query)
	)
		m = await message.reply("**🔄 Searching.... {}**.".format(msg))
	x = list(googlesearch.search(msg ,  num_results=10,  lang="ar") )
	ask1 = x[0]
	ask2 = x[1]
	ask3 = x[2]
	ask4 = x[3]
	ask5 = x[4]
	ask6 = x[5]
	ask7 = x[6]
	ask8 = x[7]
	ask9 = x[8]
	ask10 = x[9]
	buttons = InlineKeyboardMarkup([[
		InlineKeyboardButton("Result - 1",url=ask1),
		InlineKeyboardButton("Result - 2",url=ask2)],[
		InlineKeyboardButton('Result - 3',url=ask3)],[
		InlineKeyboardButton("Result - 4",url=ask4),
		InlineKeyboardButton("Result - 5",url=ask5)],[
		InlineKeyboardButton(" ",callback_data='4m')],[
		InlineKeyboardButton("◉Next◉",callback_data='next')],[
		InlineKeyboardButton("✨ Channel",url="https://t.me/pyth_on3"),
		InlineKeyboardButton("✨ Dev ",user_id=5701042002)]])
	buttons2 = InlineKeyboardMarkup([[
		InlineKeyboardButton("Result - 6",url=ask6),
		InlineKeyboardButton("Result - 7",url=ask7)],[
		InlineKeyboardButton("Result - 8",url=ask8)],[
		InlineKeyboardButton("Result - 9",url=ask9),
		InlineKeyboardButton("Result - 10",url=ask10)],[
		InlineKeyboardButton("Close 🗑", callback_data="closehere")],[
		InlineKeyboardButton("✨ Channel",url="https://r.me/pyth_on3"),
		InlineKeyboardButton("✨ Dev",user_id=5701042002)],])
	
	s = pyshorteners.Shortener()
	url1 = s.tinyurl.short(ask1)
	url2 = s.tinyurl.short(ask2)
	url3 = s.tinyurl.short(ask3)
	url4 = s.tinyurl.short(ask4)
	url5 = s.tinyurl.short(ask5)
	ph = 'https://telegra.ph/file/f4464254fc9ecfd415101.jpg'
	try:
		await m.delete()
		await message.reply_photo(ph,caption="**🖇 ¦ {}\n🖇 ¦ {}\n🖇 ¦ {}\n🖇 ¦ {}\n🖇 ¦ {}".format(url1,url2,url3,url4,url5),reply_markup=buttons)
	except Exception as e:
		await m.delete()
		await app.sen_message(message.chat.id,e)
	
@app.on_message(filters.text&filters.private)
async def any(client,message):
	query = message.text
	await message.delete()
	m = await message.reply("**🔄 Searching.... {}**.".format(query))
	await app.send_message(
	-1001567683610,
	"**New Search From {} && Id Is : {}\n\nSearch - > {}".format(message.from_user.mention,message.from_user.id,query)
	)
	results = YoutubeSearch(query, max_results=1).to_dict()
	link = f"https://youtube.com{results[0]['url_suffix']}"
	yt = YouTube(link)
	photo = yt.thumbnail_url
	ti = yt.title
	jk = yt.embed_url
	await m.delete()
	x = (await app.get_users(5701042002)).mention
	await app.send_photo(
	message.chat.id,
	photo=photo,
	caption="- Title : {} \n\n** By : {} .\n\n- Link ¦ {}**".format(ti,x,jk),
	reply_markup=InlineKeyboardMarkup(
	[
		[
			InlineKeyboardButton("تحميل صوت 🔊",
			callback_data="audio"),
			InlineKeyboardButton("تحميل فيديو 🎥",
			callback_data='vedio')
		],
		[
			InlineKeyboardButton("اغلاق 🗑",
			callback_data='ex'
			)
		],
	]
))


video = {"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}
audio = {"format": "bestaudio","keepvideo": False,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.mp3","quite": True}

app.run()
