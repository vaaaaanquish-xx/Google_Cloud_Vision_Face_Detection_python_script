#! /usr/bin/python
# -*- coding: utf-8 -*-
'''Gooogle Cloud Vision APIに画像を投げるやつ.'''

import base64
import cv2
from requests import Request, Session
import json

# ここにAPIキーを入れる
api_key = ''
# このスクリプトを単体で実行する場合はここにファイルパスを指定
sample_img_path = 'sample.jpg'
# 検出する顔の数の最大数 (多いほどレスポンスが返ってくるのが遅い)
max_results = 4
# DISCOVERY_URLは現時点(2016/08)でこれしかないのでこのまま
DISCOVERY_URL = 'https://vision.googleapis.com/v1/images:annotate?key='


# cv画像と画像ファイルへのPathと検出最大数が引数
def facedetector_gcv(img, image_path, max_results):
    # 通信不良等を考慮してTry...expectしておく
    try:
        # base64convert用に読み込む
        image = open(image_path, 'rb').read()

        # 顔を検出するやつのResponse作成
        str_headers = {'Content-Type': 'application/json'}
        batch_request = {'requests': [{'image': {'content': base64.b64encode(image)}, 'features': [{'type': 'FACE_DETECTION', 'maxResults': max_results, }]}]}

        # セッション作ってリクエストSend
        obj_session = Session()
        obj_request = Request("POST", DISCOVERY_URL + api_key, data=json.dumps(batch_request), headers=str_headers)
        obj_prepped = obj_session.prepare_request(obj_request)
        obj_response = obj_session.send(obj_prepped, verify=True, timeout=180)

        # Responseからjsonを抽出
        response_json = json.loads(obj_response.text)
        # 返り値用
        s = ''
        # 'faceAnnotations'があれば顔あり
        if 'faceAnnotations' in response_json['responses'][0]:
            faces = response_json['responses'][0]['faceAnnotations']

            # OpenCVで矩形を書き込み
            for face in faces:
                # 0と2が両端の番地
                x = face['fdBoundingPoly']['vertices'][0]['x']
                y = face['fdBoundingPoly']['vertices'][0]['y']
                x2 = face['fdBoundingPoly']['vertices'][2]['x']
                y2 = face['fdBoundingPoly']['vertices'][2]['y']
                cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 255), thickness=10)
                # 矩形情報を保存
                s += (str(x) + ' ' + str(y) + ' ' + str(x2) + ' ' + str(y2) + ' ')
            # 画像情報
            s += image_path
        # 矩形が書き込まれた画像とs = 'x1 y1 x2 y2 x1 y1 x2 y2 file_name'
        # 顔が無ければsは空
        return img, s, response_json

    except:
        return img, ""


if __name__ == '__main__':
    # 画像読み込み
    img = cv2.imread(sample_img_path)

    # Goog;e API
    img, s, responses = facedetector_gcv(img, sample_img_path, max_results)

    # 画像出力
    cv2.imwrite('output_' + sample_img_path, img)

    # 矩形情報出力
    f = open('./rect.txt', 'w')
    f.write(s)
    f.close()
