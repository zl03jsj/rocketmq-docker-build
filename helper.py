import os
import platform
import shutil
import time

import alive_progress
import psutil as psutil

from context import Context


class Helper(object):
    """
    工具类
    """

    @staticmethod
    def get_current_work_dir() -> str:
        """
        获取当前工作目录

        :return:
        """
        return os.getcwd()

    @staticmethod
    def is_os_support_java() -> bool:
        """
        操作系统支持java命令

        :return: 布尔值
        """
        return Helper.__is_os_tool("java")

    @staticmethod
    def is_os_support_javac() -> bool:
        """
        操作系统支持javac命令

        :return: 布尔值
        """
        return Helper.__is_os_tool("javac")

    @staticmethod
    def is_os_support_mvn() -> bool:
        """
        操作系统支持mvn命令

        :return: 布尔值
        """
        return Helper.__is_os_tool("mvn")

    @staticmethod
    def is_os_support_docker() -> bool:
        """
        操作系统支持docker命令

        :return: 布尔值
        """
        return Helper.__is_os_tool("docker")

    @staticmethod
    def __is_os_tool(cmd_tool_name: str) -> bool:
        """
        操作系统支持命令工具

        :param cmd_tool_name: 命令行程序名
        :return: 布尔值
        """
        return shutil.which(cmd_tool_name) is not None

    @staticmethod
    def is_docker_runing() -> bool:
        """
        docker正在运行

        :return: 布尔值
        """
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "docker.exe" or p.name() == "dockerd":
                return True

        return False

    @staticmethod
    def is_linux() -> bool:
        """
        是linux系统

        :return: 布尔值
        """
        return Helper.__get_sys_name() == "linux"

    @staticmethod
    def is_mac() -> bool:
        """
        是mac系统

        :return: 布尔值
        """
        return Helper.__get_sys_name() == "darwin"

    @staticmethod
    def is_wondows() -> bool:
        """
        是windows系统

        :return: 布尔值
        """
        return Helper.__get_sys_name() == "windows"

    @staticmethod
    def __get_sys_name() -> str:
        """
        获取操作系统名称

        :return: 操作系统名称字符串
        """
        return platform.system().lower()

    @staticmethod
    def print_error(str_: str):
        """
        打印错误

        :param str_: 字符串
        :return: None
        """
        print("\033[1;31m%s\033[0m" % str_)

    @staticmethod
    def print_warn(str_: str):
        """
        打印警告

        :param str_: 字符串
        :return: None
        """
        print("\033[1;33m%s\033[0m" % str_)

    @staticmethod
    def cmd_clean() -> None:
        """
        清屏

        :return: None
        """
        sys_name = Helper.__get_sys_name()
        if sys_name == "windows":
            os.system("cls")
        elif sys_name == "mac" or sys_name == "linux":
            os.system("clear")

    @staticmethod
    def progress(title: str, fn, /, *args, **kwargs):
        """
        显示进度条

        :param title: 进度条标题
        :param fn: 函数
        :param args: 函数的参数
        :param kwargs: 函数的参数
        :return: None
        """
        future = Context.executor.submit(fn, *args, **kwargs)
        with alive_progress.alive_bar(title=title, unknown="triangles",
                                      force_tty=True, receipt=False) as bar:
            while True:
                if future.done():
                    break
                else:
                    bar()
                    time.sleep(.1)