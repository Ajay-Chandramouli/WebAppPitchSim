import numpy as np
import dash_html_components as html

#Function to calculate the Power Spectral Density (PSD) of a timeseries.
def CalcPSD(t,timeseries,deltat):
    fFFT = np.fft.rfftfreq(len(t),deltat)
    dfFFT = fFFT[1] - fFFT[0]
    a = abs(np.fft.fft(timeseries)) / len(timeseries)
    PSD = 2 * a ** 2 / dfFFT
    PSD=PSD[:len(fFFT)]
    PSD[0] = 0
    return fFFT,PSD

#This function is used to create value-label pairs for the dropdown options. Output is a list of value-label pairs.
def create_value_label_for_dropdown(label_list, value_list):
    dictlist = []
    for n, label in enumerate(label_list):
        dictlist.append({'value': value_list[n], 'label': label})
    return dictlist

#This function is used to get the indices corresponding to an item in a list containing strings
def IndicesinList(list,item):
    i = [i for i,x in enumerate(list) if x.strip()==item.strip()] #strictly only for strings, for integers use np.where
    return i

#This function is used to get unique elements in a list
def GetUniqueinList(list):
    unique_list = []
    for x in list:     # traverse overall elements
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

"""
Custom function to read text for the app from a text file. In the text file, the text is written as:
 *
 Heading 1 
 Text to be displayed
 *
 Heading 2 
 Text to be displayed
 *
and so on. Heading an a text are sandwiched between two * 
"""

def Text2DictForLayout(textfilepath):
    fo = open(textfilepath, 'r')
    a = []
    for i, line in enumerate(fo.readlines()):
        if line.startswith('*'):
            a.append(i)
    Text = {}
    fo.seek(0)
    b = fo.read().splitlines()
    for i in range(len(a) - 1):
        fo.seek(0)
        TextInsideAsList = b[a[i] + 2:a[i + 1]]
        Breaks = IndicesinList(TextInsideAsList, 'html.Br()') #haha a bit complicated but serves the purpose
        if len(Breaks) > 0:
            Breaks = [0] + Breaks
            JoinedSentencesAsList = []
            for num, Break in enumerate(Breaks):
                if num == 0:
                    SentencesIndividuallyAsList = TextInsideAsList[Breaks[num]:Breaks[num + 1]]
                    JoinedSentencesAsList.append(' '.join(SentencesIndividuallyAsList))
                if (num != 0) & (num < len(Breaks) - 1):
                    SentencesIndividuallyAsList = TextInsideAsList[Breaks[num] + 1:Breaks[num + 1]]
                    JoinedSentencesAsList.append(' '.join(SentencesIndividuallyAsList))
                if num == len(Breaks) - 1:
                    SentencesIndividuallyAsList = TextInsideAsList[Breaks[num] + 1:]
                    JoinedSentencesAsList.append(' '.join(SentencesIndividuallyAsList))
            Paragraph = []
            for num, Sentence in enumerate(JoinedSentencesAsList):
                if num == 0:
                    Paragraph = Paragraph + [Sentence]
                else:
                    Paragraph = Paragraph + [html.Br()] + [Sentence]
        else:
            Paragraph = TextInsideAsList

        Text[b[a[i] + 1]] = Paragraph
    fo.close()

    return Text