import os
import re
import zipfile

from adb_tools.providers.anr import ANR
from adb_tools.providers.crash import CRASH


def get_anr_info(file_path):
    zipFile = zipfile.ZipFile(file_path, 'r')
    anr_file_name = ''
    anr_file_time = '1997-01-01-00-00-00-000'
    for file_name in zipFile.namelist():
        if 'anr_' in file_name:
            time = file_name.split('anr_')[1]
            if time > anr_file_time:
                anr_file_name = file_name
                anr_file_time = time
    print(anr_file_name)
    if len(anr_file_name) == 0: return
    data = zipFile.read(anr_file_name).decode()
    zipFile.close()
    # 2.解析

    if '"main" prio=5 tid=1 Native' in data:
        anr_reason = data.split('"main" prio=5 tid=1 Native')[1].split('\n\n')[0]
        return ANR(reason=anr_reason, time=anr_file_time)
    else:
        return


def get_crash_info(file_path):
    f = open(file_path, 'r')
    data = f.read()

    def get_value(key, split_key):
        return data.split(key)[1].split(split_key)[0].strip("'") if len(data.split(key))>1 else None
    f.close()
    title = get_value(' : ', '\n')
    procese = get_value('Process name is', '\n')
    ABI = get_value('ABI: ', '\n')
    time = get_value('Timestamp: ', '\n')
    # fingerprint = get_value("Build fingerprint: '", '/')
    fingerprint = data.split("Build fingerprint: '")[1].split('/') if len(data.split("Build fingerprint: '"))>1 else None
    channel = fingerprint[0]
    device_model = fingerprint[1]
    device_os_version = fingerprint[2]
    pid = get_value("pid: ", ',')
    tid = get_value('tid: ', ',')
    other_threads = get_value('tid: %s, name:' % tid, '\n')
    backtrace = get_value('backtrace:', 'F libc    :')
    return CRASH(title, time=time, process=procese, ABI=ABI, channel=channel, device_model=device_model,
                 device_os_version=device_os_version, pid=pid, tid=tid, other_threads=other_threads,
                 backtrace=backtrace)


if __name__ == '__main__':
    # print(get_anr_info('/Users/zhuhuiping/Downloads/bugreport-BMH-AN10-HUAWEIBMH-AN10-2021-06-24-21-39-49.zip'))
    print(get_anr_info('/Users/zhuhuiping/Downloads/bugreport-BMH-AN10-HUAWEIBMH-AN10-2021-06-24-21-39-49.zip'))
    # print(get_crash_info('/Users/zhuhuiping/Desktop/脚本/crash.log'))
    # print(os.listdir('/Users/zhuhuiping/Desktop/脚本/bugreport'))
    # print(get_anr_info('/Users/zhuhuiping/Desktop/脚本/bugreport.zip'))


