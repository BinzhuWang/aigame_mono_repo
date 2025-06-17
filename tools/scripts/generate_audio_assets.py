# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generate_audio_assets.py                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/14 23:22:53 by dfine             #+#    #+#              #
#    Updated: 2025/05/14 23:22:54 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
from pathlib import Path

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(current_script_dir, os.pardir)
tools_dir = os.path.join(project_root_dir, "src")

sys.path.insert(0, project_root_dir)
sys.path.insert(0, tools_dir)
from tools.generate_audio_lib import generate_lib

if __name__ == "__main__":
    audio_lib = generate_lib(Path("./bgm"))
    with open("audio_lib.json", "w") as f:
        _ = f.write(audio_lib.model_dump_json())
