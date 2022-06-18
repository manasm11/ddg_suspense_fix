import json
import os
import glob
import shutil

def combine_all_json_files(jsons_directory, output_json):
  final_data = list()
  ids = set()
  for filepath in glob.glob(os.path.join(jsons_directory, '*.json')):      
      with open(filepath, encoding='utf-8', mode='r') as file:
          data: list = json.load(file)
          filtered_data = filter(lambda d: "party_name" in d and d['party_name'], data)
          for d in filtered_data:
            if d["id"] not in ids:
              final_data.append(d)
            ids.add(d["id"])
      directory, filename = os.path.split(filepath)
      backup_dir = os.path.join(directory, "backup")
      if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
      shutil.move(filepath, os.path.join(backup_dir, filename))
  with open(output_json, "w") as f:
    json.dump(final_data, f)
  