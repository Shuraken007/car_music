import config
import os
from pprint import pprint
import re
from unidecode import unidecode
from .util import remove_same_words_from_sentence
from .file import File, Dir, apply_updatables, FileConvertor

class Scan:
   def __init__(self):
      self.torrents = []

   def get_torrents(self, main_dir):
      torrents = []
      for sub_dir in os.listdir(main_dir): 
         full_path = os.path.join(main_dir, sub_dir)
         if not os.path.isdir(full_path):
            continue
         torrents.append(Torrent(sub_dir, full_path))
      return torrents

   def run(self):
      torrents = self.get_torrents(config.DOWNLOAD_PATH)
      for torrent in torrents:
         torrent.collect_files()
         torrent.add_convertors()
         torrent.convert()

class Torrent:
   def __init__(self, name, path):
      self.name = name
      self.path = path
      self.files = []
      self.convertors = []

   def get_files_by_ext(self, files, ext_tuple):
      return [file for file in files if file.endswith(ext_tuple)]

   def collect_files(self, path = None, dir_stack = []):
      if path is None:
         path = self.path

      cur_dir, s_dirs, file_names = next(os.walk(path))

      music_files = self.get_files_by_ext(file_names, config.MUSIC_EXT)
      files = [File(f, dir_stack) for f in music_files]  
      files.sort(key=lambda f: f.sort_key)
      apply_updatables(files, remove_same_words_from_sentence)
      apply_updatables(files, lambda arr: [unidecode(e) for e in arr])

      for file in files:
         self.files.append(file)
      
      dirs = [Dir(d) for d in s_dirs ]
      dirs.sort(key=lambda d: d.sort_key)
      apply_updatables(dirs, remove_same_words_from_sentence)
      apply_updatables(dirs, lambda arr: [unidecode(e) for e in arr])
      for d in dirs:
         cur_path = os.path.join(cur_dir, d.name)
         self.collect_files(cur_path, [*dir_stack, d])

   def add_convertors(self):
      files_amount = len(self.files)
      max_num_width = len(str(files_amount))
      i = 1
      for file in self.files:
         padded_number = str(i).rjust(max_num_width, '0') + '.'
         self.convertors.append(FileConvertor(file, padded_number))
         i += 1

   def convert(self):
      for conv in self.convertors:
         conv.convert(
            os.path.join(config.DOWNLOAD_PATH, self.name),
            os.path.join(config.CONVERT_PATH, self.name)
         )
         