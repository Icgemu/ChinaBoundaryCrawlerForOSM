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
    
    ways_dict = {}
    ways_id = []
    #seq_nodes = []
    for way in ways :
        nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        nds = sel.xpath(nd_rels)
        ways_dict[way] = nds
        ways_id.append(way)
    
    for i in range(1,len(ways_id),1) :
        sub = ways_id[i:]
        end_node_id = ways_dict[ways_id[i-1]][-1]
        for k,v in enumerate(sub):
            if ways_dict[v][0] == end_node_id:
                tmp = ways_id[i]
                ways_id[i] = v
                ways_id[i+k] = tmp
            if ways_dict[v][-1] == end_node_id:
                tmp = ways_id[i]
                ways_id[i] = v
                ways_id[i+k] = tmp
                ways_dict[v].reverse()
    
    for way in ways_id :
        print("way->(%s/%s)" % (way,len(ways_id)))
        #nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        #nds = sel.xpath(nd_rels)
        nds = ways_dict[way]
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