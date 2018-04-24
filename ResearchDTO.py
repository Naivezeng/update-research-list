

class Research(object):
    def __init__(self, regNo=0, author='', dept='', achi='', pub='', time='', cat='', others=''):
        self.regNo = regNo
        self.author = author
        self.dept = dept
        self.achi = achi
        self.pub = pub
        self.time = time
        self.cat = cat
        self.others = others

    def __str__(self):
        return '编号：' + str(self.regNo) + \
               '，作者：' + str(self.author) + \
               '，学院：' + str(self.dept) + \
               '，著作名称：' + str(self.achi) + \
               '，期刊：' + str(self.pub)