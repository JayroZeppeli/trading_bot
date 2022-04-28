import smtplib
import ssl


port = 465
adresse_mail = "echoes.act.alert@gmail.com"
destinataire = "alexis.zaimi@yahoo.com"
password = "43_VAydowJ"


def envoyer_mail(sujet, message):
    contenu = "Subject: " + sujet + "\n\n" + message
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(adresse_mail, password)
        server.sendmail(adresse_mail, destinataire, contenu)



