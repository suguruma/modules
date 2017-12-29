# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 02:00:43 2017

@author: Terada
"""

import cv2
import numpy as np


def main():

    # 動画の読み込み
    cap = cv2.VideoCapture("../tmp_data/ken.MOV")

    # 動画終了まで繰り返し
    while(cap.isOpened()):

        # フレームを取得
        ret, frame = cap.read()

        # フレームを表示
        cv2.imshow("Flame", frame)

        # qキーが押されたら途中終了
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()