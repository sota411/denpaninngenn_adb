import subprocess
import time
import random
import string
import openpyxl

def adb_command(command):
    """ADBコマンドを実行する関数"""
    result = subprocess.run(['adb', 'shell'] + command.split(), capture_output=True, text=True)
    return result.stdout.strip()

def generate_random_string(length=5):
    """指定した長さのランダムな文字列を生成する関数"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def navigate_to_tethering_settings():
    """テザリング設定画面に移動する関数"""
    adb_command('am start -a android.intent.action.MAIN -n com.android.settings/.TetherSettings')
    time.sleep(2)  # 設定画面が開くまで待つ

def change_ssid(ssid):
    """SSIDを変更する関数"""
    adb_command('input keyevent 19')  # 上キーを押してナビゲート（必要に応じて回数を調整）
    adb_command('input keyevent 20')
    adb_command('input keyevent 23')  # SSIDフィールドを選択
    for _ in range(10):
        adb_command('input keyevent 67')  # 既存のSSIDを削除
    adb_command(f'input text "{ssid}"')  # 新しいSSIDを入力
    adb_command('input keyevent 61') 
    adb_command('input keyevent 61') 
    adb_command('input keyevent 66')  # Enterキーを押して確定
    time.sleep(2.1)

def change_password(password):
    """パスワードを変更する関数"""
    adb_command('input keyevent 20')  # 下キーを押してパスワードフィールドに移動（必要に応じて回数を調整）
    adb_command('input keyevent 20')
    adb_command('input keyevent 23')  # パスワードフィールドを選択
    for _ in range(15):
        adb_command('input keyevent 67')  # 既存のパスワードを削除
    adb_command(f'input text "{password}"')  # 新しいパスワードを入力
    adb_command('input keyevent 61') 
    adb_command('input keyevent 61') 
    adb_command('input keyevent 66')  # Enterキーを押して確定
    time.sleep(0.1)

def save_to_excel(ssid, password, filename='ssid_passwords.xlsx'):
    """SSIDとパスワードをExcelファイルに保存する関数"""
    try:
        # 既存のExcelファイルを開く
        workbook = openpyxl.load_workbook(filename)
    except FileNotFoundError:
        # ファイルが存在しない場合は、新しいWorkbookを作成
        workbook = openpyxl.Workbook()
        # シートの最初の行にヘッダーを追加
        workbook.active.append(["SSID", "Password"])  

    # アクティブなシートを取得
    sheet = workbook.active
    # シートにSSIDとパスワードを追加
    sheet.append([ssid, password])
    # ファイルを保存
    workbook.save(filename)

def main():
    while True:
        ssid = generate_random_string(5)  # ランダムなSSIDを生成
        password = generate_random_string(12)  # ランダムなパスワードを生成

        print(f"Changing SSID to: {ssid} and Password to: {password}")

        # 生成したSSIDとパスワードをExcelに保存
        save_to_excel(ssid, password)

        # navigate_to_tethering_settings()  # テザリング設定画面へ移動
        change_ssid(ssid)  # SSIDを変更
        # change_password(password)  # パスワードを変更

        time.sleep(30)  # 5秒待機（次のループに移行する前に待機）

if __name__ == "__main__":
    main()


