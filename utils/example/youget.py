import subprocess, time


def download_by_url(url):
    # p = subprocess.Popen('you-get --itag=135 -x 127.0.0.1:1080 "' + url +'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = subprocess.Popen('youtube-dl --proxy 127.0.0.1:1080 "' + url +'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # p = subprocess.Popen('you-get -i -x 127.0.0.1:1080 "' + url +'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("********\tStart download:" + url + "\t")
    while True:
        line = p.stdout.readline()
        if line:
            print(line)
        else:
            break
    print("********\tEnd\t")

# download_by_url('https://www.bilibili.com/video/av44814898/')
download_by_url('https://www.youtube.com/watch?v=RIK76FiITBo')