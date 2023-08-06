# Fn-api.com Python Library  :

- for help you can enter our discord server [Fn-api](https://discord.gg/YNXhEn3XGt)
----------------------------------------------------------------------------------------------------------------------------------
```
from FNAPILIB import *

api = FNapi()
```
## language example :

 -  api.status(lang="en")
 -  api.status(lang="ar")

- ### default language is ENGLISH

# Supported languages
-  ar 
-  de 
-  en
-  es  
-  es-419  
-  fr  
-  it  
-  ja  
-  ko  
-  pl  
-  pt-BR  
-  ru  
-  tr

________________________________________
_______________________________________
## all cosmetics
```
api.allcosmetics()
```

### Parameters: 
- `language`[Optional]

##### Return :
###### data of all Fortnite Cosmetics.
--------------------------------------------------------

## Blogposts
```
api.Blogposts()
```
### Parameters:
- `language`[Optional]

##### Return :
- data of Fortnite's Blogposts and Fortnite Competitive Blogposts.
--------------------------------------------------------

## calendar
```
api.calendar()
```
### Parameters:
-  `None`

##### Return :
- data of the current Fortnite Calendar.
--------------------------------------------------------

## status
```
api.status()
```
### Parameters:
- `None`

##### Return :
- data of Fortnite's Server Status.
--------------------------------------------------------

## staging
```
api.staging()
```
### Parameters:
- `None`

##### Return :
- data of Fortnite's Staging/Dev Servers.
--------------------------------------------------------

## cloudStorage
```
api.cloudStorage()
```
### Parameters:
- `None`

##### Return :
- data of Fortnite's Cloud Storage.
--------------------------------------------------------

## cloudstorefile
```
api.cloudstorefile()
```
### Parameters:
- `filename` [Required]
- `example` : api.cloudstorefile(filename="Ver-13920814_DefaultEngine.ini")

##### Return :
- content of a specific Cloud Store file.
--------------------------------------------------------

## Emergency
```
api.Emergency()
```
### Parameters:
- `language`[Optional]

##### Return :
- data of Fortnite's Emergency Notices and General Issues.
--------------------------------------------------------

## radios
```
api.Radios()
```
### Parameters:
- `language`[Optional]

##### Return :
- data of Fortnite's Radio Stations.
--------------------------------------------------------

## backgrounds
```
api.backgrounds()
```
### Parameters:
- `None`

##### Return :
- data of Fortnite's In-Game Lobby.
--------------------------------------------------------

## news
```
api.news()
```
### Parameters:
- `language`[Optional]

##### Return :
- data of Fortnite's General news.
--------------------------------------------------------

## news_type
```
api.news_type()
```
### Parameters:
- `gameMode` : [Required]
-  Game Modes =  `(br,stw,creative)`
- `language`[Optional]

- `example` : api.news_type(game_mode="br")

##### Return :
- news data of a specific Fortnite Game Mode.
--------------------------------------------------------

## playlists
```
api.playlists()
```
### Parameters:
- language[Optional]

##### Return :
- data of all Fortnite Playlists.
--------------------------------------------------------

## active_playlists
```
api.active_playlists()
```
### Parameters:
- language[Optional]

##### Return :
- data of Fortnite's Currently Active Playlists.
--------------------------------------------------------

## playlist_search
```
api.playlist_search()
```
### Parameters:
- `playlistid`[Required]
- `example` : api.playlist_search(playlistid="Playlist_Love_Squads")

##### Return :
- data of a specific Fortnite Playlist.
--------------------------------------------------------

## shop_sections
```
api.shop_sections()
```
### Parameters:
- `language`[Optional]

##### Return :
- data of Fortnite's current Shop Sections.
--------------------------------------------------------

## stores
```
api.stores()
```
### Parameters:
- `language`[Optional]  

##### Return :
- data of some stores that contains Fortnite.
--------------------------------------------------------

## store_select
```
api.store_select()
```
### Parameters:
- `storename`[Required ] 
- **stores** : `( epicgames, playstation, nintendoswitch )`

##### Return :
- data of Fortnite from a specific store.
--------------------------------------------------------

## stream
```
api.stream()
```
### Parameters:
- `stream_id`: [Required]
- `language`[Optional] 

- `example` : api.stream(stream_id="pjNcFLxWpoysrGkood")

##### Return :
- data of a Fortnite Stream.
--------------------------------------------------------

## aes
```
api.aes()
```
### Parameters:
- `None`

##### Return :
- data of Dynamic Pak Aes keys.
--------------------------------------------------------

## map
```
api.map()
```
### Parameters:
- `language`[Optional] 

##### Return :
- data of current Fortnite Map information.
--------------------------------------------------------

## rarities
```
api.rarities()
```
### Parameters:
- `language`[Optional]  

##### Return :
- data of all Fortnite Rarities and Series.
--------------------------------------------------------

## sections_list
```
api.sections_list()
```
### Parameters:
- `language`[Optional]  

##### Return :
- list of all Fortnite Shop Sections.
--------------------------------------------------------

## trello
```
api.trello()
```
### Parameters:
- `None`

##### Return :
- data of Fortnite's Trello page.
--------------------------------------------------------

- # Premium ![image](https://user-images.githubusercontent.com/86381194/132698076-8dffebcd-34e4-4eea-852f-7df5a4b839ef.png)


## weapons
```
api.weapons() 
```
### Parameters:
- `language`[Optional]  
- `auth`[Required ]
- `example`: api.weapons(auth="your Premium token here")

##### Return :
###### list of all Fortnite Weapons
--------------------------------------------------------

## NPCs
```
api.npcs() 
```
### Parameters:
- language[Optional]
- auth[Required ]
- `example`: api.weapons(auth="your Premium token here")

##### Return :
- list of all Fortnite npcs
--------------------------------------------------------------------------------------------

- Fn-api discord : **[FN-API](https://discord.gg/YNXhEn3XGt)**
- Powered By : ![image](https://user-images.githubusercontent.com/86381194/132597270-ca520e56-de2f-422c-b75c-efa7702c5cdd.png)
___________________________________________________________________________________
___________________________________________________________________________________
___________________________________________________________________________________
# Information
# FN-api.com developers :
- **command**
- **caser**
- #### THE LIBRARY DEV : **[LKST1](https://twitter.com/Leaks_station)**
