import codecs
import shapefile
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
node_dict = {}
link_dict = {}

def write(type, l_shp, n_shp, f):
    for line in f.readlines():
        l_strs = line.replace("\n", "").split('|')
        flag = l_strs[0]
        if flag == 'n':
            id = l_strs[1]
            if node_dict.get(id) == None:
                node_dict[id] = 1
                n_shp.point(float(l_strs[2]),float(l_strs[3]))
                n_shp.record(l_strs[1],l_strs[4])
        elif flag == 'w':
            parts = []
            id = l_strs[2]
            if node_dict.get(id) == None:
                link_dict[id] = 1
                points = l_strs[5].split(',')
                for point in points:
                    p = point.split(' ')
                    parts.append([float(p[0]),float(p[1])])
                l_shp.line(parts=[parts])
                l_shp.record(type, l_strs[1],l_strs[2],l_strs[3],l_strs[4],l_strs[6])
        else:
            pass
def main():
    f1 = codecs.open('China_Expressways_rel.txt', 'r', 'utf-8')
    f2 = codecs.open('China_National_Highway_rel.txt', 'r', 'utf-8')
    l_shp = shapefile.Writer(shapefile.POLYLINE)
    l_shp.field('level')
    l_shp.field('rid')
    l_shp.field('id')
    l_shp.field('snode')
    l_shp.field('enode')
    l_shp.field('attr', 'C', 255)

    n_shp = shapefile.Writer(shapefile.POINT)
    n_shp.field('id')
    n_shp.field('attr', 'C', 255)
    write('G', l_shp, n_shp, f1)
    write('S', l_shp, n_shp, f2)
    l_shp.save('shp/R/R')
    n_shp.save('shp/N/N')

if __name__ == '__main__':
    main()