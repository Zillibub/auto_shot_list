import argparse
import json_tricks
from pathlib import Path
import pandas as pd
from uuid import uuid1
from langchain.embeddings import OpenAIEmbeddings, LlamaCppEmbeddings
from langchain.vectorstores import Chroma


def process_shots(shot_list_dir: Path, result_dir: Path):
    ids = []
    timings_db = []
    texts = []

    for shot_list_path in shot_list_dir.iterdir():
        with open(shot_list_path, "r") as f:
            data = json_tricks.load(f)
        for shot in data.scenes_description:
            shot_id = str(uuid1())
            ids.append(shot_id)
            duration = shot["timing"][1].get_seconds() - shot["timing"][0].get_seconds()
            timings_db.append({
                "id": shot_id,
                "path": str(Path(data.video_path).resolve()),
                "start": shot["timing"][0].frame_num,
                "stop": shot["timing"][1].frame_num,
                "duration": duration,
            })
            texts.append(shot["description"])

    timings_df = pd.DataFrame(timings_db)
    timings_df.to_parquet(result_dir / "timing.parquet")
    lang_db = result_dir / "lang_db"
    lang_db.mkdir(exist_ok=True)
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_texts(texts, embeddings, ids=ids, persist_directory=str(lang_db))
    vector_store.persist()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process shots')
    parser.add_argument('output_dir', type=str, help='Path to output directory')
    parser.add_argument('result_dir', type=str, help='Path to result directory')
    args = parser.parse_args()

    output_directory = Path(args.output_dir)
    result_directory = Path(args.result_dir)

    process_shots(output_directory, result_directory)