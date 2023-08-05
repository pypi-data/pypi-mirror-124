#!usr/bin/python
# -*- coding: utf-8 -*-
import requests

__version__ = '1.1.0'

class Psychopumpum(object):

    def __init__(self, apikey, heroku = True):
        self.session = requests.session()
        self.session.headers.update(
            {
                'apikey': apikey
            }
        )
        if heroku:self.baseUrl = 'https://psychopumpum-api.herokuapp.com'
        else:self.baseUrl = 'https://psychopumpum.com'
        

    def get(self, path, *args, **kwargs):
        return self.session.get(self.baseUrl + path, *args, **kwargs)

    def check_apikey(self):
        return self.get(f'/check/?apikey={self.session.headers.get("apikey")}').json()

    ''' Instagram '''
    def instagram_info(self, username, highlight = True, post = True):
        params = {
            'username': username,
            'highlight': highlight,
            'post': post
        }
        return self.get('/apis/instagram/info/', params=params).json()

    def instagram_post(self, username, **kwargs):
        params = {'username': username}
        if kwargs.get('next_max_id'):
            params.update({'next_max_id': kwargs.get('next_max_id')})
        return self.get('/apis/instagram/post/', params = params).json()

    def instagram_post_byurl(self, url):
        params = {
            'url': url
        }
        return self.get('/apis/instagram/post/', params=params).json()

    def instagram_story(self, username_or_url, username = True):
        if username:params = {'username': username_or_url}
        else:params = {'url': username_or_url}
        return self.get('/apis/instagram/story/', params = params).json()

    def instagram_highlight(self, username):
        params = {'username': username}
        return self.get('/apis/instagram/highlight/', params=params).json()

    ''' TikTok '''
    def tiktok_search(self, q):
        params = {'q': q}
        return self.get('/apis/tiktok/search/', params=params).json()

    def tiktok_profile(self, username):
        params = {'username': username}
        return self.get('/apis/tiktok/profile/', params = params).json()

    def tiktok_download(self, url):
        params = {'url': url}
        return self.get('/apis/tiktok/download/', params = params).json()

    ''' YouTube '''
    def youtube_search(self, q, max_results = 20, download=False):
        params = {'q': q, 'max_results': max_results, 'download': download}
        return self.get('/apis/youtube/search/', params = params).json()

    def youtube_download(self, url):
        params = {'url': url}
        return self.get('/apis/youtube/download/', params = params).json()

    ''' Google '''
    def google_search(self, q, page = 0):
        params = {'q': q, 'page': page}
        return self.get('/apis/google/search/', params = params).json()

    def google_image(self, q, count=50):
        params = {'q': q, 'max_results': count}
        return self.get('/apis/google/image/', params = params).json()

    def google_reverse(self, url):
        params = {'url': url}
        return self.get('/apis/google/reverse/', params = params).json()

    def google_news(self):
        return self.get('/apis/google/news/').json()

    def google_playstore_search(self, q):
        params = {'q': q}
        return self.get('/apis/google/playstore/search/', params = params).json()

    def google_playstore_info(self, url):
        params = {'url': url}
        return self.get('/apis/google/playstore/info/', params = params).json()

    ''' Pinterest '''
    def pinterest_search(self, q, max_results = 10):
        params = {'q': q, 'max_results': max_results}
        return self.get('/apis/pinterest/search', params = params).json()

    def pinterest_reverse(self, url):
        params = {'url': url}
        return self.get('/apis/pinterest/similiar/', params = params).json()

    def pinterest_download(self, url):
        params = {'url': url}
        return self.get('/apis/pinterest/download/', params=params).json()

    ''' Joox '''
    def joox_search(self, q, max_results = 10, download = True):
        params = {'q': q, 'max_results': max_results, 'download': download}
        return self.get('/apis/joox/search/', params = params).json()

    def joox_download(self, songId):
        params = {'songId': songId}
        return self.get('/apis/joox/download/', params=params).json()

    ''' Lyric '''
    def lyric_search(self, q):
        params = {'q': q}
        return self.get('/apis/genius-lyric/search/', params = params).json()

    def lyric_get(self, url):
        params = {'url': url}
        return self.get('/apis/genius-lyric/get/', params = params).json()

    ''' Nine gag '''
    def ninegag(self):
        return self.get('/apis/ninegag/').json()

    def ninegag_search(self, q, start=0, count=10):
        params = {'q': q, 'start': start, 'max_results': count}

    def ninegag_random(self):
        return self.get('/apis/ninegag/random/').json()

    def ninegag_info(self, section = 'nsfw', type_ = 'hot', count = 10):
        params = {'section': section, 'type': type_, 'max_results': count}
        return self.get('/apis/ninegag/info/', params = params).json()

    ''' nulis '''
    def nulis(self, text):
        params = {'text': text}
        return self.get('/apis/tulisin/', params = params).json()

    ''' Movie Clip 
        NOTE!!
            TO download video,
                if you have error bout' dont ssl verification.
                using verify=False if you use requests module `python`
            example:
                import requests
                requests.get(
                    'https://video.playphrase.me/5b96a8e0cc77853d88560e06/5e8bd38b24aa9a00293c16ba.mp4',
                    verify=False
                )
                
                import warnings
                warnings.filterwarnings("ignore")
                if u dont want to get warnings.
                
    '''
    def movie_phrase(self, text):
        params = {'q': text}
        return self.get('/apis/phrase/clip/', params=params).json()

    ''' Twitter '''
    def twitter_profile(self, q, count = 20):
        params = {'q': q, 'max_results': count}
        return self.get('/apis/twitter/info/', params = params).json()

    def twitter_download(self, url):
        params = {'url': url}
        return self.get('/apis/twitter/download/', params = params).json()

    ''' PIXIV '''
    '''
        NOTE!!
            TO SEND IMAGE USING PIXIV URL,
                add headers in your request
           'referer': 'https://pixiv.net/en/'
    '''
    def pixiv_novel_search(self, q, page = 1):
        params = {'q': q, 'page': page}
        return self.get('/apis/pixiv-novel/search/', params=params).json()

    def pixiv_novel_info(self, url):
        params = {'url': url}
        return self.get('/apis/pixiv-novel/series/', params=params).json()

    def pixiv_novel_read(self, url):
        params = {'url': url}
        return self.get('/apis/pixiv-novel/read/', params=params).json()

    def pixiv_illust_search(self, q, page=1):
        params = {'q': q, 'page': page}
        return self.get('/apis/pixiv-illust/search/', params=params).json()

    def pixiv_manga_search(self, q, page=1):
        params = {'q': q, 'page': page}
        return self.get('/apis/pixiv-manga/search/', params=params).json()

    def pixiv_top_search(self, q, page=1):
        params = {'q': q, 'page': page}
        return self.get('/apis/pixiv-top/search/', params=params).json()

    def pixiv_artworks_get(self, url):
        params = {'url': url}
        return self.get('/apis/pixiv-artworks/read/', params=params).json()

    ''' Danbooru '''
    def danbooru_search(self, q):
        params = {'q': q, 'page': page}
        return self.get('/apis/danbooru/search/', params=params).json()

    ''' LINE '''
    def search_sticker(self, q, start=0, limit = 20):
        params = {'q': q, 'start': start, 'max_results': limit}
        return self.get('/apis/line-sticker/search/', params = params).json()
        
    def search_theme(self, q, start=0, limit = 20):
        params = {'q': q, 'start': start, 'max_results': limit}
        return self.get('/apis/line-theme/search/', params = params).json()
        
    def search_emoji(self, q, start=0, limit = 20):
        params = {'q': q, 'start': start, 'max_results': limit}
        return self.get('/apis/line-sticon/search/', params = params).json()