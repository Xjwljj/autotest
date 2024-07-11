import re
import os
import uiautomator2 as u2
import traceback
import time
import datetime

need_dump_log = False
def get_log():
    t = time.localtime()

    now_time = str(t.tm_hour) + "_" + str(t.tm_min) + "_" + str(t.tm_sec)
    log_folder = r"D:\log\ULC\log\Logs_" + now_time
    os.mkdir(log_folder)

    os.system("adb pull /sdcard/device_log.zip %s" % log_folder)
    print(os.path.abspath(log_folder))
    return

def ota_log(d ,need_start):
    global need_dump_log
    need_dump_log = False
    return
    if need_start:
        d.xpath('//*[@text="日志导出"]').click()
        time.sleep(2)
        d.xpath('//*[@resource-id="com.huawei.hiaudio:id/btn_confirm"]').click()
    print("开始导日志")
    ota_progress_text = d(resourceId="com.huawei.hiaudio:id/tv_home_log_status").get_text(timeout=5)
    result = re.match('(\d+)', ota_progress_text, re.X)
    str = "".join(result.groups(1))
    print(f'ota log progress {result}', str)
    while int(str) < 95 and ota_progress_text != '刚刚':
        try:
            if d(text="点击此处开启荣耀分享，无需流量，极速分享").exists():
                d.xpath('//*[@text="取消"]').click(timeout=5)
                break
            ota_progress_text = d(resourceId="com.huawei.hiaudio:id/tv_home_log_status").get_text(timeout=5)
            result = re.match('(\d+)', ota_progress_text, re.X)
            str = "".join(result.groups(1))
        except Exception as e:
            print(e)
        print(f'log progress {ota_progress_text}%', int(str), int(str) < 99)
        time.sleep(5)


    time.sleep(5)
    get_log()
    need_dump_log = False

    return

def ota():
    result = False
    step = 0
    global need_dump_log
    try:
        package = 'com.hihonor.android.launcher'
        device1_id = None  # '92cc093a'
        d = u2.connect(device1_id)
        d.press("back")
        time.sleep(2)
        for i, v in enumerate(d.xpath('//*').all()):
            if v.text != '':
                print("【{0:0=4}】{1}  ====".format(i, v.text),v.text)
                if v.text == 'HUAWEI FreeBuds SE 2':
                    step = 1


                if v.text == '固件更新':
                    step = 2
                if v.text == '若取消,将中断耳机升级。是否取消?':
                    step = 3
                    d.xpath(
                        '//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_dialog_negative"]').click()
        print(step, d.info)
        d.app_stop(package)
        d.app_start(package, 'com.hihonor.android.launcher.business.MainActivity')

        if d(text="	荣耀分享").exists(timeout=2):
            d(text="取消").click(timeout=2)
        if d(text="强制升级取消").exists(timeout=5):
            d.xpath('//*[@resource-id="com.huawei.hiaudio:id/dialog_title_message_negative_button"]').click()
            step = 4
            time.sleep(2)
        if d(text="文件传输过程中失败").exists(timeout=2):
            d.xpath('//*[@resource-id="com.huawei.hiaudio:id/dialog_title_message_positive_button"]').click()
        # log_te = d.xpath('//*[@resource-id="com.huawei.hiaudio:id/tv_home_log_status"]')
        # log_progress_text = log_te.test()
        # print(f'log test progress {log_progress_text}%')

        if d(text="升级成功。请关闭盒盖后再打开使用。").exists(timeout=5):
            d.xpath('//*[@resource-id="com.huawei.hiaudio:id/dialog_title_message_positive_button"]').click()
            time.sleep(2)
            d.xpath('//*[@resource-id="com.huawei.hiaudio:id/btn_cancel"]').click()
            print("升级成功")
            ota_log(d, 1)
        if need_dump_log:
            ota_log(d, 1)
            #导日志
        if d(text="正在更新…").exists(timeout=5):
            step = 4
        if step < 4:
            log_test = d(resourceId="com.huawei.hiaudio:id/tv_home_log_status").get_text()
            if re.match('(\d+) %',log_test):
                ota_log(d, 0)
                #print(log_test)
            else:
                print(log_test, re.match('(\d+) %',log_test))
        print("准备升级====================")
        if not step:
            d.xpath('//*[@text="HiAudio Studio Tool"]').click()
            time.sleep(3)
            d.xpath('//*[@resource-id="com.huawei.hiaudio:id/tv_bluetooth"]').click()
            time.sleep(2)
            step = 1
        if step == 1:
            reconnect = 0
            while not d(text="HUAWEI FreeBuds SE 2").exists(timeout=5):
                if reconnect > 10:
                    print("升级失败")
                    result = False
                    # 下拉状态栏，点击蓝牙图标
                    d.open_notification()
                    time.sleep(2)
                    d.click(0.349, 0.147)
                    time.sleep(2)
                    d.click(0.349, 0.147)
                    return result
                reconnect += 1
                print(f'重新连接 {reconnect}')
                d.xpath('//*[@resource-id="com.huawei.hiaudio:id/tv_bluetooth"]').click()
                time.sleep(7)
        print("已连接")
        step = 3
        if step == 3:
            if d(text="升级").exists:
                d.xpath('//*[@resource-id="com.huawei.hiaudio:id/iv_ota"]').click()
                time.sleep(2)
            print(d(text="这可能需要4-6分钟").exists)
            if d(text="这可能需要4-6分钟").exists(timeout=5):
                d.xpath('//*[@resource-id="com.huawei.hiaudio:id/btn_confirm"]').click()#ota 升级需要4-6分钟，点击确认

                d.xpath('//*[@content-desc="显示根目录"]').click()#选择最近的文件
                time.sleep(2)
                d.xpath('//*[@text="文件管理"]').click()
                time.sleep(2)
                d.xpath('//*[@resource-id="com.huawei.filemanager:id/file_name"]').click()#内部存储
                time.sleep(2)
            if d(text="628").exists(timeout=5):
                d.xpath('//*[@text="628"]').click()
            time.sleep(2)
            if d(text="ota.dfu").exists(timeout=5):
                d.xpath('//*[@text="ota.dfu"]').click()
            step = 4


        # time.sleep(5)
        # fw_update = d.xpath(
        #     '//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/recyclerView"]/android.widget'
        #     '.FrameLayout[4]')
        # # fw_update = d.xpath('//*[@text="固件更新"]')
        # fw_update.click()
        # print('下载并安装')
        # time.sleep(6)
        # d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_update"]').click()

        print('ota update...')
        # ota_progress = d.xpath('//*[@resource-id="com.huawei.hiaudio:id/fl_progress"]')
        # print(f'ota progress {ota_progress.text}%')
        # ota_result = d.xpath('//*[@resource-id="com.huawei.hiaudio:id/fl_progress"]')
        # ota_progress_text = ota_progress.text
        #d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_dialog_negative"]').click()
        #d.xpath('//*[@resource-id="com.hihonor.audioassistantplugin.eco.beta:id/btn_positive"]').click()#知道了
        if step == 4:
            while d(text="正在更新…").exists(timeout=1):
                need_dump_log = True
                print("ota process")


            # for i, v in enumerate(d.xpath('//*').all()):
            #     if d(text="强制升级取消").exists(timeout=1):
            #         d.xpath('//*[@resource-id="com.huawei.hiaudio:id/dialog_title_message_negative_button"]').click()
            #         time.sleep(2)
            #     if v.text:
            #
            #         if re.match('(\d+)', v.text, re.X) and not i == 43:
            #             ota_progress_text1 = re.match('(\d+)', v.text, re.X)
            #             result1 = ota_progress_text1
            #             if result1.groups(1):
            #                 str = "".join(result1.groups(1))
            #                 print("process============", str)
            #             if int(str) >= 100:
            #                 break
            #         else:
            #             print("test============NONE")
            #
            #
            # result1 = ota_progress_text1
            # if result1.groups(1):
            #     str = "".join(result1.groups(1))
            # else:
            #     printf(result1)
            # while int(str) < 100:
            #     try:
            #         # ota_progress_text1 = d.xpath('//*[@resource-id="com.huawei.hiaudio:id/fl_progress"]').info()
            #         # result1 = re.match('(\d+)', ota_progress_text1, re.X)
            #         for i, v in enumerate(d.xpath('//*').all()):
            #             if v.text:
            #                 if re.match('(\d+)', v.text, re.X):
            #                     ota_progress_text1 = re.match('(\d+)', v.text, re.X)
            #                     result1 = ota_progress_text1
            #                     print("test============", ota_progress_text1)
            #                     break
            #                 else:
            #                     print("test============NONE")
            #     except Exception as e:
            #         print(e)
            #     print(f'ota progress {ota_progress_text1}%')
            #     time.sleep(5)
            time.sleep(2)
        # if ota_result.exists:
        #     ota_result_text = ota_result.text
        #     print(ota_result_text)
        #     result = True if ota_result_text.find('升级成功') >= 0 else False
        if d(text="升级成功。请关闭盒盖后再打开使用。").exists(timeout=5):
            result = 1
        print(result)
        print('==========================',result)
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
            time.sleep(20)
        else:
            print("ota failed, wait 5S")
            time.sleep(5)

