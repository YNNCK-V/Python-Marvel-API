# Task for the course "Emerging Technologies" in 3CCS

# Necessary modules: send HTTP requests; hash messages
import requests
import hashlib

# API Link
url = "http://gateway.marvel.com/v1/public/characters?"
# Public key (use your own)
public_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# Private key (use your own)
private_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
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
            print("NAME: " + name)
            print("DESCRIPTION:\n" + str(data["data"]["results"][0]["description"]))
            print("ID: " + str(data["data"]["results"][0]["id"]) + "\n " + "-" * 30)
            print("\nSERIES:")
            for each in data["data"]["results"][0]["series"]["items"]:
                print(" - " + each["name"])
            print("\n " + str(data["attributionText"]) + "\n ")
