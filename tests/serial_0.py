#!/usr/bin/env python
# -*- coding: utf-8 -*

#
# @author XU Kai(xukai.ken@gmail.com)
# @date 2016-12-04 星期日
#
#
# #fileOverview 树莓派串口操作事件，用来输入和输出陀螺仪数据信息 
#
#
#

import os
import sys
import math
import codecs

import serial

sensor = serial.Serial(port='/dev/ttyAMA0', baudrate='9600', timeout=1)

while True:
    data = sensor.read(size=1)
    if (data == b'\x55'):
        print('Get the data !')
        sensor.read(size=10)

        break

    print('trying', data)


def convert(hexVal):
    return int(codecs.encode(hexVal, 'hex'), 16)


try:
    while True:
        data = sensor.read(size=11)
        if not len(data) == 11:
            print('Byte error !')
            break

        if data[1] == b'\x54':

            x = convert(data[2:4])
            y = convert(data[4:6])
            z = convert(data[6:8])

            print("Magnetic output:{}, {}, {}".format(x, y, z))

        #Angle
        elif data[1] == 83:
            x = convert(data[2:4]) / 32768 * 180
            y = convert(data[4:6]) / 32768 * 180
            z = convert(data[6:8]) / 32768 * 180

            print("Angle output:{}, {}, {}".format(x, y, z))

        #Acceleration
        elif data[1] == b'\x51':
            x = convert(data[2:4]) / 32768 * 16
            y = convert(data[4:6]) / 32768 * 16
            z = convert(data[6:8]) / 32768 * 16

            print("Acceleration output:{}, {}, {}".format(x, y, z))

        print("----", data[0], data[1])

except KeyboardInterrupt:
    sensor.close()
    print('Close the sensor !')