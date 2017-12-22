i,o,b=24435.0,345128.0,16637.0
class FPP():
    word_dict = {}
    word_list = []

    def __init__(self, filename):
        self.filein = open(filename)

    def file_close(self):
        self.filein.close()

    def gwc(self):
        for line in self.filein:
            line_list = line.split('\t')
            self.word_list.append(line_list[0])
            #get the words in training or test data and add it to dictionary

        for wordsh in self.word_list:
            if not self.word_dict.has_key(wordsh):
                self.word_dict[wordsh] = 1
            else:
                self.word_dict[wordsh] += 1

    def rtrf(self, filein, fileout):
        filein = open(filein, 'r')
        fileout = open(fileout, 'w')


        for line in filein:
            line_list = line.split('\t')
            word = line_list[0]
            if self.word_dict[word] == 1:

                line_list[0] = 'Unknown word'
                line = '\t'.join(line_list)
            fileout.write(line)

        filein.close()
        fileout.close()

    def rtef(self, filein, fileout, word_set):
        filein = open(filein, 'r')
        fileout = open(fileout, 'w')

        for word in filein:
            if word != '\n':
                word = word.rstrip('\n')
                if not word in word_set:
                    word = 'Unknown word'
                fileout.write(word + '\n')
            else:
                fileout.write(word)

        filein.close()
        fileout.close()


class FP():
    unique_word_list = []

    def __init__(self, filename):
        self.filein = open(filename)

    def file_close(self):
        self.filein.close()

    def get_start_prob_dict(self):

        start_prob_dict = {}

        start_prob_dict['B\n'] = 0.33
        start_prob_dict['I\n'] = 0.33
        start_prob_dict['O\n'] = 0.33

        return start_prob_dict

    def tagtransprob(self):
        self.filein.seek(0)
        tag_list = []
        for line in self.filein:
            if line != '\n':
                line_list = line.split('\t')
                tag_list.append(line_list[1])

        translist = []
        for i in range(0, len(tag_list) - 1):
            item = [tag_list[i], tag_list[i + 1]]
            translist.append(item)

        Bdict = {}
        Bdict['B\n'] = (translist.count(['B\n', 'B\n']) ) / (b )
        Bdict['I\n'] = (translist.count(['B\n', 'I\n']) ) / (b )
        Bdict['O\n'] = (translist.count(['B\n', 'O\n']) ) / (b )

        Idict = {}
        Idict['B\n'] = (translist.count(['I\n', 'B\n']) ) / (i )
        Idict['I\n'] = (translist.count(['I\n', 'I\n']) ) / (i )
        Idict['O\n'] = (translist.count(['I\n', 'O\n']) ) / (i )

        Odict = {}
        Odict['B\n'] = (translist.count(['O\n', 'B\n']) ) / (o )
        Odict['I\n'] = (translist.count(['O\n', 'I\n']) ) / (o )
        Odict['O\n'] = (translist.count(['O\n', 'O\n']) ) / (o )

        tagdict = {}
        tagdict['B\n'] = Bdict
        tagdict['I\n'] = Idict
        tagdict['O\n'] = Odict

        return tagdict

    def tagwordprob(self):
        self.filein.seek(0)
        B_list = []
        I_list = []
        O_list = []
        word_list = []

        for line in self.filein:
            if line != '\n':
                line_list = line.split('\t')
                word_list.append(line_list[0])
                if line_list[1] == 'B\n':
                    B_list.append(line_list[0])
                elif line_list[1] == 'I\n':
                    I_list.append(line_list[0])
                else:
                    O_list.append(line_list[0])
        print len(I_list),len(O_list),len(B_list)
        # get the values for tag transition probability
        self.unique_word_list = list(set(word_list))
        B_dict = {}
        I_dict = {}
        O_dict = {}

        for word in self.unique_word_list:
            B_dict[word] = 0
            I_dict[word] = 0
            O_dict[word] = 0

        for word in B_list:
            B_dict[word] += 1
        for word in I_list:
            I_dict[word] += 1
        for word in O_list:
            O_dict[word] += 1

        for word in self.unique_word_list:
            B_dict[word] = B_dict[word] / b
            I_dict[word] = I_dict[word] / i
            O_dict[word] = O_dict[word] / o

        tagdict = {}
        tagdict['B\n'] = B_dict
        tagdict['I\n'] = I_dict
        tagdict['O\n'] = O_dict

        return tagdict


def viterbish(obs, states, start_p, trans_p, emit_p):
    if len(obs) < 2:
        return ['O\n']

    V = [{y: (start_p[y] * emit_p[y][obs[0]]) for y in states}] #get iniatial values for initialization
    path = {y: [y] for y in states}
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]

    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            (prob, state) = max((V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath

    (prob, state) = max((V[t][y], y) for y in states)   #take max at each level
    return path[state]


def rtef(filename):
    filein = open(filename, 'r')
    total_line = ''
    for line in filein:
        total_line += line
    print len(total_line)
    sentence_list = total_line.split('\n\n')
    test_list = []
    for each in sentence_list:
        words = each.split('\n')
        if '' in words:
            words.remove('')
        test_list.append(tuple(words))
    return test_list


def printoutputfile(word_list, tag_list, output_filename):
    fileoutput = open(output_filename, 'w')
   # counter=0
    for i in range(0, len(word_list)):
        counter=0
        for j in range(0, len(word_list[i])):
            counter=counter+1
            if (str(word_list[i][j] != '')):
                line = str(counter) + "\t"+word_list[i][j] + '\t' + tag_list[i][j]
            else:
                line=word_list[i][j] + '\t' + tag_list[i][j]
                counter=0

            fileoutput.write(line)

        fileoutput.write('\n')

    fileoutput.close()



def main():
    filename = 'geneshe.txt'
    a=open(filename,'r+')
    filename='geneshe.txt'
    trainchange = FPP(filename)
    trainchange.gwc()
    new_filename = 'modified.train.txt'
    trainchange.rtrf(filename, new_filename)
    trainchange.file_close()

    traincheck = FP(new_filename)
    startdict = traincheck.get_start_prob_dict()
    tagtransdict = traincheck.tagtransprob()
    tagworddict = traincheck.tagwordprob()
    traincheck.file_close()

    testname = 'finalinputdata.txt'
    b=open(testname,'r+')
    fileoutput = open('fileoutput.txt', 'w+')

    testname = 'finalinputdata.txt'

    testcheck = FPP(testname)
    new_testname = 'genesh.txt'
    wordset = set(traincheck.unique_word_list)
    testcheck.rtef(testname, new_testname, wordset)

    tags_tuple = ('B\n', 'I\n', 'O\n')
    testlist = rtef(new_testname)
    resultlist = []
    for words_tuple in testlist:
        path = viterbish(words_tuple, tags_tuple, startdict, tagtransdict, tagworddict)
        resultlist.append(path)

    rawwordlist = rtef(testname)
    printoutputfile(rawwordlist, resultlist, 'outputgenesh2.txt')



if __name__ == '__main__':
    main()