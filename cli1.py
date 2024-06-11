import requests
import sys
from pydebugger.debug import debug
from jsoncolor import jprint
from make_colors import make_colors

# Configuration
API_KEY = '04122f3453fa4d6c92752849360626ae'
SERVER_URL = 'http://127.0.0.1:8096'

# Get list of devices
devices_url = f"{SERVER_URL}/emby/Sessions"
params = {
    'api_key': API_KEY
}
response = requests.get(devices_url, params=params)
data = response.json()
debug(data=data)
jprint(data)

DEVICE_ID_DATA = []
DEVICE_NAME_SELECTED = ""

# Display device IDs
for session in data:
    device_id = session.get('DeviceId')
    device_name = session.get('DeviceName')
    if device_id and device_name:
        print(f"Device Name: {device_name}, Device ID: {device_id}")
        DEVICE_ID_DATA.append([device_id, device_name])

if len(DEVICE_ID_DATA) > 1:
    n = 1
    for d in DEVICE_ID_DATA:
        print(
            make_colors(str(n).zfill(2), 'lc') + ". " +
            make_colors(d[1], 'b', 'y') + " " +
            make_colors(d[0], 'lw', 'bl')
        )
        n += 1

    q = input(make_colors("Select Device:", 'lw', 'r') + " ")
    if q and q.isdigit() and int(q) <= len(DEVICE_ID_DATA):
        DEVICE_ID = DEVICE_ID_DATA[int(q) - 1][0]
        DEVICE_NAME_SELECTED = DEVICE_ID_DATA[int(q) - 1][1]
else:
    DEVICE_ID = DEVICE_ID_DATA[0][0]
    DEVICE_NAME_SELECTED = DEVICE_ID_DATA[0][1]

# Get list of users
users_url = f"{SERVER_URL}/emby/Users"
params = {
    'api_key': API_KEY
}
response = requests.get(users_url, params=params)
data = response.json()
debug(data=data)
jprint(data)

USER_ID_DATA = []
# Display user IDs
for user in data:
    print(f"Username: {user['Name']}, User ID: {user['Id']}")
    USER_ID_DATA.append([user['Id'], user['Name']])

if len(USER_ID_DATA) > 1:
    n = 1
    for u in USER_ID_DATA:
        print(
            make_colors(str(n).zfill(2), 'lc') + ". " +
            make_colors(u[1], 'b', 'y') + " " +
            make_colors(u[0], 'lw', 'bl')
        )

    n += 1

    q = input(make_colors("Select user:", 'lw', 'r') + " ")
    if q and q.isdigit() and int(q) <= len(USER_ID_DATA):
        USER_ID = USER_ID_DATA[int(q) - 1][0]
else:
    USER_ID = USER_ID_DATA[0][0]

# Search term
search_query = sys.argv[1]

# Search for artists and albums
search_url = f"{SERVER_URL}/emby/Users/{USER_ID}/Items"
params = {
    'api_key': API_KEY,
    'searchTerm': search_query,
    'IncludeItemTypes': 'MusicAlbum,MusicArtist',
    'Recursive': 'true'
}
response = requests.get(search_url, params=params)
data = response.json()

# Extract and format results
results = []
for item in data['Items']:
    if item['Type'] == 'MusicAlbum':
        artist_name = item['AlbumArtist']
        album_name = item['Name']
        results.append((artist_name, album_name, item['Id']))

# Display results
for index, (artist_name, album_name, item_id) in enumerate(results, start=1):
    print(f"{index}. {artist_name} - {album_name} (ID: {item_id})")

# Prompt user to select an album
selected_index = int(input("Select number to play: ")) - 1
selected_album_id = results[selected_index][2]

# Verify the selected album ID
print(f"Selected album ID: {selected_album_id}")

# Get the user's active sessions
sessions_url = f"{SERVER_URL}/emby/Sessions"
sessions_response = requests.get(sessions_url, params={'api_key': API_KEY})
sessions_data = sessions_response.json()

# Find the session for the given device ID
session_id = None
for session in sessions_data:
    if session.get('DeviceId') == DEVICE_ID:
        session_id = session['Id']
        break

debug(session_id = session_id, debug = 1)
if not session_id:
    print("No active session found for the specified device.")
else:
    print(f"Using session ID: {session_id}")

    # Get media sources for the selected album
    media_sources_url = f"{SERVER_URL}/Users/{USER_ID}/Items/"
    debug(media_sources_url = media_sources_url)
    params = {
        'ParentId': selected_album_id,
        'Filters': 'IsNotFolder',
        'Recursive': 'true',
        'Limit': '1000',
        'Fields': 'Chapters,ProductionYear,PremiereDate,Container',
        'ExcludeLocationTypes': 'Virtual',
        'EnableTotalRecordCount': 'false',
        'CollapseBoxSetItems': 'false',
        'ProjectToMedia': 'true',
        'X-Emby-Client': 'Emby Web',
        'X-Emby-Device-Name': DEVICE_NAME_SELECTED,
        'X-Emby-Device-Id': DEVICE_ID,
        'X-Emby-Client-Version': '4.8.8.0',
        'X-Emby-Token': API_KEY,
        'X-Emby-Language': 'en-us'
    }
    debug(params = params)
    media_sources_response = requests.get(media_sources_url, params=params)
    debug(media_sources_response = media_sources_response, debug = 1)
    debug(media_sources_response = media_sources_response.content, debug = 1)
    jprint(media_sources_response.json())
    #sys.exit()
    
    # Debugging: check the response content
    print("Media sources response status code:", media_sources_response.status_code)
    print("Media sources response content:", media_sources_response.text)

    if media_sources_response.status_code == 200:
        media_sources_data = media_sources_response.json()
        #if 'MediaSources' in media_sources_data and media_sources_data['MediaSources']:
            #media_source_id = media_sources_data['MediaSources'][0]['Id']

        # Play the selected album
        play_url = f"{SERVER_URL}/Sessions/{session_id}/Playing"
        debug(play_url = play_url)
        play_payload = {
            "VolumeLevel":100,
            "IsMuted":"false",
            "IsPaused":"false",
            "RepeatMode":"RepeatNone",
            "Shuffle":"false",
            "SubtitleOffset":0,
            "PlaybackRate":1,
            "MaxStreamingBitrate":200000000,
            "PositionTicks":0,
            "PlaybackStartTimeTicks":17172987384900000,
            "SubtitleStreamIndex":-1,
            "BufferedRanges":[
                {
                    "start":0,
                    "end":836440630
                }],
            "SeekableRanges":[
                {
                    "start":0,
                    "end":836440630
                }],
            "PlayMethod":"Transcode",
            "PlaySessionId":"1717298630338",
            "MediaSourceId":"1805",
            "CanSeek":"true",
            "ItemId":"1805",
            "PlaylistIndex":0,
            "PlaylistLength":11,
            "NowPlayingQueue":[
                {"Id":"1805","PlaylistItemId":"playlistItem0"},
                {"Id":"1806","PlaylistItemId":"playlistItem1"},
                {"Id":"1807","PlaylistItemId":"playlistItem2"},
                {"Id":"1808","PlaylistItemId":"playlistItem3"},
                {"Id":"1809","PlaylistItemId":"playlistItem4"},
                {"Id":"1810","PlaylistItemId":"playlistItem5"},
                {"Id":"1811","PlaylistItemId":"playlistItem6"},
                {"Id":"1812","PlaylistItemId":"playlistItem7"},
                {"Id":"1813","PlaylistItemId":"playlistItem8"},
                {"Id":"1814","PlaylistItemId":"playlistItem9"},
                {"Id":"1815","PlaylistItemId":"playlistItem10"}
            ]}
        
        debug(play_payload = play_payload, debug = 1)
        headers = {
            'X-Emby-Token': API_KEY
        }
        debug(headers = headers)
        play_response = requests.post(play_url, json=play_payload, headers=headers)
        debug(play_response = play_response, debug = 1)
        debug(play_response = play_response.content, debug = 1)
    
        # Debugging: print response details
        print("Response status code:", play_response.status_code)
        print("Response content:", play_response.text)
    
        if play_response.status_code == 200:
            print("Playing selected album...")
        elif play_response.status_code == 204:
            print("Playback command accepted but no content to return.")
        else:
            print("Failed to play selected album.")
        #else:
            #print("No media sources found for the selected album.")
    else:
        print("Failed to retrieve media sources for the selected album.")
