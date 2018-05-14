import codecs
import shapefile
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    #f = codecs.open('China_Expressways_rel.txt', 'r', 'utf-8')
    f = codecs.open('China_National_Highway_rel.txt', 'r', 'utf-8')
    l_shp = shapefile.Writer(shapefile.POLYLINE)
    l_shp.field('rid')
    l_shp.field('id')
    l_shp.field('snode')
    l_shp.field('enode')
    l_shp.field('attr', 'C', 255)

    n_shp = shapefile.Writer(shapefile.POINT)
    n_shp.field('id')
    n_shp.field('attr', 'C', 255)

    for line in f.readlines():
        l_strs = line.replace("\n", "").split('|')
        flag = l_strs[0]
        if flag == 'n':
            n_shp.point(float(l_strs[2]),float(l_strs[3]))
            n_shp.record(l_strs[1],l_strs[4])
        elif flag == 'w':
            parts = []
            points = l_strs[5].split(',')
            for point in points:
                p = point.split(' ')
                parts.append([float(p[0]),float(p[1])])
            l_shp.line(parts=[parts])
            l_shp.record(l_strs[1],l_strs[2],l_strs[3],l_strs[4],l_strs[6])
        else:
            pass
    
    l_shp.save('shp/R/R1')
    n_shp.save('shp/N/N1')

if __name__ == '__main__':
    main()