#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/7/5 18:06
# @Author : wangjie
# @File : file_util.py
# @project : SensoroApiAutoTest

import os
import shutil
import zipfile

from core.logger import logger


class FileUtil:
    """文件和目录操作工具类，所有方法均为静态方法，无需实例化直接调用"""

    @staticmethod
    def list_files(directory: str, prefix: str = '', suffix: str = '') -> list[str]:
        """
        递归获取目录下所有文件路径，支持按文件名前缀/后缀过滤

        :param directory: 目标目录的绝对路径
        :param prefix: 文件名前缀过滤，仅返回以该字符串开头的文件，为空则不过滤
        :param suffix: 文件名后缀过滤，仅返回以该字符串结尾的文件（如 '.yaml'），为空则不过滤
        :return: 满足过滤条件的文件绝对路径列表
        """
        result: list[str] = []
        # root：表示获取的目录的路径，以string形式返回值。
        # _： 包含了当前dirpath路径下所有的子目录名字（不包含目录路径），以列表形式返回值。
        # files：包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）。
        for root, _, files in os.walk(directory):
            for f in files:
                # 前缀/后缀匹配
                if f.startswith(prefix) and f.endswith(suffix):
                    result.append(os.path.join(root, f))
        return result

    @staticmethod
    def get_newest_file(dir_path: str) -> str | None:
        """
        获取目录下最新修改的文件路径，按文件修改时间（mtime）降序排列后取第一条

        :param dir_path: 目标目录的绝对路径，传入文件路径时将返回 None
        :return: 最新文件的绝对路径，目录为空或传入的路径非目录时返回 None
        """
        if not os.path.isdir(dir_path):
            logger.warning(f"传入路径不是目录: {dir_path}")
            return None

        files = os.listdir(dir_path)
        if not files:
            logger.warning(f"目录为空: {dir_path}")
            return None

        sorted_files = sorted(
            [(os.path.join(dir_path, f), os.path.getmtime(os.path.join(dir_path, f))) for f in files],
            key=lambda x: x[1],
            reverse=True,
        )
        return sorted_files[0][0]

    @staticmethod
    def zip_file(in_path: str, out_path: str) -> None:
        """
        将指定目录压缩为 zip 文件

        :param in_path: 要压缩的目标目录绝对路径
        :param out_path: 压缩文件保存路径，需包含完整文件名（如 /data/output.zip）
        """
        if not os.path.isdir(in_path):
            logger.warning(f"目标路径不是目录，跳过压缩: {in_path}")
            return

        logger.info(f"开始压缩目录: {in_path} -> {out_path}")
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for path, _, filenames in os.walk(in_path):
                # 去掉目标根路径，仅保留相对路径结构进行压缩
                arc_dir = path.replace(in_path, '')
                for filename in filenames:
                    zf.write(
                        os.path.join(path, filename),
                        os.path.join(arc_dir, filename),
                    )
        logger.info(f"压缩完成: {out_path}")

    @staticmethod
    def delete_dir_file(file_path: str) -> None:
        """
        删除指定目录下的所有一级子文件和子目录（不递归删除子目录内容）

        注意：仅处理传入目录下的直接子项，不递归删除深层嵌套内容。
        若子目录非空，os.rmdir 会失败，此时请手动清理或改用 shutil.rmtree。

        :param file_path: 目标目录的绝对路径
        """
        if not os.path.isdir(file_path):
            logger.warning(f"目标路径不是目录: {file_path}")
            return

        items = os.listdir(file_path)
        if not items:
            logger.info(f"目标目录已是空目录: {file_path}")
            return

        logger.info(f"开始清空目录: {file_path}")
        for item in items:
            full_path = os.path.join(file_path, item)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                os.rmdir(full_path)

    @staticmethod
    def copy_file(src_file_path: str, dest_dir_path: str) -> None:
        """
        复制文件到目标目录，目标路径可以是目录或带新文件名的完整路径

        :param src_file_path: 源文件的绝对路径
        :param dest_dir_path: 目标路径，若以分隔符结尾或指向已有目录，则保持源文件名；
                              若指定完整文件名，则复制并重命名
        :raises FileNotFoundError: 源文件不存在
        """
        if not os.path.isfile(src_file_path):
            raise FileNotFoundError(f"源文件不存在: {src_file_path}")

        shutil.copy(src_file_path, dest_dir_path)
        logger.info(f"文件复制成功: {src_file_path} -> {dest_dir_path}")

    @staticmethod
    def get_file_field(file_path: str) -> tuple[str, bytes]:
        """
        获取文件的名称和二进制内容，用于文件上传等场景

        :param file_path: 文件的绝对路径
        :return: (文件名, 二进制内容) 元组
        """
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            file_content = f.read()
        return file_name, file_content

    @staticmethod
    def get_relative_path(file_path: str, directory_path: str) -> str:
        """
        计算文件路径相对于目标目录的相对路径（不含文件名部分）

        示例：
            file_path     = data/gitlink/project/test_login_demo.yaml
            directory_path = data
            返回           = gitlink/project

        :param file_path: 文件绝对路径
        :param directory_path: 参考目录绝对路径
        :return: 文件所在目录相对于目标目录的相对路径（不含文件名）
        """
        rel = os.path.relpath(os.path.abspath(file_path), os.path.abspath(directory_path))
        return os.path.dirname(rel)


if __name__ == '__main__':
    print(FileUtil.list_files('/Users/wangjie/SensoroApi/config'))
