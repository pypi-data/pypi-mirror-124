import re
import zipfile

from adb_tools.providers.anr import ANR
from adb_tools.providers.crash import CRASH


def get_anr_info(file_path):
    # 1.解压
    zipFile = zipfile.ZipFile(file_path, 'r')
    file_name = file_path.split('/')[-1].split('.zip')[0]
    data = zipFile.read('%s.txt' % file_name)
    zipFile.close()
    # 2.解析
    try:
        anr_reason = str(re.split(b'ANR time: ', data)[-1], encoding='utf-8')
        lins = anr_reason.splitlines(keepends=True)
        for word in lins:
            if 'Reason:' in word:
                # 3.输出
                return ANR(reason=word.split('Reason: ')[-1], time=lins[0].strip())
    except Exception as e:
        print(e)
        # 没有anr
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
    print(get_crash_info('/Users/zhuhuiping/Desktop/脚本/crash.log'))


