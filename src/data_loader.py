"""
data_loader.py
--------------
Loads MULTITuDE v3 data and prepares it for SFA-CA training/evaluation.

Expected input format: a CSV (or set of per-language CSVs) with at least
these columns:
    text        -> the raw text sample
    label       -> generator class, one of:
                   "human", "mistral", "opt", "eagle", "vicuna",
                   "llama2", "aya", "gpt35"
    lang        -> ISO 639-1 language code (e.g. "en", "ru", "zh")

Adjust COLUMN_MAP / load paths to match however you actually download
MULTITuDE v3 from Zenodo -- the base paper's repo
(github.com/MLNTeam-Unical/Multilingual-MGT-AA) shows their exact schema.
"""

import pandas as pd
from torch.utils.data import Dataset
from clusters import get_cluster, all_clusters, BASE_PAPER_18_LANGUAGES


LABEL2ID = {
    "human": 0,
    "Mistral-7B-Instruct-v0.2": 1,
    "opt-iml-max-30b": 2,
    "v5-Eagle-7B-HF": 3,
    "vicuna-13b": 4,
    "Llama-2-70b-chat-hf": 5,
    "aya-101": 6,
    "gpt-3.5-turbo-0125": 7,
    "Gemini-1.5-Flash": 8,
    "Claude-3.5-Sonnet": 9,
    "gemini": 8,
    "claude": 9,
    "gemini-flash": 8,
    "gemini-3.6-flash": 8,
    "claude-3.5-sonnet": 9,
}
ID2LABEL = {
    0: "human",
    1: "Mistral-7B-Instruct-v0.2",
    2: "opt-iml-max-30b",
    3: "v5-Eagle-7B-HF",
    4: "vicuna-13b",
    5: "Llama-2-70b-chat-hf",
    6: "aya-101",
    7: "gpt-3.5-turbo-0125",
    8: "Gemini-1.5-Flash",
    9: "Claude-3.5-Sonnet",
}


def load_multitude_csv(path: str, restrict_to_base_paper_18: bool = True) -> pd.DataFrame:
    """
    Load the raw MULTITuDE v3 dataframe and prepare it for SFA-CA.

    The real file uses these column names (confirmed from the actual
    downloaded multitude_v3_clean.csv):
        text         -> the raw text sample
        label        -> BINARY 0=human, 1=machine (not used for attribution)
        multi_label  -> the actual class we need: "human" or a specific
                        generator name, e.g. "gpt-3.5-turbo-0125"
        split        -> "train" or "test" (already provided by the dataset)
        language     -> ISO 639-1 language code (21 total in the raw file)

    restrict_to_base_paper_18: if True, drops the 3 extra languages
        (ca, ga, gd) that are in the raw file but were NOT part of the
        base paper's 18-language selection, so your results stay directly
        comparable to their reported numbers (Table 1, Table 2, etc.).
    """
    df = pd.read_csv(path)

    if restrict_to_base_paper_18:
        df = df[df["language"].isin(BASE_PAPER_18_LANGUAGES)].reset_index(drop=True)

    df["cluster"] = df["language"].apply(get_cluster)
    df["label_id"] = df["multi_label"].map(LABEL2ID)

    # Sanity check: flag any rows whose multi_label didn't match LABEL2ID
    # (would show up as NaN in label_id) instead of silently training on
    # broken labels.
    unmapped = df["label_id"].isna().sum()
    if unmapped > 0:
        unknown_values = df.loc[df["label_id"].isna(), "multi_label"].unique()
        raise ValueError(
            f"{unmapped} rows have a multi_label value not found in "
            f"LABEL2ID: {unknown_values}. Update LABEL2ID in data_loader.py."
        )

    return df


def filter_by_clusters(df: pd.DataFrame, clusters: list) -> pd.DataFrame:
    """Keep only rows whose language cluster is in `clusters`."""
    return df[df["cluster"].isin(clusters)].reset_index(drop=True)


def filter_by_languages(df: pd.DataFrame, langs: list) -> pd.DataFrame:
    """Keep only rows whose language code is in `langs`."""
    return df[df["language"].isin(langs)].reset_index(drop=True)


def filter_by_split(df: pd.DataFrame, split_name: str) -> pd.DataFrame:
    """Keep only rows matching the dataset's own 'train' or 'test' split
    (MULTITuDE v3 already provides this -- no need to re-split randomly)."""
    assert split_name in ("train", "test"), "split_name must be 'train' or 'test'"
    return df[df["split"] == split_name].reset_index(drop=True)


class AttributionDataset(Dataset):
    """
    A thin torch Dataset wrapper around a filtered dataframe, ready to
    be tokenized on the fly in the training loop.
    """

    def __init__(self, df: pd.DataFrame, tokenizer, max_length: int = 512):
        self.texts = df["text"].tolist()
        self.labels = df["label_id"].tolist()
        self.clusters = df["cluster"].tolist()
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        item = {k: v.squeeze(0) for k, v in encoding.items()}
        item["labels"] = self.labels[idx]
        item["cluster"] = self.clusters[idx]
        return item


if __name__ == "__main__":
    # Example usage once you have the real CSV downloaded:
    # df = load_multitude_csv("data/raw/multitude_v3.csv")
    # print(df["cluster"].value_counts())
    print("Defined clusters:", all_clusters())
    print("Update the path in load_multitude_csv(...) once your data is downloaded.")
