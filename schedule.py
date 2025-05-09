from apscheduler.schedulers.blocking import BlockingScheduler
from raw import load_and_save_raw
from transform import transform_merapi

sched = BlockingScheduler()
sched.add_job(load_and_save_raw,  'cron', minute='0')   # setiap jam
sched.add_job(transform_merapi,   'cron', minute='5')   # jam +5 menit
sched.start()
