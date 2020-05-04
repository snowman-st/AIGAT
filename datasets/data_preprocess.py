#-*- coding: utf-8 -*-
'''
	将XML格式的原始数据转换成 pytorch-ABSA中需要的数据格式：

	Nevertheless the $T$ itself is pretty good .
	food
	1
    term1_T_term2
'''
import re
from xml.etree.ElementTree import parse

def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9(),.;\-:!?$\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'m", " am ", string)
    string = re.sub(r"\'ve", " have ", string)
    string = re.sub(r"n\'t", " not", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " will", string)
    # string = re.sub(r"\' "," \' ",string)
    string = re.sub(r"\,", " , ", string)
    string = re.sub(r"\!", " ! ", string)
    string = re.sub(r"\;"," ; ",string)
    string = re.sub(r"\:"," : ",string)
    string = re.sub(r"\\"," ",string)
    string = re.sub(r"\.", " . ", string)
    string = re.sub(r"\(", " ( ", string)
    string = re.sub(r"\)", " ) ", string)
    string = re.sub(r"\?", " ? ", string)
    string = re.sub(r"\n"," ",string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()

def parse_sentence_term(basepath, outpath,lowercase=False):
    path = basepath
    tree = parse(path)
    sentences = tree.getroot()
    data = []
    term_slot = '$T$'
    term_seg = '_T_'
    polarity_seg = '_P_'
    d = {
        'positive': 1,
        'negative': 2,
        'neutral': 0,
    }
    f = open(outpath,'w+',encoding='utf-8')
    sentences_count = 0
    for sentence in sentences:
        text = sentence.find('text')
        if text is None:
            continue
        text = text.text
        if lowercase:
            text = text.lower()
        aspectTerms = sentence.find('aspectTerms')
        if aspectTerms is None:
            continue
        aspects = []
        polarities = []
        slot_texts = []
        for aspectTerm in aspectTerms:
            term = aspectTerm.get('term')
            if lowercase:
                term = term.lower()
            polarity = aspectTerm.get('polarity')
            try:
                d[polarity]
            except:
                continue
            start = aspectTerm.get('from')
            end = aspectTerm.get('to')
            try:
                sloted_text = re.sub(term,term_slot,text)
            except:
                sloter_text = text[:int(start)] + ' ' + term_slot + ' ' + text[int(end):]
            aspects.append(clean_str(term))
            polarities.append(d[polarity])
            slot_texts.append(sloted_text)
        if len(aspects)==0:
            continue
        sentences_count += 1
        for i in range(len(aspects)):
            f.write(clean_str(slot_texts[i])+'\n')
            f.write(aspects[i]+'\n')
            f.write(str(polarities[i])+'\n')
            f.write(term_seg.join(aspects)+'\n')
            f.write(polarity_seg.join([str(p) for p in polarities])+'\n')
    print('there are {} sentences.'.format(sentences_count))
    f.close()

if __name__ == '__main__':
    parse_sentence_term("/home1/xk/document/datasets/SemEval-ABSA/ABSA-SemEval2014/Restaurants_Train.xml","semeval14/restaurant_train.raw")
    parse_sentence_term("/home1/xk/document/datasets/SemEval-ABSA/ABSA-SemEval2014/Restaurants_Test_Gold.xml","semeval14/restaurant_test.raw")
