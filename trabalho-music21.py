#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from contour.contour import Contour
from music21 import corpus


def voice_contour_reduction(piece_path, voice):
    """Retorna a redução de contornos de Morris a partir de uma voz de
    uma peça.

    >>> voice_contour_reduction('bach/bwv7.7', 'Soprano')
    [< 0 2 1 >, 4]
    """

    piece = corpus.parse(piece_path)
    voice_notes = piece.getElementById(voice).flat.notes
    voice_freq = [n.frequency for n in voice_notes]
    voice_contour = Contour(voice_freq).translation()
    return voice_contour.reduction_algorithm()
