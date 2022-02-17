import time
import schedule
import refresh


def run():
    refresh.Refresh().save_cookies()
    print("refresh successfully")

schedule.every(8).minutes.do(run)
while True:
    schedule.run_pending()