from pyrogram import Client, filters
import datetime
import pytz
from helper.database import codeflixbots
import logging
from config import Config

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Commande pour ajouter un utilisateur premium
@Client.on_message(filters.command("addpremium") & filters.user(Config.BOT_OWNER))
async def add_premium_command(client, message):
    """Ajouter un utilisateur premium pour une durée donnée"""
    try:
        # Format de commande : /addpremium [réponse/userid/username] [durée: Xm/Xh/Xd/Xmh]
        command_parts = message.text.split()
        
        # Cas d'une réponse avec juste la durée
        if message.reply_to_message and len(command_parts) == 2:
            user_id = message.reply_to_message.from_user.id
            duration = command_parts[1]
        # Cas d'une commande directe avec utilisateur et durée
        elif len(command_parts) == 3:
            user_identifier = command_parts[1]
            duration = command_parts[2]
            
            # Vérification si l'identifiant est numérique
            if user_identifier.isdigit():
                user_id = int(user_identifier)
            else:
                # Gestion du nom d'utilisateur
                if user_identifier.startswith("@"):
                    username = user_identifier[1:]  # Supprime le @
                else:
                    username = user_identifier
                    
                # Conversion du nom d'utilisateur en ID
                try:
                    user = await client.get_users(username)
                    user_id = user.id
                except Exception as e:
                    return await message.reply_text(f"Utilisateur introuvable : {e}")
        else:
            return await message.reply_text(
                "**Utilisation :** `/addpremium [réponse/userid/username] [durée: Xm/Xh/Xd/Xmh]`\n\n"
                "**Exemples :**\n"
                "- `/addpremium 123456789 30d` (30 jours)\n"
                "- `/addpremium @username 2mh` (2 mois)\n"
                "- Répondre à un message : `/addpremium 6h` (ajoute 6 heures)"
            )
        
        # Vérifie si l'utilisateur existe dans la base
        if not await codeflixbots.is_user_exist(user_id):
            user = codeflixbots.new_user(user_id)
            await codeflixbots.col.insert_one(user)
        
        # Ajoute l'utilisateur premium
        success, result = await codeflixbots.add_premium_user(user_id, duration)
        
        if success:
            # Récupère le nom d'utilisateur pour le message
            try:
                user_info = await client.get_users(user_id)
                username_text = f"@{user_info.username}" if user_info.username else f"[Utilisateur](tg://user?id={user_id})"
            except:
                username_text = f"ID Utilisateur : `{user_id}`"
                
            # Formatage de la date d'expiration en IST
            try:
                expiry_date = datetime.datetime.fromisoformat(result)
                ist_timezone = pytz.timezone('Africa/Lome')
                expiry_date_ist = expiry_date.astimezone(ist_timezone)
                formatted_expiry = expiry_date_ist.strftime("%d %b %Y, %H:%M:%S IST")
            except:
                formatted_expiry = result

            await message.reply_text(
                f"✅ {username_text} est maintenant premium !\n\n"
                f"Expiration : `{formatted_expiry}`"
            )
        else:
            await message.reply_text(f"❌ Échec : {result}")
    
    except Exception as e:
        logger.error(f"Erreur dans add_premium_command: {e}")
        await message.reply_text(f"❌ Erreur : {str(e)}")


# Commande pour vérifier le statut premium
@Client.on_message(filters.command("myplan"))
async def check_premium_command(client, message):
    """Vérifier le statut premium d'un utilisateur"""
    user_id = message.from_user.id
    
    # Vérification par un admin
    command_parts = message.text.split()
    if len(command_parts) > 1 and message.from_user.id in Config.BOT_OWNER:
        try:
            check_user = command_parts[1]
            if check_user.isdigit():
                user_id = int(check_user)
            elif check_user.startswith("@"):
                user = await client.get_users(check_user[1:])
                user_id = user.id
            else:
                user = await client.get_users(check_user)
                user_id = user.id
        except Exception as e:
            return await message.reply_text(f"Utilisateur introuvable : {e}")
    
    # Récupération des infos premium
    is_premium = await codeflixbots.is_premium_user(user_id)
    premium_details = await codeflixbots.get_premium_details(user_id)
    
    if is_premium and premium_details:
        try:
            expiry_date = datetime.datetime.fromisoformat(premium_details["expiry_date"])
            ist_timezone = pytz.timezone('Africa/Lome')
            expiry_date_ist = expiry_date.astimezone(ist_timezone)
            remaining_time = expiry_date_ist - datetime.datetime.now(ist_timezone)
    
            # Formatage du temps restant
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
    
            time_str = ""
            if days > 0:
                time_str += f"{days} jours, "
            if hours > 0 or days > 0:
                time_str += f"{hours} heures, "
            time_str += f"{minutes} minutes"
    
            await message.reply_text(
        f"✨ **Statut : Actif** ✨\n\n"
        f"**Expire le :** `{expiry_date_ist.strftime('%d %b %Y, %H:%M:%S IST')}`\n"
        f"**Temps restant :** `{time_str}`\n\n"
        f"Accès à toutes les fonctionnalités premium !"
    )
        except Exception as e:
            await message.reply_text(
        f"✨ **Statut : Actif** ✨\n\n"
        f"**Expire le :** `{premium_details.get('expiry_date', 'Inconnu')}`\n\n"
        f"Accès à toutes les fonctionnalités premium !"
    )
    else:
        await message.reply_text(
            "❌ **Statut : Inactif** ❌\n\n"
            "Vous n'avez pas d'abonnement premium. Contactez @ZeeXDevBot pour débloquer toutes les fonctionnalités !. pout ta première fois, tu auras un accès gratuit d'un Mois"
        )


# Commande pour retirer le premium
@Client.on_message(filters.command("rmpremium") & filters.user(Config.BOT_OWNER))
async def remove_premium_command(client, message):
    """Retirer le statut premium d'un utilisateur"""
    try:
        # Analyse de la commande
        command_parts = message.text.split()
        
        if len(command_parts) != 2 and not message.reply_to_message:
            return await message.reply_text(
                "**Utilisation :** `/rmpremium [userid/username]` ou en réponse à un message"
            )
        
        # Cas d'une réponse
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_identifier = command_parts[1]
            
            # Vérification si l'identifiant est numérique
            if user_identifier.isdigit():
                user_id = int(user_identifier)
            else:
                # Gestion du nom d'utilisateur
                if user_identifier.startswith("@"):
                    username = user_identifier[1:]
                else:
                    username = user_identifier
                    
                # Conversion du nom d'utilisateur en ID
                try:
                    user = await client.get_users(username)
                    user_id = user.id
                except Exception as e:
                    return await message.reply_text(f"Utilisateur introuvable : {e}")
        
        # Retrait du premium
        success = await codeflixbots.remove_premium(user_id)
        
        if success:
            try:
                user_info = await client.get_users(user_id)
                username_text = f"@{user_info.username}" if user_info.username else f"[Utilisateur](tg://user?id={user_id})"
            except:
                username_text = f"ID Utilisateur : `{user_id}`"
                
            await message.reply_text(f"✅ Accès premium retiré pour {username_text}")
        else:
            await message.reply_text("❌ Échec du retrait")
    
    except Exception as e:
        logger.error(f"Erreur dans remove_premium_command: {e}")
        await message.reply_text(f"❌ Erreur : {str(e)}")

# Commande pour lister les utilisateurs premium
@Client.on_message(filters.command("premiumusers") & filters.user(Config.BOT_OWNER))
async def list_premium_users(client, message):
    """Lister tous les utilisateurs premium actifs"""
    try:
        # Récupération de tous les utilisateurs
        all_users = await codeflixbots.get_all_users()
        
        # Compteur
        premium_count = 0
        premium_users_list = []
        
        # Vérification du statut premium
        async for user in all_users:
            user_id = user["_id"]
            
            # Passe si non premium
            if "premium" not in user or not user["premium"].get("is_premium", False):
                continue
                
            # Vérification de la date d'expiration
            expiry = user["premium"].get("expiry_date")
            if not expiry:
                continue
                
            # Conversion de la date
            try:
                expiry_date = datetime.datetime.fromisoformat(expiry)
                current_date = datetime.datetime.now(pytz.UTC)
                
                # Passe si expiré
                if current_date > expiry_date:
                    continue
                    
                # Premium actif
                premium_count += 1
                
                # Formatage de la date
                ist_timezone = pytz.timezone('Asia/Kolkata')
                expiry_date_ist = expiry_date.astimezone(ist_timezone)
                formatted_expiry = expiry_date_ist.strftime("%d %b %Y")
                
                # Récupération des infos utilisateur
                try:
                    user_info = await client.get_users(user_id)
                    if user_info.username:
                        user_display = f"@{user_info.username}"
                    else:
                        user_display = f"{user_info.first_name} [{user_id}]"
                except:
                    user_display = f"ID Utilisateur : {user_id}"
                    
                # Ajout à la liste
                premium_users_list.append(f"{premium_count}. {user_display} (Expire : {formatted_expiry})")
                
            except Exception as e:
                logger.error(f"Erreur avec l'utilisateur {user_id}: {e}")
                continue
        
        # Création du message avec pagination si nécessaire
        if premium_count == 0:
            await message.reply_text("Aucun utilisateur premium actif.")
            return
            
        # Découpage par lots de 20
        chunk_size = 20
        chunks = [premium_users_list[i:i + chunk_size] for i in range(0, len(premium_users_list), chunk_size)]
        
        # Envoi de la première page
        await message.reply_text(
            f"**Total : {premium_count} utilisateurs premium**\n\n" + 
            "\n".join(chunks[0]) +
            (f"\n\nPage 1/{len(chunks)}" if len(chunks) > 1 else "")
        )
        
        # Envoi des pages supplémentaires
        for i, chunk in enumerate(chunks[1:], 2):
            await message.reply_text(
                "\n".join(chunk) +
                f"\n\nPage {i}/{len(chunks)}"
            )
    
    except Exception as e:
        logger.error(f"Erreur dans list_premium_users: {e}")
        await message.reply_text(f"❌ Erreur : {str(e)}")