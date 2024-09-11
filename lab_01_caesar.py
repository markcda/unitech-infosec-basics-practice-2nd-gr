#!/usr/bin/env python

"""Шифр Цезаря
"""

import sys
from typing import Optional, Tuple

RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENCRYPT_ACTION = "--enc"
DECRYPT_ACTION = "--dec"


# Считывает информацию из файла
def read_from_file(filename: str) -> Optional[Tuple[str, int]]:
  try:
    with open(filename, "r") as f:
      buf = f.read().split('\n')
      s, k = buf[0].lower(), int(buf[1])
      return (s, k)
  except Exception as e:
    print(f'Ошибка: {str(e)}')
    return None


# Считывает информацию из терминала
def read_from_console() -> Tuple[str, int]:
  print("Введите текст (на русском языке), который требуется зашифровать/расшифровать:")
  s = input().lower()
  k = int(input("Введите ключ шифрования (число): "))
  return (s, k)


# Шифрует текст предоставленным ключом
def encrypt(text: str, key: int) -> str:
  encrypted = []
  for symbol in text:
    pos = RU_ALPHABET.find(symbol)
    if pos == -1:
      encrypted.append(symbol)
      continue
    new_pos = (pos + key) % len(RU_ALPHABET)
    new_sym = RU_ALPHABET[new_pos]
    encrypted.append(new_sym)
  return ''.join(encrypted)


# Расшифровывает текст предоставленным ключом
def decrypt(encrypted: str, key: int) -> str:
  decrypted = []
  for symbol in encrypted:
    pos = RU_ALPHABET.find(symbol)
    if pos == -1:
      decrypted.append(symbol)
      continue
    old_pos = (pos + len(RU_ALPHABET) - key) % len(RU_ALPHABET)
    old_sym = RU_ALPHABET[old_pos]
    decrypted.append(old_sym)
  return ''.join(decrypted)


# Уточняет, что нужно сделать
def decide_action() -> str:
  def print_prompt() -> None:
    print('Выберите действие: ')
    print('1. Зашифровать текст с помощью ключа')
    print('2. Расшифровать текст с помощью ключа')
  
  def read_opt(allowed: list[int]) -> Optional[int]:
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
def read(filename: Optional[str]) -> Optional[Tuple[str, int]]:
  if filename is None:
    return read_from_console()
  else:
    return read_from_file(filename)


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
    s, k = read(filename)
    encrypted = encrypt(s, k)
    print(f'Результат: "{encrypted}"')
  elif action == DECRYPT_ACTION:
    s, k = read(filename)
    decrypted = decrypt(s, k)
    print(f'Результат: "{decrypted}"')
