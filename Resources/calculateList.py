# -*- coding: utf-8 -*-
from Resources.utils import Utils
from Resources.constants import SIMILARITY_SWITCH, GROUP_UTILITY_SWITCH, DISAGREEMENT_SWITCH
import csv
import numpy as np
from Resources.utils import Utils


class CalculateList:
    def refined_pre_processing(self, fp, similarity="cosine"):
        # print(fp)
        M, item_dict = Utils().get_user_item_matrix(fp)
        # fp1 = fp[:-4] + "-user-item.csv"
        # gen_csv_from_list(M, fp1)
        # fp2 = fp[:-4] + "-item-item.csv"
        M = [[int(collumn) for collumn in row] for row in M]
        S = self.get_similarity_matrix(M, similarity)
        # gen_csv_from_list(S, fp2)
        return M, S

    '''
        Receives the user-item matrix and the name of the similarity
        function and returns the similarity matrix
        @param M the user-item matrix
        @param similarity string of the similarity function to be used
        @returns the similarity matrix
    '''

    def get_similarity_matrix(self, M, similarity):
        M = np.transpose(M)
        S = Utils().get_function_switch(similarity, SIMILARITY_SWITCH)
        return [[S(item1, item2) for item2 in M] for item1 in M]

    def get_utility_score(self, M, group_utility, disagreement, w):
        '''
            Receives the user-item matrix, the strings with the names
            of the group-utility and disagreement strategies and a
            contant w for the
            @param M the user X item matrix, the matrix should have
            @param group_utility string with the name of the group-utility strategy
            @param disagreement string with the name of the dis. strategy
            @param w weight used to control the proportion between group-utility and disagreement
            @returns an array with the overall utility-score for each item
        '''
        pref = Utils().get_function_switch(
            group_utility, GROUP_UTILITY_SWITCH)
        dis = Utils().get_function_switch(
            disagreement, DISAGREEMENT_SWITCH)

        M = np.transpose(M)
        r = list()
        utility_score = 0
        w1 = w
        w2 = -w

        for row in M:
            utility_score = w1*pref(row) + w2*(1 - dis(row))
            r.append(utility_score)
        return r

    def get_weight_factor(self, M, r, s):
        '''
            Receives the user-item matrix, the utility score
            and the similarity matrix, returns the weight_factor
            array
            @param M the user-item matrix
            @param r the utility score array
            @param s the similarity matrix
            @return the weight_factor array
        '''
        M = np.transpose(M)
        q = list()
        weight_factor = 0

        for i in range(0, len(M)):
            for j in range(0, len(M)):
                weight_factor += s[i][j]*r[i]

            q.append(weight_factor)
            weight_factor = 0

        return q

    def update_ranking_score(self, rank, r, w, s, last_item_index):
        '''
            Receives the rank array, the utility score, a weight,
            the similarity matrix and the last inserted item index
            @param rank an array with the rank of all items
            @param r the utility score of all items
            @param w the weight of the function
            @param s the similarity matrix
            @param last_item_index the index of the last inserted item at the M array
            @returns the updated rank
        '''
        for i in range(0, len(rank)):
            rank[i] = rank[i] - w*r[i]*s[i][last_item_index]*r[last_item_index]
        return rank

    def diversify_group_recommendation_the_algorithm(self, dataset, M, S, k, group_utility="average", disagreement="variance", similarity="cosine", w=2):

        fpi = {}

        # fp1 = fp[:-4] + "-user-item.csv"
        # fp2 = fp[:-4] + "-item-item.csv"

        M, item_dict = Utils().get_user_item_matrix(dataset)
        # M = get_list_from_csv(fp1)
        M = M[:20]
        M = [[float(collumn) for collumn in row] for row in M]
        # print("user-item-matrix [x]")
        # print(" dimensions: " + str(len(M)) + "x" + str(len(M[0])))

        # S = get_list_from_csv(fp2)
        S = [[float(collumn) for collumn in row] for row in S]
        # print("similarity-matrix [x]")
        # print(" dimensions: " + str(len(S)) + "x" + str(len(S[0])))

        # avg_rev = [np.nanmean(row) for row in S] < -- apenas se formos fazer o preenchimento usando média
        # avg_rev = [np.nan_to_num(x) for x in avg_rev]
        S = Utils().replace_missing_values_nn(S)

        # print(S)

        r = self.get_utility_score(M, group_utility, disagreement, w)
        # print("utility-score [x] len= #" + str(len(r)))
        # print(" dimensions: " + str(len(r)))

        q = self.get_weight_factor(M, r, S)
        # print("weight-factor [x] len= #" + str(len(q)))
        # print(" dimensions: " + str(len(q)))

        rank = [w*x*y for x, y in zip(q, r)]
        I = list()

        for i in range(0, k):
            x = np.max(rank)
            last_item_idex = rank.index(x)
            I.append(last_item_idex)

            rank = self.update_ranking_score(rank, r, w, S, last_item_idex)

            rank.pop(last_item_idex)
            r.pop(last_item_idex)
            S.pop(last_item_idex)
            [s.pop(last_item_idex) for s in S]

        songs = list()
        for i in range(0, len(I)):
            songs.append([k for k, v in item_dict.items() if v == I[i]][0])
            # print("Item #" + str(i) + " = " +
            #       str([k for k, v in item_dict.items() if v == I[i]]))
        return songs
