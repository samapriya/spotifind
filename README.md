# spotifind
Combined Spotify and Tunefind Simple Command Line Tool

[![Twitter URL](https://img.shields.io/twitter/follow/samapriyaroy?style=social)](https://twitter.com/intent/follow?screen_name=samapriyaroy)
[![Hits-of-Code](https://hitsofcode.com/github/samapriya/spotifind?branch=master)](https://hitsofcode.com/github/samapriya/spotifind?branch=master)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5242608.svg)](https://doi.org/10.5281/zenodo.5242608)
[![CI spotifind](https://github.com/samapriya/spotifind/actions/workflows/CI.yml/badge.svg)](https://github.com/samapriya/spotifind/actions/workflows/CI.yml)
[![PyPI version](https://badge.fury.io/py/spotifind.svg)](https://badge.fury.io/py/spotifind)
![PyPI - Downloads](https://img.shields.io/pypi/dm/spotifind)

![spotifind_transparent_copy](https://user-images.githubusercontent.com/6677629/77322716-8489ec80-6cea-11ea-8d1c-bd2b6e598d21.jpg)

[Tunefind is a music search website](https://www.tunefind.com/), which helps find music featured in television series and movies. Users can suggest songs related to TV shows or movies. If approved, the song will be listed on that page.

[Spotify is a digital music streaming service](https://www.spotify.com/) that gives you access to millions of songs, podcasts, and videos from artists worldwide, like Apple Music and Amazon Music Unlimited.

Over the last week, as people are cooped up working from home, I thought it would be a fun project to think about soundtracks. In addition, I was getting a new Spotify premium account. Though you can probably find public playlists for almost any TV series, I thought it would be fun to link Tunefind and Spotify to do this for user-generated TV show lists.

Spotifind (Spotify+Tunefind) is a tool designed to authorize and authenticate your Spotify API and work with Tunefind to search for and create playlists.

![spotifind_main](https://user-images.githubusercontent.com/6677629/77280532-fafefe00-6c9a-11ea-9cf8-be0ff9c0f1fd.png)

There are two requirements for this tool:
* You have a Spotify account
* Create a new [spotify client here]

Spotify client setup needs two main steps
* The Client ID and Client Secret
* Setting up a redirect URI; you use this to redirect the authorization flow for Spotify. In short, once you authorize your app, the redirect URI will open along with a code that allows for authorization. I use "http://google.com," but you can use whatever you would like.

![spotify_client](https://user-images.githubusercontent.com/6677629/77280925-14547a00-6c9c-11ea-91e3-10d898d96ed7.gif)

Let's go back to the problem and the setup.

```
> spotifind -h
usage: spotifind [-h] {spot_init,spot_auth,spot_refresh,spot_tune} ...

Spotify and Tunefind Bridge Simple CLI

positional arguments:
  {spot_init,spot_auth,spot_refresh,spot_tune}
    spot_init           Initialize Spotify & setup client credentials
    spot_auth           Authorize Spotify Client and get access and refresh
                        tokens
    spot_refresh        Refresh spotify token
    spot_tune           Tunefind playlist to spotify playlist

optional arguments:
  -h, --help            show this help message and exit
```

Install now

```
pip install spotifind
```

### Spot Init
You only have to do this once. This takes a few things into account: your client id and your client secret (don't worry, your client secret is not stored in clear text or anywhere). It holds three specific things,
* your client id
* base64 encoded clientid:clientsecret *(Since base64 encoding is not encryption, it is possible to decode this, so try to use this app on your personal computer or virtual machine: Don't worry, you can always reset your client secret)*
* Redirect URI we set earlier

Run

```
spotifind spot_init
```

### Spot Auth
This is the authorization setup; this uses your client id and client secret file you set up using spot_init. Copy and paste the redirect URI, and you should be able to create the auth.json credentials file, which has the following setup. The setup includes all scopes; in the future, the idea would be for a user to send out the scopes they want to access simply. Therefore, I kept all possible scopes active.

```
{
    "access_token": "BQzxzRkNgSxJm0mEc..............lq74SenuW0lFEIqKjJF",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "AQD80AT2u..............85j2Hk579vTQkstZG-dinGDK7L4",
    "scope": "playlist-read-private playlist-read-collaborative user-follow-read playlist-modify-private user-read-email user-read-private user-follow-modify user-modify-playback-state user-library-read user-library-modify playlist-modify-public user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read"
}
```

The tool setup is as follows.

```
> spotifind spot_auth -h
usage: spotifind spot_auth [-h] [--overwrite OVERWRITE]

optional arguments:
  -h, --help            show this help message and exit

Optional named arguments:
  --overwrite OVERWRITE
                        Type yes to overwrite existing
```
If you have already done this step but want to use a different client or different account, you can use the setup.

```
spotifind spot_auth --overwrite "yes"
```

### Spot refresh
This will be used all the times; though your access token expires every one hour, the refresh token can be used to generate new access tokens. You won't necessarily need this tool, but it is built in and used as a module for the spot_tune tool to create the playlist by first refreshing the access token. Setup is simply

```
spotifind spot_refresh
```

### Spot Tune
This is the main tool used to convert a Tunefind series URL to a spotify playlist and add it to your account. The tool adds some features such as
* Checking for the existing playlist in case you want to use an existing playlist
* Checking if songs exist in the playlist, so the same songs are not added twice
* Since you can only add 100 songs simultaneously, it also iterates through the song list and adds it to the playlist in chunks.

The tool setup is

```
> spotifind spot_tune -h
usage: spotifind spot_tune [-h] --url URL --name NAME --desc DESC --playlist
                           PLAYLIST

optional arguments:
  -h, --help           show this help message and exit

Required named arguments.:
  --url URL            Tunefind series url
  --name NAME          Spotify playlist name
  --desc DESC          Spotify Playlist Description
  --playlist PLAYLIST  public or private
```

![spotifind_spot_tune](https://user-images.githubusercontent.com/6677629/77282763-3270a900-6ca1-11ea-9a1e-99bf3eb38f8e.gif)

The setup was

```
spotifind spot_tune --url "https://www.tunefind.com/show/self-made-inspired-by-the-life-of-madam-cj-walker" --name "walker" --desc "playlist-test" --playlist private
```

This was a weekend project and so much fun to implement. For now, this will be maintained ad hoc, and I hope to add more Spotify tools inspired by some fantastic projects out there. Since you are authorizing yourself with all scopes, why not explore more :)

## Changelog

### v0.0.6
- Pull [3](https://github.com/samapriya/spotifind/pull/3)
- fix paths changed by Tunefind
- parsing more robust and better logging
- fixed typos in code and ReadMe

### v0.0.5
- Pull [request 2](https://github.com/samapriya/spotifind/pull/2)
- fix old css classes, keep tracks sorted

### v0.0.4
* Replaced fuzzywuzzy with [rapidfuzz](https://github.com/samapriya/spotifind/pull/1)

### v0.0.3
* Added pagination to get all tracklist
* Overall improvements
* Applied Fuzzy song search
