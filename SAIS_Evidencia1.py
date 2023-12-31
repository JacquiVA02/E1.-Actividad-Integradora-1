import re
import time

from memory_profiler import profile
from pylab import plot, show
import matplotlib.pyplot as plt


def getBuckets(T):
   count = {}
   buckets = {}
   for c in T:
      count[c] = count.get(c, 0) + 1
      start = 0
   for c in sorted(count.keys()):
      buckets[c] = (start, start + count[c])
      start += count[c]
   return buckets


def sais(T):
   t = ["_"] * len(T)
   t[len(T) - 1] = "S"
   for i in range(len(T) - 1, 0, -1):
      if T[i - 1] == T[i]:
         t[i - 1] = t[i]
      else:
         t[i - 1] = "S" if T[i - 1] < T[i] else "L"

   buckets = getBuckets(T)

   count = {}
   SA = [-1] * len(T)
   LMS = {}
   end = None
   for i in range(len(T) - 1, 0, -1):
      if t[i] == "S" and t[i - 1] == "L":
         revoffset = count[T[i]] = count.get(T[i], 0) + 1
         SA[buckets[T[i]][1] - revoffset] = i
         if end is not None:
            LMS[i] = end
         end = i

   LMS[len(T) - 1] = len(T) - 1
   count = {}
   for i in range(len(T)):
      if SA[i] >= 0:
         if t[SA[i] - 1] == "L":
            symbol = T[SA[i] - 1]
            offset = count.get(symbol, 0)
            SA[buckets[symbol][0] + offset] = SA[i] - 1
            count[symbol] = offset + 1

   count = {}
   for i in range(len(T) - 1, 0, -1):
      if SA[i] > 0:
         if t[SA[i] - 1] == "S":
            symbol = T[SA[i] - 1]
            revoffset = count[symbol] = count.get(symbol, 0) + 1
            SA[buckets[symbol][1] - revoffset] = SA[i] - 1

   namesp = [-1] * len(T)
   name = 0
   prev = None
   for i in range(len(SA)):
      if t[SA[i]] == "S" and t[SA[i] - 1] == "L":
         if prev is not None and T[SA[prev]:LMS[SA[prev]]] != T[
             SA[i]:LMS[SA[i]]]:
            name += 1
         prev = i
         namesp[SA[i]] = name

   names = []
   SApIdx = []
   for i in range(len(T)):
      if namesp[i] != -1:
         names.append(namesp[i])
         SApIdx.append(i)

   if name < len(names) - 1:
      names = sais(names)

   names = list(reversed(names))

   SA = [-1] * len(T)
   count = {}
   for i in range(len(names)):
      pos = SApIdx[names[i]]
      revoffset = count[T[pos]] = count.get(T[pos], 0) + 1
      SA[buckets[T[pos]][1] - revoffset] = pos

   count = {}
   for i in range(len(T)):
      if SA[i] >= 0:
         if t[SA[i] - 1] == "L":
            symbol = T[SA[i] - 1]
            offset = count.get(symbol, 0)
            SA[buckets[symbol][0] + offset] = SA[i] - 1
            count[symbol] = offset + 1

   count = {}
   for i in range(len(T) - 1, 0, -1):
      if SA[i] > 0:
         if t[SA[i] - 1] == "S":
            symbol = T[SA[i] - 1]
            revoffset = count[symbol] = count.get(symbol, 0) + 1
            SA[buckets[symbol][1] - revoffset] = SA[i] - 1

   return SA


def search_word_in_suffix_array(word, array, content):
   found = False

   for i, suffix_start in enumerate(array):
      suffix = content[suffix_start:]
      if suffix.startswith(word):
         found = True
         print(
             f"Palabra encontrada en el índice {suffix_start} (Ocurrencia {i + 1})"
         )

   if not found:
      print(f"Palabra '{word}' no encontrada en el archivo.")


@profile
def create_suffix_array_from_file(file_path):
   start_time = time.time()
   with open(file_path, 'r', encoding='utf-8') as file:
      content = file.read()

   content = re.sub(r'[^a-zA-Z0-9\s]', '', content).lower()
   content = content.replace(" ", "").replace("\n", "")
   content += "$"
   T = [ord(c) for c in content]
   SA = sais(T)

   end_time = time.time()
   execution_time = end_time - start_time
   print(f"Tiempo de ejecución: {execution_time} segundos")

   return SA, content


# Palabra a buscar
word_to_search = "under"

array, content = create_suffix_array_from_file(
    'Libros/Pinocchio under the sea.txt')
print("array size: ", len(array))
search_word_in_suffix_array(word_to_search, array, content)

#En caso de que se desee imprimir el arreglo de sufijos:
#print(array)
