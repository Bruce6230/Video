import requests  # 数据请求模块
import re  # 正则表达式模块
import json  # 数据类型处理模块
from tqdm import tqdm  # 进度条配置
import os  # 处理文件和目录

# 请求头信息
headers = {
    'cookie': 'VISITOR_INFO1_LIVE=h7V0bl8uHYs; PREF=tz=Asia.Shanghai; SID=WQj5NpLzj1naJQlX2435vkvaK8uvcVEJbLEfDK-ThaW5div9cqIr0NeNrQES1zcHs5xj9A.; __Secure-1PSID=WQj5NpLzj1naJQlX2435vkvaK8uvcVEJbLEfDK-ThaW5div9MB_vId3nvHSusO4HNIwocA.; __Secure-3PSID=WQj5NpLzj1naJQlX2435vkvaK8uvcVEJbLEfDK-ThaW5div9V76Igy71_zivc7uM1c8eqA.; HSID=AfzcBiNp9Fz3KnNoo; SSID=AiYjpBdjP_RA90Toe; APISID=XfSLrawldAucfHNJ/Ax8tUpM8m8QQfWOd4; SAPISID=K4czjWiqrxgWsKjr/AoqZvAlw6LD3WExx_; __Secure-1PAPISID=K4czjWiqrxgWsKjr/AoqZvAlw6LD3WExx_; __Secure-3PAPISID=K4czjWiqrxgWsKjr/AoqZvAlw6LD3WExx_; LOGIN_INFO=AFmmF2swRQIhANqtt-iKUtARr4KqqgGkS7Mg2CSn1d9Ofa8obaopn9I1AiAqC3cgfjwB3hTjlNvtJNBIKlGchphMP0-2yTHaa9K9bg:QUQ3MjNmekc4QjZIQzk3RnRTLUUzQ2F0TFRvNEdxOEx5cmdER2lydld1VU0wdTQzUUU0WmpxQW5sSE9FcEEwcmZiRW5qNWRkMlRzVDVoMHRaWndEczREeUhfdnhWTWUwNnNNR1RmR2ZpWG1XV043cy1SZE5QTWJNUFg1VmZoNWptZ3pZS0VlWjZCSGs1S2NsdUR2WHFlcFBzbmNXMVNkQmx3; YSC=ERcINBq4P-c; SIDCC=AP8dLtwCDoAXayxw09FDWRkqrcBq16JHjHbLVFT7gUEkwtBIGQvjhNE4DNY1g57oY5RJ7M36vbE; __Secure-1PSIDCC=AP8dLtzA5SrBeBcAnHKNEae_P-8ZbWGhfJMZzqknWyNAxaChMvjPbKJTSFp1HPazLj2pFc9V7w; __Secure-3PSIDCC=AP8dLtxFWoci2hQV87ZgXxePNQaKWCyNr0Sho2QOd6Rspt-DMCi0yqufpuGyDYHP3Z2aJFKihg',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

# 要下载的视频链接
url = 'https://www.youtube.com/watch?v=Q3R1qRxd-Us'

# 发送请求，获取视频页面源代码
response = requests.get(url=url, headers=headers)

# 从页面源代码中提取视频信息的JSON字符串
json_str = re.findall('var ytInitialPlayerResponse = (.*?);var', response.text)[0]

# 解析JSON字符串，获取视频下载链接和标题等信息
json_data = json.loads(json_str)
#视频地址
video_url = json_data['streamingData']['adaptiveFormats'][0]['url']
#音频地址
audio_url = json_data['streamingData']['adaptiveFormats'][-2]['url']
#视频名称
title = json_data['videoDetails']['title']

# 处理视频标题，去掉空格和特殊字符，作为文件名
title = title.replace(' ', '')
title = re.sub(r'[\/:|?*"<>]', '', title)

#mode='wb':以二进制方式覆盖写入数据
#mode='ab':以二进制方式追加写入数据

# 下载视频文件
video = requests.get(video_url, stream=True)
file_size = int(video.headers.get('Content-Length'))
video_pbar = tqdm(total=file_size)
with open(f'{title}.mp4', mode='wb') as f:
    for video_chunk in video.iter_content(1024 * 1024 * 2):
        f.write(video_chunk)
        video_pbar.set_description(f'正在下载{title}视频中......')
        video_pbar.update(1024 * 1024 * 2)
    video_pbar.set_description('下载完成！')
    video_pbar.close()

# 下载音频文件
audio = requests.get(audio_url, stream=True)
file_size = int(audio.headers.get('Content-Length'))
audio_pbar = tqdm(total=file_size)
with open(f'{title}.mp3', mode='wb') as f:
    for audio_chunk in audio.iter_content(1024 * 1024 * 2):
        f.write(audio_chunk)
        audio_pbar.set_description(f'正在下载{title}音频中......')
        audio_pbar.update(1024 * 1024 * 2)
    audio_pbar.set_description('下载完成！')
    audio_pbar.close()

# 合并视频和音频文件
def merge(title):
    ffmpeg = r'D:\ffmpeg\bin\ffmpeg.exe -i ' + title + '.mp4 -i ' + title + '.mp3 -acodec copy -vcodec copy ' + title + '-out.mp4'
    os.popen(ffmpeg)
merge(title)
