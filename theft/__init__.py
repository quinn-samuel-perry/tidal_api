#!/usr/bin/env python2

import requests
import json
import subprocess

class Session():
    def __init__(s):
        s.login_token = '' #use login key
        s.music_token = 'P5Xbeo5LFvESeDy6' #these were borrowed from somewhere else
        s.ios_token   = 'GvFhCVAYp3n43EN3' #ditoo
        s.ios_unique_key    = '8ED5FAF9-10ED-4C34-V43V-284F2BB801C3'
        s.username    = 
        s.password    = 
        s.api_url     = 'https://api.tidalhifi.com/v1/'
        s.seshId      = None

        s.param_def   = {'countryCode':'AU',
                            'token':s.music_token}

    def add_dicts(s,dict1,dict2):
        #lazy way to add two dicts together
        return dict(dict1.items() + dict2.items())

    def debug_print(s, msg):
        print '[*]',msg

    def pretty_json(s,j):
        return json.dumps(j,indent=4,sort_keys=True)

    def login(s):
        s.debug_print('logging in...')
        url = s.api_url + 'login/username/'
        params = {'token':s.login_token,'clientVerison':'1.3.0'}
        payload = {'username':s.username,'password':s.password}

        r = requests.post(url,data=payload,params=params)
        r.raise_for_status()
        j = r.json()
        if j['sessionId'] != None:
            s.debug_print('login successful')
        s.seshId = j['sessionId']

    def getAlbum(s,id):
        id=str(id)
        s.debug_print('getting album details')
        
        url = s.api_url + 'albums/'+id
        params = s.add_dicts({},s.param_def)
        
        r = requests.get(url,params=params)
        j = r.json()
        
        #print s.pretty_json(j)
        return j['title'],j['numberOfTracks'],j['audioQuality']

    def getAlbumTracks(s,id,limit=10):
        id=str(id)
        s.debug_print('getting album details, limit=' + str(limit))
        
        url = s.api_url + 'albums/'+id+'/tracks'
        params = s.add_dicts({'limit':limit},s.param_def)
        
        r = requests.get(url,params=params)
        j = r.json()
        #print s.pretty_json(j)
        tracks = []
        for x in j['items']:
            tracks.append([ x['id'], 
                            x['title']])
        return tracks

    def getStreamUrl(s,id,quality='HIGH'):
        id=str(id)
        s.debug_print('fetching song url ' + id + '...')
        
        url = s.api_url + 'tracks/'+id+'/streamUrl'


        if quality == 'HIGH':
            params = s.add_dicts({'sessionId':s.seshId,
                    'soundQuality':quality},s.param_def)
        elif quality == 'LOSSLESS':
            params = s.add_dicts({'sessionId':s.seshId,
                    'soundQuality':quality},s.param_def)

        r = requests.get(url,params=params)
        j = r.json()
        
        if quality == 'HIGH':
            #print s.pretty_json(j)
            return j['url']
        else:
            #print s.pretty_json(j)
            return

    def download(s,id,output,stream):
        id=str(id)
        while True:
            try:
                f = open('lock','a')
                break
            except IOError as e:
                pass

        f.write(id+'\n')
        f.close()
        print "[+] set lock"
        
        output = 'downloads/' + output + '.aac'
        print "[+] downloading %s to %s from %s" % (id,output,stream)
        subprocess.call(['ffmpeg','-hide_banner','-y','-i','rtmp://'+stream,output])
        
        while True:
            try:
                f = open('lock','a')
                break
            except IOError as e:
                pass

        d=f.readlines()
        f.seek(0)
        for i in d:
            if id not in i:
                f.write(i)
        f.truncate()
        f.close()
        print "[+] removed lock"
