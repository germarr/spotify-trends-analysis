import requests
import base64
import datetime
from urllib.parse import urlencode
import pandas as pd

from IPython.display import Image
from IPython.core.display import HTML 

def main(client_id, client_secret, artist, lookup_id=None, playlist_id=None, fields="", query=None, search_type='artist'):
    access_token = auth(client_id, client_secret)
    search = search_spotify(at=access_token , query=query, search_type=search_type)
    artist_id = get_artist_id(access_token, artist=artist)
    albums_ids = get_list_of_albums(lookup_id=lookup_id, artist=artist, at=access_token)
    album_info_list, albums_json = album_information(list_of_albums=albums_ids, at=access_token)
    artists_in_ablums_= get_multiple_artists_from_albums(albums_json= albums_json)
    list_of_songs_, list_of_songs_tolist= songs_information(albums_json= albums_json)
    artists_in_albums_, songs_json, artist_id_, songs_id_= artists_from_songs(list_of_songs_ids=list_of_songs_tolist ,at=access_token)
    artist_list_df= multiple_artists_songs(list_of_artists_ids= artist_id_, at=access_token)
    song_features, songs_features_json = song_features(list_of_songs_ids = songs_id_ , at=access_token)
    play_list_json_V2, empty_list_one_V2= playlist_data(at=access_token, playlist_id=playlist_id, fields=fields)

def auth():
    base_url = "https://accounts.spotify.com/api/token"
    client_id = input("client_id: ")
    client_secret = input("client_secret: ")

    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode())

    data_for_token = {"grant_type": "client_credentials"}
    headers_for_token = {"Authorization": f"Basic {b64_credentials.decode()}"} 

    access_token = requests.post(base_url, data=data_for_token, headers=headers_for_token).json()
    return access_token

def search_spotify(at, query=None, search_type='artist'):
    """
    Search_Type Options: album , artist, playlist, track, show and episode
    """
    endpoint = "https://api.spotify.com/v1/search"
    headers = { "Authorization": f"Bearer {at['access_token']}" }
    data = urlencode({"q": query, "type": search_type.lower()})
    lookup_url = f"{endpoint}?{data}"
    search = requests.get(lookup_url, headers=headers).json()      
    return search

def get_artist_id(access_token, artist):
    endpoint = "https://api.spotify.com/v1/search"
    headers = { "Authorization": f"Bearer {access_token['access_token']}" }    
    data = urlencode({"q": artist, "type": "artist"})    
    lookup_url = f"{endpoint}?{data}"
    artist_id = requests.get(lookup_url, headers=headers).json()["artists"]["items"][0]["id"]    
    return artist_id

def get_list_of_albums(lookup_id, at, artist=None, resource_type='albums', versions='v1', market="US"):
    
    if lookup_id == None:
        lookup_id = get_artist_id(at, artist=artist)
    
    dataV1 = urlencode({"market": market})
    endpoint = f"https://api.spotify.com/{versions}/artists/{lookup_id}/{resource_type}?{dataV1}"
    headers = { "Authorization": f"Bearer {at['access_token']}" }
    album_json = requests.get(endpoint, headers=headers).json()
    
    album_df=[]

    for albums in range(len(album_json["items"])):
        album_df.append({
            "album_id":album_json["items"][albums]["id"],
            "artist_id":album_json["items"][0]["artists"][0]["id"]
        })
        
    albums_ids = pd.DataFrame(album_df)["album_id"].tolist()
    
    return albums_ids


def album_information(list_of_albums, at, market="US"):
    
    counter = len(list_of_albums)
    info=[]
    
    while counter > 0:
        var1 = counter-20
        var2= counter
        
        headers = { "Authorization": f"Bearer {at['access_token']}" }
    
        if var1 < 0:
            var1 = 0
        
        joined_list = ",".join(list_of_albums[var1:var2])
        data = urlencode({"market": market,"ids":joined_list})
        endpoint = f"https://api.spotify.com/v1/albums?{data}"
        albums_json = requests.get(endpoint, headers=headers).json()    
       
        for index in range(len(list_of_albums[var1:var2])):
            albums= albums_json["albums"][index]
            
            info.append({
            "name_of_album":albums["name"],
            "album_id":albums["id"],
            #"artist_name":albums["artists"][0]["name"],
            #"artist_id":albums["artists"][0]["id"],
            "album_url":albums["external_urls"]["spotify"],
            "album_genres":albums["genres"],
            "album_cover": albums["images"][1]["url"],
            "album_popularity":albums["popularity"],
            "release_date":albums["release_date"]
        })
    
        counter -= 20
    
    album_info_list= pd.DataFrame.from_dict(info)
    
    return album_info_list, albums_json

def get_multiple_artists_from_albums(albums_json):
    artists_in_albums = []
    
    for si in range(len(albums_json["albums"])):
        for i in range(len(albums_json["albums"][si]["artists"])):
            
            artists = albums_json["albums"][si]["artists"][i]
            album_info= albums_json["albums"][si]
            
            artists_in_albums.append({
                "album_id":album_info["id"],
                "album_name":album_info["name"],
                f"album_artist{i+1}":artists["name"],
                f"album_artist{i+1}_id": artists["id"]
            })
        
    artists_in_ablums_=pd.DataFrame.from_dict(artists_in_albums).groupby('album_id').first().reset_index()
    
    return artists_in_ablums_

def songs_information(albums_json):
    albums = albums_json["albums"]
    number_of_albums = len(albums)
    list_of_songs = []
    
    for i in range(number_of_albums):
        songs_key = albums[i]["tracks"]["items"]
        number_of_songs_in_album = len(songs_key)
        album_id = albums[i]["id"]
        
        for si in range(number_of_songs_in_album):
            songs_subkey= songs_key[si]
            
            list_of_songs.append({
                "album_id":album_id,
                "song_id":songs_subkey["id"],
                "name_of_song":songs_subkey["name"],
                "duration":songs_subkey["duration_ms"],
                "song_url": songs_subkey["external_urls"]["spotify"],
                "song_preview": songs_subkey["preview_url"]
            })
    list_of_songs_= pd.DataFrame.from_dict(list_of_songs)
    list_of_songs_tolist = list_of_songs_["song_id"].tolist()
    
    return list_of_songs_, list_of_songs_tolist

def artists_from_songs(list_of_songs_ids,at):
    counter = len(list_of_songs_ids)
    artists_in_albums=[]
    artists_id = []
    
    while counter > 0:
        var1 = counter-50
        var2= counter
        
        headers = { "Authorization": f"Bearer {at['access_token']}" }
    
        if var1 < 0:
            var1 = 0
        
        joined_list = ",".join(list_of_songs_ids[var1:var2])
        endpoint = f"https://api.spotify.com/v1/tracks?ids={joined_list}"
        songs_json = requests.get(endpoint, headers=headers).json()    
        songs_in_list = len(songs_json["tracks"])
        
        for i in range(songs_in_list):
            tracks_in_list = songs_json["tracks"][i]
            artists_in_track = len(tracks_in_list["artists"])
            
            for si in range(artists_in_track):
                count_artist = tracks_in_list["artists"][si]
                
                artists_in_albums.append({
                    "song_id":tracks_in_list["id"],
                    "song_popularity":tracks_in_list["popularity"],
                    "song_image":tracks_in_list["album"]["images"][1]["url"],
                    f"name_artist_{si+1}":count_artist["name"],
                    f"id_artist_{si+1}": count_artist["id"]
                })
                
                artists_id.append(count_artist["id"])              
                
        counter -= 50
        
    artists_in_albums_= pd.DataFrame.from_dict(artists_in_albums).groupby('song_id').first().reset_index()
    artist_id_ = list(set(artists_id))
    songs_id_ = artists_in_albums_["song_id"].tolist()
     
    return artists_in_albums_, songs_json, artist_id_, songs_id_

def multiple_artists_songs(list_of_artists_ids,at):
    counter = len(list_of_artists_ids)
    empty_list_one = []
    
    while counter > 0:
        var1 = counter-50
        var2= counter
        
        headers = { "Authorization": f"Bearer {at['access_token']}" }
    
        if var1 < 0:
            var1 = 0
        
        joined_list = ",".join(list_of_artists_ids[var1:var2])
        endpoint = f"https://api.spotify.com/v1/artists?ids={joined_list}"
        artists_json = requests.get(endpoint, headers=headers).json()           
        artist_count = len(artists_json["artists"])
        
        for i in range(artist_count):
            working_with_artist= artists_json["artists"][i]
            count_genres = len(working_with_artist["genres"])
            
            for si in range(count_genres):
                empty_list_one.append({
                    "id_artist":working_with_artist["id"],
                    "name_artist":working_with_artist["name"],
                    "url": working_with_artist["external_urls"]["spotify"],
                    "followers":working_with_artist["followers"]["total"],
                    "image":working_with_artist["images"][1]["url"],
                    "artist_popluarity":working_with_artist["popularity"],
                    f"genre_{si}":working_with_artist["genres"][si]
                })
        
        
        counter -= 50
        
    artist_list_df = pd.DataFrame.from_dict(empty_list_one).groupby('id_artist').first().reset_index()
        
    return artist_list_df

def song_features(list_of_songs_ids,at):
    counter = len(list_of_songs_ids)
    empty_list_one = []
    
    while counter > 0:
        var1 = counter-100
        var2 = counter
        headers = { "Authorization": f"Bearer {at['access_token']}" }
    
        if var1 < 0:
            var1 = 0
        
        joined_list = ",".join(list_of_songs_ids[var1:var2])
        print(joined_list)
        endpoint = f"https://api.spotify.com/v1/audio-features?ids={joined_list}"
        songs_features_json = requests.get(endpoint, headers=headers).json()
        count_features = len(songs_features_json["audio_features"])
        
        for i in range(count_features):
            sf = songs_features_json["audio_features"][i]
            
            if sf != None:
                empty_list_one.append({
                    'song_id': sf["id"],'danceability': sf["danceability"],
                     'energy': sf["energy"],'key': sf["key"],
                     'loudness': sf["loudness"],'mode': sf["mode"],
                     'speechiness': sf["speechiness"],'acousticness': sf["acousticness"],
                     'instrumentalness': sf["instrumentalness"],'liveness': sf["liveness"],
                     'valence': sf["valence"],'tempo': sf["tempo"],
                })
            else:
                empty_list_one.append({
                    'song_id': 0,'danceability': 0,
                     'energy': 0,'key': 0,
                     'loudness': 0,'mode': 0,
                     'speechiness': 0,'acousticness': 0,
                     'instrumentalness': 0,'liveness': 0,
                     'valence': 0,'tempo': 0,
                })
                

        counter -= 100
        
    song_features = pd.DataFrame.from_dict(empty_list_one)
    
    return song_features

def playlist_data(at, playlist_id, market="US", fields=""):
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = { "Authorization": f"Bearer {at['access_token']}" }
    fields = fields
    data = urlencode({"market": market,"fields":fields})    
    lookup_url = f"{endpoint}?{data}"
    play_list_json_V2 = requests.get(lookup_url, headers=headers).json()
    songs_in_playlist = len(play_list_json_V2["tracks"]["items"])
    
    empty_list_one=[]
    
    for i in range(songs_in_playlist):
        songs_data = play_list_json_V2["tracks"]["items"][i]["track"]
        count_artists = len(songs_data["artists"])
        
        for si in range(count_artists):
            songs_data_artist = songs_data["artists"]
            
            empty_list_one.append({
                "playlist_id":play_list_json_V2["id"],
                "playlist_name":play_list_json_V2["name"],
                "playlist_owner":play_list_json_V2["owner"]["display_name"],
                "owner_url":play_list_json_V2["owner"]["external_urls"]["spotify"],
                "playlist_url":play_list_json_V2["external_urls"]["spotify"],
                "playlist_followers": play_list_json_V2["followers"]["total"],
                "playlist_cover_art": play_list_json_V2["images"][0]["url"],
                "song_id":songs_data["id"],
                "song_added_at": play_list_json_V2["tracks"]["items"][i]["added_at"],
                "song_name":songs_data["name"],
                "song_duration":songs_data["duration_ms"],
                "song_popularity":songs_data["popularity"],
                "song_url":songs_data["external_urls"]["spotify"],
                f"name_artist_{si+1}":songs_data_artist[si]["name"],
                f"id_artist_{si+1}":songs_data_artist[si]["id"]
            })
            
    empty_list_one_V2 = pd.DataFrame.from_dict(empty_list_one).groupby("song_id").first().reset_index()
    
    return play_list_json_V2, empty_list_one_V2 

def podcast_info(at, show_id, market="MX"):
    endpoint = f"https://api.spotify.com/v1/shows/{show_id}"
    headers = { "Authorization": f"Bearer {at['access_token']}" }
    data = urlencode({"market": market})    
    lookup_url = f"{endpoint}?{data}"
    podcast_json = requests.get(lookup_url, headers=headers).json()

    empty_list =[]
    count_episodes = len(podcast_json["episodes"]["items"])

    empty_list.append({
        "name" : podcast_json["name"],
        "publisher":podcast_json["publisher"],
        "total_episodes":podcast_json["total_episodes"],
        "show_id":show_id,
        "show_cover": podcast_json["episodes"]["items"][0]["images"][1]["url"]
    })
    
    podcast_basic_info = pd.DataFrame.from_dict(empty_list)
    
    return podcast_basic_info, podcast_json

def browse_new_playlists(at,limit,offset, country="MX", asset_type="categories"):
    """
    featured-playlists | new-releases | categories | categories/{category_id} | categories/{category_id}/playlists
    """
    base_url =f"https://api.spotify.com/v1/browse/{asset_type}"
    headers = { "Authorization": f"Bearer {at['access_token']}" }
    data=urlencode({"country":country, "limit":limit, "offset":offset })
    lookup_url = f"{base_url}?{data}"
    featured_playlist_json = requests.get(lookup_url, headers=headers).json()
    return featured_playlist_json

def top_playlists(at, country):
    empty_list=[]  
    
    for countries in range(len(country)):
        categories_toplists = browse_new_playlists(at, limit=50, offset=0, asset_type=f"featured-playlists", country=country[countries])
        
        len_playlists= range(len(categories_toplists["playlists"]["items"]))
        
        for playlist_id in len_playlists:
            first_key = categories_toplists["playlists"]["items"][playlist_id]
            empty_list.append({
                "name_of_playlist":first_key["name"],
                "playlist_id":first_key["id"],
                "owner":first_key["owner"]["display_name"],
                "playlist_cover":first_key["images"][0]["url"],
                "country": country[countries]
            })
            
    top_playlists = pd.DataFrame.from_dict(empty_list)
    return top_playlists

def songs_from_the_playlists(list_of_countries):
    # Getting the playlists id's from the list of countries
    dataframe_of_countries = top_playlists(list_of_countries)
    playlists_ids= dataframe_of_countries.playlist_id.tolist()
    count_playlists_ids= range(len(playlists_ids))
    df_countries= dataframe_of_countries[["playlist_id","country"]] 
    
    # Getting all the songs from the playlists ids
    empty_list_one=[]
    
    for ids_of_songs in count_playlists_ids:
        play_list_json_V2, songs_from_playlist= playlist_data(at=access_token, playlist_id=f"{playlists_ids[ids_of_songs]}")
        empty_list_one.append(songs_from_playlist)
    
    df_songs_many_features = pd.concat(empty_list_one).merge(df_countries, on="playlist_id", how="inner").drop_duplicates(subset="song_id")
    list_df_songs_many_features = df_songs_many_features.song_id.tolist()

    return list_df_songs_many_features, df_songs_many_features


if __name__ == "__main__":
    main(client_id="",client_secret="", artist="Ed Sheeran")