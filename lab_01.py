#!/usr/bin/env python

"""Шифр простой замены
"""

import random
import sys
from typing import Optional, Tuple, Union

RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENCRYPT_ACTION = "--enc"
DECRYPT_ACTION = "--dec"


# Считывает текст из файла
def read_from_file_enc(filename: str) -> Optional[str]:
  try:
    with open(filename, "r") as f:
      buf = f.read().split('\n')[0].lower()
      return buf
  except Exception as e:
    print(f'Ошибка: {str(e)}')
    return None

def read_from_file_dec(filename: str) -> Optional[Tuple[str, str]]:
  try:
    with open(filename, "r") as f:
      buf = f.read().split('\n')
      s, k = buf[0], buf[1]
      return (s, k)
  except Exception as e:
    print(f'Ошибка: {str(e)}')
    return None


# Считывает текст из терминала
def read_from_console_enc() -> str:
  print("Введите текст (на русском языке), который требуется зашифровать/расшифровать:")
  return input().lower()

def read_from_console_dec() -> Tuple[str, str]:
  print("Введите текст (на русском языке), который требуется зашифровать/расшифровать:")
  s = input().lower()
  k = input("Введите ключ шифрования: ")
  return (s, k)


# Шифрует текст предоставленным ключом
def encrypt(text: str) -> Union[str, str]:
  key = []
  ru_sample = list(RU_ALPHABET)
  while len(ru_sample) != 0:
    letter = random.choice(ru_sample)
    key.append(letter)
    ru_sample.remove(letter)
  key = ''.join(key)
  
  encrypted = []
  for symbol in text:
    pos = RU_ALPHABET.find(symbol)
    if pos == -1:
      encrypted.append(symbol)
      continue
    new_sym = key[pos]
    encrypted.append(new_sym)
  return ''.join(encrypted), key


# Расшифровывает текст предоставленным ключом
def decrypt(encrypted: str, key: str) -> str:
  decrypted = []
  for symbol in encrypted:
    pos = key.find(symbol)
    if pos == -1:
      decrypted.append(symbol)
      continue
    old_sym = RU_ALPHABET[pos]
    decrypted.append(old_sym)
  return ''.join(decrypted)


# Уточняет, что нужно сделать
def decide_action() -> str:
  def print_prompt() -> None:
    print('Выберите действие: ')
    print('1. Зашифровать текст с помощью ключа')
    print('2. Расшифровать текст с помощью ключа')
  
  def read_opt(allowed: list) -> Optional[int]:
    try:
      opt = int(input("Введите номер [1-2]: "))
      if opt not in allowed:
        print(f'Ошибка: опция #{opt} недоступна!')
        return None
      return opt
    except Exception as e:
      print(f'Ошибка: {str(e)}')
      return None
  
  print_prompt()
  opt = read_opt([1, 2])
  while opt is None:
    print_prompt()
    opt = read_opt([1, 2])
  
  match opt:
    case 1:
      return ENCRYPT_ACTION
    case 2:
      return DECRYPT_ACTION
    case _:
      return None


# Читает в программу текст и ключ
def read(filename: Optional[str], action: str) -> Optional[Union[Tuple[str, str], str]]:
  if filename is None:
    if action == ENCRYPT_ACTION:
      return read_from_console_enc()
    else:
      return read_from_console_dec()
  else:
    if action == ENCRYPT_ACTION:
      return read_from_file_enc(filename)
    else:
      return read_from_file_dec(filename)


# Начало программы
if __name__ == '__main__':
  # Если программу запустить с аргументами (именем файла с текстом и ключом), ввод будет считан из файла
  filename = None
  action = None
  for arg in sys.argv[1:]:
    if arg == ENCRYPT_ACTION:
      action = ENCRYPT_ACTION
    elif arg == DECRYPT_ACTION:
      action = DECRYPT_ACTION
    else:
      filename = arg
  
  if action is None:
    action = decide_action()
  
  if action == ENCRYPT_ACTION:
    s = read(filename, action)
    encrypted, key = encrypt(s)
    print(f'Результат: "{encrypted}"')
    print(f'Ключ: "{key}"')
  elif action == DECRYPT_ACTION:
    s, k = read(filename, action)
    decrypted = decrypt(s, k)
    print(f'Результат: "{decrypted}"')
