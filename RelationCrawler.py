#coding=utf-8
import codecs
import requests
from lxml import etree


def process_relation(rid) :
    
    sel = etree.parse('boundary/'+rid+'.xml')
    path = []
    ways_rel = '//relation[@id="'+ rid +'"]/member[@type="way"][@role="outer"]/@ref'
    ways = sel.xpath(ways_rel)
    path = []
    nodes_rel = '//node'
    nodes = sel.xpath(nodes_rel)
    nodes_dict = {}
    for node in nodes :
        id = node.get('id')
        lon = node.get('lon')
        lat = node.get('lat')
        nodes_dict[id] = '%s %s' % (lon, lat)
    for way in ways :
        print("way->(%s/%s)" % (way,len(ways)))
        nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        nds = sel.xpath(nd_rels)
        for nd in nds :
            #print("node->(%s/%s)" % (nd,len(nds)))
            path.append(nodes_dict[nd])
    return ','.join(path)

def main():
    f = codecs.open('rel.txt','r','utf-8')
    out = codecs.open('rel_path_added.txt','w','utf-8')
    for line in f.readlines() :
        line = line.replace("\n", "")
        infs = line.split(';')  
        rid = infs[1]
        path = process_relation(rid)
        out.write('%s;%s\n' % (line, path))
    out.close()
    f.close()
    
if __name__ == '__main__':
    main()