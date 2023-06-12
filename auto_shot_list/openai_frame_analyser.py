import numpy as np
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

class OpenAIFrameAnalyser:

    def __init__(
            self,
            device: str = "cuda",

    ):
        self.device = device
        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16
        )
        self.model.to(device)

    def _analyse_image(
            self,
            frame: np.array,
            question: str = None
    ):
        """
        Evaluates one question on given frame
        :param frame:
        :param question:
        :return:
        """
        if not question:
            prompt = None
        else:
            prompt = f"Question: {question} Answer: "
        inputs = self.processor(
            images=frame, text=prompt, return_tensors="pt"
        ).to(self.device, torch.float16)

        generated_ids = self.model.generate(**inputs)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        return generated_text


    def evaluate(self, frame: np.array):

