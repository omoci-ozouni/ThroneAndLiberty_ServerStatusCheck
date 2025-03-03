import requests
from bs4 import BeautifulSoup
import time
import winsound
from ctypes import windll

URL = 'https://www.playthroneandliberty.com/ja-jp/support/server-status'
SERVER_NAME = 'Sunstorm'
SLEEP_TIME = 20
BEEP_DURATION = 400
MSG_TITLE = 'ThroneAndLiberty_ServerStatusCheck'

def get_server_status():
    """ サーバーステータスを取得 """
    try:
        response = requests.get(URL, timeout=6)
        soup = BeautifulSoup(response.text, "html.parser")
        server_span = soup.find("span", string=SERVER_NAME)  # 修正: text → string
        return server_span.get("aria-label") if server_span else None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def main():
    try:
        while True:
            server_status = get_server_status()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Server status: {server_status}")

            if server_status and not server_status.endswith("Maintenance"):
                break  # メンテナンス終了時にループを抜ける
            
            time.sleep(SLEEP_TIME)

        # ビープ音 3回
        for freq in [2500, 3000, 4000]:
            winsound.Beep(freq, BEEP_DURATION)

        # メッセージボックス表示
        windll.user32.MessageBoxW(0, server_status, MSG_TITLE, 0x40)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
