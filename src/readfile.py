#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 本日の投票した回数を取得する関数
def getVotesCntToday(today, file_l_cnt):

    likes_cnt = ""
    data_other_than_today = ""
    file_check = os.path.isfile(file_l_cnt)
    if file_check:# ファイルが存在した

        with open(file_l_cnt, 'r') as f:
        	for row in f:
        		if row != "":
        			date, num = row.split(',')
                    # print(date)
                    # print(likes_cnt)
        			if date == today:
        				likes_cnt = int(num.strip())
        			else:
        				data_other_than_today += row
        f.close()
        # ファイル内に本日の日付が見つからなかった場合
        if likes_cnt == "":
        	f = open(file_l_cnt, 'a')
        	f.write(today + '\t0\n')
        	likes_cnt = 0
        	f.close()

    else:#ファイルが存在しなかった
        f = open(file_l_cnt, 'w')
        f.write(today + ',0')
        likes_cnt = 0
        f.close()

    print(f"本日（{today}）すでに投票している数 : {likes_cnt}")
    return likes_cnt, data_other_than_today
