#coding:utf-8
import json
import logging
class PATH:


    def __init__(self,field_name,field_tag):

        self._field_tag = field_tag

        self._field_name = field_name

        ''' ==========文件列表=============='''
        ##存储文章id列表文件地址
        self._field_paper_ids_path = 'data/paper_ids_{}.txt'.format(self._field_tag)
        ## 文章对应的发表年份
        self._field_paper_year_path = 'data/paper_year_{}.json'.format(self._field_tag)
        ## 存储参考关系的文件地址
        self._paper_ref_relation_path = 'data/paper_ref_relations_{}.txt'.format(self._field_tag)

        self._paper_cit_num_dis_path = 'data/paper_cit_num_dis_{}.json'.format(self._field_tag)

        ### 论文每年的引用次数
        self._paper_year_citations_path = 'data/paper_year_citation_{}.txt'.format(self._field_tag)

    def loads_json(self,path):
        return json.loads(open(path).read())

    def read_file(self,path):
        return [line.strip() for line in open(path)]

    def losses_file(self,m,n,model):
        return 'losses/sip_m{}n{}_{}_{}_loss.json'.format(m,n,model,self._field_tag)

    def save_json(self,path,obj):
        open(path,'w').write(json.dumps(obj))
        logging.info('json obj saved to {}.'.format(path))



    @property
    def field_papers(self):
        paper_ids = []
        for paper_id in open(self._field_paper_ids_path):
            paper_ids.append(paper_id.strip())

        return paper_ids

    @property
    def paper_year(self):
        return json.loads(open(self._field_paper_year_path).read())



