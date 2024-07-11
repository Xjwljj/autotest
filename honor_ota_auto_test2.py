import uiautomator2 as u2
import traceback
import time
import datetime


def ota():
    result = False
    step = 0
    try:
        package = 'com.google.android.apps.nexuslauncher'
        device1_id = None  # '92cc093a'
        d = u2.connect(device1_id)
        d.press("back")
        time.sleep(2)
        for i, v in enumerate(d.xpath('//*').all()):
            if v.text != '':
                print("【{0:0=4}】{1}  ====".format(i, v.text),v.text)
                if v.text == '荣耀亲选耳机X5s Pro':
                    step = 1
                if v.text == '固件更新':
                    step = 2
                if v.text == '若取消,将中断耳机升级。是否取消?':
                    step = 3
                    d.xpath(
                        '//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_dialog_negative"]').click()
        print(step,d.info)
        d.app_stop(package)
        d.app_start(package, 'com.google.android.apps.nexuslauncher.business.MainActivity')


        if not step:
            d.xpath('//*[@text="智慧空间"]').click()
            time.sleep(3)
            d.xpath('//*[@resource-id="com.hihonor.magichome:id/btn_magic"]').click()
            time.sleep(2)
            step = 1
        if step == 1:
            d.xpath('//*[@resource-id="com.hihonor.magichome:id/device_card_container"]').click()
            step = 2
        # d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]'
        #         '/android.widget.FrameLayout[4]/android.widget.RelativeLayout[1]').click()
        print('检查设备是否连接')
        reconnect = 0
        if step == 2:
            while not d(text="已连接").exists(timeout=5):
                if reconnect > 10:
                    print("升级失败")
                    result = False
                    #下拉状态栏，点击蓝牙图标
                    d.open_notification()
                    time.sleep(2)
                    d.click(0.349, 0.147)
                    time.sleep(2)
                    d.click(0.349, 0.147)
                    return result
                reconnect += 1
                print(f'重新连接 {reconnect}')
                d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_reconnection"]').click()
                time.sleep(7)
        print('固件更新')
        d.swipe_ext('up', scale=1)
        time.sleep(5)
        fw_update = d.xpath(
            '//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]/android.widget'
            '.FrameLayout[4]')
        # fw_update = d.xpath('//*[@text="固件更新"]')
        fw_update.click()
        print('下载并安装')
        time.sleep(6)
        d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_update"]').click()
        print('ota update...')
        ota_progress = d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_progress_num"]')
        print(f'ota progress {ota_progress.text}%')
        ota_result = d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_content"]')
        ota_progress_text = ota_progress.text
        #d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_dialog_negative"]').click()
        #d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_positive"]').click()#知道了
        while ota_result.exists is False and ota_progress.exists and int(ota_progress_text) < 100:
            try:
                ota_progress_text = ota_progress.text
            except Exception as e:
                print(e)
            print(f'ota progress {ota_progress_text}%')
            time.sleep(5)
        time.sleep(2)
        if ota_result.exists:
            ota_result_text = ota_result.text
            print(ota_result_text)
            result = True if ota_result_text.find('升级成功') >= 0 else False
        print(result)
        print('==========================',ota_result.exists)
        step = 0
        return result
    except Exception as e:
        print(e)
        print(str(traceback.format_exc()))
        step = 0
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

