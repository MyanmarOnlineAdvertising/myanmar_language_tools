#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright Zeta Co., Ltd.
## written by @moeseth based on research by @aye_hnin_khine

from __future__ import division

import math

class TFIDF():
    def __init__(self, total_counted_documents, document_words_list, words_dictionary, sql_manager=None):
        self.TOTAL_COUNTED_DOCUMENTS = total_counted_documents

        self.words_dictionary = {}

        if sql_manager is None:
            self.words_dictionary = words_dictionary
        else:
            ## if total_documents_count is 0, we need to download df from server
            self.__prepare_df_for_words_list(document_words_list, sql_manager)


    def __prepare_df_for_words_list(self, document_words_list, sql_manager):
        self.df_count_dict = {}

        if sql_manager is not None:
            query = "select df, word from document_frequency where word in (%s)"
            query = query % (", ".join(['%s'] * len(document_words_list)))
            results = sql_manager.execute(query, document_words_list)

            largest_df = 0

            for r in results:
                df = int(r["df"])
                word = r["word"]

                if df > largest_df:
                    largest_df = df

                self.words_dictionary[word] = df

            self.TOTAL_COUNTED_DOCUMENTS = largest_df


    ## calculate how many times the word appeared in a document
    def getTF(self, word, document_words_list):
        word_count = document_words_list.count(word)

        return (word_count/len(document_words_list))


    ## calculate how many documents the word appeared in out of the whole document corpus
    def getIDF(self, word):
        ## df always starts at 1 to avoid division by zero case
        df = 1

        if word in self.words_dictionary:
            df = self.words_dictionary[word]
        
        idf = math.log(self.TOTAL_COUNTED_DOCUMENTS/df)
        return idf
