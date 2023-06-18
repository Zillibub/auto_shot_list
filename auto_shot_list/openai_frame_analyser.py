import numpy as np
import torch
import openai
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
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

        self._details_prompt = \
            "Give me the list of questions to fully understand the shot based on this description {} " \
            "If there are some characters always ask about their appearance " \
            "ask no more than 10 questions only about the image elements " \
            "return only questions always separated by symbol * " \
            " without any answer options and numerations on the beginning"

        self._summary_prompt = \
            "you are an experienced filmmaker " \
            "do not add any additional information, reply only on given description " \
            "based on this information summarize a full comprehensive description of a shot {}"

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
            prompt = f"Question: {question} Answer:"
        inputs = self.processor(
            images=frame, text=prompt, return_tensors="pt"
        ).to(self.device, torch.float16)

        generated_ids = self.model.generate(**inputs)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        return generated_text

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_fixed(0.2),
        # retry=retry_if_exception_type(openai.error.RateLimitError)
    )
    def _complete_openai(self, prompt: str):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content

    def evaluate(self, frame: np.array):
        first_description = self._analyse_image(frame)

        completion = self._complete_openai(self._details_prompt.format(first_description))

        questions = [x for x in completion.split("*") if x]

        frame_details = []
        for question in questions:
            frame_details.append(self._analyse_image(frame, question))

        frame_summary = self._complete_openai(self._summary_prompt.format(
            first_description + " " + " ".join(frame_details)
        ))

        return frame_summary
