from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv


# To get your user agent go to this link: https://www.whatismybrowser.com/detect/what-is-my-user-agent/

load_dotenv()
# Create your own environment variables
client_id_var = os.environ.get('CLIENT_ID')
client_secret_var = os.environ.get('CLIENT_SECRET')
user_agent = os.environ.get('USER_AGENT')

def authorization_flow(scope=""):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    # Create a Spotify API Client
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id_var,
            client_secret=client_secret_var,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope=scope
        )
    )

    return sp

date = input("Witch year would you like to travel to? (YYYY-MM-DD): ")
# date ="2020-10-10"
header = {"user-agent": user_agent}
url = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(url,header)
html_website = response.text

soup = BeautifulSoup(html_website, "html.parser")
t = soup.select("li ul li h3")
titles_list = [title.string.strip() for title in t]

# DISPALY THE SONG NAME
# optional here, can make a .txt file with all the songs and the artists

# with open("songs.txt", "w") as file:
#     for index in range(0,100):
#         file.write(f"{index}. {titles_list[index]}\n")
#
# print(titles_list)

sp = authorization_flow(scope="playlist-modify-private")
user = sp.current_user()
user_id = user["id"]

# create the playlist in spotify
playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 Song from {date}", public=False)

# making a URIs list
uris = []
for index in range(0,100):
    results = sp.search(q=f'track:"{titles_list[index]}"', type="track", market="RO",
                        limit=1)  # can change the market to another country
    try:
        uri = results["tracks"]["items"][0]["uri"]
    except IndexError:
        print(index)  # prints the index's song that cannot find. If you want to know the song and debug, uncomment the part where is creating the .txt file
    else:
        uri = results["tracks"]["items"][0]["uri"]
    uris.append(uri)



# add the  URI's to the created playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=uris)

print("Created playlist:", playlist["name"])
print("Link:", playlist["external_urls"]["spotify"])



