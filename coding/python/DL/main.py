sentence = input()
words = input()
# get the new sentence
#
words = words.lower()
word_ls = words.split(" ")
sentence_ls = sentence.split(" ")
word_dict = dict()
for i, word in enumerate(word_ls):
    word_dict[word] = str(i)

ret_ls = list()
for sen in sentence_ls:
    if sen.lower() in word_dict.keys():
        sentence = sentence.replace(sen, word_dict[sen.lower()])
#
quote_num = 0
new_sentence = ""
for i in range(len(sentence)):
    if sentence[i] == '"':
        quote_num += 1
    if quote_num%2 and sentence[i] in word_dict.values():
        new_sentence += word_ls[int(sentence[i])]
    else:
        new_sentence += sentence[i]

print(new_sentence)