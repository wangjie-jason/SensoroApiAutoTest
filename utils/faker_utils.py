#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2023/8/7 11:14
# @Author : wangjie
# @File : faker_utils.py
# @project : SensoroApiAutoTest
import random

from faker import Faker


class FakerUtils:

    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    def random_int(self) -> int:
        """
        :return: 5000以内随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def random_IDcard(self) -> str:
        """
        :return: 随机生成身份证号码
        """
        id_card = self.faker.ssn()
        return id_card

    def random_name(self) -> str:
        """
        :return: 随机姓名
        """
        while True:
            name = self.faker.name()
            if '敏感词' not in name:
                break
        return name

    def random_female_name(self) -> str:
        """
        :return: 随机女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def random_male_name(self) -> str:
        """
        :return: 随机男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def random_adress(self) -> str:
        """
        :return: 随机地址
        """
        adress = self.faker.adress()
        return adress

    def random_mobile(self) -> str:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone

    def random_email(self) -> str:
        """
        :return: 生成邮箱
        """
        email = self.faker.email()
        return email


if __name__ == '__main__':
    s = FakerUtils().random_IDcard()
    print(s)
    print(type(s))
