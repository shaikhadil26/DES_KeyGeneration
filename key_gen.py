# Key generation for 16 rounds of DES

import random, string

def leftRotate(n, d):
  x = n[:d]
  n = n[d:]
  n += x
  return n

def gen_56bit(init_key):
  # Dict for hex to binary conversion
  h_b = {'0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100",'5': "0101",'6': "0110",'7': "0111",
      '8': "1000",'9': "1001",'A': "1010",'B': "1011",'C': "1100",'D': "1101",'E': "1110",'F': "1111"}

  # Converting init key to bits
  key_bits = ''.join([h_b[x] for x in init_key])
 
  # Permuting 64 bits to generate 56 bits.
  perm_ch1 = [57, 49, 41, 33, 25, 17, 9,
              1, 58, 50, 42, 34, 26, 18,
              10, 2, 59, 51, 43, 35, 27,
              19, 11, 3, 60, 52, 44, 36,
              63, 55, 47, 39, 31, 23, 15,
              7, 62, 54, 46, 38, 30, 22,
              14, 6, 61, 53, 45, 37, 29,
              21, 13, 5, 28, 20, 12, 4]

  bit_56 = ''
  for i in perm_ch1:
    bit_56 += key_bits[i-1]

  return bit_56

def generate_key(bit, shifts):
  # Dict for converting binary to hex
  b_h = {'0000': '0','0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5', '0110': '6', '0111': '7',
         '1000': '8','1001': '9', '1010': 'A', '1011': 'B', '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'}
  
  # Dividing 56 bits into two halves
  left = bit[:28]
  right = bit[28:]
  
  # Applying circular left shift on each half respectively
  sh_l = leftRotate(left, shifts)
  sh_r = leftRotate(right, shifts)

  sh = sh_l + sh_r
  
  # generating 48-bit subkey for the round
  perm_ch2 = [14, 17, 11, 24, 1, 5, 3, 28,
              15, 6, 21, 10, 23, 19, 12, 4,
              26, 8, 16, 7, 27, 20, 13, 2,
              41, 52, 31, 37, 47, 55, 30, 40,
              51, 45, 33, 48, 44, 49, 39, 56,
              34, 53, 46, 42, 50, 36, 29, 32]

  bkey = ''
  for i in perm_ch2:
    bkey += sh[i-1]
  
  # Converting binary 48 bit key to hex
  key =''
  for i in range(0, len(bkey), 4):
    x = bkey[i:i+4]
    key += b_h[x]

  return key, sh


round = {1:[1, 2, 9, 16], 
         2: [3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]}

# Creating random 64 bit hex key
random_key = ''.join(random.choice(string.ascii_uppercase[:6] + string.digits) for _ in range(16))

bin_key = gen_56bit(random_key)

for i in range(16):
  curr = [x for x in round if i+1 in round[x]][0]

  fin_key, bin_key = generate_key(bin_key, curr)

  print(f'For round {i+1} sub key: \t{fin_key}')