#coding=utf-8
import sys
import codecs
import requests
from lxml import etree


def process_relation(rid, out) :
    """
    prosss relation
    """
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
        nodes_dict[id] = '%s,%s' % (lon, lat)
    
    ways_dict = {}
    ways_id = []
    #seq_nodes = []
    for way in ways :
        nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        nds = sel.xpath(nd_rels)
        ways_dict[way] = nds
        ways_id.append(way)
    ok = True
    for i in range(1,len(ways_id),1) :
        sub = ways_id[i:]
        end_node_id = ways_dict[ways_id[i-1]][-1]
        # if end_node_id == '3981863987' :
        #     print("")
        
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
        #print('%s->%s:%s' % (ways_dict[ways_id[i-1]][-1],ways_dict[ways_id[i]][0],ways_dict[ways_id[i-1]][-1]==ways_dict[ways_id[i]][0]))
    if not ok :
        print("Relation %s uncomplete." % (rid,))
    
    for way in ways_id :
        #print("way->(%s/%s)" % (way,len(ways)))
        #nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        #nds = sel.xpath(nd_rels)
        nds = ways_dict[way]
        i = 0
        for nd in nds :
            #print("node->(%s/%s)" % (nd,len(nds)))
            #path.append(nodes_dict[nd])
            out.write('%s,%s,%s,%s\n' % (i,way, nd, nodes_dict[nd]))
            i += 1
    #return ','.join(path)

def main(rid):
    #f = codecs.open('rel.txt','r','utf-8')
    out = codecs.open(rid + '.csv','w','utf-8')
    #path = 
    process_relation(rid, out)
    #out.write('%s;%s\n' % (line, path))
    out.close()
    
if __name__ == '__main__':
    main(sys.argv[1])