# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import resources.lib.Utils as utils
import datetime
import urlparse
import time
import unicodedata
import os
import xbmc,xbmcgui,xbmcaddon,xbmcplugin

# Script constants
__addon__      = xbmcaddon.Addon()
__addonid__    = __addon__.getAddonInfo('id')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString
__cwd__        = __addon__.getAddonInfo('path')


def in_hours_and_min(minutes_string):
#twolaw code
    try:
        full_minutes = int(minutes_string)
        minutes = full_minutes % 60
        hours   = full_minutes // 60
        return str(hours) + 'h' + str(minutes).zfill(2)
    except:
        return ''

class Main:
    def __init__( self ):
        #utils.logMsg("version %s started / Parameter string: %s" % (__version__,sys.argv[2]),0)
        self._init_vars()
        #get params
        action = None
        #self.backend = None
        try:
         params = urlparse.parse_qs(sys.argv[2][1:].decode("utf-8"))
         #utils.logMsg("Parameter string: %s" % sys.argv[2])
        
         if params:        
            path=params.get("path",None)
            if path: path = path[0]
            limit=params.get("limit",None)
            if limit: limit = int(limit[0])
            else: limit = 25
            action=params.get("action",None)
            if action: action = action[0].upper()
        
         if action:
             if action == "GETGENRE":
                genre=params.get("genre",None)
                if genre: genre = genre[0]  
               
                genretype=params.get("genretype",None)
                if genretype: genretype = genretype[0]
                origtitle=params.get("title",None)
                if origtitle: origtitle = origtitle[0]    
                if origtitle and genre and genretype:
                    utils.getGenre(genre,genretype,origtitle)  
                
             if action == "GETSAGA":
                Id=params.get("id",None)
                if Id: Id = Id[0]  
                #start = time.time()                
                utils.CheckSaga(Id)
                #utils.logMsg("Temps passe GETSAGA :"+str(time.time()-start),0) 
                return  
                              
             if action == "GETTRAILER":
                Id=params.get("id",None)
                if Id: Id = Id[0] 
                trailertype=params.get("trailertype",None)
                if trailertype: trailertype = trailertype[0] 
                #utils.logMsg("Temps passe GETTRAILER :"+str(Id)+"/"+str(trailertype),0)                          
                utils.getTrailer(Id,trailertype)        

             if action == "GETCAST":
                Id=params.get("id",None)
                if Id: Id = Id[0] 
                castingtype=params.get("casttype",None)
                if castingtype: castingtype = castingtype[0]
                Id=xbmc.getInfoLabel("ListItem.DBID")              
                utils.getCasting(castingtype,Id)
                
                #utils.logMsg("Temps passe GETCAST :"+"["+str(Id)+"]["+str(castingtype)+"]:"+str(time.time()-start),0) 
                
             if action == "GETTVFILMACTEUR":
                Id=params.get("id",None)
                if Id: Id = Id[0] 
                infotype=params.get("infotype",None)
                if infotype: infotype = infotype[0]
                KodiLocal=params.get("local",None)
                start = time.time()                           
                if not KodiLocal: 
                    utils.getFilmsTv(infotype,Id)
                    #utils.logMsg("Temps passe GETTVFILMACTEUR TMDB:"+str(time.time()-start),0)
                else:
                    utils.getFilmsParActeur(xbmc.getInfoLabel("ListItem.DBTYPE"),Id)
                    #utils.logMsg("Temps passe GETTVFILMACTEUR LOCAL:"+str(time.time()-start),0)
                
                
             if action == "TVDIFFUSION":
                TvSe=xbmc.getInfoLabel("ListItem.Season")
                TvId=xbmc.getInfoLabel("ListItem.DBID")
                TvType=xbmc.getInfoLabel("ListItem.DBTYPE")
                #start = time.time()                  
                #utils.logMsg("TVDIFFUSION :"+str(TvId)+","+str(TvSe)+","+str(TvType),0) 
                utils.getDiffusionTV(TvId,TvSe,TvType)
                #utils.logMsg("Temps passe GETCAST :"+"["+str(Id)+"]:"+str(time.time()-start),0) 
                      

                     
                     
        except:
           params= {}
        
        try:
            params = dict( arg.split( '=' ) for arg in sys.argv[ 1 ].split( '&' ) )
        except:
            params = {}
        #utils.logMsg("params: %s" % params,0)
        self.backend = params.get( 'backend', False )
        self.trailer = params.get( 'trailer', False )

        
        # don't run if already in backend
        
        if not action :
            saga=""
            if self.backend and xbmc.getCondVisibility("IsEmpty(Window(home).Property(IconMixToolsbackend))"):
                # run in backend if parameter was set
                xbmc.executebuiltin("SetProperty(IconMixToolsbackend,true,home)")
                self.run_backend()
            
            if not self.backend and xbmc.getCondVisibility("Window.IsVisible(10000)"):
                   dialogC = xbmcgui.Dialog()
                   ret=dialogC.select("IconMixTools", [__language__( 32505 )+xbmc.getLocalizedString( 20434 ), __language__( 32505 )+xbmc.getLocalizedString( 20343 )])
                   if ret==0: saga="1"
                   if ret==1: saga="2"
                   
            
            if not self.trailer and not self.backend and ( xbmc.getInfoLabel("ListItem.DBTYPE")=="set" or xbmc.getInfoLabel("ListItem.DBTYPE")=="tvshow" or saga!=""):
                   if saga=="":
                     Unique="ok"
                   else:
                     Unique=""
                   if xbmc.getInfoLabel("ListItem.DBTYPE")=="set": saga="1"
                   else: 
                     if saga=="2" : saga=""
                   dialog = xbmcgui.Dialog()
                   if saga: 
                    Titre=xbmc.getLocalizedString( 20434 )
                   else :
                    Titre=xbmc.getLocalizedString( 20343 )
                   
                   if Unique: 
                     Unique=__language__( 32507 )+" ["+xbmc.getInfoLabel("ListItem.Label")+"]"
                     ret=dialog.select(Titre, [__language__( 32502 )+Titre, __language__( 32503 )+Titre,Unique])
                   else:
                     ret=dialog.select(Titre, [__language__( 32502 )+Titre, __language__( 32503 )+Titre])
                    #utils.logMsg("Retour: %s" % ret,0)
                   if ret==0: 
                    if saga: utils.UpdateSagas(0,1)
                    else : utils.UpdateSeries(0,1)
                   if ret==1: 
                    if saga: utils.UpdateSagas()
                    else: utils.UpdateSeries()
                   if ret==2 and Unique: 
                    if saga: utils.UpdateSagas(xbmc.getInfoLabel("ListItem.DBID"))
                    else : utils.UpdateSeries(xbmc.getInfoLabel("ListItem.IMDBNumber"))
                         
            if self.trailer and not self.backend:
                utils.logMsg('recherche trailers',0)
                TypeVideo=xbmc.getInfoLabel("Container(5051).ListItem.Writer")
                if not xbmc.getInfoLabel("Container(5051).ListItem.Mpaa"):
                  ListeTrailer=utils.getTrailer(xbmc.getInfoLabel("Container(5051).ListItem.Trailer"),TypeVideo) 
                else:
                  ListeTrailer=[]
                  TmdbId=utils.get_externalID(xbmc.getInfoLabel("Container(5051).ListItem.Mpaa"),TypeVideo)
                  utils.logMsg("Resultat  Tmdb --> "+str(TmdbId)+"/"+xbmc.getInfoLabel("Container(5051).ListItem.Mpaa")+"/"+str(TypeVideo),0) 
                  if TmdbId:
                    ListeTrailer=utils.getTrailer(TmdbId,TypeVideo) 
                Titre=xbmc.getInfoLabel("Container(5051).ListItem.Label").decode('utf-8','ignore')
                if ListeTrailer:
                    ListeNomTrailer=[]
                    #utils.logMsg('Liste trailers: ' + str(ListeTrailer),0)
                    for Item in  ListeTrailer:
                         try: 
                              ListeNomTrailer.append(utils.try_decode(Item["name"])+" ("+str(Item["size"])+")"+"-"+str(Item["iso_3166_1"]))
                         except:
                              ListeNomTrailer.append(str(Item["type"])+" ("+str(Item["size"])+")"+"-"+str(Item["iso_3166_1"]))
                    if len(ListeNomTrailer)>0:
                          
                          dialogC = xbmcgui.Dialog()
                          
                          Pos=int(xbmc.getInfoLabel("Container(1998).CurrentItem"))-1
                          Pos5051=int(xbmc.getInfoLabel("Container(5051).CurrentItem"))-1
                          ret=dialogC.select("[COLOR=yellow]"+Titre+"[/COLOR][I] "+xbmc.getLocalizedString( 20410 )+"[/I]", ListeNomTrailer)
                          #utils.logMsg('Liste trailers choisie: ' + str(ret),0)
                          if ret<len(ListeTrailer) and ret>=0:
                              #utils.logMsg('Liste trailers choisie: ' + str(ListeTrailer[ret]["key"]),0)
                              
                              #xbmc.executebuiltin('PlayMedia("https://www.youtube.com/watch?v=%s")' %(str(ListeTrailer[ret]["key"])))
                              xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s)' %(ListeTrailer[ret]["key"]))
                          else:   
                              self.windowhome.setProperty('ActeurVideoReset','')
                              xbmc.executebuiltin("SetFocus(1998)")                             
                             
                else: 
                    dialog=xbmcgui.Dialog()
                    dialog.notification('IconMixTools', Titre+": "+__language__( 32506 ), "acteurs/arfffff.png", 3000)

                              
                  
			     
          
			
			     
       	         
			    

    def _init_vars(self):
          #self.winid = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        #utils.logMsg('window ID: ' + str(winid))
          self.windowhome = xbmcgui.Window(10000) # Home.xml 
        



    def run_backend(self):
        self._stop = False
        self.previousitem = ""
        self.DBTYPEOK = False
        self.DBTYPE= ""
        self.duration=""
        self.TvShow=""
        self.TvSeason=""
        TvSe="o"
        TvSh="o"
        self.EpSa=0
        self.xx1999=None
        self.windowhome.clearProperty('DurationTools')                   
        self.windowhome.clearProperty('DurationToolsEnd')
        self.windowhome.clearProperty('IconMixExtraFanart') 
        self.windowhome.clearProperty('IconMixEpSa')
        self.windowhome.clearProperty('IconMixSaga')
        """
        con = sqlite3.connect('c:/Users/HTPC/AppData/Roaming/Kodi/userdata/Database/MyVideos107.db')
        cursor = con.cursor()
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #cursor.execute("SELECT strSet FROM sets;")
        
        # tables = version, bookmark, settings, stacktimes, genre, genre_link, country, country_link, movie, actor, actor_link, 
        #          director_link, writer_link, path, files, tvshow, episode, tvshowlinkpath, movielinktvshow, studio, studio_link, 
        #          musicvideo, streamdetails, sets, seasons, art, tag, tag_link, rating, uniqueid
        
        #utils.logMsg('backend Sql SETS='+str(cursor.fetchall()),0)
        
        cursor.execute("SELECT c00 FROM movie WHERE idSet='%d';" %(int(xbmc.getInfoLabel("ListItem.DBID"))))
        utils.logMsg('backend Sql SET %s=' %(xbmc.getInfoLabel("ListItem.DBID"))+str(cursor.fetchall()),0)
        con.close()
        """
        
        utils.logMsg('Service en cours...',0)
        while not self._stop:
            if not xbmc.getCondVisibility("Container.Scrolling"):
                if xbmc.getCondVisibility("Control.HasFocus(1999)"):
                    #self.xx1999=self.winid.getControl(1999)
                    #self.xx1999.reset()
                    #if self.xx1999: utils.logMsg('Getcontrol OK :  '+xbmc.getInfoLabel("Container(1999).ListItem.DBID"),0)
                    self.selecteditem = xbmc.getInfoLabel("Container(1999).ListItem.Label")
                    self.DBTYPE=xbmc.getInfoLabel("Container(1999).ListItem.DBTYPE")                    
                else : 
                    self.selecteditem = xbmc.getInfoLabel("ListItem.DBID")
                    self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")                    
                if not self.selecteditem :
                    self.windowhome.clearProperty('IconMixExtraFanart')
                    #self.windowhome.clearProperty('IconMixEpSa')
                    #self.windowhome.clearProperty('IconMixSaga') 
                    #utils.logMsg('backend Self :  '+'p='+self.previousitem+' a='+self.selecteditem,0)
                if (self.selecteditem != self.previousitem): 
                    #self.DBTYPEOK= self.DBTYPE=="movie" or self.DBTYPE=="episode" or self.DBTYPE=="song" or self.DBTYPE=="musicvideo"
                    self.DBTYPEOK= self.DBTYPE!="set" and self.DBTYPE!="tvshow" and self.DBTYPE!="season" and self.DBTYPE!="addon" and self.DBTYPE!="artist"
                    #utils.logMsg('backend DBTYPE='+self.DBTYPE,0)                                        
                    self.previousitem = self.selecteditem
                    self.windowhome.clearProperty('DurationTools')                   
                    self.windowhome.clearProperty('DurationToolsEnd')
                    self.windowhome.clearProperty('IconMixExtraFanart') 
                    #self.windowhome.clearProperty('IconMixEpSa')
                    #self.windowhome.clearProperty('IconMixSaga')
                    #utils.logMsg('backend updated',0)
                    if xbmc.getCondVisibility("Control.HasFocus(1999)"):
                        if xbmc.getInfoLabel("Container(1999).ListItem.DBID")> -1:                          
                          # allez ! on teste si le répertoire extrafanart existe et si non vide !
                            
                            if self.DBTYPEOK:
                               self.windowhome.setProperty('IconMixExtraFanart',utils.getItemPath(xbmc.getInfoLabel("Container(1999).ListItem.DBTYPE"),xbmc.getInfoLabel("Container(1999).ListItem.DBID")))   
                               self.duration = xbmc.getInfoLabel("Container(1999).ListItem.Duration") 
                               #utils.logMsg('backend 1999 duration :'+str(self.duration)+"/"+ xbmc.getInfoLabel("Container(1999).ListItem.DBID"),0)                                         
                               self.display_duration()
                   
                          #utils.logMsg('backend OK.',0)
                     
                    else:
                      if xbmc.getInfoLabel("ListItem.DBID") > -1:                          
                         
                         
                          if self.DBTYPEOK : 
                               self.windowhome.setProperty('IconMixExtraFanart',utils.getItemPath(xbmc.getInfoLabel("ListItem.DBTYPE"),xbmc.getInfoLabel("ListItem.DBID")))
                               self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                               #utils.logMsg('backend  duration :'+str(xbmc.getInfoLabel("ListItem.Duration"))+"/"+ str(xbmc.getInfoLabel("ListItem.DBID")),0)                                            
                               self.display_duration()
                          if self.DBTYPE=="episode" and xbmc.getCondVisibility("Skin.HasSetting(CheckSeries)"):
                               TvSh=xbmc.getInfoLabel("ListItem.TVShowTitle") 
                               TvSe=xbmc.getInfoLabel("ListItem.Season")
                               TvId=xbmc.getInfoLabel("ListItem.DBID")
                               #utils.logMsg('Saison episodes = DBID:['+str(TvSh)+"/"+str(TvSe)+"]"+ xbmc.getInfoLabel("ListItem.DBID")+' Saison :'+xbmc.getInfoLabel("ListItem.Season")+' IMDnumber :'+xbmc.getInfoLabel("ListItem.IMDBNumber") ,0)
                               #self.EpSa=utils.getepisodes("tt"+xbmc.getInfoLabel("ListItem.IMDBNumber"),xbmc.getInfoLabel("ListItem.Season"))
                               if TvId and TvSe and TvSh :
                                 if TvSe!=self.TvSeason or TvSh!=self.TvShow : 
                                   self.windowhome.clearProperty('IconMixEpSa')
                                   self.EpSa=utils.getepisodes(TvId,int(TvSe),xbmc.getInfoLabel("ListItem.DBTYPE"))
                                   if self.EpSa>0: 
                                     self.windowhome.setProperty('IconMixEpSa',str(self.EpSa))
                                     self.TvShow=TvSh
                                     self.TvSeason=TvSe
                               else : self.windowhome.clearProperty('IconMixEpSa')
                          else : 
                              self.windowhome.clearProperty('IconMixEpSa')
                              self.TvShow=""
                              self.TvSeason=""
                      else : 
                         self.windowhome.clearProperty('IconMixEpSa')
                         self.TvShow=""
                         self.TvSeason=""
                                    
                                   
                          
                    
            xbmc.sleep(200)
            if not xbmc.getCondVisibility("Window.IsVisible(10025)") and not xbmc.getCondVisibility("Window.IsVisible(10502)") and not xbmc.getCondVisibility("Window.IsVisible(10000)"):
                utils.logMsg('service IconMixTools fini.',0)
                self.windowhome.clearProperty('DurationTools')
                self.windowhome.clearProperty('DurationToolsEnd')
                xbmc.executebuiltin('ClearProperty(IconMixToolsbackend,home)')
                self._stop = True

    def display_duration(self):
    #twolaw code
        xxx="null"
        
        typeId=xbmc.getInfoLabel("ListItem.DBTYPE")
        itemId=xbmc.getInfoLabel("ListItem.DBID")
        imdbId=xbmc.getInfoLabel("ListItem.IMDBNumber")
       
        if (not self.duration or self.duration<10) and imdbId :
            #utils.logMsg('GetRuntime selfduration: '+ str(self.duration) +' minutes'+" movie =" +str(xbmc.getInfoLabel("ListItem.DBID"))+" type =" +str(xbmc.getInfoLabel("ListItem.DBTYPE"))+" imdb="+str(xbmc.getInfoLabel("ListItem.IMDBNumber")),0)
            if typeId.find('episode')==-1: self.duration=utils.getRuntime(imdbId,typeId)
            #else : self.duration=utils.getRuntime("tt"+imdbId)
            if self.duration and typeId :                    
                    #mise à jour de la durée dans la base pour éviter de renouveller l'opération !
                    utils.setJSON('VideoLibrary.Set%sDetails' %(typeId.encode("utf-8")),'{"%sid":%d,"runtime":%d}' %(typeId.encode("utf-8"),int(itemId),int(self.duration)*60))
                     #http://127.0.0.1:8080/jsonrpc?request={%22jsonrpc%22:%222.0%22,%22method%22:%22VideoLibrary.SetMovieDetails%22,%22params%22:{%22movieid%22:37,%22runtime%22:111},%22id%22:1}
                    #utils.logMsg('Mise a jour : %d' %( int(self.duration)*60) +' minutes'+" movie =" +str(itemId)+" type =" +typeId+"imdb="+imdbId,0)
        if self.duration :
        #else :
         if self.duration.find(':')==-1:
            readable_duration = in_hours_and_min(self.duration)
            self.windowhome.setProperty('DurationTools', readable_duration)
            
            if int(self.duration)>0:
              now = datetime.datetime.now()
              now_plus_10 = now + datetime.timedelta(minutes = int(self.duration))
              xxx = format(now_plus_10, '%Hh%M')
              self.windowhome.setProperty('DurationToolsEnd', xxx)
            else:
              self.windowhome.clearProperty('DurationToolsEnd')
              self.windowhome.clearProperty('DurationTools')
         else:
           self.windowhome.setProperty('DurationTools', self.duration)
           #utils.logMsg('backend time : %s.- now: %s' % (self.duration,xxx),0)
         

           		   

if (__name__ == "__main__"):
    Main()
#utils.logMsg('script finished.')