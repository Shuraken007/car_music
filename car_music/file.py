import os
import re
from functools import total_ordering
from shutil import copyfile
import config

class Updatable:
   def __init__(self, val):
      self._u_val = val

   def update(self, val):
      self._u_val = val

   def get_val(self):
      return self._u_val

def apply_updatables(updatables, call):
   old_val_arr = [item.get_val() for item in updatables]
   new_val_arr = call(old_val_arr)
   for i in range(len(updatables)):
      updatables[i].update(new_val_arr[i])

MATCH_NUM = re.compile(r"^[^\w]*(\d+)[^\w]*(.+)")

@total_ordering
class NumStr:
   def split_str(self, num_str):
      if m := MATCH_NUM.match(num_str):
         self.num = int(m.group(1))
         self.str = m.group(2)
      else:
         self.str = num_str
         self.num = None

   def __init__(self, num_str):
      self.str = None
      self.num = None
      self.split_str(num_str)

   def __eq__(self, other):
      if not isinstance(other, NumStr):
         return NotImplemented
      return self.str == other.str

   def __lt__(self, other):
      if not isinstance(other, NumStr):
         return NotImplemented
      if self.num is not None and other.num is not None:
         return self.num < other.num
      else:
         return self.str < other.str

class Dir(Updatable):
   def __init__(self, dir_name):
      self.name = dir_name
      self.sort_key = NumStr(dir_name)
      super().__init__(self.sort_key.str)

class File(Updatable):
   def __init__(self, file_name, dirs):
      self.dirs = dirs
      self.name = file_name
      self.base_name, self.ext = os.path.splitext(self.name)
      self.sort_key = NumStr(self.base_name)
      super().__init__(self.sort_key.str)

   def get_path(self):
      return os.path.join(
         *[d.name for d in self.dirs], 
         self.name
      )

MAX_DIRS_DEPTH = 1

class FileConvertor:
   def __init__(self, file, f_prefix):
      self.prefix = f_prefix
      self.file = file

      self.base_name = None
      self.dirs = None
      self.prepare_file()

   def prepare_file(self):
      if self.file.ext.endswith(config.SUPPORTED_MUSIC_EXT):
         self.ext = self.file.ext
      else:
         self.ext = ".mp3"

      self.dirs = self.file.dirs[:MAX_DIRS_DEPTH]
      remove_dirs_str = '_-_'.join([d.get_val() for d in self.file.dirs[MAX_DIRS_DEPTH:]])

      base_name = f'{self.prefix} {self.file.get_val()}'
      if remove_dirs_str:
         base_name = f'{self.prefix} {self.file.get_val()} ({remove_dirs_str})'
      
      self.base_name = base_name

   def get_path(self):
      return os.path.join(
         *[d.name for d in self.dirs], 
         self.base_name + self.ext
      )

   def convert(self, path_from, path_to):
      old_path = os.path.join(path_from, self.file.get_path())
      new_path = os.path.join(path_to, self.get_path())
      if os.path.exists(new_path):
         return
      os.makedirs(os.path.dirname(new_path), exist_ok=True)
      if self.file.ext == self.ext:
         copyfile(old_path, new_path)
      else:
         flac_audio = config.AUDIO_SEGMENT.from_file(old_path, self.file.ext[1:])
         flac_audio.export(new_path, format="mp3")