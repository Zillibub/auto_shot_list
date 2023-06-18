import cv2
import logging

from scenedetect import open_video, SceneManager, ContentDetector
from auto_shot_list.openai_frame_analyser import OpenAIFrameAnalyser


class VideoManager:

    def __init__(
            self,
            video_path: str,
            frame_analyser: OpenAIFrameAnalyser
    ):
        self.video_path = video_path

        self.scenes = None
        self.scenes_description = []
        self.frame_analyser = frame_analyser

    def detect_scenes(self):
        video = open_video(self.video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        scene_manager.detect_scenes(video)

        self.scenes = scene_manager.get_scene_list()

    def analyse_scenes(self, num_scenes: int = None, continue_analysis: bool = False):
        if not self.scenes:
            raise ValueError("Scenes are not detected")

        start = 0
        if continue_analysis:
            start = len(self.scenes_description)

        num_scenes = num_scenes or len(self.scenes)

        cap = cv2.VideoCapture(self.video_path)

        for scene in self.scenes[start:num_scenes]:
            self.scenes_description.append({
                "timing": scene,
                "description": self.describe_scene(scene, cap)
            })

    def describe_scene(self, scene, cap):

        middle_frame_num = (scene[0].frame_num + scene[1].frame_num) // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_num)

        success, frame = cap.read()

        if not success:
            logging.warning(f"Couldn't read the frame {middle_frame_num}")
            return

        description = self.frame_analyser.evaluate(frame)

        return description





