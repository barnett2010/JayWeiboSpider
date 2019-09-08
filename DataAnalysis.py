import csv
import collections # 会使用集合中的Counter

import jieba.analyse
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from pyecharts.charts import Pie #, Bar, Map,WordCloud # 饼图、柱状图、地图、云词

# 新浪话题数据保存文件
CSV_FILE_PATH = 'sina_topic.csv'
# 需要清洗的词
STOP_WORDS_FILE_PATH = 'stop_words.txt'

def read_csv_to_dict(index) -> dict:
    """
    读取CSV数据
    数据格式为:'用户id','用户名','性别','地区','生日','微博id','微博内容'
    :param index:读取某一列从0开始
    :return : dic属性为key，次数为value
    """
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        column = [columns[index] for columns in reader]
        # print(column)  # 打印出传入参数index对应的那一列数据
        dic = collections.Counter(column)
        # 删除空字符串
        if '' in dic:
            dic.pop('')
        print(dic)
        return dic

def analysis_gender():
    """
    分析性别
    """
    # 读取性别列,第二列
    dic = read_csv_to_dict(2)
    # 生成二维数组
    gender_count_list = [list(z) for z in zip(dic.keys(), dic.values())]
    print(gender_count_list)
    pie = (
        Pie()
            .add("", gender_count_list)
            .set_colors(["red", "blue"])
            .set_global_opts(title_opts=opts.TitleOpts(title="性别分析"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
    )
    pie.render('gender.html')
    pie.render_notebook()  # 或者直接在notebook中显示。(出了问题，显示不出来)
    
def analysis_age():
    """
    分析年龄
    """
    # 读取性别列,第四列,获取到的是年龄的列表
    dic = read_csv_to_dict(4)
    # 生成柱状图
    sorted_dic = {}
    for key in sorted(dic):
        sorted_dic[key] = dic[key]
    print(sorted_dic)
    bar = (
        Bar()
            .add_xaxis(list(sorted_dic.keys()))
            .add_yaxis("周杰伦打榜粉丝年龄分析", list(sorted_dic.values()))
            .set_global_opts(
            yaxis_opts = opts.AxisOpts(name="数量"),
            xaxis_opts = opts.AxisOpts(name="年龄"),
            )
    )
    bar.render('age_bar.html')
    bar.render_notebook()
    # 生成饼图
    age_count_list = [list(z) for z in zip(dic.keys(), dic.values())]
    print(age_count_list)
    pie = (
        Pie()
            .add("", age_count_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="周杰伦打榜粉丝年龄分析"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
    )
    pie.render('age-pie.html')
    # pie.render_notebook()  # 或者直接在notebook中显示。(出了问题，显示不出来)    

def analysis_area():
    """
    分析地区
    :return
    """
    # 读取地区列,第三列
    dic = read_csv_to_dict(3)
    # 生成二维数组
    area_count_list = [list(z) for z in zip(dic.keys(), dic.values())]
    print(area_count_list)
    map = (
        Map()
            .add("周杰伦打榜粉丝地区分析", area_count_list, "china")
            .set_global_opts(
            visualmap_opts = opts.VisualMapOpts(max_=200)
            )
            
    )
    map.render('area.html')
    map.render_notebook()  # 或者直接在notebook中显示。(出了问题，显示不出来)
    
def analysis_sina_content():
    """
    分析微博内容
    :return
    """
    # 读取微博内容列,第六列
    dic = read_csv_to_dict(6)
    # 数据清洗，去掉无效的词
    jieba.analyse.set_stop_words(STOP_WORDS_FILE_PATH)
    # 词数统计
    words_count_list = jieba.analyse.textrank(' '.join(dic.keys()), topK=50, withWeight=True)
    print(words_count_list)
    # 生成词云
    word_cloud = (
        WordCloud()
            .add("", words_count_list, word_size_range=[20,100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="周杰伦打榜微博内容分析"))
    )
    word_cloud.render('word_cloud.html')
    word_cloud.render_notebook()  # 或者直接在notebook中显示。(出了问题，显示不出来)
    
    
if __name__ == '__main__':
    analysis_gender()
    analysis_age()
    analysis_area()
    analysis_sina_content()
    