# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qs
import json
import re
import os
from pathlib import PureWindowsPath, PurePosixPath

import requests
from bs4 import BeautifulSoup
import pandas as pd
from idebug import *


__all__ = [
    'YouTubeMusic',
]

def clean_path(p):
    # 운영체제 타입에 따라 path 를 수정한다
    if os.name == 'posix':
        return str(PurePosixPath(p))
    elif os.name == 'nt':
        return str(PureWindowsPath(p))

class Y2MateBrowser:

    def __init__(self, dl_path, title=None):
        self.set_dlpath(dl_path)
        self.set_title(title)

    @property
    def dl_path(self):
        return self._dl_path

    def set_dlpath(self, p):
        self._dl_path = clean_path(p)

    @property
    def title(self):
        return self._title

    def set_title(self, s):
        s = '' if s is None else s
        # [Windows|MacOS] 에서 지원하지 않는 파일명에 대한 청소
        s = re.sub('[\s]+', repl=' ', string=s)
        s = re.sub('[:\|\?\*"\<\>/]+', repl='#', string=s)
        # print('title:', s)
        self._title = s

    @funcIdentity
    def search(self, url):
        # url: 유투브 영상 URL
        # PartGubun('search')
        o = urlparse('https://suggestqueries.google.com/complete/search?jsonp=jQuery340004144273343421623_1635056106020&q=https%3A%2F%2Fyoutu.be%2Fc9h5VloOhCc%3Flist%3DTLPQMjQxMDIwMjEgBM7O0V7Bvg&hl=en&ds=yt&client=youtube&_=1635056106021')
        # print(o)
        qs = parse_qs(o.query)
        # pp.pprint(qs)
        o = o._replace(query='')
        # print(o)

        # 입력받은 유투브URL을 qs객체에 업데이트
        self.yt_url = url
        yt = urlparse(self.yt_url)
        # print(yt)
        param = {k:v[0] for k,v in qs.items()}
        param['q'] = self.yt_url
        # pp.pprint(param)
        # print('geturl:', o.geturl())
        r = requests.get(o.geturl(), param)
        # dbg.dict(r)
        # print(r.text, type(r.text))

    @funcIdentity
    def ajax(self):
        # PartGubun('Ajax')
        url = 'https://www.y2mate.com/mates/en105/analyze/ajax'
        qs = parse_qs('url=https%3A%2F%2Fyoutu.be%2FagnV2YjuzSM%3Flist%3DPLP9YOa5MTwu06to2NmlacATe-zEXHUOTw&q_auto=0&ajax=1')
        # print(qs)
        data = {k:v[0] for k,v in qs.items()}
        data['url'] = self.yt_url
        r = requests.post(url, data)
        # dbg.dict(r)

        # SectionGubun('Response-Data')
        d = json.loads(r.text)
        # pp.pprint(d)

        # SectionGubun('HTML파싱')
        soup = BeautifulSoup(d['result'], 'html.parser')
        # print(soup.prettify())

        s = soup.find('div', class_='caption text-left').b.get_text().strip()
        # print('title:', s)
        self.set_title(s)

        # print(soup.input.attrs)
        self.data_id = soup.input.attrs['data-id']

        # SectionGubun('KData 추출')
        s = soup.find('script', attrs={'type':'text/javascript'})
        # print(s.get_text())
        li = s.get_text().split(';')
        li = [e.strip() for e in li if len(e.strip()) > 0]
        d = {}
        for e in li:
            m = re.search('var\s([a-z_]+)\s=\s"(.+)"', e)
            d.update({m[1]:m[2]})
        # pp.pprint(d)
        self.KData = d

    @funcIdentity
    def fetch_img(self):
        # PartGubun('이미지 저장')
        downloader = Downloader(self.dl_path)
        url = f'https://i.ytimg.com/vi/{self.data_id}/0.jpg'
        filename = f"{self.title}.jpg"
        downloader.get(url, filename)

    @funcIdentity
    def xc(self):
        # PartGubun('xc')
        r = requests.get('https://habeglee.net/s9np/xc')
        # dbg.dict(r)
        d = json.loads(r.text)
        # pp.pprint(d)

    @funcIdentity
    def convert(self):
        # PartGubun('convert')
        qs = parse_qs('type=youtube&_id=5e9b86ec7527f838068b4591&v_id=agnV2YjuzSM&ajax=1&token=&ftype=mp3&fquality=128')
        qs['_id'] = self.KData['k__id']
        qs['v_id'] = self.KData['k_data_vid']
        r = requests.post('https://www.y2mate.com/mates/convert', data=qs)
        # dbg.dict(r)
        d = json.loads(r.text)

        # SectionGubun('HTML파싱')
        soup = BeautifulSoup(d['result'], 'html.parser')
        # print(soup.prettify())
        href = soup.find('a').attrs['href']
        # print('href:', href)
        # o = urlparse(href)
        # print(o)
        self.mp3_url = href

    @funcIdentity
    def download(self):
        # PartGubun('MP3파일 다운로드')
        downloader = Downloader(self.dl_path)
        filename = f"{self.title}.mp3"
        downloader.get(self.mp3_url, filename)

    @funcIdentity
    def get_mp3(self, url):
        self.search(url)
        self.ajax()
        self.fetch_img()
        self.convert()
        self.download()

class Downloader:

    def __init__(self, path):
        self._dl_path = path

    def get(self, url, filename, **kw):
        r = requests.get(url, **kw)
        # dbg.dict(r)
        fpath = f"{self._dl_path}/{filename}"
        with open(fpath, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        fd.close()
        logger.info(f'{self} | Done. FilePath: {fpath}')

class YouTubeBrowser:

    def __init__(self):
        pass

    def get(self, url):
        r = requests.get(url)
        # dbg.dict(r)
        # SectionGubun('HTML파싱')
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())

        s = soup.find('script', string=re.compile('var ytInitialData'))
        # print(s.prettify())

        txt = s.get_text().strip()
        txt = re.sub('^var ytInitialData = ', repl='', string=txt)
        txt = re.sub(';$', repl='', string=txt)
        txt = re.sub('\s+', repl=' ', string=txt)
        # print(txt)

        d = json.loads(txt)
        d = d['contents']['twoColumnWatchNextResults']['playlist']['playlist']
        # print('len(d):', len(d))
        # print('d.keys:', list(d.keys()))

        self._playlistId = d['playlistId']
        self._playlistTitle = d['title']
        d = d['contents']
        # print('type(d):', type(d), isinstance(d, list), len(d))

        # SectionGubun('JSON_Normalize')
        data = []
        for e in d:
            data.append(e['playlistPanelVideoRenderer'])
        df = pd.json_normalize(data)
        # pp.pprint(sorted(df.columns))

        for c in sorted(df.columns):
            # SectionGubun(c)
            # print(df[c])
            if c == 'videoId':
                self._videoIds = list(df[c])
            elif c == 'title.simpleText':
                pp.pprint(list(df[c]))

    @property
    def PlayListId(self):
        return self._playlistId

    @property
    def PlayListTitle(self):
        return self._playlistTitle

    @property
    def VideoIds(self):
        return self._videoIds

class YouTubeMusic:

    def __init__(self, dl_path=None):
        self.youtube = YouTubeBrowser()
        self.y2mate = Y2MateBrowser('/', None)
        self.set_dlpath(dl_path)

    @property
    def dl_path(self):
        return self._dl_path

    @funcIdentity
    def set_dlpath(self, path):
        if path is None:
            if os.name == 'nt':
                path = 'C:/Users/innovata/Music'
            elif os.name == 'posix':
                path = '/Users/sambong/Music'

        p = clean_path(path)
        self._dl_path = p
        self.y2mate.set_dlpath(p)
        # 해당 경로가 존재하지 않으면 강제로 생성한다
        if not os.path.exists(p):
            os.makedirs(p)

    @funcIdentity
    def download_playlist(self, url):
        # url: 유투브 플레이리스트 URL
        self.youtube.get(url)
        for videoId in self.youtube.VideoIds:
            _url = f'https://youtu.be/{videoId}?list={self.youtube.PlayListId}'
            self.y2mate.get_mp3(_url)
        logger.info(f'{self} | Done.')

    @funcIdentity
    def download_one(self, url):
        # url: 유투브 비디오 URL
        self.y2mate.get_mp3(url)
        logger.info(f'{self} | Done.')
