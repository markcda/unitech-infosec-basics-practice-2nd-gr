#!/usr/bin/env python

"""Частотный анализ
"""

from collections import Counter
import lab_01

s = lab_01.read_from_file_enc('lab-01-text.txt')
encrypted, key = lab_01.encrypt(s)

print(f'Результат: "{encrypted}"')
print(f'Ключ: "{key}"')

ru_letters = ""
for symbol in encrypted:
  if symbol in lab_01.RU_ALPHABET:
    ru_letters += symbol

cntr = Counter(ru_letters)
size = len(ru_letters)

print('Частотный анализ:')
for ch, freq in cntr.most_common():
  p = freq / size
  print(f'"{ch}":\t{p}')
