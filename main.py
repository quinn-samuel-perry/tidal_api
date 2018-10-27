#! /usr/bin/env python2
import theft
import threading

#need to add tagging

def run(albums):
	threads = []
	for album in albums:
		print "[*] downloading %s" % album
		title, notracks, qual = sesh.getAlbum(album)
		tracks = sesh.getAlbumTracks(album,limit=notracks)

		#id,title,stream
		#trix = []
		for x in tracks:
			#print "starting %s : %s" %(x[0], x[1])
			trix = sesh.getStreamUrl(x[0],quality='HIGH')
			t = threading.Thread(target=sesh.download, 
								args=(x[0],
									x[1],
									trix,))
			threads.append(t)
		for t in threads:
			t.start()

		for t in threads:
			t.join()	
		print "[*] album %s finished" % album


albums = [3390060]
sesh = theft.Session()
seshId = sesh.login()
print sesh.seshId
run(albums)
