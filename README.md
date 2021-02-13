# **Analyzing Data on Spotify** 
This README file contains the Index of the first part of a project I created to do research using Spotify. It covers how to get access to the Spotify API and the description of several helper functions I coded to interact with it.

If you want to interact with the Spotify API as fast as possible and, create quick datasets with almost 0 code, I highly recommend checking the [`helper_func.py`](https://github.com/germarr/spotify_trends_analysis/helper_func.py) file and read the instructions of how to use it by clicking [**here**](#3.-Helper-Functions). 

If you want to check the full project, check my Jupyter Notebook [`spotify_analysis.ipynb`](https://github.com/germarr/spotify-trends-analysis/blob/main/spotify_analysis.ipynb)

## **About this project**
---
I wanted to accomplish 2 things with this project. First, I wanted to learn how to use the Spotify API. Learning how to use this API serves as a  gateway into the API Universe. The documentation is amazing, the calls you can make to Spotify per day is more than enough for almost any kind of project and the information you can gather is really interesting.

The second thing I wanted to do, was to do some research on the song profiles that different countries consume and predict if new releases could be successful in different regions. To accomplish this, I'm going to create a dataframe with all the songs from some of the most popular playlists per country. Once I have these songs I'm going to use the [**Spotify Audio Features**](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-several-audio-features) on each song and as the last step, I'm applying a Machine Learning model to use these features as my Dependent Variable in a prediction exercise. 

In addition to that, I wanted to do some research on the characteristics of music that each country consumes and how this consumption has changed over the last decade. To do this I want to create a dataset with all the songs from the most important albums of the last 20 years, analyze their characteristics, and see if there's a particular change in the consumption of certain types of artists or genres.


## **Index**
---
* **1.** [**`spotify_analysis.ipynb`**](#1.-`spotify_analysis.ipynb`)
* **2.** [**Spotify Web API**](#2.-Spotify-Web-API)
* **3.** [**Helper Functions**](#3.-Helper-Functions)
    * **3.1** [`auth()`](#3.1-auth())
    * **3.2** [`search_spotify()`](#3.2-search_spotify())
    * **3.3** [`get_list_of_albums()`](#3.3-get_list_of_albums())
    * **3.4** [`album_information()`](#3.4-album_information())
    * **3.5** [`get_multiple_artists_from_albums()`](#3.5-get_multiple_artists_from_albums())
    * **3.6** [`songs_information()`](#3.6-songs_information())
    * **3.7** [`artists_from_songs()`](#3.7-artists_from_songs())
    * **3.8** [`multiple_artists_songs()`](#3.8-multiple_artists_songs())
    * **3.9** [`song_features()`](#3.9-song_features())
    * **3.10** [`playlist_data()`](#3.10-playlist_data())

## **1.** `spotify_analysis.ipynb`
---

This jupyter notebook has the research project that I did. To check how I used all the helper functions I highly recommend checking this file. 

## **2. Spotify Web API**
---
To kick off this project I read the [**Quick Start Guide**](https://developer.spotify.com/documentation/web-api/quick-start/) that Spotify offers. That article is great because it explains how their API works and the different pieces you need to understand before being able to use it. Basically to start you need to create a new app inside their developer platform. Access to this platform is through the use of a simple Spotify Account. Once the app is created you can get a `Client_ID` and a `Client_Secret`. The combination of these two strings creates an `access_token` which is necessary to use the API from the Jupyter Notebook. 

I created a function inside the `helper_func.py` file to manage the code that is necessary to create the `access_key`. To learn about this helper function click [**here**](#4.1-auth()).

To create the Spotify App you need to go to the Spotify Developer Dashboard. [**Here**](https://developer.spotify.com/dashboard/login) is a direct link.

Spotify offers several flavors of their API. For this project, I used the [**Web API**](https://developer.spotify.com/documentation/web-api/quick-start). One of the things that the Spotify API offers when you choose this particular API is the possibility of testing different methods on a console.

You can find the console by clicking here -->[**Spotify API Console**](https://developer.spotify.com/console/)

## **3. Helper Functions**
---
I created several functions inside this python file and, I use them inside my main jupyter notebook to gather all the data I need from Spotify, in the most efficient way possible.

Here's a brief summary of each of those functions : 

>* `auth()`: This functions generates the `access_token` by requesting the Client_ID and the Client_Secret. This token is important because it's the key to use all the functionalities of the API.
>* `search_spotify()`: The purpose of this function is to do searches using the Spotify API and get a JSON file with the information that was requested. Using this function, we can search for information about albums, artists, playlists, tracks, shows, and episodes.
>* `get_list_of_albums()`: This query will return a dataframe with all the albums from a single artist. 

<br>

### **3.1** `auth()`
---
This function follows the [**Clients Credentials Flow**]("https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow") to create the `access_token`. To use it the only thing that is required is to have at hand the "Client_ID" and "Client_Secret" of an active Spotify App. [**Here**](https://developer.spotify.com/documentation/web-api/quick-start/) you can find the Quick Start Guide to create a Spotify App and get those pieces of information. 

Here´s an example of how the function works:
```python
access_token = auth()

#Once the function is called a prompt will ask for "Client_ID" and "Client_Secret". Once the information is added, the access_token is ready and stored in the variable of the same name.

Add Client_ID: XXXXXXXXXXXXXXXXXX
Add Client_Secret: XXXXXXXXXXXXXX

```
><ins>**Notes:**</ins>
>* The lifespan of an `access_token` is 60 minutes. After this time you will start to get errors every time you do a call through the Spotify API. To avoid this just run the `auth()` function again and a new access_token will be generated.

<br>

### **3.2** `search_spotify()`
---
This function will do a simple search for a 'albums', 'artists', 'playlists' or 'tracks' by using a query.
It accepts 3 parameters:

>* `at`: Which is the Access_Token
>* `query`: Add the word you’re looking for.
>* `search_type`: Specify if your looking for an 'album', 'artist', 'playlist' or 'track'

For example, if I want to get the album cover of the latest Harry Styles album this is what I would do:

```python
# This call will return a json() file with the results of the query.
albums = search_spotify(at= access_token, query="Fine Line", search_type='album')

# We work with the json file to get exactly the piece of information we want
album_cover = albums["albums"]["items"][0]["images"][1]["url"]

print(album_cover)
'https://i.scdn.co/image/ab67616d00001e0277fdcfda6535601aff081b6a'
```
<img src="https://i.scdn.co/image/ab67616d00001e0277fdcfda6535601aff081b6a" alt="MarineGEO circle logo" style="height: 80px; width:80px;
  display: block;
  margin-left: auto;
  margin-right: auto;"/>

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-search) to learn more about the "Search" module of the Spotify API.
>* If you want to test the "Search" API call in a Spotify Console click [**here**](https://developer.spotify.com/console/get-search-item/).

<br>


### **3.3** `get_list_of_albums()`
---
This function will return a list with all the albums from a single artist. The parameters that this function accepts are: 

>* `at`: Which is the Access_Token. REQUIRED
>* `artist`: String with the name of a single artist. OPTIONAL
>* `lookup_id`: ID of a single Artist. OPTIONAL.
>* `market`: Choose the country you would like to get the information from. The default is "US". OPTIONAL

><ins>**Notes:**</ins>
>* You must choose to use `artist` or `lookup_id` but not the two at the same time. 

Here's an example of how the function works:
```python
#If you decide to use "lookup_id" here's how the function would look like
get_list_of_albums(lookup_id="1vyhD5VmyZ7KMfW5gqLgo5", at=access_token)

#If you decide to use "artist" this is how the function should be called
get_list_of_albums(artist="Ed Sheeran", at=access_token)

list_of_ablums = get_list_of_albums(artist="Ed Sheeran", at=access_token)

print(list_of_ablums)

['3oIFxDIo2fwuk4lwCmFZCx','5oUZ9TEZR3wOdvqzowuNwl','3T4tUhGYeRNVUGevb0wThu',
 '2hyDesSAYNefikDJXlqhPE','1xn54DMo2qIqBuMqHtUsFd']
```

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-albums) to learn more about the information you can get from the "Albums" API call.

<br>

### **3.4** `album_information()`
---
This function returns key information about a list of album ids. The parameters that this function accepts are:

>* `list_of_albums`. A python list with all the albums that we want to transform into a dataset. REQUIRED.
>* `at`: Which is the Access_Token. REQUIRED
>* `market`: Choose the country you would like to get the information from. The default is "US". OPTIONAL

This function simultaneously will return a json file that can be used by other functions inside the `helper_func.py` file.

Here's an example of how to call this function:

```python
album_info_list, albums_json = album_information(list_of_albums = albums_ids, at=access_token) 

print(album_info_list)
```
Here's a preview of the returned dataframe:

|| name_of_album| album_id| album_url| album_genres| album_cover |   album_popularity| release_date|
|---:|:---|:---|:---|:---|:---|---:|:---|
| 0 | No.6 Collaborations Project | 3oIFxDIo2fwuk4lwCmFZCx | https://open.spotify.com/album/3oIFxDIo2fwuk4lwCmFZCx | []| https://i.scdn.co/image/ab67616d00001e0273304ce0653c7758dd94b259 | 85 | 2019-07-12 |
| 1 | No.6 Collaborations Project | 5oUZ9TEZR3wOdvqzowuNwl | https://open.spotify.com/album/5oUZ9TEZR3wOdvqzowuNwl | []| https://i.scdn.co/image/ab67616d00001e027ed2a6d678a53a5959b2894f | 55 | 2019-07-12 |
| 2 | ÷ (Deluxe)| 3T4tUhGYeRNVUGevb0wThu | https://open.spotify.com/album/3T4tUhGYeRNVUGevb0wThu |[]| https://i.scdn.co/image/ab67616d00001e02ba5db46f4b838ef6027e6f96 | 92 | 2017-03-03 |
<br>
><ins>**Notes:**</ins>
>* In addition of returning a dataframe, this function also returns a json file. This json is used by the `get_multiple_artists_from_albums()` and the `songs_information()` functions that I'm going to explain below.
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-albums) to learn more about the information you can get from the "Albums" API call.

<br>


### **3.5** `get_multiple_artists_from_albums()`
---
Some albums have more than 1 artist. This function creates a dataframe that creates new columns for each of the artists that collaborated on the album.

The only parameter this function accepts is:
>* `albums_json`: A json file previously generated when the `album_information()` function is called.  REQUIRED.

Here's an example of how that function would look like:

```python
# First we call the "album_information()" function.
album_info_list, albums_json = album_information(list_of_albums = albums_ids, at=access_token) 

# Once we have the json file that is returned from the "album_information()" function we can use "artists_in_ablums_()"
artists_in_ablums_= get_multiple_artists_from_albums(albums_json= albums_json)   

print(artists_in_ablums_)
```
Here's how the returned dataframe looks like:

|| album_id| album_name | album_artist1| album_artist1_id| album_artist2   | album_artist2_id | album_artist3 | album_artist3_id |
|---:|:---|:---|:---|:---|:---|:---|:---|:---|
| 0 | 02pi98kE0nra0yBqCStzbC | + | Ed Sheeran | 6eUKZXaKkcviH0Ku9w2n3V | nan | nan | nan | nan |
|1 | 05Bru0ZVTxp4orAyrZIA77 | South of the Border (feat. Camila Cabello & Cardi B) [Sam Feldt Remix] | Ed Sheeran| 6eUKZXaKkcviH0Ku9w2n3V | Cardi B | 4kYSro6naA4h99UJvo89HB | Sam Feldt | 20gsENnposVs2I4rQ5kvrf |
|  2 | 0W5GGnapMz0VwemQvJDqa7 | + | Ed Sheeran | 6eUKZXaKkcviH0Ku9w2n3V | nan | nan| nan | nan |
|  3 | 0Whkv3Bi9hP9ev2cFPlZR3 | Antisocial (with Travis Scott) [MK Remix]| Ed Sheeran| 6eUKZXaKkcviH0Ku9w2n3V | Travis Scott | 0Y5tJX1MQlPlqiwlOH1tJY | MK | 1yqxFtPHKcGcv6SXZNdyT9 |
| 4 | 1GHkv48TNqI8MKWJ1FwKFC | Remember The Name (feat. Eminem & 50 Cent)| Ed Sheeran | 6eUKZXaKkcviH0Ku9w2n3V | Eminem | 7dGJo4pcD2V6oG8kP0tJRR | 50 Cent| 3q7HBObVc0L8jNeTe5Gofh |

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-albums) to learn more about the information you can get from the "Albums" API call.


### **3.6** `songs_information()`
---
This function returns a dataframe with all the songs from an artist along with additional data from those songs and the function also returns a list with the unique ids from those songs.

The only parameter this function accepts is:
>* `albums_json`: A json file previously generated when the `album_information()` function is called.  REQUIRED.

Here's an example of how that function would look like:

```python
# First we call the "album_information()" function.
album_info_list, albums_json = album_information(list_of_albums = albums_ids, at=access_token) 

# Once we have the json file that is returned from the "album_information()" function we can use "songs_information()"
list_of_songs_, list_of_songs_tolist = songs_information(albums_json= albums_json)

print(list_of_songs_)
```
Here's an example of the dataframe that is returned after calling the `songs_information()` function.

|| album_id| song_id | name_of_song | duration | song_url | song_preview |
|---:|:---|:---|:---|---:|:---|:---|
|  0 | 3oIFxDIo2fwuk4lwCmFZCx | 70eFcWOvlMObDhURTqT4Fv | Beautiful People (feat. Khalid) | 197866 | https://open.spotify.com/track/70eFcWOvlMObDhURTqT4Fv | https://p.scdn.co/mp3-preview/3ad904af9567a7c7df7d23a8d6700296ded34b4f?cid=6d9cda272a144d6988f08949e9f4cad9 |
| 1 | 3oIFxDIo2fwuk4lwCmFZCx | 4vUmTMuQqjdnvlZmAH61Qk | South of the Border (feat. Camila Cabello & Cardi B) |204466 | https://open.spotify.com/track/4vUmTMuQqjdnvlZmAH61Qk | https://p.scdn.co/mp3-preview/686f1dc5c92030c8e4b48f94098386a89df4b06d?cid=6d9cda272a144d6988f08949e9f4cad9 |
| 2 | 3oIFxDIo2fwuk4lwCmFZCx | 4wuCQX7JvAZLlrcmH4AeZF | Cross Me (feat. Chance the Rapper & PnB Rock)| 206186 | https://open.spotify.com/track/4wuCQX7JvAZLlrcmH4AeZF | https://p.scdn.co/mp3-preview/b79732826d505f627cf3940f7c83cc50c41f9548?cid=6d9cda272a144d6988f08949e9f4cad9 |

```python
# Here's an example of the list of songs id's that is returned after calling the `songs_information()` function.
list_of_songs_, list_of_songs_tolist = songs_information(albums_json= albums_json)

print( list_of_songs_tolist[0:10] )

['70eFcWOvlMObDhURTqT4Fv','4vUmTMuQqjdnvlZmAH61Qk','4wuCQX7JvAZLlrcmH4AeZF',
 '1AI7UPw3fgwAFkvAlZWhE0','0VsGaRXR5WAzpu51unJTis','0hVXuCcriWRGvwMV1r5Yn9',
 '1DhRbox3xkceP64k3JeYfW','0AtP8EkGPn6SwxKDaUuXec','1Bdptrvb7nQkq8kCw3siE9',
 '5T03itPFOPGGkvVPvPiyla']
```
<br>

><ins>**Notes:**</ins>
>* The list of songs ids that is returned after calling the `songs_information()` function is used by the `artists_from_songs()` function that I'm going to discuss below.
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-albums) to learn more about the information you can get from the "Albums" API call.

<br>

### **3.7** `artists_from_songs()`
---
Some songs have more than 1 performer. This list creates a dataframe that adds new columns for each artist that was involved with the song.

This function accepts the next parameters:
>* `list_of_songs_ids`: A python list with the unique ids of songs. A list of these characteristics is generated after calling the `songs_information()` function. However, it works with any python list as long as it has the unique id's that Spotify assigns to each song.  REQUIRED.
>* `at`: The Access_Token. REQUIRED

Here's an example of how to call this function:

```python
artists_in_albums_, songs_json, artists_id_, songs_id_ = artists_from_songs(list_of_songs_ids= list_of_songs_tolist,at=access_token)
```

The function returns 4 different results. Each of them serves different purposes. In the above example, the `artists_in_albums_` variable returns the dataframe with a new column for each of the artists.

```python
print(artists_in_albums_)
```
Here's an example of the dataframe:
| | song_id | song_popularity | song_image | name_artist_1   | id_artist_1 | name_artist_2 | id_artist_2 | name_artist_3| id_artist_3 |   name_artist_4 | id_artist_4 |name_artist_5 | id_artist_5 |
|---:|:---|---:|:---|:----------------|:-----------------------|:---|:---|:---|:---|---:|---:|---:|---:|
|  0 | 0A2J5TumCpT4aJVvQHNEQW | 46 | https://i.scdn.co/image/| Ed Sheeran  6eUKZXaKkcviH0Ku9w2n3V |nan | nan | nan | nan                    | nan | nan | nan |nan |
|  1 | 0AtP8EkGPn6SwxKDaUuXec | 67 | https://i.scdn.co/image/ | Ed Sheeran      | 6eUKZXaKkcviH0Ku9w2n3V | Eminem | 7dGJo4pcD2V6oG8kP0tJRR | 50 Cent         | 3q7HBObVc0L8jNeTe5Gofh |nan | nan | nan |nan |
|  2 | 0CNrpbpJ9HsFffF9hqWIIe | 43 | https://i.scdn.co/image/ | Ed Sheeran  6eUKZXaKkcviH0Ku9w2n3V | nan | nan| nan | nan | nan | nan |nan |           nan |

The function also returns a list with all the artist’s id's. In my example I stored it in the variable called `artists_id_`. Here's an example of how that variable would look like if we printed it:

```python
artists_in_albums_, songs_json, artists_id_, songs_id_ = artists_from_songs(list_of_songs_ids= list_of_songs_tolist,at=access_token)

print( songs_id_ )

['50co4Is1HCEo8bhOyUWKpn','6LuN9FCkKOj5PcnpouEgny','1uNFoZAHBGtllmzznpCI3s',
 '1ooV8YZC1KbpEcrmI8WH0F','7zJL978NtANOysfGY21ty6','3q7HBObVc0L8jNeTe5Gofh',
 '6Ip8FS7vWT1uKkJSweANQK','2SrSdSvpminqmStGELCSNd','3vQ0GE3mI0dAaxIMYe5g7z',
 '2tAbkZSNg8OdcUVzSOrYRW']
```

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-artists) to learn more about the information you can get from the "Artists" API call.


### **3.8** `multiple_artists_songs()`
---
This function can return a dataframe with detailed information about an artist. 

The parameters that this function accepts are:
>* `at`: The Access Token
>* `list_of_artists_ids`: A python list with the id's that Spotify assigns to each artist. The function `list_of_songs_tolist()` returns a list with this characteristics.

Here's an example of how to call this function:

```python
artist_list_df= multiple_artists_songs(list_of_artists_ids=artists_id_,at=access_token)

print(artist_list_df)
```

Here's an example of the dataframe that this function returns:

<br>

|| id_artist| name_artist | url|   followers | image|   artist_popluarity | genre_0 | genre_1|genre_2 |genre_3 |genre_4 |genre_5 |genre_6 |genre_7 |   genre_8 |   genre_9 |
|---:|:---|:---|:---|---:|:---|---:|:---|:---|---:|---:|---:|---:|----:|---:|---:|---:|
|0| 0T2sGLJKge2eaFmZJxX7sq|Wretch 32| https://open.spotify.com/artist/0T2sGLJKge2eaFmZJxX7sq |262561| https://i.scdn.co/image/d4c5e537525f312ab1f9c73feb2a21c209919558 |59 | grime | uk hip hop |       nan |nan |nan |nan |nan |nan |nan |nan |
|  1 | 0Y5tJX1MQlPlqiwlOH1tJY | Travis Scott  | https://open.spotify.com/artist/0Y5tJX1MQlPlqiwlOH1tJY |15082068 | https://i.scdn.co/image/5801b0d47fbf34b228a1f800bb36a58eced54796 |95 | rap| slap house |nan |       nan |nan |nan |nan |nan |nan |nan |
|2| 0du5cEVh5yTK9QJze8zA0C | Bruno Mars| https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C |28703871 | https://i.scdn.co/image/aba91de7087e3b657cf11e98c45026ac6b7df544 |90 | pop| nan |nan |nan |       nan |nan |nan |nan |nan |nan |
<br>

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-artists) to learn more about the information you can get from the "Artists" API call.

### **3.9** `song_features()`
---
This function returns a dataframe with the features that Spotify assigns to each song.
The parameters that this function accept are:
>* `at`: The Access Token 
>* `list_of_songs_ids`: A python list with the unique id's that Spotify assigns to each track. The functions `list_of_songs_ids()` and `artists_from_songs()` return a list with this characteristisc.

Here's an example of how to call this function:

```python
song_features, songs_features_json= song_features(list_of_songs_ids=list_of_songs_tolist,at=access_token)

print( song_features )
```
And here's an example of the dataframe that is returned:
| | song_id| danceability|energy| key| loudness |mode | speechiness |   acousticness |instrumentalness |liveness |valence |tempo |
|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 103 | 1AI7UPw3fgwAFkvAlZWhE0 |0.885 |0.762 |8 |-5.513 | 0 |0.216 | 0.219 | 0 | 0.162 | 0.605 | 138.058 |
|118| 3ERZA2UXA1cD5WAELjSpa6 |0.885 |0.762 |8 |-5.513 |0 |0.216 |          0.219 |0 |0.162 | 0.605 | 138.059 |
|122| 663iGCIjbc3DfpGOooKvDR |0.863 |0.649 |11 |-7.194 |0 |0.156 |          0.196 |0 |0.783|0.761 |91.018 |

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-tracks) to learn more about the information you can get from the "Tracks" API call.

<br>

### **3.10** `playlist_data()`
---
This function returns a dataframe with key data about a particular playlist.
The parameters that this function accepts are:
>* `at`: The Access Token
>* `playlist_id`: The unique id that Spotify assigns to each playlist.

Here's an example of how to call the function.
```python
play_list_json_V2, empty_list_one_V2= playlist_data(at=access_token, playlist_id="37i9dQZF1DX0BcQWzuB7ZO")

print( empty_list_one_V2.head(3) )
```
Here's an example of how the dataframe that is returned would look like:

||song_id |playlist_id| playlist_url| playlist_followers| song_added_at| song_name|song_duration|song_popularity| song_url| name_artist_1 | id_artist_1 | name_artist_2 | id_artist_2| name_artist_3 |id_artist_3|   name_artist_4 |id_artist_4 |
|---:|:---|:---|:---|---:|:---|:---|---:|---:|:---|:---|:---|:---|:---|---:|---:|---:|---:|
|0| 06kxa3al7bUqRRo5nAFduZ|37i9dQZF1DX0BcQWzuB7ZO| https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO |3171104|2021-02-11T23:38:47Z | Nightlight |222400 |73 | https://open.spotify.com/track/06kxa3al7bUqRRo5nAFduZ | ILLENIUM | 45eNHdiiabvmbp4erw26rg | Annika Wells| 0kErUwb6xgWfkdn0RyZWHZ |nan |nan |nan |nan |
| 1 | 074x9OaRq8m4Kn3J3Qgavf | 37i9dQZF1DX0BcQWzuB7ZO | https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO |3171104 | 2021-02-11T23:38:47Z | 2AM |182400 |51 | https://open.spotify.com/track/074x9OaRq8m4Kn3J3Qgavf | MK| 1yqxFtPHKcGcv6SXZNdyT9 | Carla Monroe| 4S9LNSZusH3XflT3g32bqB |nan |nan |nan |nan |
|2| 0DmAvNCAK08oCi7miSZUIY|37i9dQZF1DX0BcQWzuB7ZO| https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO |3171104 | 2021-02-11T23:38:47Z | Lasting Lover |218358 |81| https://open.spotify.com/track/0DmAvNCAK08oCi7miSZUIY | Sigala| 1IueXOQyABrMOprrzwQJWN | James Arthur| 4IWBUUAFIplrNtaOHcJPRM |nan |nan |nan |nan |

><ins>**Notes:**</ins>
>* Click [**here**](https://developer.spotify.com/documentation/web-api/reference/#category-playlists) to learn more about the information you can get from the "Playlist" API call.



