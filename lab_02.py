#!/usr/bin/env python

"""Шифр перестановки Кардано

NOTE: поворот осуществляется против часовой стрелки
"""

import random
import sys
from typing import Optional, Tuple, Union

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


# Создаёт ключ и шифрует текст с его помощью
def encrypt(text: str) -> Tuple[str, str]:
  square_len = find_nearest_bigger_square(len(text))
  padded_text = text.ljust(square_len ** 2)
  key = make_cardano_lattice_key(square_len)
  encrypted = []
  for si in key:
    encrypted.append(padded_text[si])
  for si in rotate_key_90(key, square_len):
    encrypted.append(padded_text[si])
  for si in rotate_key_180(key, square_len):
    encrypted.append(padded_text[si])
  for si in rotate_key_270(key, square_len):
    encrypted.append(padded_text[si])
  return ''.join(encrypted), encode_key(key)


# Расшифровывает текст с помощью ключа
def decrypt(encrypted: str, key: str) -> str:
  size = int(len(encrypted) ** 0.5)
  key = decode_key(key)
  decrypted = [' '] * (size ** 2)
  
  quarter = len(encrypted) // 4
  rotations = [
    key,
    rotate_key_90(key, size),
    rotate_key_180(key, size),
    rotate_key_270(key, size)
  ]
    
  for i, rotation in enumerate(rotations):
    for j, pos in enumerate(rotation):
      decrypted[pos] = encrypted[i * quarter + j]
  
  return ''.join(decrypted)


# Ищет ближайший больший квадрат
def find_nearest_bigger_square(text_size: int) -> int:
  i = 1
  while i ** 2 < text_size:
    i += 1
  return i


# Кодирует ключ
def encode_key(key: list[int]) -> str:
  return '-'.join(map(str, key))
# Декодирует ключ
def decode_key(key: str) -> list[int]:
  return list(map(int, key.split('-')))


# Поворот на 90 градусов
def rotate_90(row: int, col: int, n: int) -> Tuple[int, int]:
  return col, n - 1 - row
# Поворот на 180 градусов
def rotate_180(row: int, col: int, n: int) -> Tuple[int, int]:
    return n - 1 - row, n - 1 - col
# Поворот на 270 градусов
def rotate_270(row: int, col: int, n: int) -> Tuple[int, int]:
    return n - 1 - col, row
# Вычисление позиции ячейки матрицы в решётке
def calc_pos(row: int, col: int, n: int) -> int:
  return row * n + col
# Вычисление позиций ячейки из решётки
def calc_pos2(pos: int, n: int) -> Tuple[int, int]:
  return pos // n, pos % n


# Вращение ключа
def rotate_key_90(key: list[int], side_len: int) -> list[int]:
  return [calc_pos(*rotate_90(*calc_pos2(i, side_len), side_len), side_len) for i in key]
def rotate_key_180(key: list[int], side_len: int) -> list[int]:
  return [calc_pos(*rotate_180(*calc_pos2(i, side_len), side_len), side_len) for i in key]
def rotate_key_270(key: list[int], side_len: int) -> list[int]:
  return [calc_pos(*rotate_270(*calc_pos2(i, side_len), side_len), side_len) for i in key]


# Ищет перемещения окна при поворотах решётки
def find_opposites(side_len: int, window: int) -> list[int]:
  opposites = [window]
  row, col = calc_pos2(window, side_len)
  # Ищем три дополнительных поворота
  w1 = calc_pos(*rotate_90(row, col, side_len), side_len)
  w2 = calc_pos(*rotate_180(row, col, side_len), side_len)
  w3 = calc_pos(*rotate_270(row, col, side_len), side_len)
  # Если повороты одинаковые, нет смысла их добавлять.
  # Это случается, когда размер квадрата нечётный, и выбранное окно - центр квадрата.
  if window != w1:
    opposites += [w1, w2, w3]
  return opposites


# Создаёт решётку Кардано
def make_cardano_lattice_key(side_len: int) -> list[int]:
  lattice = [i for i in range(side_len ** 2)]
  key = []
  while len(lattice) != 0:
    window = random.choice(lattice)
    key.append(window)
    windows = find_opposites(side_len, window)
    for w in windows:
      lattice.remove(w)
  return key


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
