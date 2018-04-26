#coding=utf-8
import codecs
import requests
from lxml import etree
import math
import random

def distance(a,b):
    """
    simple distance 
    a ,b = (lon,lat)
    """
    x = a[0] - b[0]
    y = a[1] - b[1]
    return math.sqrt(x*x + y*y)

def find_shortest_distance(a, b_list):
    """
    find the most shortest distance item in the b_list to a = str lon,lat
    """
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

def find_region(ways_id,ways_dict,nodes_dict):
    """
    find the topology from the start way to the end way where node id should the same.
    """
    for i in range(1,len(ways_id),1) :
        sub = ways_id[i:]
        #last way , the tail node id of the way 
        end_node_id = ways_dict[ways_id[i-1]][-1]
        #fist way , the head node id of the way 
        target_node_id = ways_dict[ways_id[0]][0]
        if end_node_id == target_node_id: # target meet. find a closed polygon topology
            #closed region , sub(othe way left to find more next iteration)
            return ways_id[0:i],sub
            
        ok = False
        for k,v in enumerate(sub):#sort the way that linked together by node id.
            if ways_dict[v][0] == end_node_id:
                tmp = ways_id[i]
                ways_id[i] = v
                ways_id[i+k] = tmp
                ok =True
            if ways_dict[v][-1] == end_node_id:#way that should reverse the node.
                tmp = ways_id[i]
                ways_id[i] = v
                ways_id[i+k] = tmp
                ways_dict[v].reverse()
                ok =True
        if not ok:
            # topology lost ,use shortest distance to last way end node id
            dist_list = []
            for k,v in enumerate(sub):
                beg = ways_dict[v][0]
                end = ways_dict[v][-1]
                dist_list.append(((nodes_dict[beg]),0,v,k))
                dist_list.append(((nodes_dict[end]),1,v,k))
            shortest_way = find_shortest_distance(nodes_dict[end_node_id], dist_list)
            k = shortest_way[3]#index
            v = shortest_way[2]#way id
            #swith
            tmp = ways_id[i]
            ways_id[i] = v
            ways_id[i+k] = tmp
            if shortest_way[1] == 1: # way node should reverse
                 ways_dict[v].reverse()
    return ways_id,[] 
        #print('%s->%s:%s' % (ways_dict[ways_id[i-1]][-1],ways_dict[ways_id[i]][0],ways_dict[ways_id[i-1]][-1]==ways_dict[ways_id[i]][0]))
    
def find_closed_region(ways_id, ways_dict, nodes_dict):
    region_list = []
    sub = ways_id
    while len(sub) >0 : # finf all closed region
        closed_region , sub = find_region(sub, ways_dict, nodes_dict)
        region_list.append(closed_region)
    
    return region_list
    
def process_relation(rid) :
    
    sel = etree.parse('boundary/'+rid+'.xml')
    ways_rel = '//relation[@id="'+ rid +'"]/member[@type="way"][@role="outer"]/@ref'
    ways = sel.xpath(ways_rel)
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
    for way in ways :
        nd_rels = '//way[@id="'+ way +'"]/nd/@ref'
        nds = sel.xpath(nd_rels)
        ways_dict[way] = nds
        ways_id.append(way)
    
    region_list = find_closed_region(ways_id[:], ways_dict, nodes_dict)
    region_path = []
    for region in region_list:
        path = []
        for way in region :
            nds = ways_dict[way]
            for nd in nds :
                path.append(nodes_dict[nd].replace(',',' '))
        if path[0] != path[-1]: # some region don't cloed. drop it now.
            print('%s/%s : %s' % (rid, path[0] , path[-1]))
        else:
            region_path.append(','.join(path))
    return region_path

def main():
    f = codecs.open('rel.txt','r','utf-8')
    out = codecs.open('rel_path_added.txt','w','utf-8')
    for line in f.readlines() :
        line = line.replace("\n", "")
        infs = line.split(';')  
        rid = infs[1]
        #print(infs)
        if(int(infs[4]) < 7):
            region_path = process_relation(rid)
            for path in region_path:
                out.write('%s;%s\n' % (line, path))
    out.close()
    f.close()
    
if __name__ == '__main__':
    main()