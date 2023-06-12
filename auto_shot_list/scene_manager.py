from scenedetect import open_video, SceneManager, ContentDetector


class VideoManager:

    def __init__(
            self,
            video_path: str,
    ):
        self.video_path = video_path

        self.scenes = None

    def detect_scenes(self):
        video = open_video(self.video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        scene_manager.detect_scenes(video)

        self.scenes = scene_manager.get_scene_list()



