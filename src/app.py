from selenium import webdriver
from time import sleep
from time import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import readfile
import datetime
import random
from concurrent.futures import ThreadPoolExecutor

"""
実行開始宣言
"""
print("------実行開始宣言------")

# 計測用初期時間[s]
t0 = time()
t0_datetime = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
print("計測開始時間")
print(t0_datetime)

# 1日に投票できる最大値
MAX_LIMITS_VOTES_COUNTER = 10
THREAD_COUNT = 3


class Vote:
    def __init__(self):
        self.likes_cnt = 0
        self.data_other_than_today = ""
        self.today = self.fetch_today()
        self.file_l_cnt = "likes_cnt.csv"
        self.read_csv()

    def fetch_today(self):
        today = datetime.date.today()
        return str(today)

    def read_csv(self):
        # ############本日、投票している数をファイルから取得
        self.likes_cnt, self.data_other_than_today = readfile.getVotesCntToday(
            self.today, self.file_l_cnt
        )

    def do_vote(self):
        with ThreadPoolExecutor(THREAD_COUNT) as executor:
            for index in range(MAX_LIMITS_VOTES_COUNTER):
                executor.submit(self.job)

    def job(self):
        # while num < max_limits_votes_counter:
        options = Options()
        # options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # --------STEP1--------
        # 10分メールのページオープン
        url1 = "https://10minutemail.net/m/?lang=ja"
        browser.get(url1)

        # メールアドレスの取得
        email_address = browser.find_element_by_xpath('//*[@id="span_mail"]').text

        # --------STEP2--------
        # スカパー会員登録ページオープン
        random_sleeptime = random.randint(2, 3)
        sleep(random_sleeptime)
        url2 = "https://adult-awards.com/register/"
        browser.execute_script("window.open();")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url2)

        # メアド貼り付け及び会員登録ボタン押下
        browser.find_element_by_xpath(
            '//*[@id="user_register"]/form/div[1]/input'
        ).send_keys(email_address)
        browser.find_element_by_xpath(
            '//*[@id="user_register"]/form/div[2]/input'
        ).click()
        browser.find_element_by_xpath(
            '//*[@id="user_register"]/form/div[3]/input'
        ).click()

        # --------STEP3--------
        # 10minメールに戻り受信メール開く
        sleep(random_sleeptime)
        browser.switch_to.window(browser.window_handles[0])
        browser.find_element_by_xpath('//*[@id="btn_refresh"]').click()
        sleep(1)
        browser.find_element_by_xpath('//*[@id="btn_refresh"]').click()
        sleep(random_sleeptime)
        browser.find_element_by_xpath('//*[@id="list_mail"]').click()
        sleep(random_sleeptime)
        try:
            # 受信メール内部のaタグ(リンク先▶︎会員登録ページ)をクリック
            # browser.find_element_by_xpath('//*[@id="mail_plain_body"]/a').click()
            url = browser.find_element_by_xpath('//*[@id="mail_plain_body"]/a').text
            browser.get(url)
            sleep(3)
        except Exception as e:
            print("メール本文のaタグの取得に失敗しました")
            print(e)
            browser.set_window_size(1200, 800)
            browser.save_screenshot(f"error_{self.today}.png")
            browser.quit()
            return self.job()

        # --------STEP4--------
        # スカパーユーザー登録
        # browser.switch_to.window(browser.window_handles[2])

        # パスワード入力(+確認用パスワード)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[1]/td[2]/input'
        ).send_keys("12345678")
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[2]/td[2]/input'
        ).send_keys("12345678")

        # アンケート回答
        # ---性別---
        sex_num = random.randint(1, 3)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[3]/input['
            + str(sex_num)
            + "]"
        ).click()
        # ---年齢---
        age_num = random.randint(1, 9)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[5]/input['
            + str(age_num)
            + "]"
        ).click()
        # ---結婚歴---
        marriage_history_num = random.randint(1, 2)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[7]/input['
            + str(marriage_history_num)
            + "]"
        ).click()
        # ---職業---
        occupation_num = random.randint(1, 10)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[9]/input['
            + str(occupation_num)
            + "]"
        ).click()
        # ---都道府県---
        dropdown = browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[11]/select'
        )
        select = Select(dropdown)
        area_num = random.randint(1, 47)
        select.select_by_index(area_num)
        # ---Q1---
        q1_num = random.randint(1, 2)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[14]/input['
            + str(q1_num)
            + "]"
        ).click()
        # ---Q2---
        q2_num = random.randint(1, 4)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[16]/input['
            + str(q2_num)
            + "]"
        ).click()
        # ---Q3---
        q3_num = random.randint(1, 4)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[20]/input['
            + str(q3_num)
            + "]"
        ).click()
        # ---Q4---
        q4_num = random.randint(1, 13)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[4]/td[2]/p[24]/input['
            + str(q4_num)
            + "]"
        ).click()
        # 完了送信
        survey_before_click_btn_sleep = random.randint(1, 3)
        sleep(survey_before_click_btn_sleep)
        browser.find_element_by_xpath(
            '//*[@id="page"]/div[2]/form/table/tbody/tr[5]/td/input'
        ).click()

        # --------STEP4--------
        # 投票
        browser.find_element_by_xpath('//*[@id="slide-container"]/div/div[1]/a').click()
        browser.find_element_by_xpath('//*[@id="category"]/li[8]/div/a').click()
        browser.find_element_by_xpath('//*[@id="wpvotes"]/form/a').click()
        browser.find_element_by_xpath("/html/body/div[6]/div/div").click()

        # if num == MAX_LIMITS_VOTES_COUNTER:
        #     # ブラウザ閉じる
        #     sleep(3)
        self.likes_cnt += 1
        print(f"本日分の投票実施数:{self.likes_cnt}")
        flc = open(self.file_l_cnt, "w")
        flc.write(
            self.data_other_than_today + self.today + "," + str(self.likes_cnt) + "\n"
        )
        flc.close()
        browser.quit()


if __name__ == "__main__":
    vt = Vote()
    vt.do_vote()


"""
実行終了時の出力テキスト
"""
print("------実行終了レポート------")
# プログラム終了時の時間[s]
t1 = time()
t1_datetime = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
elapsed_time = t1 - t0
print("計測開始時間:" + str(t0_datetime))
print("計測終了時間:" + str(t1_datetime))
print("プログラムの実行時間" + str(round(elapsed_time, 1)) + "秒")
print("-------------------------")
