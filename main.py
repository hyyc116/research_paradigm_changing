#coding:utf-8
'''
统计领域内的高被引论文，然后限制时间范围，可视化发表年份及5年内被引次数

'''

from basic_config import *
from paths import PATH


def outstanding_papers(pathObj):

    ## 根据引用次数分布 来去高被引论文列表
    logging.info('loading pid citnum ...')
    pid_citnum = json.loads(open(pathObj._paper_cit_num_dis_path).read())

    ## 获取高被引论文
    citnum_list = pid_citnum.values()

    citnum_counter = Counter(citnum_list)

    max_min = 0
    isfirst = 0

    highly_cited_pids = []
    for citnum in sorted(citnum_counter.keys()):

        if citnum_counter[citnum]==1:

            if isfirst==0:

                max_min = citnum
                break

    for pid in pid_citnum.keys():

        if pid_citnum[pid]>=max_min:

            highly_cited_pids.append(pid)


    ##规定时间，并且画出分布
    logging.info('maxmin:{}, {} highly cited papers,paper year ...'.format(max_min,len(highly_cited_pids)))
    pid_year = json.loads(open(pathObj._field_paper_year_path).read())

    logging.info("paper year citnum ...")

    pid_year_citnum = json.loads(open(pathObj._paper_year_citations_path).read())


    xs = []
    ys  = []


    ## 记录
    selected_ids = []

    for pid in highly_cited_pids:

        pub_year = int(pid_year[pid])

        year_citnum = pid_year_citnum[pid]

        total_in_5 = 0
        for year in sorted(year_citnum.keys(),key= lambda x:int(x)):

            if int(year)- pub_year>5:
                break

            total_in_5 += year_citnum[year]

        if total_in_5 > max_min:

            selected_ids.append(pid)

            xs.append(pub_year)
            ys.append(total_in_5)


    logging.info('{} outstanding papers filtered.'.format(len(xs)))


    plt.figure(figsize=(5,4))

    plt.plot(xs,ys,'>')

    plt.xlabel('year')

    plt.ylabel('number of citations')

    plt.yscale('log')

    plt.tight_layout()

    plt.savefig('fig/outstanding_papers.png',dpi=400)

    logging.info('fig saved to fig/outstanding_papers.png.')

    #将这些ID的plot全画出来
    row = 14

    fig,axes = plt.subplots(row,10,figsize=(10*2.5,row*2))

    for i,pid in enumerate(selected_ids[:140]):

        ax = axes[i/10,i%10]

        year_citnum = pid_year_citnum[pid]

        xs = []
        ys = []

        for year in sorted(year_citnum.keys(),key= lambda x:int(x)):
            citnum = int(year_citnum[year])

            xs.append(int(year))
            ys.append(int(citnum))

        ax.plot(xs,ys)

        ax.set_xlabel('year')
        ax.set_ylabel('number of citations')

    plt.tight_layout()

    plt.savefig('fig/cd_figure.png',dpi=200)

    logging.info('figure saved to cd_figrue.png')



## 读取引用关系，所有引用关系必须在上述id的范围内,并且控制时间在2018年之前
def read_ref_relations(pathObj):

    ##目标ID列表
    paper_year = json.loads(open(pathObj._field_paper_year_path).read())
    ## 参考关系存放文件
    ref_relation_file = open(pathObj._paper_ref_relation_path,'w')

    sql = 'select paper_id,paper_reference_id from mag_core.paper_references'
    cit_relations = []
    citing_ids = []
    query_op = dbop()
    total_num = 0

    progress = 0
    pid_citnum = defaultdict(int)

    pid_max_length = defaultdict(list)
    for paper_id,paper_reference_id in query_op.query_database(sql):

        progress+=1

        if progress%100000000==0:
            logging.info('progress {:}, {} ref realtions saved.'.format(progress,total_num))

        if int(paper_year.get(paper_reference_id,9999))<1970 or int(paper_year.get(paper_reference_id,9999))>2017:

            continue

        else:

            citing_ids.append(paper_id)

            cit_relation = '{},{}'.format(paper_id,paper_reference_id)
            cit_relations.append(cit_relation)

            pid_citnum[paper_reference_id]+=1

            ## 每100万条存储一次
            if len(cit_relations)%10000000==0:
                ref_relation_file.write('\n'.join(cit_relations)+'\n')
                total_num+=len(cit_relations)
                cit_relations = []

    if len(cit_relations)>0:
        total_num+=len(cit_relations)
        ref_relation_file.write('\n'.join(cit_relations)+'\n')

    ref_relation_file.close()
    logging.info('{} ref relations saved to {}'.format(total_num,pathObj._paper_ref_relation_path))

    open(pathObj._paper_cit_num_dis_path,'w').write(json.dumps(pid_citnum))
    logging.info('paper cit num saved to {}.'.format(pathObj._paper_cit_num_dis_path))

    citing_ids = set(citing_ids)
    open('data/citing_ids.txt'.format('\n'.join(citing_ids)))
    logging.info('{} citing ids saved.'.format(len(citing_ids)))

    query_op = dbop()
    sql = 'select paper_id,year from mag_core.papers'
    progress = 0
    year_dis = defaultdict(int)
    logging.info('starting to read paper years ...')
    for paper_id,year in query_op.query_database(sql):

        progress+=1

        if progress%10000000==0:
            logging.info('Read paper year， progress {}, {} paper has year ...'.format(progress,len(paper_year)))

        if paper_id in citing_ids and paper_year.get(paper_id,None) is None:

            paper_year[paper_id] = int(year)

            year_dis[int(year)]+=1

    logging.info('Done, {}/{} paper has year ...'.format(len(paper_year),len(paper_ids)))
    open(pathObj._field_paper_year_path,'w').write(json.dumps(paper_year))
    logging.info('Data saved to data/mag_{}_paper_year.json'.format(pathObj._field_paper_year_path))


if __name__ == '__main__':

    field_name = 'computer science'
    tag = 'cs'

    pathObj = PATH(field_name,tag)

    read_ref_relations(pathObj)
    # outstanding_papers(pathObj)


