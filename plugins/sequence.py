import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import re
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime
from config import Config

# Configuration de la base de données
db_client = MongoClient(Config.DB_URL)
db = db_client[Config.DB_NAME]
users_collection = db["users_sequence"]
sequence_collection = db["active_sequences"]  # Nom simplifié

# Modèles pour extraire les numéros d'épisode
patterns = [
    re.compile(r'\b(?:EP|E)\s*-\s*(\d{1,3})\b', re.IGNORECASE),  # Format "Ep - 06"
    re.compile(r'\b(?:EP|E)\s*(\d{1,3})\b', re.IGNORECASE),  # "EP06" ou "E 06"
    re.compile(r'S(\d+)(?:E|EP)(\d+)', re.IGNORECASE),  # "S1E06" / "S01EP06"
    re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)\s*(\d+)', re.IGNORECASE),  # "S 1 Ep 06"
    re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)', re.IGNORECASE),  # "E(06)"
    re.compile(r'(?:EP|E)?\s*[-]?\s*(\d{1,3})', re.IGNORECASE),  # "E - 06" / "- 06"
    re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE),  # "S1 - 06"
    re.compile(r'(\d+)')  # Solution de repli
]

def extract_episode_number(filename):
    """Extrait le numéro d'épisode pour le tri"""
    for pattern in patterns:
        match = pattern.search(filename)
        if match:
            return int(match.groups()[-1])
    return float('inf')  

def is_in_sequence_mode(user_id):
    """Vérifie si l'utilisateur est en mode séquence"""
    return sequence_collection.find_one({"user_id": user_id}) is not None

@Client.on_message(filters.private & filters.command("startsequence"))
async def start_sequence(client, message):
    user_id = message.from_user.id
    
    # Vérifie si déjà en mode séquence
    if is_in_sequence_mode(user_id):
        await message.reply_text("⚠️ Mode séquence déjà actif. Envoyez vos fichiers ou utilisez /endsequence.")
        return
        
    # Crée une nouvelle entrée de séquence
    sequence_collection.insert_one({
        "user_id": user_id,
        "files": [],
        "started_at": datetime.now()
    })
    
    await message.reply_text("✅ Mode séquence activé ! Envoyez vos fichiers maintenant.")

@Client.on_message(filters.private & filters.command("endsequence"))
async def end_sequence(client, message):
    user_id = message.from_user.id
    
    # Récupère les données de séquence
    sequence_data = sequence_collection.find_one({"user_id": user_id})
    
    if not sequence_data or not sequence_data.get("files"):
        await message.reply_text("❌ Aucun fichier dans la séquence !")
        return
    
    # Trie les fichiers
    files = sequence_data.get("files", [])
    sorted_files = sorted(files, key=lambda x: extract_episode_number(x["filename"]))
    total = len(sorted_files)
    
    # Message de progression
    progress = await message.reply_text(f"⏳ Traitement et tri de {total} fichiers...")
    
    sent_count = 0
    
    # Envoie les fichiers dans l'ordre
    for i, file in enumerate(sorted_files, 1):
        try:
            await client.copy_message(
                chat_id=message.chat.id, 
                from_chat_id=file["chat_id"], 
                message_id=file["msg_id"]
            )
            sent_count += 1
            
            # Met à jour la progression tous les 5 fichiers
            if i % 5 == 0:
                await progress.edit_text(f"📤 Envoyés {i}/{total} fichiers...")
            
            await asyncio.sleep(0.5)  # Délai anti-flood
        except Exception as e:
            print(f"Erreur d'envoi : {e}")
    
    # Met à jour les statistiques
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"files_sequenced": sent_count}, 
         "$set": {"username": message.from_user.first_name}},
        upsert=True
    )
    
    # Supprime les données de séquence
    sequence_collection.delete_one({"user_id": user_id})
    
    await progress.edit_text(f"✅ {sent_count} fichiers envoyés dans l'ordre !")

# Gestionnaire de fichiers avec priorité élevée
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=0)
async def sequence_file_handler(client, message):
    user_id = message.from_user.id
    
    # Vérifie le mode séquence
    if is_in_sequence_mode(user_id):
        # Récupère le nom du fichier
        if message.document:
            file_name = message.document.file_name
        elif message.video:
            file_name = message.video.file_name or "vidéo"
        elif message.audio:
            file_name = message.audio.file_name or "audio"
        else:
            file_name = "Inconnu"
        
        # Stocke les informations
        file_info = {
            "filename": file_name,
            "msg_id": message.id,
            "chat_id": message.chat.id,
            "added_at": datetime.now()
        }
        
        # Ajoute à la séquence
        sequence_collection.update_one(
            {"user_id": user_id},
            {"$push": {"files": file_info}}
        )
        
        message.stop_propagation()
        
        await message.reply_text(f"📂 Ajouté à la séquence : {file_name}")

@Client.on_message(filters.private & filters.command("cancelsequence"))
async def cancel_sequence(client, message):
    user_id = message.from_user.id
    
    # Annule la séquence
    result = sequence_collection.delete_one({"user_id": user_id})
    
    if result.deleted_count > 0:
        await message.reply_text("❌ Séquence annulée. Tous les fichiers ont été supprimés.")
    else:
        await message.reply_text("❓ Aucune séquence active à annuler.")

@Client.on_message(filters.private & filters.command("showsequence"))
async def show_sequence(client, message):
    user_id = message.from_user.id
    
    # Récupère la séquence
    sequence_data = sequence_collection.find_one({"user_id": user_id})
    
    if not sequence_data or not sequence_data.get("files"):
        await message.reply_text("Aucun fichier dans la séquence actuelle.")
        return
    
    files = sequence_data.get("files", [])
    sorted_files = sorted(files, key=lambda x: extract_episode_number(x["filename"]))
    
    file_list = "\n".join([
        f"{i}. {file['filename']}" 
        for i, file in enumerate(sorted_files, 1)
    ])
    
    if len(file_list) > 4000:
        file_list = file_list[:3900] + "\n\n... (liste tronquée)"
    
    await message.reply_text(
        f"**Fichiers en séquence ({len(files)}) :**\n\n{file_list}"
    )

@Client.on_message(filters.command("leaderboard"))
async def leaderboard(client, message):
    top_users = list(users_collection.find().sort("files_sequenced", -1).limit(5))
    
    if not top_users:
        await message.reply_text("Aucune donnée disponible dans le classement !")
        return
        
    leaderboard_text = "**🏆 Top des renommeurs 🏆**\n\n"

    for index, user in enumerate(top_users, start=1):
        username = user.get('username', 'Utilisateur inconnu')
        files_count = user.get('files_sequenced', 0)
        leaderboard_text += f"**{index}. {username}** - {files_count} fichiers\n"

    await message.reply_text(leaderboard_text)