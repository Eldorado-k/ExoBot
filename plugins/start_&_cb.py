import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from helper.database import codeflixbots
from config import *
from config import Config
from config import Txt

# Gestionnaire de commande start
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    user = message.from_user
    await codeflixbots.add_user(client, message)

    # Séquence interactive de texte et stickers
    m = await message.reply_text("☎️")
    await asyncio.sleep(0.5)
    await m.edit_text("<code>Le GOAT, c'est Kingcey...</code>")
    await asyncio.sleep(0.6)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("<code>Jackpot!!!</code>")
    await asyncio.sleep(0.4)
    await m.delete()

    # Envoi d'un sticker après la séquence de texte
    await message.reply_sticker("CAACAgQAAxkBAAIOsGf5RIq9Zodm25_NfFJGKNFNFJv5AALHGAACukfIUwkk20UPuRnvNgQ")

    # Définition des boutons pour le message de démarrage
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("• Mes commandes •", callback_data='help')
        ],
        
        [
            InlineKeyboardButton("• Premium •", callback_data='premiumx')
        ],
        
        [
            InlineKeyboardButton('• Mises à jour', url='https://t.me/ZeeXDev'),
            InlineKeyboardButton('Support •', url='https://t.me/BTZF_CHAT')
        ],
        [
            InlineKeyboardButton('• À propos', callback_data='about')
        ]
    ])

    # Envoi du message de démarrage avec ou sans image
    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=Txt.START_TXT.format(user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )


# Gestionnaire de callback
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "home":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Mes commandes •", callback_data='help')],
                [InlineKeyboardButton("• Premium •", callback_data='premiumx')],
                [InlineKeyboardButton('• Mises à jour', url='https://t.me/ZeeXClub'), InlineKeyboardButton('Support •', url='https://t.me/BTZF_CHAT')],
                [InlineKeyboardButton('• À propos', callback_data='about'), InlineKeyboardButton('Code source •', callback_data='source')]
            ])
        )
    elif data == "caption":
        await query.message.edit_text(
            text=Txt.CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Support", url='https://t.me/BTZF_CHAT'), InlineKeyboardButton("Retour •", callback_data="help")]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Format auto-renommage •", callback_data='file_names')],
                [InlineKeyboardButton("• Séquence de fichiers •", callback_data='sequence_help')],
                [InlineKeyboardButton('• Miniature', callback_data='thumbnail'), InlineKeyboardButton('Légende •', callback_data='caption')],
                [InlineKeyboardButton('• Métadonnées', callback_data='meta'), InlineKeyboardButton('Donation •', callback_data='donate')],
                [InlineKeyboardButton('• Accueil', callback_data='home')]
            ])
        )

    elif data == "meta":
        await query.message.edit_text(
            text=Txt.SEND_METADATA,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Retour •", callback_data="help")]
            ])
        )
    elif data == "donate":
        await query.message.edit_text(
            text=Txt.DONATE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Retour", callback_data="help"), InlineKeyboardButton("Propriétaire •", url='https://t.me/ZeeXDevBot')]
            ])
        )
    elif data == "file_names":
        format_template = await codeflixbots.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Retour •", callback_data="help")]
            ])
        )
    elif data == "thumbnail":
        await query.message.edit_caption(
            caption=Txt.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Retour •", callback_data="help")]
            ])
        )
    elif data == "sequence_help":
        await query.message.edit_caption(
            caption=Txt.SEQUENCE_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Retour •", callback_data="help")]
            ])
        )
    elif data == "metadatax":
        await query.message.edit_caption(
            caption=Txt.SEND_METADATA,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Retour •", callback_data="help")]
            ])
        )
    elif data == "source":
        await query.message.edit_caption(
            caption=Txt.SOURCE_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Retour •", callback_data="home")]
            ])
        )
    elif data == "premiumx":
        await query.message.edit_caption(
            caption=Txt.PREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Offres •", callback_data='plans')],
                [InlineKeyboardButton("• Retour", callback_data="help"), InlineKeyboardButton("Acheter Premium •", url='https://t.me/ZeeXDevBot')]
            ])
        )
    elif data == "plans":
        await query.message.edit_caption(
            caption=Txt.PREPLANS_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Fermer", callback_data="close"), InlineKeyboardButton("Acheter Premium •", url='https://t.me/ZeeXDevBot')]
            ])
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Support", url='https://t.me/BTZF_CHAT'), InlineKeyboardButton("Commandes •", callback_data="help")],
                [InlineKeyboardButton("• Développeur", url='https://t.me/ZeeXDevBot'), InlineKeyboardButton("Réseau •", url='https://t.me/ZeeXClub')],
                [InlineKeyboardButton("• Retour •", callback_data="home")]
            ])
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

# Gestionnaire de commande donation
@Client.on_message(filters.command("donate"))
async def donation(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Retour", callback_data="help"), InlineKeyboardButton(text="Propriétaire", url='https://t.me/ZeeXDevBot')]
    ])
    yt = await message.reply_photo(photo='https://i.ibb.co/S7vgk8Hj/c8d9f3039813.jpg', caption=Txt.DONATE_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Gestionnaire de commande premium
@Client.on_message(filters.command("premium"))
async def getpremium(bot, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("• Offres •", callback_data='plans')],
        [InlineKeyboardButton("Propriétaire", url="https://t.me/ZeeXDevBot"), InlineKeyboardButton("Fermer", callback_data="close")]
    ])
    yt = await message.reply_photo(photo='https://i.ibb.co/S7vgk8Hj/c8d9f3039813.jpg', caption=Txt.PREMIUM_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Gestionnaire de commande plan
@Client.on_message(filters.command("plan"))
async def premium(bot, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Envoyer capture", url="https://t.me/ZeeXDevBot"), InlineKeyboardButton("Fermer", callback_data="close")]
    ])
    yt = await message.reply_photo(photo='https://i.ibb.co/S7vgk8Hj/c8d9f3039813.jpg', caption=Txt.PREPLANS_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Gestionnaire de commande bought
@Client.on_message(filters.command("bought") & filters.private)
async def bought(client, message):
    msg = await message.reply('Vérification en cours...')
    replied = message.reply_to_message

    if not replied:
        await msg.edit("<b>Veuillez répondre avec la capture d'écran de votre paiement pour l'achat premium.\n\nPar exemple, uploadez d'abord votre capture, puis répondez-y avec la commande '/bought'</b>")
    elif replied.photo:
        await client.send_photo(
            chat_id=Config.LOG_CHANNEL,
            photo=replied.photo.file_id,
            caption=f'<b>Utilisateur - {message.from_user.mention}\nID - <code>{message.from_user.id}</code>\nPseudonyme - <code>{message.from_user.username}</code>\nNom - <code>{message.from_user.first_name}</code></b>',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Fermer", callback_data="close_data")]
            ])
        )
        await msg.edit_text('<b>Votre capture a été envoyée aux administrateurs</b>')

@Client.on_message(filters.private & filters.command("help"))
async def help_command(client, message):
    bot = await client.get_me()
    mention = bot.mention

    await message.reply_text(
        text=Txt.HELP_TXT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Format auto-renommage •", callback_data='file_names')],
            [InlineKeyboardButton("• Séquence de fichiers •", callback_data='sequence_help')],
            [InlineKeyboardButton('• Miniature', callback_data='thumbnail'), InlineKeyboardButton('Légende •', callback_data='caption')],
            [InlineKeyboardButton('• Métadonnées', callback_data='meta'), InlineKeyboardButton('Donation •', callback_data='donate')],
            [InlineKeyboardButton('• Accueil', callback_data='home')]
        ])
    )