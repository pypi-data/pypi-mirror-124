import subprocess
import os
# from debug.utils.cmd.custom_exception import *
# from adb_tools.providers.custom_exception import InstallApplicationError
from iOS_tools.custom_exception import InstallApplicationError, UninstallApplicationError


def get_app_version(bundle_identifier):
    f = os.popen(r"ideviceinstaller -l | grep %s" % bundle_identifier, "r")
    out = f.read()
    f.close()
    app_info = [x.replace('"', "").strip() for x in out.split(',') if x != '']
    return app_info[1] if len(app_info)>1 else None


def get_local_ios_device_info():
    f = os.popen(r"idevice_id -l", "r")
    out = f.read()
    f.close()
    device_id_list = [x for x in out.split('\n') if x != '']  # 去掉空''
    return device_id_list


def get_ios_device_info(device_udid):
    f_name = os.popen(r"ideviceinfo -u %s -k DeviceName" % device_udid, "r")
    device_name = f_name.read().replace('\n', '')
    f_name.close()
    f_product_name = os.popen(r"ideviceinfo -u %s -k ProductName" % device_udid, "r")
    device_platform = f_product_name.read().replace('\n', '')
    f_product_name.close()
    f_product_version = os.popen(r"ideviceinfo -u %s -k ProductVersion" % device_udid, "r")
    device_version = f_product_version.read().replace('\n', '')
    f_product_version.close()
    f_product_type = os.popen(r"ideviceinfo -u %s -k ProductType" % device_udid, "r")
    product_model = f_product_type.read().replace('\n', '')
    f_product_type.close()
    # ProductType 手机型号
    # 排除不正确的udid
    if "No device found with udid" not in device_name:
        return {"name": device_name, "platform": device_platform, "build_version": device_version, "product_model": product_model, "udid": device_udid}
    return None


def get_device_info():
    f = os.popen(r"instruments -s devices", "r")
    out = f.read()
    f.close()
    string_list = [x for x in out.split('\n') if x != '']  # 去掉空''
    try:
        string_list.pop(0)      # 去掉首个元素 Known Devices
        return string_list
    except Exception as e:
        print(e)
        return list()


def get_ios_device_udid_simulator():
    string_list = get_device_info()
    print(string_list)
    info_list = list()
    for x in string_list:
        if '(' in x and '[' in x and 'null' not in x:
            info_list.append({"name": x.split('(')[0].strip(),
                              "platform_version": x.split('(')[1].split(')')[0],
                              "udid": x.split('[')[1].split(']')[0],
                              "platform_name": 'iOS ' + x.split('(')[2].split(')')[0] if len(x.split('(')) > 2 else 'iOS'
                              }
                             )
    print(info_list)
    return info_list


def get_ios_real_device():
    string_list = get_device_info()
    print(string_list)
    info_list = list()
    for x in string_list:
        if '(' in x and '[' in x and 'null' not in x and len(x.split('(')) <= 2:
            info_list.append({"name": x.split('(')[0].strip(),
                              "platform_version": x.split('(')[1].split(')')[0],
                              "udid": x.split('[')[1].split(']')[0],
                              "platform_name": 'iOS'
                              })
    print(info_list)
    return info_list


def install_ipa_for_device(udid, ipa_path):
    cmds = "ideviceinstaller -u %s -i %s" % (udid, ipa_path)
    print(cmds)
    proc = subprocess.Popen(
        cmds,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()
    if proc.returncode == 0:
        print('安装成功')
    else:
        buff = proc.stdout.readline()
        raise InstallApplicationError((buff, proc.stderr.readlines()))


def uninstall_app_for_device(udid, bundle_identifier):

    cmds = "ideviceinstaller -u %s -U %s" % (udid, bundle_identifier)
    print(cmds)
    proc = subprocess.Popen(
        cmds,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.wait()
    if proc.returncode == 0:
        print('卸载成功')
    else:
        buff = proc.stdout.readline()
        raise UninstallApplicationError((buff, proc.stderr.readlines()))


def get_installed_app_list(udid):
    f = os.popen(r"ideviceinstaller -u %s -l" % udid, "r")
    app_list = [x for x in f.read().split('\n') if x != '']  # 去掉空''
    f.close()
    app_info_list = list()

    def f(x):
        return x.replace('"', '').replace(' ', '')
    try:
        app_list.pop(0)
        for app in app_list:
            info = list(map(f, app.split(',')))
            app_info_list.append({'package': info[0], "version": info[1], "name": info[2]})
    except Exception as e:
        print(e)
    return app_info_list


if __name__ == '__main__':
    # print(get_installed_app_list('00008030-001911663EE0802E'))
    print(get_ios_device_info("00008030-001911663EE0802E"))
