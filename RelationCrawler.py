#coding=utf-8
import codecs
import requests
from lxml import etree
import math
import random

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
def process_relation(rid) :
    
    sel = etree.parse('boundary/'+rid+'.xml')
    #path = []
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
        if nds[0] != nds[-1]:
            ways_dict[way] = nds
            ways_id.append(way)
    
    # random.shuffle(ways_id)
    for i in range(1,len(ways_id),1) :
        sub = ways_id[i:]
        end_node_id = ways_dict[ways_id[i-1]][-1]
        target_node_id = ways_dict[ways_id[0]][0]
        if end_node_id == target_node_id:
            #print("target break")
            old_len = len(ways_id)
            ways_id = ways_id[0:i]
            new_len = len(ways_id)
            # rate = float(new_len)/old_len
            # if rate < 0.2:
            #     print(rid +','+ str(rate))
            #     return process_relation(rid)
            print('%s->%s/%s' % (rid,new_len,old_len))
            break
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

        #print('%s->%s:%s' % (ways_dict[ways_id[i-1]][-1],ways_dict[ways_id[i]][0],ways_dict[ways_id[i-1]][-1]==ways_dict[ways_id[i]][0]))
    
    for way in ways_id :
        #print("way->(%s/%s)" % (way,len(ways_id)))
        #nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        #nds = sel.xpath(nd_rels)
        nds = ways_dict[way]
        
        for nd in nds :
            #print("node->(%s/%s)" % (nd,len(nds)))
            path.append(nodes_dict[nd].replace(',',' '))
    if len(path) >0:
        head = ways_dict[ways_id[0]][0]
        tail = ways_dict[ways_id[-1]][-1]
        if head != tail :
            #print(True)
            print('%s->%s:%s=>%s:%s' % (rid,head,tail,path[0],path[-1]))
    return ','.join(path)

def main():
    f = codecs.open('rel.txt','r','utf-8')
    out = codecs.open('rel_path_added.txt','w','utf-8')
    for line in f.readlines() :
        line = line.replace("\n", "")
        infs = line.split(';')  
        rid = infs[1]
        #print(infs)
        if(int(infs[4]) < 6):
            path = process_relation(rid)
            out.write('%s;%s\n' % (line, path))
    out.close()
    f.close()
    
if __name__ == '__main__':
    main()