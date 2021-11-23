#!/usr/bin/env python3

import json
import smtplib
from email.message import EmailMessage
import questionary
from halo import Halo

import files
import emails
import colors


# Load config
config = open("config.json")
configData = json.load(config)

host = configData["smtp"]["host"]
port = configData["smtp"]["port"]
user = configData["smtp"]["user"]

spinner = Halo(spinner='dots', color="grey")


def send(recipients, html, plain):
    with smtplib.SMTP(host, port) as smtp:
        spinner.start()
        smtp.starttls()
        spinner.stop()
        password = questionary.password(f'Password for {user}?').ask()
        spinner.start()
        try:
            smtp.login(configData["smtp"]["user"], password)
        except:
            print(f'{colors.bcolors.FAIL}Error:{colors.bcolors.ENDC} Wrong password.')
            exit()
        spinner.stop()

        for recipient in recipients:

            # Build message
            msg = EmailMessage()
            msg["Subject"] = configData["subject"]
            msg["From"] = configData["from"]
            msg["To"] = recipient

            # Set plain text message
            msg.set_content(plain)

            # Set html message
            msg.add_alternative(html, subtype="html")

            # Send message
            smtp.send_message(msg)

            # Notify of send
            print(f"Sent to {recipient}")

        print(f'{colors.bcolors.OKGREEN}Success:{colors.bcolors.ENDC} All emails sent.')


# Ask user which template to send
templates = files.getEmailTemplatesFromFolder(configData["templatesFolder"])

if templates == None:
    exit()

emailChoice = questionary.select(
    "What email do you want to send?",
    choices=templates,
).ask()

html_file = open(
    f'{configData["templatesFolder"]}/{emailChoice}.html', "r").read()
text_file = open(
    f'{configData["templatesFolder"]}/{emailChoice}.txt', "r").read()

# Ask if this is a test
isTest = questionary.confirm(
    f'Do you want to send a test first?').ask()

if isTest:
    testRecipient = questionary.text(
        "What email address to you want to send the test to?").ask()
    send([testRecipient], html_file, text_file)
    exit()

# Ask user who to send it to
lists = files.getContactsFromFolder(configData["contactsFolder"])

if lists == None:
    exit()

listChoice = questionary.select(
    "Who do you want to send it to?",
    choices=lists,
).ask()

# Get emails from choosen list
contactEmails = emails.getEmails(
    f'{configData["contactsFolder"]}/{listChoice}.csv')

# Confirm
confirm = questionary.confirm(
    f'Are you sure you want to send {emailChoice} to {len(contactEmails)} contacts from {listChoice}?').ask()

if confirm:
    send(contactEmails, html_file, text_file)
else:
    print(f'{colors.bcolors.WARNING}Warning:{colors.bcolors.ENDC} Canceled by user.')
