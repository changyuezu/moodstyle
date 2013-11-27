#!/usr/bin/env python
# coding:utf-8


class Document(object):

    """
    整个是一个封装的 dict{}
    分别为  word - > 分类类别 -> 词数目
    """

    def __init__(self):
        self.__doc = {}
        self.doc_count = 0  # 文档数目
        self.__type_count = {}

    def insert_document(self, doc_type, document={}):
        if not isinstance(document, (set, list)):
            raise TypeError, 'document  must is list or set'
        for word in document:
            self.__insert_doc_dict(doc_type, word)
        self.__insert_type_dict(doc_type)
        self.doc_count = self.doc_count + 1

    def get_word_count(self, word):
        if not (word and isinstance(word, (str, unicode))):
            raise TypeError, 'word must be is str or unicode'
        count = 0
        if self.__doc.has_key(word):
            for _key, _val in self.__doc[word].items():
                count = count + _val
        return count

    def __insert_type_dict(self, doc_type):
        count = 1
        if self.__type_count.has_key(doc_type):
            count = self.__type_count[doc_type] + 1
        self.__type_count[doc_type] = count

    def get_type_word_count(self, doc_type, word):
        if self.__doc.has_key(word):
            if self.__doc[word].has_key(doc_type):
                return self.__doc[word][doc_type]
        return 0

    def __insert_doc_dict(self, doc_type, word):
        __value = 1
        if self._doc.has_key(word):
            if self._doc[word].has_key(doc_type):
                __value = self._doc[word][doc_type] + 1
        else:
            self._doc[word] = {}
        self._doc[word][doc_type] = __value


    def get_doc_count(self , doc_type):
    	if self.__type_count.has_key(doc_type):
    		return self.__type_count[doc_type]
    	return 0

    def get_word_set(self):
    	return self.__doc.keys()

    def get_type_set(self):
    	return self.__type_count.keys()



class ITextFeatureScore(object):

 	'''
 	doc_word_count , 特定文档中出现该词的文档数目
 	doc_count , 特定类别的文档数目
 	word_count , 特定存在文档总数目
 	doc_sum , 文档总数目
 	功能： 计算 每个词的分值
 	返回: double

 	'''
	def feature_socre(self , doc_word_count , doc_count , word_count , doc_sum):
		raise NotImplementedError

class IM(ITextFeatureScore):
		
	def feature_socre(self , doc_word_count , doc_count , word_count , doc_sum):
		return 0.

class TextFeature(object):


	def __init__(self ,text_feature_score  , filter_rate = 0.0004 ):
		if text_feature_score and isinstance(text_feature_score , ITextFeatureScore):
			raise TypeError
		self.filter_rate = filter_rate
		self.text_feature_score = text_feature_score
    
	def insert_document_list(self , contents):
		doc = Document()
		for line in contents:
			lineInfo = line.split('\t')
			if len(lineInfo) >=2 :
				word_set = set(lineInfo[1].split(" "))
				doc.insert_document(lineInfo[0] , word_set)
		return doc


	def extract_feature_from_contents(self , top_word ,contents):
		doc = self.insert_document_list(contents)
		doc_word_score_map = {}
		for doc_type in doc.get_type_set():
			doc_word_score_map[doc_type] = {}
		for word in doc.get_word_set():
			for doc_type in doc.get_type_set():
				if doc.get_type_word_count(doc_type , word) < long(doc.get_doc_count(doc_type) * self.filter_rate):
					continue
				score = self.text_feature_score(doc.get_type_word_count(doc_type , word) , doc.get_doc_count(doc_type) , doc.get_word_count(word) , doc.doc_count)
				doc_word_score_map[doc_type][word] = score







if __name__ == '__main__':
	s = TextFeature(IM)



