from helper.database import codeflixbots as db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import Txt

@Client.on_message(filters.command("metadata"))
async def metadata(client, message):
    user_id = message.from_user.id

    # Récupération des métadonnées depuis la base de données
    current = await db.get_metadata(user_id)
    title = await db.get_title(user_id)
    author = await db.get_author(user_id)
    artist = await db.get_artist(user_id)
    video = await db.get_video(user_id)
    audio = await db.get_audio(user_id)
    subtitle = await db.get_subtitle(user_id)

    # Affichage des métadonnées actuelles
    text = f"""
**㊋ Votre métadonnée est actuellement : {current}**

**◈ Titre ▹** `{title if title else 'Non défini'}`  
**◈ Auteur ▹** `{author if author else 'Non défini'}`  
**◈ Artiste ▹** `{artist if artist else 'Non défini'}`  
**◈ Audio ▹** `{audio if audio else 'Non défini'}`  
**◈ Sous-titre ▹** `{subtitle if subtitle else 'Non défini'}`  
**◈ Vidéo ▹** `{video if video else 'Non défini'}`  
    """

    # Boutons inline pour activer/désactiver
    buttons = [
        [
            InlineKeyboardButton(f"On{' ✅' if current == 'On' else ''}", callback_data='on_metadata'),
            InlineKeyboardButton(f"Off{' ✅' if current == 'Off' else ''}", callback_data='off_metadata')
        ],
        [
            InlineKeyboardButton("Comment configurer", callback_data="metainfo")
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await message.reply_text(text=text, reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex(r"on_metadata|off_metadata|metainfo"))
async def metadata_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    if data == "on_metadata":
        await db.set_metadata(user_id, "On")
    elif data == "off_metadata":
        await db.set_metadata(user_id, "Off")
    elif data == "metainfo":
        await query.message.edit_text(
            text=Txt.META_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Accueil", callback_data="home"),
                    InlineKeyboardButton("Fermer", callback_data="close")
                ]
            ])
        )
        return

    # Mise à jour après modification
    current = await db.get_metadata(user_id)
    title = await db.get_title(user_id)
    author = await db.get_author(user_id)
    artist = await db.get_artist(user_id)
    video = await db.get_video(user_id)
    audio = await db.get_audio(user_id)
    subtitle = await db.get_subtitle(user_id)

    # Message mis à jour
    text = f"""
**㊋ Votre métadonnée est actuellement : {current}**

**◈ Titre ▹** `{title if title else 'Non défini'}`  
**◈ Auteur ▹** `{author if author else 'Non défini'}`  
**◈ Artiste ▹** `{artist if artist else 'Non défini'}`  
**◈ Audio ▹** `{audio if audio else 'Non défini'}`  
**◈ Sous-titre ▹** `{subtitle if subtitle else 'Non défini'}`  
**◈ Vidéo ▹** `{video if video else 'Non défini'}`  
    """

    # Boutons mis à jour
    buttons = [
        [
            InlineKeyboardButton(f"On{' ✅' if current == 'On' else ''}", callback_data='on_metadata'),
            InlineKeyboardButton(f"Off{' ✅' if current == 'Off' else ''}", callback_data='off_metadata')
        ],
        [
            InlineKeyboardButton("Comment configurer", callback_data="metainfo")
        ]
    ]
    await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command('settitle'))
async def title(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Indiquez le titre\n\nExemple : /settitle Encodé par @@ZeeXDev**")
    title = message.text.split(" ", 1)[1]
    await db.set_title(message.from_user.id, title=title)
    await message.reply_text("**✅ Titre enregistré**")

@Client.on_message(filters.private & filters.command('setauthor'))
async def author(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Indiquez l'auteur\n\nExemple : /setauthor @@ZeeXDev**")
    author = message.text.split(" ", 1)[1]
    await db.set_author(message.from_user.id, author=author)
    await message.reply_text("**✅ Auteur enregistré**")

@Client.on_message(filters.private & filters.command('setartist'))
async def artist(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Indiquez l'artiste\n\nExemple : /setartist @@ZeeXDev**")
    artist = message.text.split(" ", 1)[1]
    await db.set_artist(message.from_user.id, artist=artist)
    await message.reply_text("**✅ Artiste enregistré**")

@Client.on_message(filters.private & filters.command('setaudio'))
async def audio(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Indiquez le titre audio\n\nExemple : /setaudio @@ZeeXDev**")
    audio = message.text.split(" ", 1)[1]
    await db.set_audio(message.from_user.id, audio=audio)
    await message.reply_text("**✅ Audio enregistré**")

@Client.on_message(filters.private & filters.command('setsubtitle'))
async def subtitle(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Indiquez le sous-titre\n\nExemple : /setsubtitle @@ZeeXDev**")
    subtitle = message.text.split(" ", 1)[1]
    await db.set_subtitle(message.from_user.id, subtitle=subtitle)
    await message.reply_text("**✅ Sous-titre enregistré**")

@Client.on_message(filters.private & filters.command('setvideo'))
async def video(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "**Indiquez le titre vidéo\n\nExemple : /setvideo Encodé par @@ZeeXDev**")
    video = message.text.split(" ", 1)[1]
    await db.set_video(message.from_user.id, video=video)
    await message.reply_text("**✅ Vidéo enregistrée**")