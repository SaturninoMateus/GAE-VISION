import json

import urllib
import urllib2

KEY = 'AIzaSyAnZTOVW-QB022OSgtdTnZOQ4Qm8DyHkr0'
URL = 'https://vision.googleapis.com/v1/images:annotate?key=' + KEY

EMOTIONS_MAP = {
    'joyLikelihood': 'joy.jpg',
    'sorrowLikelihood': 'sorrow.png',
    'angerLikelihood': 'anger.jpg',
    'surpriseLikelihood': 'surprised.jpg',
}

LIKELYHOOD_PRIORITY = ['VERY_LIKELY', 'LIKELY', 'UNLIKELY', 'VERY_UNLIKELY']


def get_emoji(file_url):
    '''
    :param file_url: image url
    :return: the emoji file name
    '''
    # requests_session = requests.session()
    # r = requests_session.post(URL)

    data = {
        "requests": [
            {
                "image": {
                    "source": {
                        "imageUri": file_url
                    }
                },
                "features": [
                    {
                        "type": "FACE_DETECTION"
                    },
                    {
                        "type": "LANDMARK_DETECTION"
                    }
                ]
            }
        ]
    }

    try:
        data = json.dumps(data)
        req = urllib2.Request(URL, data, headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        r = urllib2.urlopen(req)
        if r.code == 200:
            content = r.read()
            r = json.loads(content)
            face_detected = r.get('responses')[0].get('faceAnnotations', False)
            if not face_detected:
                return ''
    except:
        raise Exception("Could not post!")

    likelyhood_list = []
    emoji = ''
    for emotion in EMOTIONS_MAP.keys():
        likelyhood = r['responses'][0]['faceAnnotations'][0].get(emotion)
        if likelyhood not in likelyhood_list:
            likelyhood_list.append(likelyhood)

    for value in LIKELYHOOD_PRIORITY:
        if value in likelyhood_list:
            likely_emotion = value
            break

    if likely_emotion:
        for emotion in EMOTIONS_MAP.keys():
            likelyhood = r['responses'][0]['faceAnnotations'][0].get(emotion)
            if likelyhood == likely_emotion:
                emoji = EMOTIONS_MAP.get(emotion)
                break
    else:
        return emoji

    return emoji
