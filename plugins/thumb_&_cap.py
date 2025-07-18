from pyrogram import Client, filters 
from helper.database import codeflixbots

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**Donnez une légende\n\nExemple :- `/set_caption 📕Nom ➠ : {filename} \n\n🔗 Taille ➠ : {filesize} \n\n⏰ Durée ➠ : {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await codeflixbots.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("**Votre légende a bien été enregistrée ✅**")

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    caption = await codeflixbots.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("**Vous n'avez aucune légende ❌**")
    await codeflixbots.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**Votre légende a bien été supprimée 🗑️**")

@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    caption = await codeflixbots.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**Votre légende :**\n\n`{caption}`")
    else:
       await message.reply_text("**Vous n'avez aucune légende ❌**")


@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):    
    thumb = await codeflixbots.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("**Vous n'avez aucune miniature ❌**") 

@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
    await codeflixbots.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Miniature supprimée avec succès 🗑️**")

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    mkn = await message.reply_text("Veuillez patienter...")
    await codeflixbots.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await mkn.edit("**Miniature enregistrée avec succès ✅**")