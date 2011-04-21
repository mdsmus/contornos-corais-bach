#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
sys.path.append('/home/marcos/work/ongoing/MusiContour/')
import re
import contour.contour
import contour.comparison
import contour.plot
import contour.humdrum
import contour.auxiliary
import pickle

krn_path = "/home/marcos/repositorios/genos-corpus/music/bach-chorales/kern/"
voices = ["*Ibass", "*Itenor", "*Ialto", "*Isoprn"]

a = contour.contour.Contour([0, 1, 3, 2])
files = [str(n).zfill(3) for n in range(1, 371)]
files.remove("150")

## problems:
files.remove("196")
files.remove("201")
files.remove("306")
files.remove("320")
## alto problems:
files.remove("280")

files.remove("121")
files.remove("252")

krn_files = [n + '.krn' for n in files]
krn_complete = [krn_path + n + '.krn' for n in files]

fermata = re.compile('.*;$[JL]?\]?')

## main functions

class Phrase():

    def __init__(self, cseg, filename, voice, number):
        self.cseg = contour.contour.Contour(cseg)
        self.filename = filename
        self.voice = voice
        self.number = number

    def __repr__(self):

        return "Cseg: {0}\nFile: {1}\nVoice: {2}\nNumber: {3}".format(self.cseg, self.filename, self.voice, self.number)


def choral_phrases(file):
    """Returns the number of phrases of a choral.

    Search for fermata regular expression in all lines of file, and
    count lines."""

    with open(file) as f:
        lines = f.readlines()
        return len([fermata.search(l) for l in lines if fermata.search(l)])


def yank_phrase(file, voice, phrase_number):
    """Returns the contour of phrase number 'n'.

    The phrases are delimited by fermata.

    >>> n_phrase('/tmp/001.krn', '*Isoprn', '0')
    """

    if phrase_number <= choral_phrases(file):
        regex = '"^[^*!](.*);[JL]?"'
        yank_option = "-o " + regex + " -e " + regex + " -r {0}".format(phrase_number)
        spine = contour.humdrum.Spine_file(file, voice)
        abs_pitch = spine.parse_yank_to_contour_space(yank_option)
        normal_form = contour.contour.Contour(abs_pitch).translation()
        no_adjacent = contour.utils.remove_adjacent(normal_form)
        return Phrase(contour.contour.Contour(no_adjacent), file, voice, phrase_number)
    else:
        return ''



def n_phrase(file, voice, phrase_number):
    """Returns the contour of phrase number 'n'.

    The phrases are delimited by fermata.

    >>> n_phrase('/tmp/001.krn', '*Isoprn', '0')
    """

    if phrase_number <= choral_phrases(file):
        regex = '"^[^*!](.*);[JL]?"'
        yank_option = "-o " + regex + " -e " + regex + " -r {0}".format(phrase_number)
        spine = contour.humdrum.Spine_file(file, voice)
        abs_pitch = spine.parse_yank_to_contour_space(yank_option)
        normal_form = contour.contour.Contour(abs_pitch).translation()
        no_adjacent = contour.utils.remove_adjacent(normal_form)
        return Phrase(no_adjacent, file, voice, phrase_number)
    else:
        return ''

def chorales_with_n_phrases(all_chorales, phrase_number):
    """Returns a list with all chorales with a given number of
    phrases."""

    return [i for i in all_chorales if choral_phrases(i) == phrase_number]


def bach_chorales_number_of_phrases():
    """Returns number of phrases in 370 Bach Chorales.

    Outputs a list with phrase and frequency, and a chart.
    """

    number_of_phrases = [choral_phrases(choral) for choral in krn_complete]
    chorales_number = len(number_of_phrases)
    phrase_sizes = sorted(list(set(number_of_phrases)))
    number_of_phrases_freq = [[x, number_of_phrases.count(x)] for x in phrase_sizes]
    phrases_plot = [[str(x), y] for [x, y] in number_of_phrases_freq]
    contour.plot.pie(phrases_plot, "Number of phrases in {0} Bach Chorales".format(chorales_number))

# def any_phrase(n, voice, phrase_num):
#     """Returns frequency of each type of contour in last n notes in a
#     given voice first phrase of all Bach Chorales.
#     """

#     files = [x for x in krn_complete if choral_phrases(x) > phrase_num]
#     contours = [contour.contour.Contour(n_phrase(file, voice, phrase_num)[-n:]) for file in files]
#     size = len(contours)
#     freq = contour.auxiliary.normal_form_subsets_count(contours)

#     return freq
#     # freq_print = [[Contour(x).cseg_visual_printing(), y] for [x, y] in freq if len(x) == n]
#     # if phrase_num == 0:
#     #     phrase = "first"
#     # elif phrase_num == "$":
#     #     phrase = "last"
#     # elif phrase_num == 1:
#     #     phrase = "{0}nd".format(phrase_num + 1)
#     # elif phrase_num == 2:
#     #     phrase = "{0}rd".format(phrase_num + 1)
#     # else:
#     #     phrase = "{0}th".format(phrase_num + 1)
#     # pie_plot(freq_print, "Last {0} cpitches in {1} {2} phrase in {3} Bach Chorales".format(n, voice, phrase, size))

def phrases_choral(file):

    phrases_number = choral_phrases(file)
    dic = {}

    def insert_key(voice):
        tmp = []
        for phrase_number in range(phrases_number):
            tmp.append(n_phrase(file, voice, phrase_number).reduction_algorithm())
        dic[voice] = tmp

    voices = ["*Ibass", "*Itenor", "*Ialto", "*Isoprn"]

    [insert_key(voice) for voice in voices]

    return dic

def incidencia(dictionary):

    reduced = []

    for key in dictionary.keys():
        reduced.append(dictionary[key])
    return [x[0] for x in sorted(contour.utils.flatten(reduced))]

def all_choral_phrases(filename):
    phrases = []

    for voice in ["*Ibass", "*Itenor", "*Ialto", "*Isoprn"]:
        for phrase_number in range(choral_phrases(filename)):
            phrases.append(yank_phrase(filename, voice, phrase_number))

    return phrases


def all_phrases(list_of_files):
    phrases = []

    for filename in list_of_files:
        print(filename)
        choral_number_phrases = range(choral_phrases(filename))
        for voice in ["*Ibass", "*Itenor", "*Ialto", "*Isoprn"]:
            for phrase_number in choral_number_phrases:
                phrases.append(yank_phrase(filename, voice, phrase_number))

    return phrases

def save_to_file(data, file):
    with open(file, "w") as f:
        pickle.dump(data, f)


def open_file(file):
    with open(file, "r") as f:
        return pickle.load(f)

def foo(lista):
    reduced_csegs = [x.cseg.reduction_algorithm()[0] for x in lista]
    reduced_csegs_types = sorted(list(set(([str(x) for x in reduced_csegs]))))
    dic = {}
    for el in reduced_csegs_types:
        i = 0
        for cseg in reduced_csegs:
            if str(cseg) == el:
                i += 1
            dic[el] = i
    return dic

def dict_to_list(dados):
    return [[cseg, incidencia] for (cseg, incidencia) in dados.items()]

contour_types = {'< 0 1 0 >': 493,
                 '< 0 1 2 1 >': 102,
                 '< 0 1 >': 1129,
                 '< 0 2 0 1 >': 253,
                 '< 0 2 1 >': 4635,
                 '< 0 >': 12,
                 '< 1 0 1 2 1 >': 14,
                 '< 1 0 1 2 >': 25,
                 '< 1 0 1 3 2 >': 12,
                 '< 1 0 1 >': 106,
                 '< 1 0 2 1 >': 195,
                 '< 1 0 2 3 2 >': 7,
                 '< 1 0 3 2 >': 973,
                 '< 1 2 0 1 >': 280,
                 '< 1 2 0 2 >': 88,
                 '< 1 2 1 0 1 >': 16,
                 '< 1 3 0 2 >': 477,
                 '< 1 3 1 0 2 >': 7,
                 '< 1 3 2 0 2 >': 20}

dados = dict_to_list(contour_types)

## processa as frases de todos os corais
# t = all_phrases(krn_complete)

# save_to_file(t, "/tmp/dados")

dir_trabalho = "/home/marcos/profissional/doutorado/disciplinas/mus504-humdrum/trabalho-final/"
frases_corais = open_file(dir_trabalho + "dados-frases.data")
dic_contour_type = foo(frases_corais)

def reducao_voz(voz, lista):
    result = []
    for phrase in lista:
        if phrase.voice == voz:
            result.append(phrase)
    return result

def phrase_score(file, voice, phrase_num):
    filename = file.split("/")[-1].split(".krn")[0]
    regex = '"^[^*!](.*);[JL]?"'
    yank_option = "-o " + regex + " -e " + regex + " -r {0}".format(phrase_num)
    data = n_phrase(file, voice, phrase_num)
    h = contour.humdrum.Spine_file(file, voice)
    h.humdrum_yank_abc(yank_option)
    contour.utils.abcm2ps("/tmp", filename + ".abc")
    contour.plot.contour_line_score(data.cseg, "/tmp/" + filename + ".ps", "k")

lista_soprano = reducao_voz("*Isoprn", frases_corais)
lista_alto = reducao_voz("*Ialto", frases_corais)
lista_tenor = reducao_voz("*Itenor", frases_corais)
lista_bass = reducao_voz("*Ibass", frases_corais)

# contour.plot.pie(dict_to_list(foo(lista_soprano)), u"Incidência de contornos reduzidos no soprano")
# contour.plot.pie(dict_to_list(foo(lista_alto)), u"Incidência de contornos reduzidos no contralto")
# contour.plot.pie(dict_to_list(foo(lista_tenor)), u"Incidência de contornos reduzidos no tenor")
# contour.plot.pie(dict_to_list(foo(lista_bass)), u"Incidência de contornos reduzidos no baixo")
# contour.plot.pie(dict_to_list(foo(frases_corais)), u"Incidência de contornos reduzidos em todas as vozes")

# bach_chorales_number_of_phrases()


# corais_6_frases = chorales_with_n_phrases(krn_complete, 6)

# phrases_6_frases = []
# for coral in corais_6_frases:
#     for voice in voices:
#         phrases_6_frases.append(n_phrase(coral, voice, 5))


def grafico_last_phrase():
    last_phrase = []
    for phrases_number in range(2, 23):
        files = chorales_with_n_phrases(krn_complete, phrases_number)
        if len(files) >= 1:
            for choral in files:
                for voice in voices:
                    last_phrase.append(n_phrase(choral, voice, phrases_number - 1))
    contour.plot.pie(dict_to_list(foo(last_phrase)), u"Incidência de contornos reduzidos na última frase dos corais")

# grafico_last_phrase

def foobarbla(lista):
    result = []
    for phrase in lista:
        result.append([phrase, phrase.cseg.reduction_algorithm()[0]])
    return result

# print(foobarbla(frases_corais[:100]))


phrase_score(krn_path + '002.krn', '*Isoprn', 4)
