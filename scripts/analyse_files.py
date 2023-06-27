import argparse
import json_tricks
from pathlib import Path
from auto_shot_list.openai_frame_analyser import OpenAIFrameAnalyser
from auto_shot_list.scene_manager import VideoManager


def analyse_files(videos_dir: Path, output_dir: Path):
    """
    Analyses all files in given folder
    :param videos_dir: path to a directory with video files
    :param output_dir: path to a directory to store created shot lists
    :return:
    """

    analyser = OpenAIFrameAnalyser()

    if not videos_dir.exists():
        raise ValueError(f"Videos directory does not exists: {videos_dir}")

    if not output_dir.exists():
        raise ValueError(f"Output directory does not exists: {videos_dir}")



    for video_path in videos_dir.iterdir():
        video_manager = VideoManager(str(video_path), frame_analyser=analyser)
        video_manager.detect_scenes()
        video_manager.analyse_scenes()
        video_manager.frame_analyser = None
        with open(output_dir / (video_path.stem + ".json"), "w") as f:
            json_tricks.dump(video_manager, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('videos_dir', type=str, help='path to the directory containing the videos')
    parser.add_argument('output_dir', type=str, help='path where the output json files will be saved')
    args = parser.parse_args()

    videos_directory = Path(args.videos_dir)
    output_directory = Path(args.output_dir)

    analyse_files(videos_directory, output_directory)
