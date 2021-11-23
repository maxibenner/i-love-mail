import os
import colors


def getEmailTemplatesFromFolder(pathToTemplates):
    filesList = os.listdir(pathToTemplates)
    htmlTemplatesList = []

    for file in filesList:
        withExtension = file.split(".")
        extension = withExtension.pop()
        name = withExtension[0]

        if extension == "html":
            htmlTemplatesList.append(name)
            hasPlainTextVersion = False

            for file in filesList:
                if f'{name}.txt' in file:
                    hasPlainTextVersion = True

            if hasPlainTextVersion == False:
                print(f'{colors.bcolors.FAIL}Error:{colors.bcolors.ENDC} Some html templates are missing a plain text fallback. Make sure the template folder contains one .txt fallback for each .html file. The names of both files need to be identical.')
                return None

    return htmlTemplatesList


def getContactsFromFolder(pathToContact):
    filesList = os.listdir(pathToContact)
    contactFilesList = []

    for file in filesList:
        withExtension = file.split(".")
        extension = withExtension.pop()
        name = withExtension[0]

        if extension == "csv":
            contactFilesList.append(name)

    if len(contactFilesList) == 0:
        return None
    else:
        return contactFilesList
