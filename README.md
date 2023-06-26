# Auto Shot List Library

The Auto Shot List library is designed to create shot lists using LLM models. It automates the process of creating shot lists by using machine learning algorithms to generate precise shots. This library is especially useful for filmmakers and video editors who need to create shot lists quickly and accurately.

## Usage

Here's an example of how to use the Auto Shot List library:

```
from auto_shot_list import create_shot_list
from video_file import VideoFile

video_file = VideoFile('example.mp4')
shot_list = create_shot_list(video_file)
print(shot_list)
```

This will generate a shot list using LLM models. The output will be a list of shots in chronological order. Each shot is represented as a dictionary with the start and end times of the shot.

**Contributing**

Contributions are welcome! If you find a bug or would like to request a new feature, please create an issue on the GitHub repository. If you would like to contribute code, please fork the repository and submit a pull request.

**License**

This library is licensed under the MIT License. See the LICENSE file for more information.