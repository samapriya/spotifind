from __future__ import print_function

__copyright__ = """

    Copyright 2020 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

import argparse
import requests
import json
import os
import time
import base64
import sys
import getpass
import webbrowser
from logzero import logger
from os.path import expanduser
from bs4 import BeautifulSoup


MAIN_URL = "https://www.tunefind.com"


# Initialize Spotify Credentials
def spotinit():
    try:
        cid = str(raw_input("Enter your Client ID:  "))
    except NameError:
        cid = str(input("Enter your Client ID:  "))
    cpass = getpass.getpass("Enter your Client Secret:  ")
    while len(cpass) == 0:
        logger.warning("Client Secret is empty: try again")
        cpass = getpass.getpass("Enter your Client Secret:  ")
    try:
        rdirect = str(raw_input("Enter your Redirect URI:  "))
    except NameError:
        rdirect = str(input("Enter your Redirect URI:  "))
    authpass = str(cid).strip() + ":" + str(cpass).strip()
    b64 = base64.b64encode(authpass.encode("utf-8")).decode("ascii")
    token_data = {"b64auth": b64, "cid": cid, "rdirect": rdirect}
    with open(os.path.join(expanduser("~"), "b64.json"), "w") as outfile:
        json.dump(token_data, outfile)
    logger.info("Auth profile setup complete")


def spot_init_from_parser(args):
    spotinit()


# Spotify authentication & token
def spotauth(overwrite):
    if (
        os.path.exists(os.path.join(expanduser("~"), "auth.json"))
        and overwrite != "yes"
    ):
        sys.exit("auth.json already exists: Use spot_refresh instead")
    else:
        with open(os.path.join(expanduser("~"), "b64.json")) as json_file:
            b64data = json.load(json_file)
            b64 = b64data["b64auth"]  # base64 encoded clientid:secret pair
            rdirect = b64data["rdirect"]  # redirect url
            cid = b64data["cid"]  # client id

        # Get all scopes
        scope = "user-read-private+user-read-email+playlist-read-private+user-library-read+user-library-modify+user-top-read+playlist-read-collaborative+playlist-modify-public+playlist-modify-private+user-follow-read+user-follow-modify+user-read-playback-state+user-read-currently-playing+user-modify-playback-state+user-read-recently-played"

        URL = "https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}&scope={}".format(
            cid, rdirect, scope
        )

        # Open the URL in browser or print it out
        try:
            webbrowser.open(URL)
        except Exception as e:
            print("Authorize your client here {}".format(URL))

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {}".format(b64),
        }

        try:
            tcode = raw_input("Enter the URL you were redirecte:  ")
        except NameError:
            tcode = input("Enter the URL you were redirected to:  ")

        ccode = tcode.split("?code=")[1].split("&")[0].strip()

        data = {
            "grant_type": "authorization_code",
            "code": ccode,
            "redirect_uri": rdirect,
        }

        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )
        if response.status_code == 200:
            print("")
            logger.info("Credentials successfully created")
            with open(os.path.join(expanduser("~"), "auth.json"), "w") as outfile:
                json.dump(response.json(), outfile)
        else:
            logger.warning(
                "Credentials creation failed with status code: {}".format(
                    response.status_code
                )
            )
            print(response.content)


def spot_auth_from_parser(args):
    spotauth(overwrite=args.overwrite)


# Spotify Token Refresh
def spot_refresh():
    # Get b64 setup
    with open(os.path.join(expanduser("~"), "b64.json")) as json_file:
        b64data = json.load(json_file)
    b64 = b64data["b64auth"]  # base64 encoded clientid:secret pair
    rdirect_uri = b64data["rdirect"]  # redirect url

    # Get current refresh Token
    with open(os.path.join(expanduser("~"), "auth.json")) as json_file:
        token_data = json.load(json_file)
    rtoken = token_data["refresh_token"]

    # Client based b64 here is Client-ID:Client-Secret base64-encoded
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {}".format(b64),
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": rtoken,
        "redirect_uri": rdirect_uri,
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )
    if response.status_code == 200:
        token_data["access_token"] = response.json()["access_token"]
        with open(os.path.join(expanduser("~"), "auth.json"), "w") as outfile:
            json.dump(token_data, outfile)
        logger.info("Access Token refresh successful")
        return response.json()["access_token"]

    else:
        logger.warning(
            "Spotify Token Refresh failed with status code {}".format(
                response.status_code
            )
        )


def spot_refresh_from_parser(args):
    spot_refresh()


#####################Tunefind and Spotify Playlist tools##################
uri_list = []


def get_spotify_uri(song_name, artist):
    with open(os.path.join(expanduser("~"), "auth.json")) as json_file:
        token_data = json.load(json_file)
    spotify_token = token_data["access_token"]

    """Search For the Song and artist"""
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
        song_name, artist
    )
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token),
        },
    )
    if response.status_code == 200:
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        if response_json["tracks"]["total"] > 0:
            # only use the first song
            uri = songs[0]["uri"]
            uri_list.append(uri)
            logger.info(
                "Found Song: {} with artist: {}".format(
                    songs[0]["name"], songs[0]["artists"][0]["name"]
                )
            )
            return uri
    else:
        logger.warning(
            "Failed to get URI with status code {}".format(response.status_code)
        )


emp = {}


def create_playlist(name, desc):
    with open(os.path.join(expanduser("~"), "auth.json")) as json_file:
        token_data = json.load(json_file)
    spotify_token = token_data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token),
    }
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    if response.status_code == 200:
        spotify_user_id = response.json()["id"]
    else:
        logger.warning(
            "Failed to get user ID with status code {}".format(response.status_code)
        )

    query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
    resp = requests.get(query, headers=headers)
    if resp.status_code == 200:
        for items in resp.json()["items"]:
            emp.update({items["name"]: items["id"]})

    if name in emp:
        logger.warning("Playlist {} already exists".format(name))
        return emp[name]
    else:
        """Create A New Playlist"""
        request_body = json.dumps(
            {"name": name, "description": desc, "public": "false"}
        )

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        response = requests.post(query, data=request_body, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            response_json = response.json()
            logger.info(
                "Successfully created Playlist: {}".format(response_json["name"])
            )
            return response_json["id"]  # # playlist id
        else:
            logger.warning(
                "Failed to create playlist with status code {}".format(
                    response.status_code
                )
            )


baselist = []


def add_song_to_playlist(playlist_id, urlist, name):
    with open(os.path.join(expanduser("~"), "auth.json")) as json_file:
        token_data = json.load(json_file)
    spotify_token = token_data["access_token"]

    resp = requests.get(
        "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token),
        },
    )
    if resp.status_code == 200:
        for things in resp.json()["items"]:
            baselist.append(things["track"]["uri"])
    urlist = list(set(urlist) - set(baselist))
    if not len(urlist) == 0:
        """Add all liked songs into a new Spotify playlist"""
        data = {"uris": urlist}
        data = json.dumps(data)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        try:
            response = requests.post(
                query,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token),
                },
            )

            # check for valid response status
            if response.status_code != 201:
                logger.warning(
                    "Failed to add song to playlist with status code {}".format(
                        response.status_code
                    )
                )
            elif response.status_code == 201:
                response_json = response.json()
                logger.info(
                    "{} Songs added to playlist {}".format(str(len(urlist)), str(name))
                )
        except Exception as e:
            print(e)
    else:
        logger.info("All songs exists in playlist")


############# Tunefind Tools ################

# Parse tunefind links
def tuneparse(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.select("h5")
    for link in links:
        songlist = link.select("a")[0].get("href")
        if songlist.endswith("songs"):
            spage = requests.get(MAIN_URL + songlist)
            if spage.status_code == 200:
                print("")
                sn = songlist.split("/")[3]
                soup = BeautifulSoup(spage.content, "html.parser")
                season = soup.findAll("div", {"EpisodePage__title___MiEq3"})
                episode = season[0].select("h1")[0].string.split(" ")[0]
                links = soup.findAll("div", {"class": "SongRow__container___3eT_L"})
                for link in links:
                    song = str(link.findAll("a")[0].string)
                    artist = link.findAll("a")[1].string
                    print("{} {} Song: {} Artist: {}".format(sn, episode, song, artist))
                    get_spotify_uri(song.replace("'", ""), artist.replace("'", ""))
                    time.sleep(1)

            else:
                print("Failed with status code " + str(spage.status_code))


# Generate main season and songs URL
def tunemain(url, name, desc):
    # Refresh Spotify Token avoids 401 Error
    spot_refresh()

    # Create empty playlist using name and description
    # Get playlist ID
    pid = create_playlist(name, desc)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.select("h3")
    for link in links:
        try:
            url = link.select("a")
            tuneparse(MAIN_URL + url[0].get("href"))
        except Exception as e:
            pass
    if len(uri_list) <= 100:
        add_song_to_playlist(pid, uri_list, name)
    else:
        print("Total number of songs: {}".format(len(uri_list)))
        divr = len(uri_list) / 100
        i = 0
        j = 0
        while j < divr:
            add_song_to_playlist(pid, uri_list[i : i + 99], name)
            i = i + 99  # Max 100 songs per request
            j = j + 1  # Split the songs


def spot_tune_from_parser(args):
    tunemain(url=args.url, name=args.name, desc=args.desc)


spacing = "                               "


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Spotify and Tunefind Bridge Simple CLI"
    )
    subparsers = parser.add_subparsers()

    parser_spot_init = subparsers.add_parser(
        "spot_init", help="Initialize Spotify & setup client credentials"
    )
    parser_spot_init.set_defaults(func=spot_init_from_parser)

    parser_spot_auth = subparsers.add_parser(
        "spot_auth", help="Authorize Spotify Client and get access and refresh tokens"
    )
    optional_named = parser_spot_auth.add_argument_group("Optional named arguments")
    optional_named.add_argument(
        "--overwrite", help="Type yes to overwrite existing", default=None
    )
    parser_spot_auth.set_defaults(func=spot_auth_from_parser)

    parser_spot_refresh = subparsers.add_parser(
        "spot_refresh", help="Refresh spotify token"
    )
    parser_spot_refresh.set_defaults(func=spot_refresh_from_parser)

    parser_spot_tune = subparsers.add_parser(
        "spot_tune", help="Tunefind playlist to spotify playlist"
    )
    parser_spot_tune.add_argument("--url", help="Tunefind series url")
    parser_spot_tune.add_argument("--name", help="Spotify playlist name")
    parser_spot_tune.add_argument("--desc", help="Spotify Playlist Description")
    parser_spot_tune.set_defaults(func=spot_tune_from_parser)
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
