import uiautomator2 as u2
import traceback
import time
import datetime


def ota():
    result = False
    try:
        package = 'com.hihonor.magichome'
        device1_id = None  # '92cc093a'
        d = u2.connect(device1_id)
        print(d.info)
        d.app_stop(package)
        d.app_start(package, 'com.hihonor.magichome.business.MainActivity')
        d.xpath('//*[@resource-id="com.hihonor.magichome:id/device_card_container"]').click()
        # d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]'
        #         '/android.widget.FrameLayout[4]/android.widget.RelativeLayout[1]').click()
        d.watcher.start()
        d.watcher.start(2.0)
        print('检查设备是否连接')
        reconnect = 0
        while not d(text="已连接").exists(timeout=5):
            if reconnect > 10:
                print("升级失败")
                result = False
                return result
            reconnect += 1
            print(f'重新连接 {reconnect}')
            d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_reconnection"]').click()
            time.sleep(3)
        print('固件更新')
        d(scrollable=True).scroll.toEnd()
        #d(scrollable=True).scroll.horiz.toEnd()
        time.sleep(1)

        d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_reconnection"]').setAsVerticalList()
        d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_reconnection"]').scrollBackward()
        fw_update = d.xpath(
            '//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]/android.widget'
            '.FrameLayout[4]')
        # fw_update = d.xpath('//*[@text="固件更新"]')
        fw_update.click()
        print('下载并安装')
        time.sleep(2)
        d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_update"]').click()
        print('ota update...')
        ota_progress = d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_progress_num"]')
        print(f'ota progress {ota_progress.text}%')
        ota_result = d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/tv_content"]')
        ota_progress_text = ota_progress.text
        while ota_result.exists is False and int(ota_progress_text) < 100:
            try:
                ota_progress_text = ota_progress.text
                print('try catch again222\n')
            except Exception as e:
                if ota_progress_text:
                    print('finally return %d\n',ota_progress_text)
                else:
                    print("try again\n")
            print(f'ota progress {ota_progress_text}%')
            time.sleep(1)
        time.sleep(2)
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
        ota()
        time.sleep(50)
