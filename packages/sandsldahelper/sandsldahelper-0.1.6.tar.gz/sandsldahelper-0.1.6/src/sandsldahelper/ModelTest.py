# --------------------------------------------------------------------------------------
# File: "ModelTest.py"
# Dir: "src/sandsldahelper/"
# Created: 2021-09-20
# --------------------------------------------------------------------------------------

"""
this file is meant to test models and hyperparameters to find a model that is a good fit

I used  Normalized  Pointwise Mutual Information (NPMI) for model evaluation
"NPMI ranges from [-1,1] and it measures how much the top-10 words of a topic are related to each other, where higher positive NMPI is better."
BERT for Arabic Topic Modeling: An Experimental Study on BERTopic Technique by Abeer Abuzayed Hend Al-Khalifa

I also used UMass for model evaluation
"I understand that as the value of UMass coherence approaches to 0 the topic coherence gets better."
https://stackoverflow.com/a/54354852

I also used C_V for model evaluation
".4 is low - .55 is okay - .65 might be as good as it is going to get - .7 is nice"
https://stackoverflow.com/a/55816086
"""

from pathlib import Path
from tqdm import tqdm
import SandsPythonFunctions.ParquetFunctions as pf
import json
import pandas as pd
import pretty_errors
import tomotopy as tp


def model_testing(
    target_label: str,
    topic_model_path: Path,
    num_topics=range(5, 15),
    term_weights=[tp.TermWeight.ONE, tp.TermWeight.IDF, tp.TermWeight.PMI],
    alphas=[0.01, 0.1, 0.5, 1.0],
    etas=[0.01, 0.1, 0.5, 1.0],
    model_type="LDA",
):
    def pre_model_trianing(num_topics, corp_path):
        corpus = tp.utils.Corpus.load(corp_path)
        if model_type == "LDA":
            mdl = tp.LDAModel(k=num_topics, min_cf=10, min_df=5, corpus=corpus)
        elif model_type == "PT":
            mdl = tp.PTModel(k=num_topics, min_cf=10, min_df=5, corpus=corpus)
        mdl.train(0)
        min_cf_5_per = int(len(mdl.used_vocabs) * 0.05)
        min_df_5_per = int(len(mdl.docs) * 0.05)
        rm_top_5_per = int(20)
        return corpus, min_cf_5_per, min_df_5_per, rm_top_5_per

    def make_hyperparameter_combos(term_weights, alphas, etas):
        hyperparameters_combos = []
        for alpha in alphas:
            for eta in etas:
                for term_weight in term_weights:
                    hyperparameters_combos.append([term_weight, alpha, eta])
        return hyperparameters_combos

    def train_model(corpus, num_topics, min_cf_5_per, min_df_5_per, rm_top_5_per, hyperparameters):
        if model_type == "LDA":
            mdl = tp.LDAModel(
                min_cf=min_cf_5_per,
                min_df=min_df_5_per,
                corpus=corpus,
                rm_top=rm_top_5_per,
                k=num_topics,
                tw=hyperparameters[0],
                alpha=hyperparameters[1],
                eta=hyperparameters[2],
            )
        elif model_type == "PT":
            mdl = tp.PTModel(
                min_cf=min_cf_5_per,
                min_df=min_df_5_per,
                corpus=corpus,
                rm_top=rm_top_5_per,
                k=num_topics,
                tw=hyperparameters[0],
                alpha=hyperparameters[1],
                eta=hyperparameters[2],
            )
        mdl.train(0)
        return mdl

    def coherence_scores_file_manage(cost_path, topics_coherence):
        all_coherence_scores = []
        if cost_path.exists():
            with open(cost_path, "r") as output_json:
                all_coherence_scores = json.load(output_json)
        all_coherence_scores.append(topics_coherence)
        with open(cost_path, "w") as output_json:
            json.dump(all_coherence_scores, output_json)

    def calculate_coherence_scores(num_topics, hyperparameters, mdl):
        coh_u_mass = tp.coherence.Coherence(mdl, coherence="u_mass")
        coh_c_v = tp.coherence.Coherence(mdl, coherence="c_v")
        coh_c_npmi = tp.coherence.Coherence(mdl, coherence="c_npmi")
        ave_coherence_u_mass = coh_u_mass.get_score()
        ave_coherence_c_v = coh_c_v.get_score()
        ave_coherence_c_npmi = coh_c_npmi.get_score()
        return [
            num_topics,
            str(hyperparameters[0]),
            hyperparameters[1],
            hyperparameters[2],
            ave_coherence_u_mass,
            ave_coherence_c_v,
            ave_coherence_c_npmi,
        ]

    def test_parameters(corp_path, cost_path, num_topics, term_weights, alphas, etas):
        corpus, min_cf_5_per, min_df_5_per, rm_top_5_per = pre_model_trianing(num_topics, corp_path)
        hyperparameter_combos = make_hyperparameter_combos(term_weights, alphas, etas)
        for hyperparameters in tqdm(
            hyperparameter_combos, desc=f"Testing hyperparameters for {num_topics} topics"
        ):
            mdl = train_model(
                corpus, num_topics, min_cf_5_per, min_df_5_per, rm_top_5_per, hyperparameters
            )
            topics_coherence = calculate_coherence_scores(num_topics, hyperparameters, mdl)
            coherence_scores_file_manage(cost_path, topics_coherence)

    def get_best_coherence_scores(cost_path, cohx_path):
        test_results = pd.read_json(cost_path)
        test_results.columns = [
            "num_topics",
            "term_weight",
            "alpha",
            "eta",
            "umass",
            "cv",
            "npmi",
        ]
        test_results.drop_duplicates(
            subset=["num_topics", "term_weight", "alpha", "eta"], inplace=True
        )
        coh_scores = ["cv", "umass", "npmi"]
        for coh_score in coh_scores:
            test_results[f"{coh_score}_rank"] = test_results[coh_score].rank(
                method="dense", ascending=False
            )
        test_results["rank_average"] = test_results[["umass_rank", "cv_rank", "npmi_rank"]].mean(
            axis=1
        )
        test_results.sort_values(by="rank_average", inplace=True)
        test_results.to_excel(cohx_path)

    if not model_type in ["LDA", "PT"]:
        raise ValueError(f"model_type must be either LDA or PT")
    corp_path = topic_model_path / f"{target_label}_corpus.tomotopy"
    cost_path = topic_model_path / f"{target_label}_{model_type}_model_coherence_testing.json"
    cohx_path = topic_model_path / f"{target_label}_{model_type}_model_coherence.xlsx"
    for num_topics in tqdm(num_topics, desc=f"Testing {target_label} topics"):
        test_parameters(corp_path, cost_path, num_topics, term_weights, alphas, etas)
    get_best_coherence_scores(cost_path, cohx_path)
