#coding=utf-8
import sys
import codecs
import requests
from lxml import etree
import math

def distance(a,b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return math.sqrt(x*x + y*y)

def find_shortest_distance(a, b_list):
    s = a.split(',')
    v = (float(s[0]),float(s[1]))
    c_list = []
    for n in b_list:
        s = n[0].split(',')
        s_v = (float(s[0]),float(s[1]))
        c_list.append((s_v,n[1],n[2],n[3]))
    dist_list = []
    for n in c_list:
        dist = distance(v , n[0])
        dist_list.append((dist, n[1], n[2],n[3]))
    
    def cmp_fn(x):
        return x[0]
    dist_list.sort(key = cmp_fn)
    return dist_list[0]
    
def process_relation(rid, out) :
    """
    prosss relation
    """
    sel = etree.parse('boundary/'+rid+'.xml')
    #path = []
    ways_rel = '//relation[@id="'+ rid +'"]/member[@type="way"][@role="outer"]/@ref'
    ways = sel.xpath(ways_rel)
    #path = []
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
    
    for i in range(1,len(ways_id),1) :
        sub = ways_id[i:]
        end_node_id = ways_dict[ways_id[i-1]][-1]
        target_node_id = ways_dict[ways_id[0]][0]
        if end_node_id == target_node_id:
            ways_id = ways_id[0:i]
            break
        # if end_node_id == '3981863987' :
        #     print("")
        ok = False
        for k,v in enumerate(sub):
            if ways_dict[v][0] == end_node_id:
                tmp = ways_id[i]
                ways_id[i] = v
                ways_id[i+k] = tmp
                ok =True
            if ways_dict[v][-1] == end_node_id:
                tmp = ways_id[i]
                ways_id[i] = v
                ways_id[i+k] = tmp
                ways_dict[v].reverse()
                ok =True
        if not ok:
            # topoogy lost ,use shortest distance by way start/end
            dist_list = []
            for k,v in enumerate(sub):
                beg = ways_dict[v][0]
                end = ways_dict[v][-1]
                dist_list.append(((nodes_dict[beg]),0,v,k))
                dist_list.append(((nodes_dict[end]),1,v,k))
            shortest_way = find_shortest_distance(nodes_dict[end_node_id], dist_list)
            k = shortest_way[3]
            v = shortest_way[2]
            tmp = ways_id[i]
            ways_id[i] = v
            ways_id[i+k] = tmp
            if shortest_way[1] == 1:
                 ways_dict[v].reverse()

        print('%s->%s:%s' % (ways_dict[ways_id[i-1]][-1],ways_dict[ways_id[i]][0],ways_dict[ways_id[i-1]][-1]==ways_dict[ways_id[i]][0]))
    
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