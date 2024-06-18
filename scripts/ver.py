thai_vowels = ['ิ', 'ึ', 'ี', 'ุ', 'ู', 'ำ', 'ื', '่', '้', '๊', '๋', 'ั']

def thai_subword_tokenize(text:str):
  subwords = []
  pointer = 0
  # current_subword = ""
  for i in text:
    # current_subword += i
    if i in thai_vowels:
      if pointer > 0 :
        subwords[pointer-1] = subwords[pointer-1] + i
      else:
        subwords.append(i)
        pointer += 1
    else:
      subwords.append(i)
      pointer += 1
    # if current_subword not in subwords:
      # subwords.append(current_subword)
  return subwords

# combination tokenize
def thai_combination_tokenize(text:list):
  result = []
  for i in range(1, len(text)+1):
      result.append(''.join(text[:i]))
  for i in range(len(text)-1, 0, -1):
      result.append(''.join(text[i:]))
  return result

# ngram tokenize
def thai_ngram(text:str, lenght:int, move:int=1):
    result = []
    count = 0
    while count < len(text):
        if count + lenght <= len(text):
            result.append(text[count:count+lenght])
        count += move
    print(count, len(text))
    if count >= len(text) and move > 1:
        result.append(text[-lenght:])
    return result

# split every n characters
def search_tokenize(text:str, n:int):
    result = []
    for i in range(0, len(text), n):
        result.append(text[i:i+n])
    return result


if __name__ == "__main__":
  # # Example usage
  # text = "คลีนีกป้าแจ๋ว"
  # # tokens = thai_subword_tokenize(text)
  # # print(tokens) 
  
  # # Example usage
  text = ['โรง', 'เรียน', 'ครับ']
  tokens = thai_combination_tokenize(text)
  print(tokens)
