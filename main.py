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

            highly_cited_pids.append(citnum)


    ##规定时间，并且画出分布
    logging.info('maxmin:{},paper year ...'.format(citnum))
    pid_year = json.loads(open(pathObj._field_paper_year_path).read())

    logging.info("paper year citnum ...")

    pid_year_citnum = json.loads(open(pathObj._paper_year_citations_path).read())


    xs = []
    ys  = []

    for pid in highly_cited_pids:

        pub_year = int(pid_year[pid])

        year_citnum = pid_year_citnum[pid]

        total_in_5 = 0
        for year in sorted(year_citnum.keys(),key= lambda x:int(x)):

            if int(year)- pub_year>5:
                break

            total_in_5 += year_citnum[year]

        if total_in_5 > max_min:

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



if __name__ == '__main__':

    field_name = 'computer science'
    tag = 'cs'

    pathObj = PATH(field_name,tag)

    outstanding_papers(pathObj)

