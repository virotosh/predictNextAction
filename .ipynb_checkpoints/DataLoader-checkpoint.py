# A DataLoader is an object that loads the log data
# A data matrix is a matrix with n rows (num_data) and d columns (num_features)
# the features are themselves grouped in different views (num_views)
class DataLoader:
    def __init__(self, data_dir, save_dir):
        """For initialization"""
        #Parameters

        self.corpus, self.dictionary, self.views_ind, self.vocab_size = preprocess(data_dir, save_dir)

        self.num_features = self.corpus.num_terms          #total number of features # here num_features is num_entities
        self.num_data = self.corpus.num_docs               #total number of data (snapshots)
        self.num_views = max(self.views_ind) + 1           #total number of views views= [0=BOW, 1=KW, 2=App, 3=People]
        self.Data = None                                   #todo: (it may be impossible to create this) a num_data*num_featurs array
        #name of the features
        self.feature_names = [self.dictionary.get(i) for i in range(self.num_features) ]
        self.num_items_per_view = [sum(self.views_ind == i) for i in range(self.num_views)]

    def print_info(self):
        print ('The corpus has %d items' %self.num_data+' and %d features'%self.num_features+\
              ' and %d views' %self.num_views +' there are %d' %self.corpus.num_nnz +' non-zero elements')
        print ('People view %d' % self.num_items_per_view[3]+ ' items, Application view %d' %self.num_items_per_view[2]+\
              ' items, Doc view %d' %self.num_items_per_view[4]+\
              ' items, KW view %d' %self.num_items_per_view[1]+' items, BOW view %d' %self.num_items_per_view[0]+' items.')

    def process_item_info(self):
        #This function is used for offline feedback gathering
        print ('The corpus has %d items' %self.num_data+' and %d features'%self.num_features+\
              ' and %d views' %self.num_views +' there are %d' %self.corpus.num_nnz +' non-zero elements')
        print ('People view %d' %sum(self.views_ind == 3)+ ' items, Application view %d' %sum(self.views_ind == 2)+\
              ' items, Doc view %d' %sum(self.views_ind == 4)+\
              ' items, KW view %d' %sum(self.views_ind == 1)+' items, BOW view %d' %sum(self.views_ind == 0)+' items.')

        def returnReverse(k,v):
            return (v,k)
        #get the document frequency of the terms (i.e. how many document did a particular term occur in):
        term_frequency_dic = self.dictionary.dfs
        sorted_term_ferequency = sorted(term_frequency_dic.items(), key=lambda x : x[1], reverse=True)
        sorted_IDs = [sorted_term_ferequency[i][0] for i in range(self.num_features)]

        count_term = [y for (x,y) in sorted_term_ferequency]
        pyplot.hist(count_term[9000:self.num_features-1], 20, facecolor='green')
        pyplot.xlabel('number of occurrences in the corpus')
        pyplot.ylabel('count')
        pyplot.show()
        num_of_1_occurance = len([y for (x,y) in sorted_term_ferequency if y==1])
        print ('%d terms' %num_of_1_occurance+' have only appeared once in the corpus')
        term_names_1_occurance = [(self.feature_names[x]) for (x,y) in sorted_term_ferequency if y==1 ]
        #with open('term_names_1_occurance.txt', 'w') as outfile:
        #    json.dump(term_names_1_occurance, outfile)
        #those terms can be removed from the dictionary.todo: HOWEVER, they should be removed when the corpus is being made
        #print self.dictionary
        #self.dictionary.filter_extremes(no_below=2)
        #print self.dictionary

        AP_names = [(self.feature_names[sorted_IDs[i]]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 2]
        AP_ids = [(sorted_IDs[i]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 2]
        
        Doc_names = [(self.feature_names[sorted_IDs[i]]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 4]
        Doc_ids = [(sorted_IDs[i]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 4]

        KW_names = [(self.feature_names[sorted_IDs[i]]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 1]
        KW_ids = [(sorted_IDs[i]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 1]

        People_names = [(self.feature_names[sorted_IDs[i]]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 3]
        People_ids = [(sorted_IDs[i]) for i in range(self.num_features) \
                    if  self.views_ind[sorted_IDs[i]] == 3]

        num_to_show = 1000 #
        data = {}
        data["AP_names"] = AP_names[:num_to_show]
        data["Doc_names"] = Doc_names[:num_to_show]
        data["KW_names"] = KW_names[:num_to_show]
        data["People_names"] = People_names[:num_to_show]
        data["AP_ids"] = AP_ids[:num_to_show]
        data["Doc_ids"] = Doc_ids[:num_to_show]
        data["KW_ids"] = KW_ids[:num_to_show]
        data["People_ids"] = People_ids[:num_to_show]

        print(data)