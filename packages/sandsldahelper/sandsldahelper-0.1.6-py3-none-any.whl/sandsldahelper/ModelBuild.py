# --------------------------------------------------------------------------------------
# File: "ModelBuild.py"
# Dir: "src/sandsldahelper/"
# Created: 2021-09-19
# --------------------------------------------------------------------------------------

"""
This file contains the functions needed to build the model
"""
from pathlib import Path
import SandsPythonFunctions.ParquetFunctions as pf
import pandas as pd
import pretty_errors
import tomotopy as tp


def create_topic_model(
    target_label: str,
    topic_model_path: Path,
    num_topics=15,
    alpha=0.1,
    eta=0.01,
    term_weight=tp.TermWeight.ONE,
    model_type="LDA",
):
    """This function will create a topic model file that can then be used to create output files

    Args:
        target_label (str): the label that will be applied to directories and files
        topic_model_path (Path): this is the parent directory where all generated files will be stored
        num_topics (int, optional): The number of topics for the LDA or PT model. Defaults to 15.
        alpha (float, optional): Dirichlet prior on the per-document topic distributions; low alpha means each document will "belong" to fewer topics. Defaults to 0.1.
        eta (float, optional): Commonly known as beta; a low beta value means each topic will be made up fewer words. Defaults to 0.01.
        term_weight ([type], optional): Options for term weights are ONE (all terms equal), IDF (common words will have low weight and visa versa) and PMI (has to do with co-occurrences of words). Defaults to tp.TermWeight.ONE.
        model_type (str, optional): The type of topic model to be created can be "LDA" or "PT". Defaults to "LDA".
    """

    def get_coherence_model_score(num_topics, mdl, cohs_path, cohx_path):
        """There is a bug with the c_v method this issue has been reported here: https://github.com/bab2min/tomotopy/issues/126"""
        if not cohs_path.exists():
            print("Processing coherence score")
            coh_c_v = tp.coherence.Coherence(mdl, coherence="c_v")
            coh_u_mass = tp.coherence.Coherence(mdl, coherence="u_mass")
            coh_c_npmi = tp.coherence.Coherence(mdl, coherence="c_npmi")
            topics_coherence = []
            for topic_num in range(0, num_topics):
                topics_coherence.append(
                    [
                        topic_num,
                        coh_c_v.get_score(topic_id=topic_num),
                        coh_u_mass.get_score(topic_id=topic_num),
                        coh_c_npmi.get_score(topic_id=topic_num),
                    ]
                )
            dta = pd.DataFrame(topics_coherence, columns=["topic_num", "cv", "umass", "npmi"])
            coh_scores = ["cv", "umass", "npmi"]
            for coh_score in coh_scores:
                dta[f"{coh_score}_rank"] = dta[coh_score].rank(method="dense", ascending=False)
            dta["rank_average"] = dta[["umass_rank", "cv_rank", "npmi_rank"]].mean(axis=1)
            dta.sort_values(by="rank_average", inplace=True)
            pf.save_dataframe_as_parquet(dta, cohs_path)
            dta.to_excel(cohx_path, index=False)

    def create_model(
        modl_path, corp_path, cohs_path, cohx_path, num_topics, term_weight, alpha, eta
    ):
        def pre_model_trianing(num_topics, corp_path, term_weight, alpha, eta):
            corpus = tp.utils.Corpus.load(corp_path)
            if model_type == "LDA":
                mdl = tp.LDAModel(
                    k=num_topics,
                    min_cf=10,
                    min_df=5,
                    corpus=corpus,
                    tw=term_weight,
                    alpha=alpha,
                    eta=eta,
                )
            elif model_type == "PT":
                mdl = tp.PTModel(
                    k=num_topics,
                    min_cf=10,
                    min_df=5,
                    corpus=corpus,
                    tw=term_weight,
                    alpha=alpha,
                    eta=eta,
                )
            mdl.train(0)
            min_cf_5_per = int(len(mdl.used_vocabs) * 0.05)
            min_df_5_per = int(len(mdl.docs) * 0.05)
            rm_top_5_per = int(20)
            return corpus, min_cf_5_per, min_df_5_per, rm_top_5_per

        def train_model(
            corpus,
            num_topics,
            min_cf_5_per,
            min_df_5_per,
            rm_top_5_per,
            term_weight,
            alpha,
            eta,
        ):
            if model_type == "LDA":
                mdl = tp.LDAModel(
                    min_cf=min_cf_5_per,
                    min_df=min_df_5_per,
                    corpus=corpus,
                    rm_top=rm_top_5_per,
                    k=num_topics,
                    tw=term_weight,
                    alpha=alpha,
                    eta=eta,
                )
            elif model_type == "PT":
                mdl = tp.PTModel(
                    min_cf=min_cf_5_per,
                    min_df=min_df_5_per,
                    corpus=corpus,
                    rm_top=rm_top_5_per,
                    k=num_topics,
                    tw=term_weight,
                    alpha=alpha,
                    eta=eta,
                )
            mdl.train(0)
            return mdl

        corpus, min_cf_5_per, min_df_5_per, rm_top_5_per = pre_model_trianing(
            num_topics, corp_path, term_weight, alpha, eta
        )
        mdl = train_model(
            corpus, num_topics, min_cf_5_per, min_df_5_per, rm_top_5_per, term_weight, alpha, eta
        )
        get_coherence_model_score(num_topics, mdl, cohs_path, cohx_path)
        model_bytes = mdl.saves(full=True)
        modl_path.write_bytes(model_bytes)

    if not model_type in ["LDA", "PT"]:
        raise ValueError(f"model_type must be either LDA or PT")
    topic_model_num_path = topic_model_path / f"{target_label}_{str(num_topics).zfill(4)}_topics"
    target_num_label = f"{target_label}_{str(num_topics).zfill(4)}"
    corp_path = topic_model_path / f"{target_label}_corpus.tomotopy"
    modl_path = topic_model_num_path / f"{target_num_label}_{model_type}_model.modl"
    cohs_path = topic_model_num_path / f"{target_label}_{model_type}_model_topics_coherence.parquet"
    cohx_path = topic_model_num_path / f"{target_label}_{model_type}_model_topics_coherence.xlsx"
    topic_model_num_path.mkdir(parents=True, exist_ok=True)
    create_model(modl_path, corp_path, cohs_path, cohx_path, num_topics, term_weight, alpha, eta)
