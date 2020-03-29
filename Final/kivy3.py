import threading
import time
import webbrowser
import os
from googleapiclient.discovery import build
import pandas as pd
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

kv = """
#:import Factory kivy.factory.Factory

<Row@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    Label:
        text: root.value
<CustomDropdown@DropDown>:
    id: dropdown
    on_select:
        app.root.ids.bt1.text = '{}'.format(args[1])
        
    Button:
        id: btn1
        text: '2'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('2')

    Button:
        id: btn2
        text: '4'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('4')
    Button:
        id: btn3
        text: '6'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('6')
        
    Button:
        id: btn4
        text: '8'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('8')
        
    Button:
        id: btn5
        text: '10'
        size_hint_y: None
        height: '48dp'
        on_release:dropdown.select('10')

<DelayDropdown@DropDown>:
    id: delaydrop
    on_select:
        app.root.ids.bt2.text = '{}'.format(args[1])
        
    Button:
        id: d1
        text: '30'
        size_hint_y: None
        height: '48dp'
        on_release:delaydrop.select('30')

    Button:
        id: d2
        text: '60'
        size_hint_y: None
        height: '48dp'
        on_release:delaydrop.select('60')
    Button:
        id: d3
        text: '90'
        size_hint_y: None
        height: '48dp'
        on_release:delaydrop.select('90')
        
    Button:
        id: d4
        text: '120'
        size_hint_y: None
        height: '48dp'
        on_release:delaydrop.select('120')
        
<CDropdown@DropDown>:
    id: ddown
    on_select:
        app.root.ids.bt3.text = '{}'.format(args[1])
        
    Button:
        id: b1
        text: 'Videos'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Videos')
        
    Button:
        id: b2
        text: 'Puzzles'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Puzzles')
        
    Button:
        id: b3
        text: 'Jokes'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Jokes')
    Button:
        id: b4
        text: 'News'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('News')
    Button:
        id: b5
        text: 'Games'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Games')
            
<GenreDropdown@DropDown>:
    id: gdown
    on_select:
        app.root.ids.gtn.text = '{}'.format(args[1])
        
    Button:
        id: g1
        text: 'Videos'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            gdown.select('Videos')
        
    Button:
        id: g2
        text: 'Puzzles'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            gdown.select('Puzzles')
        
    Button:
        id: g3
        text: 'Jokes'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            gdown.select('Jokes')
    Button:
        id: g4
        text: 'News'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('News')
    Button:
        id: g5
        text: 'Games'
        size_hint_y: None
        height: '48dp'
        
        on_release:
            ddown.select('Games')

<TBreak>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Queue'
            on_press: root.queue()
        Button:
            text: 'Shuffle'
            on_press: root.shuffle()
        Button:
            text: 'Reset'
            on_press: root.resetHistory(bt3.text)
        BoxLayout:
            spacing: dp(8)
            Button:
                text: "Start/Stop"
                on_press: root.play(bt1.text,bt2.text)
            
        BoxLayout:
            spacing: dp(8)
            Button:
                text: "Next"
                on_press: root.proceed()
        BoxLayout:
            spacing: dp(8)           
            Button:
                text: 'History'
                on_press: root.history()
    GridLayout:
        cols: 3
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(8)
        BoxLayout:
            spacing: dp(8)
            Button:
                id: bt1
                text: 'Select timing in hours'
                on_release: Factory.CustomDropdown().open(self)
                size_hint_y: None
                height: '30dp'
        BoxLayout:
            spacing: dp(8)
            Button:
                id: bt2
                text: 'Select delay in minutes'
                on_release: Factory.DelayDropdown().open(self)
                size_hint_y: None
                height: '30dp'
        BoxLayout:
            spacing: dp(8)
            Button:
                id: bt3
                text: 'Select genre for Queue'
                on_release: Factory.CDropdown().open(self)
                size_hint_y: None
                height: '30dp'
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(40)
        padding: dp(8)
        spacing: dp(8)
        BoxLayout:
            spacing: dp(8)
            Label:
                text: ('[b]Add to Playlist[/b]')
                markup: True
                font_size:'15pt'
        
    GridLayout:
        cols: 4
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        BoxLayout:
            spacing: dp(8)
            TextInput:
                id: name_input
                size_hint_x: 0.6
                hint_text: 'Name'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            TextInput:
                id: url_input
                size_hint_x: 0.6
                hint_text: 'Url*'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            Button:
                id: gtn
                text: 'Select genre'
                on_release: Factory.GenreDropdown().open(self)
                size_hint_y: None
                height: '30dp'
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Add'
                on_press: root.additem('Playlist added',name_input.text,url_input.text,gtn.text)
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(40)
        padding: dp(8)
        spacing: dp(8)
        BoxLayout:
            spacing: dp(5)
            Label:
                id: updlbl
                text:'Please press add button to add to playlist' if gtn.text!='Select genre' and url_input.text!='' else 'Please add playlist url and genre'
                
                font_size:'10pt'
                
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        BoxLayout:
            spacing: dp(8)
            Button:
                text: "Exit"
                on_press: root.close()

    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: 'Row'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)
"""

# To load the string above. It contains everything related to the GUI
Builder.load_string(kv)


# Function to reset the cache created because of the App
def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


# Function to get the details using the url_list and genre for youtube videos.
# Parameters:
#   url_list <- Should be a list of youtube urls. The urls can be of a video, playlist or a channel.
#   genre <- Should be the genre specified by the user for the urls provided.
def youtubeOperations(url_list, genre):
    youTubeApiKey = "AIzaSyBPzZFvrWZdaHPrWrYfp8km-zGuTMJM-Qw"
    youtube = build('youtube', 'v3', developerKey=youTubeApiKey)

    # Loop to handle every type of video separately.
    for url in url_list:
        url_check = url.split('/')[3]

        # Check to verify whether the url should be treated as a youtube channel.
        if 'channel' == url_check:
            channelId = url.split('/')[4]
            contentdata = youtube.channels().list(id=channelId, part='contentDetails').execute()
            playlist_id = contentdata['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            videos = []
            next_page_token = None

            while 1:
                res = youtube.playlistItems().list(playlistId=playlist_id,
                                                   part='snippet',
                                                   maxResults=50,
                                                   pageToken=next_page_token).execute()
                videos += res['items']
                next_page_token = res.get('nextPageToken')

                if next_page_token is None:
                    break

            video_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], videos))
            stats = []

            for i in range(0, len(video_ids), 40):
                res = (youtube).videos().list(id=','.join(video_ids[i:i + 40]), part='statistics').execute()
                stats += res['items']

            sNo = []
            title = []
            views = []
            url = []
            mainListSize = TBreak.mainDF.shape[0]

            # Storing info of every video present in the channel to lists.
            for i in range(len(videos)):
                sNo.append(mainListSize + i)
                title.append((videos[i])['snippet']['title'])
                url.append("https://www.youtube.com/watch?v=" + (video_ids[i]))
                views.append(int((stats[i])['statistics']['viewCount']))

            # Using the lists to creata a DataFrame. This DataFrame will be directly appended to the mainDF.
            data = {'id': sNo, 'title': title, 'url': url, 'views': views}
            df_to_append = pd.DataFrame(data)
            df_to_append['genre'] = genre
            TBreak.mainDF = TBreak.mainDF.append(df_to_append)

        # Check to verify whether the current url is a youtube video.
        elif 'watch?v=' in url_check:
            id_string = ''

            # When the video which is being added is a part of a playlist, the url works differently.
            # Condition to check whether the video is part of a playlist and getting the unique id.
            if '&list=' in url:
                id_string = url.split('=')[1].split('&list')[0]
            else:
                id_string = url.split('=')[1]

            list_videos_byid = youtube.videos().list(
                id=id_string,
                part="id, snippet, contentDetails, statistics",
            ).execute()

            # extracting the results from search response
            results = list_videos_byid.get("items", [])
            sNo = []
            title = []
            views = []
            url = []
            mainListSize = TBreak.mainDF.shape[0]

            # Storing info of every video present in the channel to lists.
            for i in range(len(results)):
                sNo.append(mainListSize+i)
                title.append(results[i]["snippet"]["title"])
                url.append('https://www.youtube.com/watch?v='+id_string.split(',')[i])
                views.append(results[i]["statistics"]['viewCount'])

            # Using the lists to creata a DataFrame. This DataFrame will be directly appended to the mainDF.
            data = {'id': sNo, 'title': title, 'url': url, 'views': views}
            df_to_append = pd.DataFrame(data)
            df_to_append['genre'] = genre
            TBreak.mainDF = TBreak.mainDF.append(df_to_append)

        # Check to verify whether the current url is a youtube playlist.
        elif 'playlist?list=' in url_check:
            playlistId = url.split('=')[1]
            res = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlistId,
                maxResults="50"
            ).execute()
            nextPageToken = res.get('nextPageToken')

            while ('nextPageToken' in res):
                nextPage = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlistId,
                    maxResults="50",
                    pageToken=nextPageToken
                ).execute()
                res['items'] = res['items'] + nextPage['items']

                if 'nextPageToken' not in nextPage:
                    res.pop('nextPageToken', None)
                else:
                    nextPageToken = nextPage['nextPageToken']

            sNo = []
            title = []
            views = []
            url = []
            mainListSize = TBreak.mainDF.shape[0]

            # Storing info of every video present in the channel to lists.
            for i in range(len(res['items'])):
                sNo.append(mainListSize + i)
                title.append(res['items'][i]['snippet']['title'])
                url.append('https://www.youtube.com/watch?v=' + res['items'][i]['snippet']['resourceId']['videoId'])
                views.append(0)

            # Using the lists to creata a DataFrame. This DataFrame will be directly appended to the mainDF.
            data = {'id': sNo, 'title': title, 'url': url, 'views': views}
            df_to_append = pd.DataFrame(data)
            df_to_append['genre'] = genre
            TBreak.mainDF = TBreak.mainDF.append(df_to_append)

        else:
            print('Unknown Item')


# TBreak: It contains every function which will be triggered when the user interacts with the GUI
class TBreak(BoxLayout):
    workdir = os.getcwd()
    mainDF = pd.read_csv(workdir + '//YoutubeList.csv')
    historyDF = pd.read_csv(workdir + '//History.csv')
    queueDF = pd.read_csv(workdir + '//Queue.csv')
    playFlag = False
    delay = 60
    shuffleFlag = False
    run_duration = 3 * 60 * 60
    selectedGenre = 'NA'

    # updateQueue: This function is used to populate the queue in case there are no items present in the queue
    def updateQueue(self):
        # Condition to check whether queue is empty.
        if TBreak.queueDF.shape[0] == 0:
            # In case no genre has been selected by the user to be played.
            if TBreak.selectedGenre == 'NA':
                TBreak.queueDF = TBreak.queueDF.append(TBreak.mainDF)
            # If a genre has been selected from the dropdown.
            else:
                TBreak.queueDF = TBreak.queueDF.append(
                    TBreak.mainDF.loc[(TBreak.mainDF.genre == TBreak.selectedGenre), :])

    # queue: This function displays the items present in queue to the user in the GUI
    # This function is triggered when the button 'Queue' is pressed in the GUI
    def queue(self):
        # Calling updateQueue function in the beginning to populate the list in case the list is empty.
        TBreak.updateQueue(self)
        self.rv.data = [{'value': TBreak.queueDF.iloc[i, 1]}
                        for i in range(0, len(TBreak.queueDF.index))]

    # shuffle: This function shuffles the items present in the queue. Pressing the button again will arrange them
    # according to their ids.
    # This function is triggered when the button 'Shuffle' is pressed in the GUI
    def shuffle(self):
        # Calling updateQueue function in the beginning to populate the list in case the list is empty.
        TBreak.updateQueue(self)
        # Check if the list is in shuffled state or not and make the changes in the list accordingly.
        if TBreak.shuffleFlag:
            TBreak.queueDF = TBreak.queueDF.sort_values('id')
            TBreak.shuffleFlag = False
        else:
            TBreak.queueDF = TBreak.queueDF.sample(frac=1)
            TBreak.shuffleFlag = True

    # resetHistory: This functions resets the queue as well as history.
    # This function is triggered when the button 'Reset' is pressed in the GUI
    def resetHistory(self, queueGenre):
        TBreak.historyDF = TBreak.historyDF.iloc[0:0]
        TBreak.queueDF = TBreak.queueDF.iloc[0:0]
        if queueGenre != 'Select genre for Queue':
            TBreak.selectedGenre = queueGenre
        TBreak.updateQueue(self)
        self.rv.data = []

    # playForThread: This function is to be run using a thread. The behaviour of the play is defined in this function.
    def playForThread(self, run_duration, delay):
        TBreak.updateQueue(self)
        currentWait = 0

        # Check if the playFlag is True. If it is true, the loop should work till the queue is empty or the run time
        # defined by the user has expired.
        while TBreak.playFlag:
            if currentWait == run_duration:
                TBreak.playFlag = False
                break
            if TBreak.queueDF.shape[0] == 0:
                TBreak.playFlag = False
                break
            # To make sure that the video is played after the exact duration specified by the user.
            if currentWait % delay == 0 and currentWait != 0:
                # Selecting the current url, executing it, adding it to the history and removing it from the queue.
                link = TBreak.queueDF.iloc[0, 2]
                webbrowser.open(link)
                TBreak.historyDF = TBreak.historyDF.append(TBreak.queueDF.iloc[0, :])
                TBreak.queueDF = TBreak.queueDF.drop(TBreak.queueDF.index[0])

                # To pop the first item which is being displayed in the GUI
                if self.rv.data:
                    self.rv.data.pop(0)

            time.sleep(0.5)
            currentWait = currentWait + 0.5

    # play: This function plays or stops the current queue.
    # This function is triggered when the button 'Start/Stop' is pressed
    # Parameters:
    #   run_duration: This variable is the option selected in the 3rd row, 1st column. (Select timing in hours)
    #   delay: This variable is the option selected in the 3rd row, 2st column. (Select delay in minutes)
    def play(self, run_duration, delay):

        # Getting the values from the dropdown only if has been changed.
        if run_duration != 'Select timing in hours':
            TBreak.run_duration = int(run_duration) * 60 * 60

        # Getting the values from the dropdown only if has been changed.
        if delay != 'Select delay in minutes':
            TBreak.delay = int(delay) * 60

        # Starting the thread
        t1 = threading.Thread(target=TBreak.playForThread, args=(self, TBreak.run_duration, TBreak.delay,))

        # Switching the flags when the button is pressed in the GUI. It helps us control the flow of the process which
        # is being executed in thread t1.
        if TBreak.playFlag:
            TBreak.playFlag = False
        else:
            TBreak.playFlag = True
            t1.start()

    # proceed: This function lets us skip the next item present in the queue.
    # This function is triggered when the button 'Next' is pressed.
    def proceed(self):
        TBreak.queueDF = TBreak.queueDF.drop(TBreak.queueDF.index[0])
        # To pop the first item which is being displayed in the GUI
        if self.rv.data:
            self.rv.data.pop(0)

    # history: This function lets us view the items present in the history using the GUI.
    # This function is triggered when the button 'History' is pressed.
    def history(self):
        self.rv.data = [{'value': TBreak.historyDF.iloc[i, 1]}
                        for i in range(0, len(TBreak.historyDF.index))]

    # additem: This function controls how the url provided by the user is going to be handled.
    # This function is triggered when the button 'Add' is pressed.
    # Parameters:
    #   text:
    #   name: Name of the url provided in the first textInput box of the Interface
    #   url: List of urls provided in the second textInput box of the Interface
    #   genre: Genre of the urls provided in the third textInput box of the Interface
    def additem(self, text, name, url, genre):
        self.ids.updlbl.text = 'Please wait while the items are being added to the database'
        youtube_flag = True

        # Verifying whether the url and genre has been entered by the user when the name field is left blank.
        if name == '' and url != "" and genre != "":
            url_list = url
            url_list = url_list.replace(' ', '').split(',')

            # Iterating through all the urls present in the text box.
            for url in url_list:

                # Check if all the links are from youtube.
                if 'https://www.youtube' not in url:
                    youtube_flag = False

            # Call the 'youtubeOperations' function only when the flag is True.
            if youtube_flag:
                youtubeOperations(url_list, genre)
                self.ids.updlbl.text = 'Items added successfully'

            else:
                sNo = []
                title = []
                views = []
                url = []
                mainListSize = TBreak.mainDF.shape[0]

                # Storing info of every video present in the channel to lists.
                for i in range(len(url_list)):
                    sNo.append(mainListSize + i)
                    title.append(str(genre + ' ' + str(mainListSize + i)))
                    url.append(url_list[i])
                    views.append(0)

                # Using the lists to creata a DataFrame. This DataFrame will be directly appended to the mainDF.
                data = {'id': sNo, 'title': title, 'url': url, 'views': views}
                df_to_append = pd.DataFrame(data)
                df_to_append['genre'] = genre
                TBreak.mainDF = TBreak.mainDF.append(df_to_append)
                self.ids.updlbl.text = 'Items added successfully'


        # In case name has been entered with other details.
        elif name != '' and url != "" and genre != "":
            name_list = name.replace(' ', '').split(',')
            url_list = url.replace(' ', '').split(',')

            if len(name_list) == len(url_list):
                sNo = []
                title = []
                views = []
                url = []
                mainListSize = TBreak.mainDF.shape[0]

                # Storing info of every video present in the channel to lists.
                for i in range(len(url_list)):
                    sNo.append(mainListSize + i)
                    title.append(name_list[i])
                    url.append(url_list[i])
                    views.append(0)

                # Using the lists to creata a DataFrame. This DataFrame will be directly appended to the mainDF.
                data = {'id': sNo, 'title': title, 'url': url, 'views': views}
                df_to_append = pd.DataFrame(data)
                df_to_append['genre'] = genre
                TBreak.mainDF = TBreak.mainDF.append(df_to_append)
                self.ids.updlbl.text = 'Items added successfully'

            else:
                self.ids.updlbl.text = 'Items not added. Please enter the same no. of names or leave it blank'

        # In case url or genre has been left empty.
        elif url == '' or genre == '':
            self.ids.updlbl.text = 'Items not added. Either URL or Genre is missing.'

        # To handle any other condition.
        else:
            self.ids.updlbl.text = 'Items not added. Situation not handled.'



    # close: This function wraps up the session and saves the current state of the application in csv and text files.
    # This function is triggered when the button 'Exit' is pressed.
    def close(self):
        TBreak.mainDF.to_csv(TBreak.workdir + '//YoutubeList.csv', index=False)
        TBreak.historyDF.to_csv(TBreak.workdir + '//History.csv', index=False)
        TBreak.queueDF.to_csv(TBreak.workdir + '//Queue.csv', index=False)
        TBreak.playFlag = False
        time.sleep(0.5)
        App.get_running_app().stop()
        Window.close()


class TakebreakApp(App):
    def build(self):
        return TBreak()


reset()

if __name__ == '__main__':
    TakebreakApp().run()
