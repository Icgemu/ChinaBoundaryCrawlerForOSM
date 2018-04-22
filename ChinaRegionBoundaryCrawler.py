#coding=utf-8
import codecs
import requests
from lxml import etree

def getRelationValue (selector, rid, name, alt_name):
    val = selector.xpath('//relation[@id="'+ rid +'"]/tag[@k="'+name+'"]/@v')
    if len(val) == 0 :
        val = selector.xpath('//relation[@id="'+ rid +'"]/tag[@k="'+alt_name+'"]/@v')
        if len(val) == 0 :
            val = ""
        else :
            val = val[0]
    else :
        val = val[0]
    return val

def getRelation (pid, rid, out) :
    """
    pid:  parent relation id for this relation
    rid:  crawl relation
    """

    full_url = 'https://api.openstreetmap.org/api/0.6/relation/'+rid+'/full'
    
    xml = requests.get(full_url)
    # save this XML to local file.
    file = codecs.open('boundary/'+rid + '.xml','w','utf-8')
    file.write(xml.text)
    file.close()
    # parse this xml by lxml
    sel = etree.fromstring(xml.content)
    # get the meta data for this relation id    
    en = getRelationValue(sel, rid, 'name:en', 'alt_name:en')
    zh  = getRelationValue(sel, rid, 'name:zh', 'name')
   
    admin_lvl = sel.xpath('//relation[@id="'+ rid +'"]/tag[@k="admin_level"]/@v')

    if len(admin_lvl) >0 :        
        out.write('%s;%s;%s;%s;%s\n' % (pid, rid, en, zh, admin_lvl[0],))
        
        sub_area_rid_path = '//relation[@id="'+ rid  +'"]/member[@type="relation"]/@ref'
        members = sel.xpath(sub_area_rid_path)
        for member in members :
            ref = member
            getRelation(rid, ref, out)


def main() :
    url = 'https://wiki.openstreetmap.org/wiki/WikiProject_China'
    html = requests.get(url).content
    selector = etree.HTML(html)
    trs = selector.xpath('//table[@class="wikitable"][1]/tr')
    out = codecs.open('rel.txt','w','utf-8')
    for tr in trs :
        t = tr[0]
        if (t.tag == 'td') : # filter table head `th`` tag
            rid = tr[2][0].text
            getRelation("0",rid, out)
    out.close()

if __name__ == '__main__':
    main()
