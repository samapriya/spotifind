# spotifind
Spotify and Tunefind Bridge Simple CLI

![Python Version](https://img.shields.io/badge/python-%3E%3D3%2F2-blue)

Tunefind is a music search website which helps to find music featured in television series and movies. Users can suggest songs related to TV show or movie.If approved, song will be listed on that page.

Spotify is a digital music streaming service that gives you access to millions of songs, podcasts and videos from artists all over the world, like Apple Music and Amazon Music Unlimited.

Over the span of the last week as people are cooped up working from home, I thought it would be a fun project, to think about soundtracks. I was just getting a new spotify premium account and though you can probably find public playlists for almost any TV series, I thought it would be fun to link Tunefind and Spotify to do this for user generated TV show lists.

Spotifind (Spotify+Tunefind) is a tool designed to first authorize and authenticate your Spotify API and work with Tunefind to search for and create playlists .

![spotifind_main](https://user-images.githubusercontent.com/6677629/77280532-fafefe00-6c9a-11ea-9cf8-be0ff9c0f1fd.png)

There are two requirements for this tool:
* You have a premium spotify account
* Create a new [spotify client here]

Spotify client setup needs two main steps
* The Client ID and Client Secret
* Setting up a redirect URI, you use this to redirect the authorization flow for Spotify. In short, once you authorize your app, the redirect URI will open along with a code that allows for authorization. In this case I use "http://google.com" but you can use whatever you would like.

![spotify_client](https://user-images.githubusercontent.com/6677629/77280925-14547a00-6c9c-11ea-91e3-10d898d96ed7.gif)

Let's go back to the problem and the setup

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
You only have to do this once. This takes a few things into account, your client id, your client secret (don't worry your client secret is not stored in clear text or directly anywhere). It stores three specific things,
* your client id
* base64 encoded clientid:clientsecret *(Since base64 encoding is not encryption it is possible to decode this, so try to use this app on your personal computer or virtual machine: Don't worry you can always reset your client secret)*
* Redirect URI we set earlier

Simply run

```
spotifind spot_init
```

### Spot Auth
This is the authorization setup, this uses your client id and client secret file you setup using spot_init. Copy and paste the redirect URI and you should be able to create the auth.json credentials file which has the following setup. The setup includes all scopes, in the future the idea would be for a user to simply send out the scopes they want to access. I kept all possible scopes active.

```
{
    "access_token": "BQzxzRkNgSxJm0mEc..............lq74SenuW0lFEIqKjJF",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "AQD80AT2u..............85j2Hk579vTQkstZG-dinGDK7L4",
    "scope": "playlist-read-private playlist-read-collaborative user-follow-read playlist-modify-private user-read-email user-read-private user-follow-modify user-modify-playback-state user-library-read user-library-modify playlist-modify-public user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read"
}
```

The tool setup is as follows

```
> spotifind spot_auth -h
usage: spotifind spot_auth [-h] [--overwrite OVERWRITE]

optional arguments:
  -h, --help            show this help message and exit

Optional named arguments:
  --overwrite OVERWRITE
                        Type yes to overwrite existing
```
If you have already done this step, but want to use a different client or different account you can use the setup

```
spotifind spot_auth --overwrite "yes"
```

### Spot refresh
This will be used all the times, though your access token expires every one hour, the refresh token can be used to generate new access tokens. You won't necessarily need this tool but it is built in and used as a module for the spot_tune tool to generate the playlist by first refreshing the access token. Setup is simply

```
spotifind spot_refresh
```

### Spot Tune
This is the main tool that will be used to convert a Tunefind series URL to a spotify playlist and add it to your account. The tool adds some features such as
* Checking for existing playlist incase you want to use an existing playlist
* Checking is songs exist in the playlist, so same songs are not added twice
* Since you can only add 100 songs at a time, it also iterates through the song list an adds it to the playlist in chunks.

The tool setup is

```
> spotifind spot_tune -h
usage: spotifind spot_tune [-h] [--url URL] [--name NAME] [--desc DESC]

optional arguments:
  -h, --help   show this help message and exit
  --url URL    Tunefind series url
  --name NAME  Spotify playlist name
  --desc DESC  Spotify Playlist Description
```

![spotifind_spot_tune](https://user-images.githubusercontent.com/6677629/77282763-3270a900-6ca1-11ea-9a1e-99bf3eb38f8e.gif)

The setup was

```
spotifind spot_tune --url "https://www.tunefind.com/show/self-made-inspired-by-the-life-of-madam-cj-walker" --name "walker" --desc "playlist-test"
```

This was a weekend project and so much fun to implement. For now this will be maintained ad hoc and I hope to add more spotify tools inspired by some amazing projects out there and since you are authorizing yourelf with all scopes why not explore more :)

