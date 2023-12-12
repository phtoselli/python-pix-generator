#!/usr/bin/python3
# -*- coding: utf-8 -*-

import crcmod
import qrcode
import os

class Payload():
  def __init__(self, name, pixKey, value, city, description, directory=''):

    self.name             = name
    self.pixKey           = pixKey
    self.value            = value.replace(',', '.')
    self.city             = city
    self.description      = description
    self.qrCodeDirectory  = directory

    self.name_size        = len(self.name)
    self.pixKey_size      = len(self.pixKey)
    self.value_size       = len(self.value)
    self.city_size        = len(self.city)
    self.description_size = len(self.description)

    self.payloadFormat        = '000201'
    self.merchantCategoryCode = '52040000'
    self.transactionCurrency  = '5303986'
    self.countryCode          = '5802BR'
    self.crc16                = '6304'
    self.gui                  = '0014BR.GOV.BCB.PIX01'

    self.merchantAccount_size   = f'{self.gui}{self.pixKey_size:02}{self.pixKey}'
    self.transactionAmount_size = f'{self.value_size:02}{float(self.value):.2f}'
    self.merchantName_size      = f'{self.name_size:02}'
    self.merchantCity_size      = f'{self.city_size:02}'
    self.addDataField_size      = f'05{self.description_size:02}{self.description}'

    self.merchantAccount    = f'26{len(self.merchantAccount_size):02}{self.merchantAccount_size}'
    self.transactionAmount  = f'54{self.transactionAmount_size}'
    self.merchantName       = f'59{self.name_size:02}{self.name}'
    self.merchantCity       = f'60{self.city_size:02}{self.city}'
    self.addDataField       = f'62{len(self.addDataField_size):02}{self.addDataField_size}'

  def payloadGenerate(self):
    self.payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategoryCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'
    self.crc16Gen(self.payload)

  def crc16Gen(self, payload):
    crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    self.crc16Code = hex(crc16(str(payload).encode('utf-8')))
    self.crc16Code_formated = str(self.crc16Code).replace('0x', '').upper().zfill(4)
    self.payload_complete = f'{payload}{self.crc16Code_formated}'
    self.qrCodeGen(self.payload_complete, self.qrCodeDirectory)

  def qrCodeGen(self, payload, diretory):
    dir = os.path.expanduser(diretory)
    self.qrcode = qrcode.make(payload)
    self.qrcode.save(os.path.join(dir, 'pixqrcode.png'))
    return print(payload)



if __name__ == '__main__':
  nome      = input("Digite o nome completo do recebedor: ")
  chavePix  = input("Digite a chave pix: ")
  cidade    = input("Digite a cidade do recebedor: ")
  descricao = input("Digite uma descrição: ")
  valor     = input("Digite o valor: ")

  Payload(nome, chavePix, valor, cidade, descricao).payloadGenerate()
