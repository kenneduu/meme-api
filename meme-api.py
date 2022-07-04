import requests
import os
from dotenv import load_dotenv


if os.path.exists(".env"):
    load_dotenv(dotenv_path=".env")
else:
    print("Please create a file called \".env\" in the same directory as this file.")
    print("The file should contain the following variables:")
    print("\tIMGFLIP_USERNAME")
    print("\tIMGFLIP_PASSWORD")
    print("Signup: https://imgflip.com/signup?redirect=%2Fsettings")


USERNAME = os.getenv("IMGFLIP_USERNAME")
PASSWORD = os.getenv("IMGFLIP_PASSWORD")


def get_memes() -> dict:
    """
    Get a list of memes from the API
    :return: A list of memes
    """
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    return response.json()


def get_meme_by_id(meme_id: str) -> dict:
    """
    Get a meme by its id
    :param meme_id: The id of the meme
    :return: The meme
    """
    url = "https://api.imgflip.com/get_meme"
    response = requests.get(url, params={"id": meme_id})
    return response.json()


def get_meme_by_name(meme_name: str) -> dict or None:
    """
    Get a meme by its name
    :param meme_name: The name of the meme
    :return: The meme
    """
    memes = get_memes()
    for meme in memes["data"]["memes"]:
        if meme["name"] == meme_name:
            return meme
    return None


def get_meme_by_url(meme_url: str) -> dict or None:
    """
    Get a meme by its url
    :param meme_url: The url of the meme
    :return: The meme
    """
    memes = get_memes()
    for meme in memes["data"]["memes"]:
        if meme["url"] == meme_url:
            return meme
    return None


def caption_meme(meme_id: str, top_text: str, bottom_text: str) -> dict:
    """
    Caption a meme
    :param meme_id: The id of the meme
    :param top_text: The text on the top of the meme
    :param bottom_text: The text on the bottom of the meme
    :return: The meme
    """
    url = "https://api.imgflip.com/caption_image"
    response = requests.get(url, params={"template_id": meme_id, "username": USERNAME, "password": PASSWORD,
                                         "text0": top_text, "text1": bottom_text})
    return response.json()


def main():
    exited = False
    while not exited:
        memes = get_memes()
        print("Valid memes:")
        for meme in memes["data"]["memes"]:
            print(f" Name: {meme['name']} \n ID: {meme['id']} \n URL: {meme['url']}", end="\n\n")

        meme_id = input("Enter a meme id: ")
        top_text = input("Enter a top text: ")
        bottom_text = input("Enter a bottom text: ")
        meme = caption_meme(meme_id, top_text, bottom_text)
        if meme["success"]:
            print(f"Meme URL: {meme['data']['url']}")
        else:
            print(f"Error: {meme['error_message']}")

        choice = input("Would you like to exit? (y/n) ")
        if choice == "y":
            exited = True
    print("Thank you")


if __name__ == "__main__":
    main()