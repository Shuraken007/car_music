def reduce_list_of_lists(l_o_l):
   # print([len(l) for l in l_o_l])
   max_length = min([len(l) for l in l_o_l])
   for i in range(max_length - 1, -1, -1):
      all_same = True
      word = l_o_l[0][i]
      for l in l_o_l:
         if l[i] != word:
            all_same = False
      if not all_same:
         continue

      for l in l_o_l:
         del l[i]
   
def remove_same_words_from_sentence(sentences):
   if len(sentences) <= 1:
      return sentences

   l_o_l = [sentence.split() for sentence in sentences]
   reduce_list_of_lists(l_o_l)
   return [' '.join(l) for l in l_o_l]


# def reduce_dirs(dirs):
#    dirs = 