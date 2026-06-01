import smtplib
import ssl


port = 465
adresse_mail = ""  # put the bot's email adress 
password = ""  # password of its email adress

destinataire = ""  # put your email adress



def envoyer_mail(sujet, message):
    contenu = "Subject: " + sujet + "\n\n" + message
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(adresse_mail, password)
        server.sendmail(adresse_mail, destinataire, contenu)
