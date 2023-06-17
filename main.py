import cv2
from scenedetect import open_video, SceneManager, ContentDetector
from auto_shot_list.openai_frame_analyser import OpenAIFrameAnalyser


def main(
        video_path: str,

):
    video = open_video(video_path)

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 12818)

    success, frame = cap.read()

    out = OpenAIFrameAnalyser().evaluate(frame)


if __name__ == "__main__":
    main(video_path="../data/chainsaw_man/[DeadLine] Chainsaw Man - 01 [Soer] [1080p].mkv")
