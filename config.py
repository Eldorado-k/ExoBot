import re, os, time
from os import environ, getenv
id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "25926022")
    API_HASH  = os.environ.get("API_HASH", "30db27d9e56d854fb5e943723268db32")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7652109026:AAF2k80j0fI6Pmiw6Io9S6FqBO4qIVQrATo") 

    # database config
    DB_NAME = os.environ.get("DB_NAME","rename")     
    DB_URL  = os.environ.get("DB_URL","mongodb+srv://altof2:123Bonjoure@cluster0.s1suq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    PORT = os.environ.get("PORT", "8080")
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "https://i.ibb.co/kgSv5sKP/3c10c3a8fc8d.jpg")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1993048420 5743248220 8140299716').split()]
    FORCE_SUB_CHANNELS = os.environ.get('FORCE_SUB_CHANNELS', 'anime_existence, zeexdev').split(',')
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002698474966"))
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "8140299716"))
    DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "-1002698474966"))
    
    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", "True"))


class Txt(object):
    # part of text configuration
        
    START_TXT = """<b>Salut ! {}  

» Je suis un bot de renommage avancé ! Je peux renommer automatiquement vos fichiers avec des légendes personnalisées, des miniatures et même les séquencer parfaitement.</b>"""
    
    FILE_NAME_TXT = """<b>» <u>Configurer le format de renommage automatique</u></b>

<b>Variables :</b>
➲ Épisode - Pour remplacer le numéro d'épisode  
➲ Saison - Pour remplacer le numéro de saison  
➲ Qualité - Pour remplacer la qualité  

<b>‣ Exemple : </b> `/autorename Série [Ssaison Eépisode] - [Dual] qualité`

<b>‣ /Autorenommer : Renommez vos fichiers multimédias en incluant les variables 'épisode' et 'qualité' dans votre texte, pour extraire l'épisode et la qualité présents dans le nom de fichier original.</b>"""
    
    ABOUT_TXT = f"""<b>❍ Mon nom : <a href="https://t.me/Auto_Rename_ZeeBot">ZeeX Autorename</a>
❍ Développeur : <a href="https://t.me/ZeeXDevBot">ZeeXDev</a>
❍ Tiktok: <a href="https://tiktok.com/@kingcey">Svp encouragez nous</a>
❍ Langage : <a href="https://www.python.org/">Python</a>
❍ Base de données : <a href="https://www.mongodb.com/">MongoDB</a>
❍ Hébergé sur : <a href="https://t.me/BTZF_CHAT">Render</a>
❍ Chaîne principale : <a href="https://t.me/ZeeXDev">ZeeX Developpeur</a>

➻ Cliquez sur les boutons ci-dessous pour obtenir de l'aide et des informations sur moi.</b>"""

    THUMBNAIL_TXT = """<b><u>» Définir une miniature personnalisée</u></b>
    
➲ /start : Envoyez une photo pour la définir automatiquement comme miniature.
➲ /del_thumb : Supprimez votre ancienne miniature.
➲ /view_thumb : Affichez votre miniature actuelle.

Note : Si aucune miniature n'est enregistrée, le bot utilisera celle du fichier original."""

    CAPTION_TXT = """<b><u>» Définir une légende personnalisée et le type de média</u></b>
    
<b>Variables :</b>         
Taille : {taille}
Durée : {durée}
Nom du fichier : {nomfichier}

➲ /set_caption : Définir une légende personnalisée.
➲ /see_caption : Voir votre légende personnalisée.
➲ /del_caption : Supprimer votre légende personnalisée.

» Exemple : /set_caption Nom du fichier : {nomfichier}"""

    PROGRESS_BAR = """\n
<b>» Taille</b> : {1} | {2}
<b>» Progression</b> : {0}%
<b>» Vitesse</b> : {3}/s
<b>» Temps restant</b> : {4}"""
    
    DONATE_TXT = """<blockquote>Merci de votre intérêt pour les dons</blockquote>

<b><i>💞 Si vous aimez notre bot, n'hésitez pas à faire un don (500F, 800F) (de n'importe quel montant que vous vouliez.).</i></b>

Les dons aident au développement du bot.

<u>Vous pouvez aussi donner via Crypto:</u>

Binance: <code>lsjjdjssjdhlindhddjsksk</code>
USDT TRC20: <code>

merci d'envoter une capture après envoie @ZeeTECHBot."""

    PREMIUM_TXT = """<b>Passez à notre service premium et profitez de fonctionnalités exclusives :
○ Renommage illimité : Renommez autant de fichiers que vous voulez.
○ Accès anticipé : Testez les nouvelles fonctionnalités en avant-première.

• Utilisez /plan pour voir nos offres.

➲ Étape 1 : Payez via Crypto: <code>Non disponible</code>.
➲ Étape 2 : Envoyez la capture du paiement à @ZeeXDevBot.
➲ Alternative : Utilisez /bought après avoir uploadé la capture.

Votre abonnement sera activé après vérification.</b>"""

    PREPLANS_TXT = """<b>👋 Salut,
    
🎖️ <u>Offres disponibles</u> :

Tarifs :
➜ Premium mensuel : 1000F/mois
➜ Premium quotidien : 300F/jour
➜ Hébergement de bot : Contactez @ZeeXDevBot

➲ Binance : <code>Non disponible</code>

‼️ Envoyez la capture de paiement avec /bought.</b>\n\n<b>Les prix sont en Fran CFA (XOF)"""
    
    HELP_TXT = """<b>Aide : Commandes principales</b>

Fonctionnalités 🫧

➲ /Autorenommer : Renommage automatique.
➲ /Metadata : Gérer les métadonnées.
➲ /Help : Assistance rapide."""

    SEND_METADATA = """
<b>--Paramètres des métadonnées--</b>

➜ /metadata : Activer/désactiver les métadonnées.

<b>Description</b> : Les métadonnées modifient les fichiers MKV (audio, sous-titres, etc.)."""

    SOURCE_TXT = """
<b>Ceci est un bot open-source de renommage automatique.</b>

Développé en Python avec :
[Pyrogram](https://github.com/pyrogram/pyrogram)
[Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot)
et [MongoDB](https://cloud.mongodb.com).

<b>Code source :</b> [GitHub](https://t.me/ZeeTECH9)

Licence [MIT](https://t.me/ZeeTECH).
© 2024 | [Support](https://t.me/weebs_union)."""

    META_TXT = """
**Gestion des métadonnées pour vos fichiers**

**Commandes :**
➜ /metadata : Activer/désactiver.
➜ /settitle : Définir un titre.
➜ /setauthor : Définir l'auteur.
➜ /setartist : Définir l'artiste.
➜ /setaudio : Définir l'audio.
➜ /setsubtitle : Définir les sous-titres.
➜ /setvideo : Définir la vidéo.

**Exemple :** /settitle Votre Titre
"""

    SEQUENCE_TXT = """
<b>📦 <u>GESTIONNAIRE DE SÉQUENCE</u></b>

Triez et envoyez des fichiers dans l'ordre des épisodes.

<b>Commandes :</b>
➲ /startsequence - Commencer une séquence
➲ /showsequence - Voir les fichiers en séquence
➲ /endsequence - Envoyer les fichiers triés
➲ /cancelsequence - Annuler
➲ /leaderboard - Classement des utilisateurs

<b>Mode d'emploi :</b>
1. Envoyez /startsequence
2. Uploadez vos fichiers (dans n'importe quel ordre)
3. Envoyez /endsequence
4. Le bot envoie les fichiers dans l'ordre.
"""
