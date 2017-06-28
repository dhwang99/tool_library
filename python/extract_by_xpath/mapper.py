#!/bin/env python
#coding=UTF-8

import re
import sys
sys.path.append("./")
import zlib
from ordered_dict import ordered_dict
from lxml import etree
import lxml.html

import re

def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id
    
def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)


def decompress(data):
    import zlib
    try:
        return zlib.decompress(data, zlib.MAX_WBITS | 32)
    except Exception, e:
        #print e
        pass
    return None

def extract(url, data):
    if data == None:
        return {}
    if url.startswith(("http://baike.baidu.com/view", "http://baike.baidu.com/subview")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_baike(url, root, data)
    elif url.startswith(("http://club.xywy.com/static")):
        root = parse_from_string(data, "GBK")
        if root != -1:
            return extract_xywy(url, root, data)
    elif url.startswith(("http://zhidao.baidu.com/question/")):
        root = parse_from_string(data, "GBK")
        if root != -1:        
            return extract_zhidao(url, root, data)
    elif url.startswith(("http://wenku.baidu.com/view/")):
        root = parse_from_string(data, "GBK")
        if root != -1:
            return extract_wenku(url, root, data)
    elif url.startswith(("http://jingyan.baidu.com/article/")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_jingyan(url, root, data)
    elif url.startswith(("http://www.docin.com/zuowen/view.do?id=")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_docin_zuowen(url, root, data)
    elif url.startswith(("http://www.babytree.com/ask/detail/")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_baby_ask(url, root, data)
    elif url.startswith(("http://www.babytree.com/learn/article/")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_baby_learn(url, root, data)
    elif url.startswith(("http://www.babytree.com/know/weekly.php?type=")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_baby_know(url, root, data)
    elif url.startswith(("http://www.haodf.com/wenda/")):
        root = parse_from_string(data, "GBK")
        if root != -1:
            return extract_haodf_wenda(url, root, data)
    elif url.startswith(("http://www.haodf.com/zhuanjiaguandian/")):
        root = parse_from_string(data, "GBK")
        if root != -1:
            return extract_haodf_zhuanjiaguandian(url, root, data)
    elif url.startswith(("http://www.docin.com/p-")):
        root = parse_from_string(data, "UTF8")
        if root != -1:
            return extract_docin_p(url, root, data)
    """ 没有case
    elif url.startswith(("http://muzhi.baidu.com/question/")):
        root = parse_from_string(data, "GBK")
        if root:
            return extract_muzhi(url, root, data)
    elif url.startswith(("http://huiyi.docin.com/meeting/doc.do?id=")):
        root = parse_from_string(data, "UTF8")
        if root:
            return extract_docin_meeting(url, root, data)
    """

    return {}

def parse_from_string(data, code):
    try:
        root = lxml.html.fromstring(data.decode(code, "ignore"))
    except Exception, e:
        #print e
        root = -1 
    return root

def extract_xywy(url, root, data):
    result = ordered_dict()

    NUM_PATTERN = re.compile("level(\d+) ")
    import extract

    result["title"] = extract.extract_text(root, "//*[@class='fl dib fb']", None)
    result["nav"] = extract.extract_text(root, "//*[@class='pt10 pb10 lh180 znblue normal-a']", None)
    result["q_desc"] = extract.extract_text(root, "//*[@id='qdetailc']", None)
    result["condition_desc"] = extract.extract_text(root, "//*[@class=' lh180 mt10 graydeep']", None)
    result["help_desc"] = extract.extract_text(root, "//*[@class=' lh180 pb20 mt10 graydeep']", None)

    # 最佳答案
    i =0 
    nodes = root.xpath("//*[@class='docall clearfix Bestbg']")
    for node in nodes:
        i += 1
        result["bestanswer"+str(i)] = extract.extract_text(node, ".//*[@class='pt15 f14 graydeep  pl20 pr20']", None)
        #result["best_gate_num"+str(i)] = extract.extract_text(node, ".//*[@class='gratenum']", None)
        result["best_user_title"+str(i)] = extract.extract_text(node, ".//*[@class='fl ml10 btn-a mr5']  | .//*[@class='cl Doc_lh24']/span", None)
        temp = extract.extract_attr(node, ".//*[@class='fl mr10']/a", "class")
        if temp != None:
            m = NUM_PATTERN.search(temp)
            if m != None:
                result["best_user_credit"+str(i)] = m.group(1) 
        result["best_user_expert"+str(i)] = extract.extract_text(node, ".//*[@class='fl graydeep'] | .//*[@class='fl w420']", None)
        result["best_answer_time"+str(i)] = extract.extract_text(node, ".//*[@class='User_newbg User_time Doc_time']", None)

    # 答案
    nodes = root.xpath("//*[@class='docall clearfix']")
    i = 0
    for node in nodes:
        i += 1
        result["answer"+str(i)] = extract.extract_text(node, ".//*[@class='pt15 f14 graydeep  pl20 pr20']", None)
        result["gate_num"+str(i)] = extract.extract_text(node, ".//*[@class='gratenum']", None)
        result["user_title"+str(i)] = extract.extract_text(node, ".//*[@class='fl ml10 btn-a mr5'] | .//*[@class='cl Doc_lh24']/span", None)
        temp = extract.extract_attr(node, ".//*[@class='fl mr10']//a", "class")
        if temp != None:
            m = NUM_PATTERN.search(temp)
            if m != None:
                result["user_credit"+str(i)] = m.group(1) 
        result["user_expert"+str(i)] = extract.extract_text(node, ".//*[@class='fl graydeep'] | .//*[@class='fl w420']", None)
        result["answer_time"+str(i)] = extract.extract_text(node, ".//*[@class='User_newbg User_time Doc_time']", None)

    return result

def extract_baike(url, root, data): 
    #print url
    result = ordered_dict()
    import extract
    #result["title"] = extract.extract_text(root, "//*[@class='lemmaTitleH1']", None)
    result["title"] = extract.extract_text(root, "//title", re.compile(u"(.*?)_百度百科"))
    result["view_num"] = extract.extract_text(root, "//*[@id='viewPV']", None)
    m = re.compile("编辑次数：(\d+)次").search(data)
    if m != None:
        result["edit_num"] = m.group(1)
    result["vote_num"] = extract.extract_text(root, "//*[@class='vote_num']", None)
    result["share_num"] = extract.extract_text(root, "//*[@class='shareCount']", None)

    nodes = root.xpath("//*[@class='reference']//li")
    result["reference_num"] = len(nodes)
    temp = extract.extract_attr(root, "//*[@class='z-album-collection-box log-set-param lazyload']", "lazy-init")
    if temp != None:
        result["img_num"] = temp.count("coverpic") 

    #  摘要信息
    result["summary"] = extract.extract_text(root, "//*[@class='intro-summary-p'] | //*[@class='card-summary-content'] | //dd[@class='desc']", None)
    # 名片信息
    nodes = root.xpath("//*[@class='biItem']")
    for node in nodes:
        k = extract.extract_text(node, ".//*[@class='biTitle']", None)
        v = extract.extract_text(node, ".//*[@class='biContent']", None)
        if k != None and v != None:
            result[k] = v
    # 正文信息
    nodes = root.xpath("//*[@id='lemmaContent-0']")
    i = 0
    for n in nodes:
        for node in n.getchildren():
            i += 1
            class_type = node.attrib.get("class", "")
            if class_type == "headline-1":
                result["title"+str(i)] = extract.extract_text(node, ".//*[@class='headline-content']", None)
                continue
            elif class_type == "para":
                result["para"+str(i)] = extract.extract_text(node, ".", None)
                continue
    return result

def extract_zhidao(url, root, data): 
    #print url
    style1 = re.compile('id="question-box"')
    m = style1.search(data)
    if m != None:
        #print "style1"
        return extract_zhidao_style1(url, root, data)
    else:
        #print "style2"
        return extract_zhidao_style2(url, root, data)

def extract_zhidao_style1(url, root, data):

    #print "page", etree.tostring(root)
    level_pattern = re.compile("\|</span>\s*(.*?)\s*</div>")
    result = ordered_dict()
    import extract
    # 问题 问题分类 浏览量 提问时间 问题描述
    result["title"] = extract.extract_text(root, "//title", re.compile(u"(.*?)_百度知道"))
    result["q_time"] = extract.extract_text(root, '//*[@class="question"]/div[@class="details"]//span[@class="gray"][1]', re.compile(u"(\d{4}-\d+-\d+\s+\d+:\d+)"))
    result["q_class"] = extract.extract_text(root, '//div[@class="bread"]', re.compile(u"百度知道 >\s*(.*?)"))
    result["q_desc"] = ""
    q_descs = root.xpath('//*[@id="question-content"]')
    for q_desc in q_descs:
        result["q_desc"] += q_desc.text_content() + " "
    q_descs = root.xpath('//*[@id="question-suply"]')
    for q_desc in q_descs:
        result["q_desc"] += q_desc.text_content() + " "

    # 最佳答案：回答时间 答案正文 赞数 回答者名称 回答者主页 回答者等级 回答者采纳率 回答者擅长分类
    best_answers = root.xpath('//*[contains(@id,"best-answer-panel")]')
    if not best_answers:
        best_answers = root.xpath('//*[contains(@id,"recommend-answer-panel")]')
    #i = 0 
    if best_answers:
        node = best_answers[0] 
        #print "best", etree.tostring(node)
        #i += 1
        # 回答时间 答案正文
        result["best_answer_time"] = extract.extract_text(node, './/div[contains(@class,"time")]/span', None)
        result["best_answer"] = extract.extract_text(node, './/div[@class="content"]/pre', None)
        # 赞数 
        agree_num = extract.extract_text(node, './/*[contains(@alog-action,"qb-zan-")]/div[2]', None)
        best_replyer = node.xpath('.//*[@class="best-replyer"]/div[@class="carefield ml10"]')
        if best_replyer:
            #print "best_replyer", etree.tostring(best_replyer[0])
            replyer_info = best_replyer[0].xpath('.//*[@class="user-name"]')
            if replyer_info:
                result["best_replyer"] = replyer_info[0].text_content()
                result["best_replyer_homepage"] = replyer_info[0].attrib.get("href")

            result["best_replyer_level"] = extract.extract_text(best_replyer[0], './/a[@log="bestreplyer.icon.grade"]', None)
            result["best_replyer_adoption_rate"] = extract.extract_text(best_replyer[0], './/*[@class="ml10 gray"]', re.compile(u"(\d+%)"))
            expert_classes = best_replyer[0].xpath('.//*[@log="bestreplyer.link.carefield"]')
            j = 0
            for expert_class in expert_classes:
                j += 1
                result["best_replyer_expert_class_"+str(j)] = expert_class.text_content()

        
    # 其他答案：回答时间 答案正文 赞数 踩数 评论数 回答者名称 回答者主页 回答者等级
    other_answers = root.xpath('//*[@id="reply-panel"]/div[contains(@id,"reply-box-")]')
    i = 0
    for node in other_answers:
        #print "other", etree.tostring(node)
        i += 1
        # 回答时间 答案正文
        result["other_answer_time_"+str(i)] = extract.extract_text(node, './/span[contains(@class,"float-r")]', None)
        result["other_answer_"+str(i)] = extract.extract_text(node, './/div[@class="content"]/pre', None)
        # 赞数
        agree_num = extract.extract_text(node, './/*[contains(@alog-action,"qb-zan-")]/div[2]', None)

        # 回答者名称 回答者主页 回答者等级 回答者采纳率 回答者擅长分类
        other_replyer = node.xpath('.//*[@class="user-name"]')
        if other_replyer:
            result["other_replyer_"+str(i)] = other_replyer[0].text_content()
            result["other_replyer_homepage_"+str(i)] = other_replyer[0].attrib.get("href")
            replyer_info = node.xpath('.//*[@class="details clf"]')
            if replyer_info:
                replyer_str = re.sub("\r|\n","",etree.tostring(replyer_info[0]))
                level_info = level_pattern.findall(replyer_str)
                if level_info:
                    result["other_replyer_level_"+str(i)] = decode_unicode_references(level_info[0])
    return result

def extract_zhidao_style2(url, root, data):

    #print "page", etree.tostring(root)
    result = ordered_dict()
    level_pattern = re.compile('<a .*?>(.*?)</a><span ')
    import extract
    # 问题 问题分类 提问时间 问题描述
    result["title"] = extract.extract_text(root, "//title", re.compile(u"(.*?)_百度知道"))
    
    result["q_time"] = extract.extract_text(root, '//*[@id="wgt-ask"]//span[contains(@class,"grid-r")]', None)
    #TODO 问题分类
    q_class = root.xpath('//div[@id="ask-info"]')
    if q_class:
        result["q_class"] = extract.extract_text(q_class[0], './/span/a', None)
    else:
        result["q_class"] = extract.extract_text(root, '//nav[contains(@class,"wgt-nav")]', None)

    q_descs = root.xpath('//*[@id="wgt-ask"]//pre')
    if q_descs:
        result["q_desc"] = ""
    for q_desc in  q_descs:
        result["q_desc"] += q_desc.text_content() + " "

    # 最佳答案：回答时间 答案正文 追问 追问答案 赞数 踩数 评论数 回答者名称 回答者主页 回答者等级 回答者采纳率 回答者擅长分类
    best_answers = root.xpath('//*[contains(@class,"wgt-best")]')
    if not best_answers:
        best_answers = root.xpath('//*[contains(@class,"wgt-recommend")]')
    #i = 0 
    if best_answers:
        node = best_answers[0] 
        #print "best", etree.tostring(node)
        #i += 1
        # 回答时间 答案正文
        result["best_answer_time"] = extract.extract_text(node, './/span[contains(@class,"grid-r")]', None)
        result["best_answer"] = extract.extract_text(node, './/*[@accuse="aContent"]', None)
        # 追问
        qRAs = node.xpath('.//div[@accuse="qRA"]')
        j = 0
        for qRA in qRAs:
            j += 1
            result["best_answer_qra_"+str(j)] = qRA.text_content() 
        # 对追问的回答
        aRAs = node.xpath('.//div[@accuse="aRA"]')
        j = 0
        for aRA in aRAs:
            j += 1
            result["best_answer_ara_"+str(j)] = aRA.text_content() 
        # 赞数 踩数
        agree_num = node.xpath('.//*[contains(@id,"evaluate-")]')
        if agree_num:
            result["best_answer_agree_num"] = agree_num[0].attrib.get("data-evaluate")
        oppose_num = node.xpath('.//*[contains(@id,"evaluate-bad-")]')
        if oppose_num:
            result["best_answer_oppose_num"] = oppose_num[0].attrib.get("data-evaluate") 
        # TODO: 评论数
        #result["best_answer_comment_num"] = extract.extract_text(node, './/*[@class="comment f-blue"]', None)
        
        # 回答者名称 回答者主页 回答者等级 回答者采纳率 回答者擅长分类
        best_replyer = node.xpath('.//div[contains(@class,"wgt-replyer-best")]/div[2]')
        if best_replyer:
            #print "best_replyer", etree.tostring(best_replyer[0])
            best_replyer_str = re.sub("\r|\n","",etree.tostring(best_replyer[0]))
            replyer_info = best_replyer[0].xpath('.//*[@class="user-name"]')
            if replyer_info:
                result["best_replyer"] = replyer_info[0].text_content()
                result["best_replyer_homepage"] = replyer_info[0].attrib.get("href")
                
                level_str = re.split("\|</span>", best_replyer_str, 0)
                if len(level_str) > 1:
                    level_info = level_pattern.findall(level_str[-1])
                    if level_info:
                        result["best_replyer_level"] = decode_unicode_references(level_info[0])

                result["best_replyer_adoption_rate"] = extract.extract_text(best_replyer[0], './/*[@class="ml-10"]', re.compile(u"(\d+%)"))
                expert_classes = best_replyer[0].xpath('.//*[contains(@class,"mr-5 f-")]')
                j = 0
                for expert_class in expert_classes:
                    j += 1
                    result["best_replyer_expert_class_"+str(j)] = expert_class.text_content()
        

    # 其他答案：回答时间 答案正文 赞数 踩数 评论数 回答者名称 回答者主页 回答者等级
    other_answers = root.xpath('//*[contains(@id,"wgt-answers")]/div[contains(@class,"bd answer")]')
    i = 0
    for node in other_answers:
        #print "other", etree.tostring(node)
        i += 1
        # 回答时间 答案正文
        result["other_answer_time_"+str(i)] = extract.extract_text(node, './/span[contains(@class,"grid-r")]', None)
        result["other_answer_"+str(i)] = extract.extract_text(node, './/*[@accuse="aContent"]', None)
        # 追问
        qRAs = node.xpath('.//div[@accuse="qRA"]')
        j = 0
        for qRA in qRAs:
            j += 1
            result["other_answer_qra_"+str(j)] = qRA.text_content() 
        # 对追问的回答
        aRAs = node.xpath('.//div[@accuse="aRA"]')
        j = 0
        for aRA in aRAs:
            j += 1
            result["other_answer_ara_"+str(j)] = aRA.text_content() 
        # 赞数 踩数
        agree_num = node.xpath('.//*[contains(@id,"evaluate-")]')
        if agree_num:
            result["other_answer_agree_num_"+str(i)] = agree_num[0].attrib.get("data-evaluate")
        oppose_num = node.xpath('.//*[contains(@id,"evaluate-bad-")]')
        if oppose_num:
            result["other_answer_oppose_num_"+str(i)] = oppose_num[0].attrib.get("data-evaluate") 
        # TODO: 评论数
        #result["other_answer_comment_num_"+str(i)] = extract.extract_text(node, './/*[@class="comment f-blue"]', None)
        
        # 回答者名称 回答者主页 回答者等级 回答者采纳率 回答者擅长分类

        other_replyer = node.xpath('.//*[@class="user-name"]')
        if other_replyer:
            result["other_replyer_"+str(i)] = other_replyer[0].text_content()
            result["other_replyer_homepage_"+str(i)] = other_replyer[0].attrib.get("href")
            result["other_replyer_level_"+str(i)] = extract.extract_text(node, './/*[contains(@class,"line info f-")]/span[last()]', None)
    return result

def extract_muzhi(url, root, data):

    cat_pattern = re.compile(u"科室：\s*(.*?)\s*</span>")
    result = ordered_dict()
    import extract
    
    result["title"] = extract.extract_text(root, "//*[@class='ask-txt']/span", None)
    q_info = root.xpath('//*[@class="wgt-recommend-info"]')
    if q_info:
        result["q_class"] = extract.extract_text(q_info[0], './/span[@class="classinfo"]',re.compile(u"分类："))
    else:
        q_info = root.xpath('//*[@class="viewer"]')
        if q_info:        
            result["q_time"] = extract.extract_text(q_info[0], '//*[@class="ask-time"]', None)
            q_info_str = re.sub("\r|\n","",etree.tostring(q_info[0]))
            q_info_str = decode_unicode_references(q_info_str)
            cat_info = cat_pattern.findall(q_info_str)
            if cat_info:
                result["q_class"] = cat_info[0]
    result["q_supply"] = extract.extract_text(root, '//*[@class="wgt-patient-info"]', None)

    best_answers = root.xpath('//*[@class="answer answer-first"]') 
    if best_answers:
        node = best_answers[0] 
        #print "best", etree.tostring(node)
        # 回答时间 答案正文
        result["best_answer_time"] = extract.extract_text(node, './/div[@class="grid-r f-aid create-time"]', None)
        result["best_answer"] = extract.extract_text(node, './/*[@class="content content-first "]//div[@class="pgc-rich line q-content"]', None)
        # 追问
        qRAs = node.xpath('.//div[@class="content  content-ask"]')
        i = 0
        for qra in qRAs:
            i += 1
            result["best_answer_qra"+str(i)] = extract.extract_text(qra, './/div[@class="pgc-rich line q-content"]', None)
        # 追问回答
        aRAs = node.xpath('.//div[@class="content  "]')
        i = 0
        for ara in aRAs:
            i += 1
            result["best_answer_ara"+str(i)] = extract.extract_text(ara, './/div[@class="pgc-rich line q-content"]', None)

        # 感谢数 
        agree_num = node.xpath('.//span[contains(@class,"evaluate evaluate-good")]')
        if agree_num:
            result["best_answer_agree_num"] = agree_num[0].attrib.get("data-evaluate")
        # 医生名字 主页 职称 医院
        best_replyer = node.xpath('.//*[@class="answer-owner"]')
        if best_replyer:
            #print "best_replyer", etree.tostring(best_replyer[0])
            replyer_info = best_replyer[0].xpath('.//*[@class="reply"]/a')
            if replyer_info:
                result["best_replyer"] = replyer_info[0].text_content()
                result["best_replyer_homepage"] = replyer_info[0].attrib.get("href")
            result["best_replyer_level"] = extract.extract_text(best_replyer[0], './/span[@class="reply"]/span', None)
            result["best_replyer_hospital"] = extract.extract_text(best_replyer[0], './/span[@class="company"]', re.compile(u"(.*?)\s*投诉"))

    return result

def extract_wenku(url, root, data): 
    result = ordered_dict()
    import extract

    #print url
    date_pattern = re.compile("(\d{4}-\d+-\d+)")
    value_pattern = re.compile(u"(.*?)分，(.*?)人评")
    #print "page", etree.tostring(root)
    # title 有 
    result["title"] = extract.extract_text(root, "//title", re.compile(u"(.*?)_百度文库"))
    # 正文 可能有
    result["doc"] = extract.extract_text(root, '//div[@class="bd doc-reader"]', None)
    # 摘要 有
    result["doc_abstract"] = extract.extract_text(root, '//span[@class="doc-desc-all"]', None)
    # nav 有
    navs = root.xpath('//ul[@alog-group="general.curmbs"]/li')
    result["nav"] = ""
    for nav in navs:
        result["nav"] += nav.text_content() + "|"
    # 评价分数 评价人数 应该没有
    doc_value = root.xpath('//span[contains(@id,"doc-info")]/span[@title]')
    if doc_value:
        doc_value_str = doc_value[0].attrib.get("title")
        doc_value_info = value_pattern.findall(doc_value_str)
        if doc_value_info:
            result["doc_score"] = doc_value_info[0][0]
            result["doc_eval_person_num"] = doc_value_info[0][1]

    # 阅读量 无
    # 下载量 无
    # 用户评论数 无 
    # 上传者名称 可能有 主页 上传时间 是否认证用户
    doc_owner_info = root.xpath('//div[@id="doc-owner-mod"]//p[@class="owner-name"]/a')
    if doc_owner_info:
        result["doc_owner"] = doc_owner_info[0].text_content()
        result["doc_owner_homepage"] = doc_owner_info[0].attrib.get("href")
        vrf_info = doc_owner_info[0].xpath('.//b[contains(@class,"ic-")]')
        if vrf_info:
            result["doc_owner_vrf"] = "YES"
        else:
            result["doc_owner_vrf"] = "NO"
    upload_date = root.xpath('//div[@id="doc-owner-mod"]//p[@class="owner-title"]')
    if upload_date:
        upload_date_str = re.sub("\r|\n","",etree.tostring(upload_date[0]))
        date_info = date_pattern.findall(upload_date_str)
        if date_info:
            result["doc_date"] = date_info[0]
    owner_values = root.xpath('//div[@id="doc-owner-mod"]//table[@class="owner-value"]/tr[@class="num"]/td')
    # 用户总评分数 可能有
    if len(owner_values) == 3:
        result["doc_owner_doc_num"] = owner_values[0].text_content()
        result["doc_owner_view_num"] = owner_values[1].text_content()
        result["doc_owner_eval"] = owner_values[2].text_content()

    # 是否免费 可能有
    price = extract.extract_text(root, '//span[@class="goods-price"]', re.compile(u"(\d+\.*\d*)"))
    download_info = extract.extract_text(root, '//div[@class="btn-download"]/span', re.compile(u"(\d+)"))
    if price:
        if float(price) > 0:
            result["is_free"] = "NO"
            result["goods_price"] = price
        else:
            result["is_free"] = "YES"
    elif download_info:
        if float(download_info) > 0:
            result["is_free"] = "NO"
            result["download_price"] = download_info
        else:
            result["is_free"] = "YES"
    else:
        result["is_free"] = "UNKNOW"

    return result 

def extract_jingyan(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    # 问题 问题分类 浏览量 更新时间 问题描述
    result["title"] = extract.extract_text(root, "//title", re.compile(u"(.*?)_百度经验"))
    result["update_time"] = extract.extract_text(root, '//ul[@class="exp-info"]//time', None) 
    result["view_num"] = extract.extract_text(root, '//ul[@class="exp-info"]//span[@class="views"]', None) 
    result["tag"] = extract.extract_text(root, '//ul[@class="exp-info"]//span[@class="exp-tag"]', None) 
    result["nav"] = extract.extract_text(root, '//div[@id="bread-wrap"]', None)

    # 正文 
    articles = root.xpath('//*[@alog-group="exp-content"]/div[@class="exp-content-block"]')
    i = 0 
    for node in articles:
        #print "paragraph", etree.tostring(node)
        i += 1
        result["paragraph"+str(i)] = node.text_content()

        images = node.xpath('//img[@*]')
        for img in images:
            print img


    # 投票数 有得 疑问 TODO：用户评论数 
    comments = root.xpath('//*[@class="wgt-comments"]')
    if comments:
        result["vote_num"] = extract.extract_text(comments[0], './/div[@class="vote-btn-wrp"]//span[@class="a-t"]', re.compile(u"(\d+)"))
        result["hads_num"] = extract.extract_text(comments[0], './/div[@class="hads-btn-wrp"]//span[@class="a-t"]', re.compile(u"(\d+)"))
        result["ques_num"] = extract.extract_text(comments[0], './/div[@class="ques-btn-wrp"]//span[@class="a-t"]', re.compile(u"(\d+)"))
    else:
        result["vote_num"] = extract.extract_text(root, '//*[@class="useful-button-wp"]//span[@class="a-h"]', re.compile(u"(\d+)"))
        result["collect_num"] = extract.extract_text(root, '//*[@class="collect-button-wp"]//span[@class="a-h"]', re.compile(u"(\d+)"))

    # 用户名 主页
    user = root.xpath('//*[@class="author-info left"]/h2/a')
    if user:
        #print "user", etree.tostring(user[0])
        result["user_name"] = user[0].text_content()
        #result["user_homepage"] = "http://jingyan.baidu.com/" + user[0].attrib.get("href")
        result["user_homepage"] = user[0].attrib.get("href")

    return result 

def extract_docin_p(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    num_pattern = re.compile(u"(\d+)")
    # title 有 
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)\s*-\s*豆丁网"))
    # nav 有
    navs = root.xpath('//ul[@class="crubms"]/li')
    result["nav"] = ""
    for nav in navs:
        result["nav"] += nav.text_content() + "|"
    # 赞数 踩数 浏览量 收藏量 评论数 
    result["agree_num"] = extract.extract_text(root, u'//div[@class="doc_active_info"]/a[@title="顶"]/span[2]', None)
    result["oppose_num"] = extract.extract_text(root, u'//div[@class="doc_active_info"]/a[@title="踩"]/span[2]', None)
    result["view_num"] = extract.extract_text(root, u'//div[@class="doc_active_info"]/a[@title="浏览"]/em', None)
    result["collect_num"] = extract.extract_text(root, '//div[@class="doc_active_info"]/a[contains(@onclick,"clickBookSave")]/em', None)
    result["comment_num"] = extract.extract_text(root, u'//div[@class="doc_active_info"]/a[@title="评论"]/em', None)
    # 上传者名称 主页 上传时间 是否认证用户
    doc_owner_info = root.xpath('//p[@class="user_name"]/a[1]')
    if doc_owner_info:
        result["doc_owner"] = doc_owner_info[0].attrib.get("title")
        result["doc_owner_homepage"] = doc_owner_info[0].attrib.get("href")
    vrf_info = root.xpath(u'//p[@class="user_name"]/a[@title="认证用户"]')
    if vrf_info:
        result["doc_owner_vrf"] = "YES"
    result["doc_owner_vrf"] = "NO"
    result["share_time"] = extract.extract_text(root,'//p[@class="share_time"]/span',None)
    # 文档描述 
    result["doc_desc"] = extract.extract_text(root, '//p[@class="doc_desc"]', None)

    # 文档文档热度 
    doc_viewhot = root.xpath('//div[@class="doc_info"]//span[contains(@class,"viewhot")]')
    if doc_viewhot:
        doc_viewhot_str = doc_viewhot[0].attrib.get("class")
        doc_viewhot_info = num_pattern.findall(doc_viewhot_str)
        if doc_viewhot_info:
            result["doc_viewhot"] = doc_viewhot_info[0]

    # 文档分类 文档标签
    doc_tags = root.xpath('//div[@class="doc_info"]//a')
    result["doc_tags"] = ""
    for tag in doc_tags:
        result["doc_tags"] += tag.text_content() + "|"
    
    # 正文 好像没 
    result["doc"] = extract.extract_text(root, '//div[contains(@class,"doc_reader")]', None)

    # TODO 是否免费？
    return result 

def extract_docin_zuowen(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    # title 有 
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)\s*-*\s*作文频道"))
    # nav 有
    navs = root.xpath('//div[@class="end_crumb"]/a')
    result["nav"] = ""
    for nav in navs:
        result["nav"] += nav.text_content() + "|"
    # 赞数 踩数  
    result["agree_num"] = extract.extract_text(root, u'//div[@class="like_right"]/a[@title="顶"]/span[2]', None)
    result["oppose_num"] = extract.extract_text(root, u'//div[@class="like_right"]/a[@title="踩"]/span[2]', None)
    
    # 正文  
    result["doc"] = extract.extract_text(root, '//div[@class="txt clear"]', None)
    
    return result 

def extract_docin_meeting(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    num_pattern = re.compile(u"(\d+)\s*\|.*?(\d+)")
    person_time_pattern = re.compile(u"<dd>\s*(.*?)\s*·*\s*<span.*?>\s*(\d{4}-\d+-\d+\s+\d+:\d+)")
    meeting_pattern = re.compile(u"所属会议:.*?<a.*?>\s*(.*?)\s*</a>")
    address_pattern = re.compile(u"会议地点:.*?</span>\s*(.*?)\s*</dd>")
    # title 有 
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)\s*-*\s*豆丁网"))
    # nav 有
    result["nav"] = extract.extract_text(root, '//div[contains(@class,"crubms")]', None)
    # 浏览量 收藏量  
    doc_data = extract.extract_text( root, '//div[contains(@class,"doc_data_detail")]', None)
    if doc_data != None:
        doc_data_str = re.sub("\r|\n","",doc_data)
        num_info = num_pattern.findall(doc_data_str)
        if num_info:
            result["view_num"] = num_info[0][0]
            result["collect_num"] = num_info[0][1]
    # TODO:评论数 没有
    #result["comment_num"] = extract.extract_text(root, '//div[@class="doc_active_info"]/a[@title="评论"]/em', None)
    doc_detail = root.xpath('//*[@class="detail_section"]')
    if doc_detail:
        doc_detail_str = re.sub("\n|\r","",etree.tostring(doc_detail[0]))
        doc_detail_str = decode_unicode_references(doc_detail_str)
        person_time_info = person_time_pattern.findall(doc_detail_str)
        if person_time_info:
            result["doc_owner"] = person_time_info[0][0]
            result["doc_time"] = person_time_info[0][1]
        meeting_info = meeting_pattern.findall(doc_detail_str)
        if meeting_info:
            result["meeting_name"] = meeting_info[0]
        address_info = address_pattern.findall(doc_detail_str)
        if address_info:
            result["meeting_address"] = address_info[0]
    # 正文 只有链接
    doc_viewer = root.xpath('//div[@class="docin_player"]//embed')
    if doc_viewer:
        result["doc_src"] = doc_viewer[0].attrib.get("src")

    return result 

def extract_baby_ask(url, root, data):

    #print url
    #print "page", etree.tostring(root)
    #num_pattern = re.compile(u"最佳回答数：\s*<a.*?>\s*(\d+)\s*</a>.*?已帮助：\s*(\d+)")
    num_pattern = re.compile("&#26368;&#20339;&#22238;&#31572;&#25968;&#65306;&lt;a.*?&gt;(\d+)&lt;/a&gt;.*?&#24050;&#24110;&#21161;&#65306;(\d+)")
    result = ordered_dict()
    import extract
    # 问题 导航 浏览量 提问时间 问题描述 浏览量 关键词
    #result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)\s_育儿问答_宝宝树"))
    result["title"] = extract.extract_text(root, '//*[@itemprop="title"]', None)
    result["q_desc"] = extract.extract_text(root, '//*[@class="qa-text"]', None)
    result["q_time"] = extract.extract_text(root, '//*[@class="qa-contributor"]//*[@itemprop="post_time"]', None)
    result["q_class"] = extract.extract_text(root, '//*[@itemprop="breadcrumb"]', None)
    result["q_status"] = extract.extract_text(root, '//li[@itemprop="status"]', None)
    result["view_num"] = extract.extract_text(root, '//span[@itemprop="view_count"]', None)
    result["keywords"] = extract.extract_text(root, '//span[@itemprop="keywords"]', None) 

    # 最佳答案：回答时间 答案正文 有用 回答者名称 回答者主页 最佳回答数 已帮助人数
    best_answers = root.xpath('//*[@id="qa-answer-best"]')
    if best_answers:
        node = best_answers[0] 
        #print "best", etree.tostring(node)
        # 回答时间 答案正文
        result["best_answer_time"] = extract.extract_text(node, './/span[@itemprop="reply_time"]', None)
        result["best_answer"] = extract.extract_text(node, './/div[@id="best_answer_content"]', None)
        # 追问
        additionals = node.xpath('.//ul[@class="answer-comments"]/li')
        i = 0
        j = 0
        for add in additionals:
            strs = add.text_content().strip()
            if strs.find(u"追问：") >= 0:
                i += 1
                result["best_answer_qra_"+str(i)] = strs[3:]
            elif strs.find(u"回答：") >= 0:
                j += 1
                result["best_answer_ara_"+str(j)] = strs[3:]
        # 追问回答
        # 赞数 
        result["agree_num"] = extract.extract_text(node, './/div[@class="qa-vote"]//em', None)
        best_replyer = node.xpath('.//*[@itemprop="replier"]')
        if best_replyer:
            #print "best_replyer", etree.tostring(best_replyer[0])
            replyer_link = best_replyer[0].xpath('.//a[@itemprop="link"]')
            if replyer_link:
                result["best_replyer_homepage"] = replyer_link[0].attrib.get("href")
            result["best_replyer"] = extract.extract_text(best_replyer[0], './/*[@itemprop="accountName"]', None)
            
            best_replyer_str = re.sub("\r|\n","",etree.tostring(best_replyer[0]))
            #best_replyer_str = decode_unicode_references(best_replyer_str)
            num_info = num_pattern.findall(best_replyer_str)
            if num_info:
                result["best_replyer_answer_num"] = num_info[0][0]
                result["best_replyer_help_num"] = num_info[0][1]

    # 其他答案：回答时间 答案正文 有用 追问 追问答案
    other_answers = root.xpath('//ul[@class="qa-answer-list"]/li[@class="answer-item"]')
    i = 0
    for node in other_answers:
        i += 1
        #print "other", etree.tostring(node)
        # 回答时间 答案正文
        result["other_answer_time_"+str(i)] = extract.extract_text(node, './/span[@itemprop="reply_time"]', None)
        result["other_answer_"+str(i)] = extract.extract_text(node, './/div[@itemprop="content"]', None)
        # 追问
        additionals = node.xpath('.//ul[@class="answer-comments"]/li')
        m = 0
        n = 0
        for add in additionals:
            strs = add.text_content().strip()
            if strs.find(u"追问：") >= 0:
                m += 1
                result["other_answer_qra_"+str(i)+"_"+str(m)] = strs[3:]
            elif strs.find(u"回答：") >= 0:
                n += 1
                result["other_answer_ara_"+str(i)+"_"+str(n)] = strs[3:]
        # 追问回答
        # 赞数 
        result["agree_num"] = extract.extract_text(node, './/a[@class="qa-answer-list-vote"]//em', None)
        other_replyer = node.xpath('.//*[@itemprop="replier"]')
        if other_replyer:
            #print "other_replyer", etree.tostring(other_replyer[0])
            replyer_link = other_replyer[0].xpath('.//a[@itemprop="link"]')
            if replyer_link:
                result["other_replyer_homepage_"+str(i)] = replyer_link[0].attrib.get("href")
            result["other_replyer_"+str(i)] = extract.extract_text(other_replyer[0], './/*[@itemprop="accountName"]', None)
            
    return result

def extract_baby_learn(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    time_num_pattern = re.compile(u"(\d{4}-\d+-\d+\s+\d+:\d+).*?浏览\s*(\d+).*?评论.*?<a.*?>\s*(\d+)\s*<")
    # title 有 
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)\s*_育儿文章_宝宝树"))
    doc_info = root.xpath("//h6")
    if doc_info:
        doc_info_str = re.sub("\r|\n","",etree.tostring(doc_info[0]))
        doc_info_str = decode_unicode_references(doc_info_str)
        time_num_info = time_num_pattern.findall(doc_info_str)
        if time_num_info:
            result["time"] = time_num_info[0][0]
            result["view_num"] = time_num_info[0][1]
            result["comment_num"] = time_num_info[0][2]

    # nav 有
    navs = root.xpath('//*[@class="bui-breadcrumb"]/a[not(@class)]')
    result["nav"] = ""
    for nav in navs:
        result["nav"] += nav.text_content() + "|"
    
    # 正文  
    result["doc"] = extract.extract_text(root, '//div[@class="article"]', None)
    
    return result 

def extract_baby_know(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    # title 有 
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)\s*_孕育周刊_宝宝树"))
    keywords = root.xpath('//meta[@name="keywords"]')
    if keywords:
        result["keywords"] = keywords[0].attrib.get("content")
    desc = root.xpath('//meta[@name="description"]')
    if desc:
        result["desc"] = desc[0].attrib.get("content")
    # nav 有
    result["nav"] = extract.extract_text(root, '//*[@class="weeklyPeriodNav"]/li[@class="current"]', None)
    
    # 正文  
    paragraphs = root.xpath('//td[@bgcolor]/div[3]/table')
    i = 0
    for node in paragraphs:
        i += 1
        if i == 1:
            result["doc"] = node.text_content()
        else:
            result["doc"] += node.text_content()
    return result 

def extract_haodf_wenda(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    # 标题
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)_好大夫在线"))
    cons_info = root.xpath('//*[@class="h_s_info_cons"]')
    if cons_info:
        result["cons_title"] = extract.extract_text( cons_info[0], './/*[@class="h_s_cons_info_title"]', None)
        result["ill_desc"] = extract.extract_text( cons_info[0], './div', None)
        result["ill_name"] = extract.extract_text( cons_info[0], './h2', None)
        ps = cons_info[0].xpath('./p')
        # 疾病 希望提供的帮助 所就诊医院科室
        for p in ps:
            strs = p.text_content()
            if strs.find(u"希望提供的帮助：") >= 0:
                result["want_help"] = strs
            elif strs.find(u"所就诊医院科室：") >= 0:
                result["hospital"] = strs
            else:
                result["ill_supply"] = strs
        result["ask_time"] = extract.extract_text( root, '//*[@class="h_s_cons_info"]/following-sibling::*[@class="h_s_time"]', re.compile(u"发表于\s*(\d{4}-\d+-\d+\s+\d+:\d+:\d+)"))

    # 问或答 状态 时间 正文
    qRAs = root.xpath('//*[@class="h_s_cons"]')
    i = 0
    for qra in qRAs:
        i += 1
        result["qra"+str(i)] = qra.text_content() 
        result["qra_time_"+str(i)] = extract.extract_text(qra, './following-sibling::*[@class="h_s_time"]', re.compile(u"(\d{4}-\d+-\d+\s+\d+:\d+:\d+)") )
            
        result["qra_state"+str(i)] = extract.extract_text(qra, './ancestor::*[@class="zzx_yh_stream"]//*[@class="yh_l_states"]/span', None)
    
    aRAs = root.xpath('//*[@class="h_s_cons_docs"]')
    i = 0
    for ara in aRAs:
        i += 1
        result["ara"+str(i)] = ara.text_content()
        result["ara_time_"+str(i)] = extract.extract_text(ara, './following-sibling::*[@class="h_s_time"]', re.compile(u"(\d{4}-\d+-\d+\s+\d+:\d+:\d+)") )
    
    num_pattern = re.compile("(\d+)")
    
    doc_name_title = root.xpath('//*[contains(@class,"doc_name")]')
    name_title_pattern = re.compile(u"(.*?)\s+(.*)")
    if doc_name_title:
        strs = re.sub("\r|\n","",doc_name_title[0].text_content().strip())
        strs = re.sub("\s+"," ",strs)
        info = name_title_pattern.findall(strs)
        if info:
            result["doc_name"] = info[0][0]
            result["doc_title"] = info[0][1]
    url_info = root.xpath('//a[@class="space_b_link_url"]')
    if url_info:
        result["doc_url"] = url_info[0].attrib.get("href")
    doctor_info = root.xpath('//*[contains(@class,"mr_line1 ")]')
    #doctor_info = root.xpath('//*[@class="mr_line1 mb20"]')
    if doctor_info:
        # 姓名 爱心值 感谢信 礼物 贡献值
        doc_hearts = doctor_info[0].xpath(u'.//a[contains(@title,"爱心值:")]')
        if doc_hearts:
            hearts_str = doc_hearts[0].attrib.get("title")
            hearts_info = num_pattern.findall(hearts_str)
            if hearts_info:
                result["doc_hearts"] = hearts_info[0]
        relative_info = doctor_info[0].xpath('.//ul[contains(@class,"doc_info_ul")]//span')
        for info in relative_info:
            strs = re.sub("\r|\n","",info.text_content())
            num_info = num_pattern.findall(strs)
            if not num_info:
                continue
            if strs.find(u"感谢信：") >= 0:
                result["doc_thank_letters"] = num_info[0] 
            elif strs.find(u"礼物：") >= 0:
                result["doc_gifts"] = num_info[0]
            elif strs.find(u"贡献值:") >= 0:
                result["doc_contrib"] = num_info[0]
        # 科室 擅长 简介
        other_info = doctor_info[0].xpath('./div[1]/div')
        for info in other_info:
            strs = re.sub("\r|\n","",info.text_content())
            if strs.find(u"科室：") >= 0:
                result["doc_hospital"] = strs
            elif strs.find(u"擅长：") >= 0:
                result["doc_expert_class"] = strs
            elif strs.find(u"简介：") >= 0:
                result["doc_desc"] = strs
    return result

def extract_haodf_zhuanjiaguandian(url, root, data):
    #print url
    #print "page", etree.tostring(root)
    result = ordered_dict()
    import extract
    # 标题
    result["title"] = extract.extract_text(root, '//title', re.compile(u"(.*?)_好大夫在线"))
    result["category"] = extract.extract_text(root, '//p[@class="art_detail_cate"]', None)

    time_pattern = re.compile(u"(\d{4}-\d+-\d+\s+\d+:\d+:\d+)")
    update_info = root.xpath('//div[@class="pb20"]')
    if update_info:
        update_info_str = update_info[0].text_content()
        time_info = time_pattern.findall(update_info_str)
        if time_info:
            result["time"] = time_info[0]
    
    doc_name_title = root.xpath('//*[contains(@class,"doc_name")]')
    name_title_pattern = re.compile(u"(.*?)\s+(.*)")
    if doc_name_title:
        strs = re.sub("\r|\n","",doc_name_title[0].text_content().strip())
        strs = re.sub("\s+"," ",strs)
        info = name_title_pattern.findall(strs)
        if info:
            result["doc_name"] = info[0][0]
            result["doc_title"] = info[0][1]
    url_info = root.xpath('//a[@class="space_b_link_url"]')
    if url_info:
        result["doc_url"] = url_info[0].attrib.get("href")
    
    num_pattern = re.compile("(\d+)")
    doctor_info = root.xpath('//*[contains(@class,"mr_line1 ")]')
    if doctor_info:
        # 姓名 爱心值 感谢信 礼物 贡献值
        doc_hearts = doctor_info[0].xpath(u'.//a[contains(@title,"爱心值:")]')
        if doc_hearts:
            hearts_str = doc_hearts[0].attrib.get("title")
            hearts_info = num_pattern.findall(hearts_str)
            if hearts_info:
                result["doc_hearts"] = hearts_info[0]
        relative_info = doctor_info[0].xpath('.//ul[contains(@class,"doc_info_ul")]//span')
        for info in relative_info:
            strs = re.sub("\r|\n","",info.text_content())
            num_info = num_pattern.findall(strs)
            if not num_info:
                continue
            if strs.find(u"感谢信：") >= 0:
                result["doc_thank_letters"] = num_info[0] 
            elif strs.find(u"礼物：") >= 0:
                result["doc_gifts"] = num_info[0]
            elif strs.find(u"贡献值:") >= 0:
                result["doc_contrib"] = num_info[0]
        # 科室 擅长 简介
        other_info = doctor_info[0].xpath('./div[1]/div')
        for info in other_info:
            strs = re.sub("\r|\n","",info.text_content())
            if strs.find(u"科室：") >= 0:
                result["doc_hospital"] = strs
            elif strs.find(u"擅长：") >= 0:
                result["doc_expert_class"] = strs
            elif strs.find(u"简介：") >= 0:
                result["doc_desc"] = strs
    
    result["article"] = extract.extract_text( root, '//*[@class="pb20 article_detail"]', None)
    comments = root.xpath('//ul[@class="clearfix pt20 pb20 bbd_e9"]/li')
    result["comment_num"] = len(comments)
    i = 0
    for comment in comments:
        i += 1
        result["comment"+str(i)] = extract.extract_text(comment, './/div[@class="oh zoom"]/p[@class="pb10"]', None)
    return result


def output(url, data):
    for k, v in data.iteritems():
        s = "%s\t%s\t%s" %(url, k, v)
        s = s.replace("\r\n", "<br>")
        s = s.replace("\n", "<br>")
        print s.encode("utf8")

url = None
orig_size = 0
store_size = 0
data = "" 
http_start = False
data_start = False
line_no = 0
for line in sys.stdin:
    #line_no += 1
    #if line_no % 1000000 == 0:
        #print "line_no", line_no
    #if line_no < 140000000:
        #continue
    if line.startswith(("http://", "https://")):     # url
        #if url != None:
        if url != None and url.startswith(("http://zhidao.baidu.com/question/",\
            "http://baike.baidu.com/view", "http://baike.baidu.com/subview",\
            "http://club.xywy.com/static",\
            "http://wenku.baidu.com/view/",\
            "http://jingyan.baidu.com/article/",\
            "http://www.docin.com/zuowen/view.do?id=",\
            "http://www.babytree.com/ask/detail/",\
            "http://www.babytree.com/learn/article/",\
            "http://www.babytree.com/know/weekly.php?type=",\
            "http://www.haodf.com/wenda/",\
            "http://www.docin.com/p-",\
            "http://www.haodf.com/zhuanjiaguandian/")):
            # parse
            #print "url1\t", url
            data = data[:-1]
            data = decompress(data)
            #print >>sys.stderr, url
            #print >>sys.stderr, data
            result = extract(url, data)
            output(url, result)
        data = ""
        http_start = False
        data_start = False
        store_size = 0
        orig_size = 0
        url = line.strip()
        continue

    if line.startswith("Original-Size:"):
        orig_size = int(line[14:].strip())
        continue
    if line.startswith("Store-Size:"):
        store_size = int(line[11:].strip())
        continue

    if line.startswith(("HTTP/1.", "Date:")):
        http_start = True
        continue
    if not data_start and http_start and line == "\n":
        data_start = True
        data = ""
        continue

    #print http_start, data_start, (len(data) if data != None  else data), len(line)
    #print "----",line
    if data_start:
        data += line

# parse the last one
if url != None:
    data = decompress(data)
    result = extract(url, data)
    output(url, result)
