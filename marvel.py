# Task for the course "Emerging Technologies" in 3CCS

# Necessary modules: send HTTP requests; hash messages
import requests
import hashlib
from prettytable import PrettyTable

# API Link
url = "http://gateway.marvel.com/v1/public/characters?"
# Public key (use your own)
public_key = "3d841a427299ab59553e2072785a7de6"
# Private key (use your own)
private_key = "bfd021ba167240818a0212094dcde76f71fb5026"
# Timestamp
timestamp = "1"
# Hash, is used in URL when getting the data
pre_hash = timestamp + private_key + public_key
result = hashlib.md5(pre_hash.encode())

# While loop to keep looking for characters
while True:
    name = input("Enter a Marvel character's name (enter 'q' to quit): ")
    # If the input is 'q', break out of loop
    if name == "q":
        break
    elif name == "":
        print("Please enter a name.")
        continue
    # Send request with parameters, store response in variable 'data'
    data = requests.get(url, params={
        "name": name,
        "ts": timestamp,
        "apikey": public_key,
        "hash": result.hexdigest(), }, ).json()

    # Status, has to be 200 (success)
    status = data["code"]
    if status == 200:
        # If this is 0, the character doesn't exist
        if data["data"]["total"] == 0:
            print("Marvel character not found, try again: ")
        # If the character DOES exist, print and parse everything requested from the JSON
        else:
            # PrettyTable for character's name
            nameDescTable = PrettyTable()
            nameDescTable.field_names = ["Character Name",]
            name = data["data"]["results"][0]["name"]
            nameDescTable.add_row([name])
            print(nameDescTable)
            print("DESCRIPTION:\n" + str(data["data"]["results"][0]["description"]))

            # PrettyTable for comics
            comicsTable = PrettyTable()
            comicsTable.field_names = ["Marvel Comics Featuring " + name]
             # For each character's name that can be found, add row
            for each in data["data"]["results"][0]["comics"]["items"]:
                comicsTable.add_row([each["name"],])
            print(comicsTable)

            # PrettyTable for series
            seriesTable = PrettyTable()
            seriesTable.field_names = ["Marvel Comic Book Series Featuring " + name]
             # For each character's name that can be found, add row
            for each in data["data"]["results"][0]["series"]["items"]:
                seriesTable.add_row([each["name"],])
            
            print(seriesTable)

            # Legal stuff
            print("\n " + str(data["attributionText"]) + "\n ")
