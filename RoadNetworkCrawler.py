#coding=utf-8
import codecs
import requests
from lxml import etree

def getRelation (rid, out) :
    """
    pid:  parent relation id for this relation
    rid:  crawl relation
    """

    full_url = 'https://api.openstreetmap.org/api/0.6/relation/'+rid+'/full'
    
    xml = requests.get(full_url)

    if not xml.ok:
        return
    # save this XML to local file.
    file = codecs.open('network/'+rid + '.xml','w','utf-8')
    file.write(xml.text)
    file.close()
    # parse this xml by lxml
    sel = etree.fromstring(xml.content)
    # get the node data for this relation id    
    nodes_rel = '//node'
    nodes = sel.xpath(nodes_rel)
    nodes_dict = {}
    nodes_tags_dict = {}
    for node in nodes :
        id = node.get('id')
        lon = node.get('lon')
        lat = node.get('lat')
        nodes_dict[id] = '%s %s' % (lon, lat)
        node_tags = node.xpath('./tag')
        node_tags_seq = []
        for tag in node_tags:
            k = tag.get('k')
            v = tag.get('v')
            node_tags_seq.append('%s=%s' % (k,v))
        nodes_tags_dict[id] = ';'.join(node_tags_seq)
        out.write('n|%s|%s|%s|%s\n' % (id, lon, lat, ';'.join(node_tags_seq)))
    tags = sel.xpath('//relation[@id="'+ rid +'"]/tag')
    tags_seq = []
    for tag in tags:
        k = tag.get('k')
        v = tag.get('v')
        tags_seq.append('%s=%s' % (k,v))           
    out.write('r|%s|%s\n' % (rid, ';'.join(tags_seq)))
        
    ways_rid_path = '//relation[@id="'+ rid  +'"]/member[@type="way"]/@ref'
    ways = sel.xpath(ways_rid_path)
    for wayid in ways :
        ref = wayid
        way_path = '//way[@id="'+ref+'"]'
        way = sel.xpath(way_path)[0]
        ways_node = way.xpath('./nd/@ref')
        s_id = ways_node[0]
        e_id = ways_node[-1]
        lon_lat_seq = []
        for nd in ways_node:
            lon_lat_seq.append(nodes_dict[nd])
        way_tags = []
        way_rags = way.xpath('./tag')
        for tag in way_rags:
            k = tag.get('k')
            v = tag.get('v')
            way_tags.append('%s=%s' % (k,v))
        out.write('w|%s|%s|%s|%s|%s|%s\n' % (rid, ref, s_id, e_id,','.join(lon_lat_seq),';'.join(way_tags)))


def getPage (url, fileName):
    ##url = 'https://wiki.openstreetmap.org/wiki/WikiProject_China'
    html = requests.get(url).content
    selector = etree.HTML(html)
    trs = selector.xpath('//span[@title="browse relation"]')
    out = codecs.open(fileName+'_rel.txt','w','utf-8')
    for tr in trs :
        rid = tr.text
        print(rid)
        getRelation(rid, out)
            
    out.close()
def main() :
    getPage('https://wiki.openstreetmap.org/wiki/WikiProject_China_National_Highway','China_National_Highway')
    getPage('https://wiki.openstreetmap.org/wiki/WikiProject_Expressways_of_China','China_Expressways')

if __name__ == '__main__':
    main()
