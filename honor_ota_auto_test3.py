import os

import uiautomator2 as u2
import traceback
import time
import datetime


def start_android_app(package_name: str, activity_name: str, device_id=''):
    try:
        name = package_name + '/' + activity_name
        if device_id != '':
            cmd = 'adb -s "%s" shell am start -n %s' % (device_id, name)
        else:
            cmd = 'adb shell am start -n %s' % name
        os.system(cmd)
        print('os.system ' + cmd)
    except BaseException as e:
        print("start_android_app_error:%s" % str(e))


def stop_android_app(package_name: str, device_id=''):
    try:
        name = package_name
        if device_id != '':
            cmd = 'adb -s %s shell am force-stop %s' % (device_id, name)
        else:
            cmd = 'adb shell am force-stop %s' % name
        os.system(cmd)
        print('os.system ' + cmd)
    except BaseException as e:
        print("stop_android_app_error:%s" % str(e))


def ota():
    result = False
    try:
        #package = 'com.hihonor.magichome'
        package1 = 'com.hihonor.android.launcher'
        device1_id = None  # '92cc093a'
        d = u2.connect(device1_id)
        print(d.info)
        # d.app_stop(package)
        # d.app_start(package, 'com.hihonor.magichome.business.MainActivity')
        #stop_android_app(package)
        #start_android_app(package, 'com.hihonor.magichome.business.MainActivity')
        stop_android_app(package1)
        start_android_app(package1,'com.hihonor.android.launcher.business.MainActivity')
        time.sleep(2)
        d.xpath('//*[@resource-id="com.hihonor.magichome:id/device_card_container"]').click(timeout=5)
        # d.xpath('//*[@resource-id="com.hihonor.magichome:id/feed_list"]/android.widget.FrameLayout[2]').click()
        # d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]'
        #         '/android.widget.FrameLayout[4]/android.widget.RelativeLayout[1]').click()
        print('检查设备是否连接')
        reconnect = 0
        while not d(text="已连接").exists(timeout=5):
            if reconnect > 10:
                print("升级失败")
                result = False
                return result
            reconnect += 1
            print(f'重新连接 {reconnect}')
            d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_reconnection"]').click(timeout=5)
            time.sleep(3)
        print('固件更新')
        d.swipe_ext('up', scale=1)
        time.sleep(1)
        fw_update = d.xpath(
            '//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]/android.widget'
            '.FrameLayout[4]')
        # fw_update = d.xpath('//*[@text="固件更新"]')
        fw_update.click(timeout=5)
        print('下载并安装')
        time.sleep(2)
        d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_update"]').click(timeout=5)
        print('ota update...')
        ota_progress = d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_progress_num"]')
        print(f'ota progress {ota_progress.text}%')
        ota_result = d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_content"]')
        ota_progress_text = ota_progress.text
        while ota_result.exists is False and ota_progress.exists and int(ota_progress_text) < 100:
            try:
                ota_progress_text = ota_progress.text
            except Exception as e:
                print(e)
            print(f'ota progress {ota_progress_text}%')
            time.sleep(1)
        time.sleep(2)
        if ota_result.exists:
            ota_result_text = ota_result.text
            print(ota_result_text)
            result = True if ota_result_text.find('升级成功') >= 0 else False
        print(result)
        return result
    except Exception as e:
        print(e)
        print(str(traceback.format_exc()))
        return result


if __name__ == '__main__':
    print("ota auto test start")
    upgrade_count = 0
    while True:
        upgrade_count += 1
        print("upgrade_count ", upgrade_count)
        if ota():
            print("ota finish, wait 50S")
            time.sleep(50)
        else:
            print("ota failed, wait 5S")
            time.sleep(5)
