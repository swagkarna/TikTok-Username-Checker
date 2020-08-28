import os
import time
import requests
import threading
from urllib3 import disable_warnings
disable_warnings()


class Main:
    def __init__(self):
        self.variables = {
            'available': 0,
            'unavailable': 0,
            'retries': 0
        }

    def _checker(self, arg):
        try:
            available = requests.get(
                'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/unique/id/check/?device_id=66'
                '22992447704270341&os_version=13.6.1&app_name=musical_ly&version_code=17.4.0&channe'
                f'l=App%20Store&device_platform=iphone&device_type=iPhone10,5&unique_id={arg}',
                verify=False, headers={
                    'x-Tt-Token': '0344ccb2867669f08b78f1db63b65933c1b38145729bad08b9725b6218dd2649'
                                  '4098feb938ee86b1ca42cac5fd714b8da943',
                    'sdk-version': '1'
                }
            ).json()['is_valid']
        except Exception:
            self.variables['retries'] += 1
            self._checker(arg)
        else:
            if available:
                self.variables['available'] += 1
                print(f'[AVAILABLE] {arg}')
                with open('Available.txt', 'a') as f:
                    f.write(f'{arg}\n')
            else:
                self.variables['unavailable'] += 1
                print(f'[UNAVAILABLE] {arg}')

    def _multi_threading(self):
        threading.Thread(target=self._update_title).start()
        for username in self.usernames:
            while True:
                if threading.active_count() <= 300:
                    threading.Thread(target=self._checker, args=(username,)).start()
                    break
                else:
                    continue

    def _update_title(self):
        while (checked := (self.variables['available'] + self.variables['unavailable'])) < len(
            self.usernames
        ):
            os.system(
                f'title [TikTok Username Checker] - Checked: {checked}/{self.total_usernames} ^| Av'
                f'ailable: {self.variables["available"]} ^| Unavailable: '
                f'{self.variables["unavailable"]} ^| Retries: {self.variables["retries"]}'
            )
            time.sleep(0.2)
        os.system(
            f'title [TikTok Username Checker] - Checked: {checked}/{self.total_usernames} ^| Availa'
            f'ble: {self.variables["available"]} ^| Unavailable: {self.variables["unavailable"]} ^|'
            f' Retries: {self.variables["retries"]} && pause >NUL'
        )

    def setup(self):
        error = False
        if os.path.exists((usernames_txt := 'Usernames.txt')):
            with open(usernames_txt, 'r', encoding='UTF-8', errors='replace') as f:
                self.usernames = f.read().splitlines()
            self.total_usernames = len(self.usernames)
            if self.total_usernames == 0:
                error = True
        else:
            open(usernames_txt, 'a').close()
            error = True

        if error:
            print('[!] Paste the usernames in Usernames.txt.')
            os.system(
                'title [TikTok Username Checker] - Restart required && '
                'pause >NUL && '
                'title [TikTok Username Checker] - Exiting...'
            )
            time.sleep(3)
        else:
            self._multi_threading()


if __name__ == '__main__':
    os.system('cls && title [TikTok Username Checker]')
    main = Main()
    main.setup()
