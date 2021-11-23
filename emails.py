
# os.chdir(os.path.dirname(__file__))

def getEmails(path_to_file):
    emails = []
    # Format of CSV needs to be [business_name,email]
    with open(path_to_file, newline='') as csvfile:

        # Find index of email column
        emailIndex = None
        for row in csvfile:
            columns = row.lower().split(";")
            for column in columns:
                if "email" in column:
                    emailIndex = columns.index(column)
            break

        # Get email
        for row in csvfile:
            email = row.lower().split(";")[emailIndex].strip()
            emails.append(email)

    return emails

