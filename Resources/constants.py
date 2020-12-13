from Resources.utils import Utils
GROUP_UTILITY_SWITCH = {
    "average": Utils.average,
    "least_misery": Utils.least_misery
}

DISAGREEMENT_SWITCH = {
    "variance": Utils.disagreement_variance,
    "pair_wise": Utils.average_pairwise_disagreement
}

SIMILARITY_SWITCH = {
    "cosine": Utils.cosine_similarity
}
