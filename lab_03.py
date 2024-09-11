#!/usr/bin/env python

"""Шифр гаммирования при помощи линейного рекуррентного регистра сдвига
"""

import random
import sys
from typing import List, Optional, Tuple, Union

RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ENCRYPT_ACTION = "--enc"
DECRYPT_ACTION = "--dec"


# Считывает текст из файла
def read_from_file_enc(filename: str) -> Optional[str]:
  try:
    with open(filename, "r") as f:
      buf = f.read().split('\n')[0]
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


# Создаёт ключ
def generate_key(length: int, a: int, c: int, m: int, seed: int) -> List[int]:
  key = [seed]
  for _ in range(1, length):
    next_value = (a * key[-1] + c) % m
    key.append(next_value)
  return key


# Конвертация индексов в символы и наоборот
def char_to_index(char: str) -> int:
  return RU_ALPHABET.index(char.lower())
def index_to_char(index: int, is_upper: bool) -> str:
  char = RU_ALPHABET[index]
  return char.upper() if is_upper else char


# Создаёт ключ и шифрует текст с его помощью
def encrypt(text: str, key: List[int]) -> Tuple[str, str]:
  encrypted = []
  for char, k in zip(text, key):
    if char.lower() in RU_ALPHABET:
      index = (char_to_index(char) + k) % 33
      encrypted_char = index_to_char(index, char.isupper())
      encrypted.append(encrypted_char)
    else:
      encrypted.append(char)
  return ''.join(encrypted), encode_key(key)


# Расшифровывает текст с помощью ключа
def decrypt(encrypted: str, key: str) -> str:
  key = decode_key(key)
  decrypted = []
  for char, k in zip(encrypted, key):
    if char.lower() in RU_ALPHABET:
      index = (char_to_index(char) - k) % 33
      decrypted_char = index_to_char(index, char.isupper())
      decrypted.append(decrypted_char)
    else:
      decrypted.append(char)
  return ''.join(decrypted)


# Кодирует ключ
def encode_key(key: list[int]) -> str:
  return '-'.join(map(str, key))
# Декодирует ключ
def decode_key(key: str) -> list[int]:
  return list(map(int, key.split('-')))


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
    # Параметры генерации ключа
    a = random.randint(1, 1000)
    c = random.randint(0, 1000)
    m = 33
    seed = random.randint(0, 32)
    
    s = read(filename, action)
    key = generate_key(len(s), a, c, m, seed)
    encrypted, key_str = encrypt(s, key)
    print(f'Результат: "{encrypted}"')
    print(f'Ключ: "{key_str}"')
  elif action == DECRYPT_ACTION:
    s, k = read(filename, action)
    decrypted = decrypt(s, k)
    print(f'Результат: "{decrypted}"')
