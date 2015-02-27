class Node(object):
    
    def parse(self, line):
        assert line.startswith('#')
        try:
            unit_start = line.index('(') + 1
            unit_end = line.index(')')
        except Exception, e:
            print line
        self.unit = line[unit_start:unit_end]
        space = line.index(' ')
        self.id = line[:space]
        self.name = line[space+1:unit_start-1]
