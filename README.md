# Auto Shot List Library

The Auto Shot List library is designed to create shot lists using LLM models. It automates the process of creating shot lists by using machine learning algorithms to generate precise shots. This library is especially useful for filmmakers and video editors who need to create shot lists quickly and accurately.

## Usage

The simpliest way to create a shot list is to use a `scripts/analyse_files.py` script.

Alternatively, you can call everythg from you code. 

```python
from pathlib import Path
import json_tricks
from auto_shot_list.openai_frame_analyser import OpenAIFrameAnalyser
from auto_shot_list.scene_manager import VideoManager

video_path = Path("path/to/your/video.mkv")
output_dir = Path("path/to/folder/with/results")
analyser = OpenAIFrameAnalyser()

video_manager = VideoManager(str(video_path), frame_analyser=analyser)
video_manager.detect_scenes()
video_manager.analyse_scenes()
video_manager.frame_analyser = None
with open(output_dir / (video_path.stem + ".json"), "w") as f: 
    json_tricks.dump(video_manager, f)
```

This will generate a shot list using LLM models. The output will be a list of shots in chronological order. Each shot is represented as a dictionary with the start and end times of the shot.


## Under the hood. 

The library uses a GPT LLM model as an arbiter and a summarizer and a `blip2-opt` model to extract 
information from the image

Workflow: 
1. Extract all shots from the video
2. Get the initial shot information with blip2 model
3. Use GPT to generate a list of additional questions about the shot
4. Retrieve answers for this questions using blip2 on the same shot
5. Summarize shot into with GPT


**Contributing**

Contributions are welcome! If you find a bug or would like to request a new feature, please create an issue on the GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request.

**License**

This library is licensed under the MIT License. See the LICENSE file for more information.