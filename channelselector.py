# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand 5
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of streamondemand 5.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------

import glob
import os
import traceback
import urlparse

from core import channeltools
from core import config
from core import logger
from core.item import Item

DEBUG = config.get_setting("debug")

def getmainlist(preferred_thumb=""):
    logger.info("channelselector.getmainlist")
    itemlist = list()

    # Añade los canales que forman el menú principal

    itemlist.append( Item(title=config.get_localized_string(30119) , channel="channelselector" , action="getchanneltypes", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_category.png"),viewmode="movie") )
    itemlist.append( Item(title=config.get_localized_string(30137) , channel="buscadorall" , action="mainlist" , thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_search.png"),viewmode="movie") )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_fav.png"),viewmode="movie") )
    if config.get_library_support():
        itemlist.append( Item(title=config.get_localized_string(30131) , channel="biblioteca" , action="mainlist", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_library.png"),viewmode="movie") )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_download.png"),viewmode="movie") )

    if "xbmceden" in config.get_platform():
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_conf.png"), folder=False,viewmode="movie") )
    else:
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_conf.png"),viewmode="movie") )

    itemlist.append( Item(title=config.get_localized_string(30138) , channel="update_version" , action="update_from_menu", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_download.png"),viewmode="movie") )

    itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_help.png"),viewmode="movie") )
    return itemlist

def get_thumb(preferred_thumb,thumb_name):
    return urlparse.urljoin(get_thumbnail_path(preferred_thumb),thumb_name)

def getchanneltypes(preferred_thumb=""):
    logger.info("channelselector getchanneltypes")

    # Lista de categorias
    valid_types = ""
    dict_cat_lang = ""

    # Lee la lista de canales
    channel_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    logger.info("channelselector.getchanneltypes channel_path=" + channel_path)

    channel_files = glob.glob(channel_path)

    channel_language = config.get_setting("channel_language")
    logger.info("channelselector.getchanneltypes channel_language=" + channel_language)

    # Construye la lista de tipos
    channel_types = []

    for index, channel in enumerate(channel_files):
        logger.info("channelselector.getchanneltypes channel=" + channel)
        if channel.endswith(".xml"):
            try:
                channel_parameters = channeltools.get_channel_parameters(channel[:-4])
                logger.info("channelselector.filterchannels channel_parameters=" + repr(channel_parameters))

                # Si es un canal para adultos y el modo adulto está desactivado, se lo salta
                if channel_parameters["adult"] == "true" and config.get_setting("adult_mode") == "false":
                    continue

                # Si el canal está en un idioma filtrado
                if channel_language != "all" and channel_parameters["language"] != channel_language:
                    continue

                categories = channel_parameters["categories"]
                for category in categories:
                    logger.info("channelselector.filterchannels category=" + category)
                    if category not in channel_types and category in valid_types:
                        channel_types.append(category)

            except:
                logger.info("Se ha producido un error al leer los datos del canal " + channel + traceback.format_exc())

    logger.info("channelselector.getchanneltypes Encontrados:")
    for channel_type in channel_types:
        logger.info("channelselector.getchanneltypes channel_type=" + channel_type)

    # Ahora construye el itemlist ordenadamente
    itemlist = list()

    itemlist.append(Item(title="Top Channels", channel="channelselector", action="filterchannels",
                         category="top channels", channel_type="top channels", thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_topchannels.png"),
                         viewmode="movie"))
    itemlist.append(Item(title=config.get_localized_string(30122), channel="channelselector", action="filterchannels",
                         category="movie", channel_type="movie", thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_film.png"), viewmode="movie"))
    itemlist.append(Item(title=config.get_localized_string(30123), channel="channelselector", action="filterchannels",
                         category="serie", channel_type="serie", thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_series.png"), viewmode="movie"))
    itemlist.append(Item(title=config.get_localized_string(30124), channel="channelselector", action="filterchannels",
                         category="anime", channel_type="anime", thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_anime.png"), viewmode="movie"))
    itemlist.append(Item(title=config.get_localized_string(30125), channel="channelselector", action="filterchannels",
                         category="documentary", channel_type="documentary", thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_documentales.png"),
                         viewmode="movie"))
    itemlist.append(Item(title="Cult", channel="channelselector", action="filterchannels",
                         category="cult", channel_type="cult", thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_filmontv.png"),
                         viewmode="movie"))
    itemlist.append(Item(title="Saghe", channel="saghe", action="mainlist",
                         category="saghe", channel_type="saghe", thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_saghe.png")))
    itemlist.append( Item(title="Oggi in TV" , channel="filmontv" , action="mainlist" , thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_filmontv.png"),viewmode="movie") )
    itemlist.append( Item(title="Liste Netflix" , channel="netflixsrc" , action="mainlist" , thumbnail = os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_series.png"),viewmode="movie") )
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="filterchannels" , channel_type="vos", category="vos" , thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_vos.png"),viewmode="movie") )
    itemlist.append( Item( title="Torrent" , channel="channelselector" , action="filterchannels" , channel_type="torrent", category="torrent" , thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "cat_menu_torrent.png"),viewmode="movie") )
    itemlist.append( Item( title="[COLOR yellow]" + config.get_localized_string(30121) + "[/COLOR]" , channel="channelselector" , action="filterchannels" , channel_type="all", category="all" , thumbnail= os.path.join(config.get_runtime_path() , "resources" , "images", "main_menu_all.png"),viewmode="movie") )

    logger.info("channelselector.getchanneltypes Ordenados:")
    for channel_type in valid_types:
        logger.info("channelselector.getchanneltypes channel_type="+channel_type)
        if channel_type in channel_types:
            title = dict_cat_lang.get(channel_type, channel_type)
            itemlist.append(Item(title=title, channel="channelselector", action="filterchannels", category=title,
                                 channel_type= channel_type, viewmode="thumbnails",
                                 thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),
                                                            "thumb_canales_"+channel_type+".png")))

    return itemlist

def filterchannels(category,preferred_thumb=""):
    logger.info("channelselector.filterchannels")

    channelslist =[]

    # Si category = "allchannelstatus" es que estamos activando/desactivando canales
    appenddisabledchannels = "false"
    if category == "allchannelstatus":
        category = "all"
        appenddisabledchannels = "true"

    # Lee la lista de canales
    channel_path = os.path.join( config.get_runtime_path() , "channels" , '*.xml' )
    logger.info("channelselector.filterchannels channel_path="+channel_path)

    channel_files = glob.glob(channel_path)
    logger.info("channelselector.filterchannels channel_files encontrados "+str(len(channel_files)))

    channel_language = config.get_setting("channel_language")
    logger.info("channelselector.filterchannels channel_language="+channel_language)
    if channel_language=="":
        channel_language = "all"
        logger.info("channelselector.filterchannels channel_language="+channel_language)

    for index, channel in enumerate(channel_files):
        logger.info("channelselector.filterchannels channel="+channel)
        if channel.endswith(".xml"):

            try:
                channel_parameters = channeltools.get_channel_parameters(channel[:-4])
                logger.info("channelselector.filterchannels channel_parameters="+repr(channel_parameters))

                # Si prefiere el bannermenu y el canal lo tiene, cambia ahora de idea
                if preferred_thumb=="bannermenu" and "bannermenu" in channel_parameters:
                    channel_parameters["thumbnail"] = channel_parameters["bannermenu"]

                # Se salta el canal si no está activo y no estamos activando/desactivando los canales
                channel_status = None
                if config.get_setting("enabled", channel_parameters["channel"]):
                    channel_status = config.get_setting("enabled", channel_parameters["channel"])
                else:
                    channel_status = channel_parameters["active"]

                if channel_status != "true":
                    if appenddisabledchannels != "true":
                        continue

                # Se salta el canal para adultos si el modo adultos está desactivado
                if channel_parameters["adult"] == "true" and config.get_setting("adult_mode") != "true": 
                    continue

                # Se salta el canal si está en un idioma filtrado
                if channel_language!="all" and channel_parameters["language"]!=config.get_setting("channel_language"):
                    continue

                # Se salta el canal si está en una categoria filtrado
                if category!="all" and category not in channel_parameters["categories"]:
                    continue

                # Si ha llegado hasta aquí, lo añade
                channelslist.append(Item(title=channel_parameters["title"], channel=channel_parameters["channel"],
                                         action="mainlist", thumbnail=channel_parameters["thumbnail"] ,
                                         fanart=channel_parameters["fanart"],
                                         category=channel_parameters["title"],
                                         language=channel_parameters["language"], viewmode="list" ))

            
            except:
                logger.info("Se ha producido un error al leer los datos del canal " + channel)
                import traceback
                logger.info(traceback.format_exc())
           
    channelslist.sort(key=lambda item: item.title.lower().strip())

    if category=="all":
        if config.get_setting("personalchannel5")=="true":
            channelslist.insert( 0 , Item( title=config.get_setting("personalchannelname5") ,action="mainlist", channel="personal5" ,thumbnail=config.get_setting("personalchannellogo5") , type="generic" ,viewmode="list" ))
        if config.get_setting("personalchannel4")=="true":
            channelslist.insert( 0 , Item( title=config.get_setting("personalchannelname4") ,action="mainlist", channel="personal4" ,thumbnail=config.get_setting("personalchannellogo4") , type="generic" ,viewmode="list" ))
        if config.get_setting("personalchannel3")=="true":
            channelslist.insert( 0 , Item( title=config.get_setting("personalchannelname3") ,action="mainlist", channel="personal3" ,thumbnail=config.get_setting("personalchannellogo3") , type="generic" ,viewmode="list" ))
        if config.get_setting("personalchannel2")=="true":
            channelslist.insert( 0 , Item( title=config.get_setting("personalchannelname2") ,action="mainlist", channel="personal2" ,thumbnail=config.get_setting("personalchannellogo2") , type="generic" ,viewmode="list" ))
        if config.get_setting("personalchannel")=="true":
            channelslist.insert( 0 , Item( title=config.get_setting("personalchannelname")  ,action="mainlist", channel="personal"  ,thumbnail=config.get_setting("personalchannellogo") , type="generic" ,viewmode="list" ))

        channel_parameters = channeltools.get_channel_parameters("tengourl")
        # Si prefiere el bannermenu y el canal lo tiene, cambia ahora de idea
        if preferred_thumb=="bannermenu" and "bannermenu" in channel_parameters:
            channel_parameters["thumbnail"] = channel_parameters["bannermenu"]

        channelslist.insert( 0 , Item( title="[COLOR gray]Inserisci un URL[/COLOR]"  ,action="mainlist", channel="tengourl" , thumbnail=channel_parameters["thumbnail"], type="generic" ,viewmode="movie" ))
        channel_parameters = channeltools.get_channel_parameters("searchchannel")
        channelslist.insert(0, Item(title="[COLOR gray]Cerca canale[/COLOR]", action="search", channel="searchchannel", thumbnail=channel_parameters["thumbnail"], type="generic", viewmode="movie"))

    return channelslist

def get_thumbnail_path(preferred_thumb=""):

    WEB_PATH = ""
    
    if preferred_thumb=="":
        thumbnail_type = config.get_setting("thumbnail_type")
        if thumbnail_type=="":
            thumbnail_type="2"

        if thumbnail_type=="0":
            WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/posters/"
        elif thumbnail_type=="1":
            WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/banners/"
        elif thumbnail_type=="2":
            WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/squares/"
    else:
        WEB_PATH = "https://raw.githubusercontent.com/Zanzibar82/images/master/" + preferred_thumb + "/"

    return WEB_PATH
