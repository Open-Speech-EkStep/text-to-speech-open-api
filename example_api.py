import base64
import io
import json
import threading

import requests
from pydub import AudioSegment
from pydub.playback import play


def play_audio():
  global speech_list
  i = 1

  while len(speech_list.keys()) > 0:
    print(speech_list)
    play(speech_list[str(i)])
    print(f"Audio duration in total is {speech_list[str(i)].duration_seconds}")
    i += 1
    # speech_list.pop(i)


def request_audio(text_to_apply, gender, language):
  global speech_list
  payload = json.dumps({
    "text": text_to_apply[:],
    "gender": gender,
    "lang": language})
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  print("Total response time ", response.elapsed.total_seconds())
  data = base64.b64decode(response.json()['data'])
  speech = AudioSegment.from_file(io.BytesIO(data), format="wav")
  speech_list[thr.name.replace("Thread-", '')] = speech


if __name__ == "__main__":
  url = "http://34.121.100.224:5000/TTS/"

  max_text_limit = 150
  text_to_convert = "भारत मेरा देश है और मुझे भारतीय होने पर गर्व है।ये विश्व का सातवाँ सबसे बड़ा और विश्व में दूसरा सबसे अधिक जनसंख्या वाला देश है।इसे भारत,हिन्दुस्तान और आर्यव्रत के नाम से भी जाना जाता है। ये एक प्रायद्वीप है जो पूरब में बंगाल की खाड़ी, पश्चिम में अरेबियन सागर और दक्षिण में भारतीय महासागर जैसे तीन महासगरों से घिरा हुआ है। भारत का राष्ट्रीय पशु चीता, राष्ट्रीय पक्षी मोर, राष्ट्रीय फूल कमल, और राष्ट्रीय फल आम है।"
  gender = "female"
  language = "hi"
  multi_run = 1
  speech_list = {}
  while multi_run:
    if len(text_to_convert) > max_text_limit:
      text_to_apply = text_to_convert[:max_text_limit]
      text_to_convert = text_to_convert[max_text_limit:]
    else:
      text_to_apply = text_to_convert
      multi_run = None
    thr = threading.Thread(target=request_audio, args=(text_to_apply, gender, language,), kwargs={})
    thr.start()
    print(thr.name)
    if thr.name == 'Thread-1':
      thr.join(10)
    else:
      thr.join()

  # time.sleep(15)
  play_audio()
