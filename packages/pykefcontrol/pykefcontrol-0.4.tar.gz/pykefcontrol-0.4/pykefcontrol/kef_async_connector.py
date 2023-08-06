from re import A
import aiohttp
from aiohttp.typedefs import StrOrURL



class KefAsyncConnector():
    def __init__(self, host):
        self.host = host
        self._session = aiohttp.ClientSession()
        self.previous_volume = 15 # Hardcoded previous volume, in case unmute is used before mute

    async def power_on(self):
        """power on speaker """
        await self.set_status('powerOn')
    
    async def shutdown(self):
        """ Shutdown speaker """
        await self.set_source("standby")

    async def mute(self):
        """mute speaker"""
        self.previous_volume = await self.volume
        await self.set_volume(0)
    
    async def unmute(self):
        """unmute speaker"""
        await self.set_volume(self.previous_volume)

    async def toggle_play_pause(self):
        """Toogle play/pause"""
        await self._track_control("pause")

    async  def next_track(self):
        """Next track"""
        await self._track_control("next")

    async def previous_track(self):
        """Previous track"""
        await self._track_control("previous")        

    async def _track_control(self, command):
        """toogle play/pause"""
        payload = {
            "path": "player:player/control",
            "roles": "activate",
             "value": """{{"control":"{command}"}}""".format(command=command)
        }

        async with self._session.get( "http://" + self.host +"/api/setData", params=payload) as response :
            json_output = await response.json()

    async def _get_player_data(self):
        """get data about currently playing media"""
        payload = {
            "path": "player:player/data",
            "roles": "value",
        }

        async with self._session.get( "http://" + self.host +"/api/getData", params=payload) as response :
            json_output = await response.json()

        return json_output[0]

    async def set_source(self, source):
        """Set spaker source, if speaker in standby, it powers on the speaker.
        Possible sources : wifi, bluetooth, tv, optic, coaxial or analog"""
        payload = {
            "path": "settings:/kef/play/physicalSource",
            "roles": "value",
             "value": """{{"type":"kefPhysicalSource","kefPhysicalSource":"{source}"}}""".format(source=source)
        }

        async with self._session.get( "http://" + self.host +"/api/setData", params=payload) as response :
            json_output = await response.json()

    async def set_volume(self, volume):
        """Set speaker volume (between 0 and 100)"""
        payload = {
            "path": "player:volume",
            "roles": "value",
             "value": """{{"type":"i32_","i32_":{volume}}}""".format(volume=volume)
        }

        async with self._session.get( "http://" + self.host +"/api/setData", params=payload) as response :
            json_output = await response.json()

    

    async def get_song_information(self):
        """Get song title, album and artist"""
        song_data = await self._get_player_data()
        info_dict = dict()
        info_dict["title"] = song_data.get('trackRoles', {}).get('title')
        info_dict["artist"] = song_data.get('trackRoles', {}).get('mediaData',{}).get('metaData',{}).get('artist')
        info_dict["album"] = song_data.get('trackRoles',{}).get('mediaData',{}).get('metaData',{}).get('album')
        info_dict["cover_url"] = song_data.get('trackRoles',{}).get('icon',None)

        return info_dict


    @property
    async def mac_address(self):
        """Get the mac address of the Speaker"""
        payload = {
            "path": "settings:/system/primaryMacAddress",
            "roles": "value"
        }
        
        async with self._session.get( "http://" + self.host + "/api/getData", params=payload) as response :
             json_output = await response.json()

        return json_output[0]["string_"]

    @property
    async def speaker_name(self):
        """Get the friendly name of the Speaker"""
        payload = {
            "path": "settings:/deviceName",
            "roles": "value"
        }
        
        async with self._session.get( "http://" + self.host + "/api/getData", params=payload) as response :
            json_output = await response.json()
        
        return json_output[0]["string_"]

    @property  
    async def status(self):
        """Status of the speaker : standby or poweredOn"""
        payload = {
            "path": "settings:/kef/host/speakerStatus",
            "roles": "value"
        }

        async with self._session.get( "http://" + self.host +"/api/getData", params=payload) as response :
            json_output = await response.json()

        return json_output[0]['kefSpeakerStatus']

    @property
    async def is_playing(self):
        """Is the speaker currently playing """
        json_output = await self._get_player_data()
        return json_output['state'] == 'playing'

    @property
    async def song_length(self):
        """Song length in ms"""
        if await self.is_playing:
            json_output = await self._get_player_data()
            return json_output['status']['duration']
        else:
            return None

    @property
    async def song_status(self):
        """Progression of song"""
        payload = {
            "path": "player:player/data/playTime",
            "roles": "value",
        }

        async with self._session.get( "http://" + self.host +"/api/getData", params=payload) as response :
            json_output = await response.json()

        return json_output[0]['i64_']

    async def set_status(self, status):
        payload = {
            "path": "settings:/kef/play/physicalSource",
            "roles": "value",
             "value": """{{"type":"kefPhysicalSource","kefPhysicalSource":"{status}"}}""".format(status=status)
        }

        async with self._session.get( "http://" + self.host +"/api/setData", params=payload) as response :
            json_output = await response.json()

        
    @property
    async def source(self):
        """Speaker soe : standby (not powered on), wifi, bluetooth, tv, optic,
        coaxial or analog"""
        payload = {
            "path": "settings:/kef/play/physicalSource",
            "roles": "value",
        }

        async with self._session.get( "http://" + self.host +"/api/getData", params=payload) as response :
            json_output = await response.json()

        return json_output[0]['kefPhysicalSource']

    @property
    async def volume(self):
        """Speaker volume (1 to 100, 0 = muted)"""
        payload = {
            "path": "player:volume",
            "roles": "value",
        }

        async with self._session.get( "http://" + self.host +"/api/getData", params=payload) as response :
            json_output = await response.json()

        return json_output[0]['i32_']

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()

    async def main():
        spkr = KefAsyncConnector("192.168.124.46")
        print(await spkr.status)
        print(type(spkr))
        print('power on'.center(30,'='))
        await spkr.power_on()
        await asyncio.sleep(1.0)
        print(' mute '.center(30,'='))
        await spkr.mute()
        await asyncio.sleep(1.0)
        print(' unmute '.center(30,'='))
        await spkr.unmute()
        await asyncio.sleep(1.0)
        print(' play/pause '.center(30,'='))
        print(await spkr.is_playing)
        await spkr.toggle_play_pause()
        await asyncio.sleep(1.0)
        print(await spkr.is_playing)
        await asyncio.sleep(2.0)
        print(' play/pause '.center(30,'='))
        await spkr.toggle_play_pause()
        await asyncio.sleep(2.0)
        print(' next track '.center(30,'='))
        out = await spkr.get_song_information()
        print(out["title"])
        await spkr.next_track()
        await asyncio.sleep(2.0)
        out = await spkr.get_song_information()
        print(out["title"])
        await asyncio.sleep(2.0)
        print(' previous track '.center(30,'='))
        await spkr.previous_track()
        await asyncio.sleep(1.0)
        print(' song information '.center(30,'='))
        await spkr.get_song_information()
        await asyncio.sleep(1.0)
        print(' set_volume '.center(30,'='))
        await spkr.set_volume(10)
        print(await spkr.mac_address)
        print(await spkr.speaker_name)
        print(await spkr.status)
        print(await spkr.is_playing)
        print(await spkr.song_length)
        print(await spkr.source)
        print(await spkr.volume)
        await asyncio.sleep(1.0)
        print(' source '.center(30,'='))
        await spkr.set_source("bluetooth")
        await asyncio.sleep(3.0)
        print(await spkr.source)
        print(' shutdown '.center(30,'='))       
        await spkr.shutdown()
        await spkr._session.close()
    # asyncio.ensure_future(main())
    loop.run_until_complete(main())