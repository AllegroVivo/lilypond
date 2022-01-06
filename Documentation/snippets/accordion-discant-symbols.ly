%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "keyboards, specific-notation, symbols-and-glyphs, workaround"

  texidoc = "
This snippet has been obsoleted by predefined markup commands, see
'Discant symbols' in the Notation Reference.  It's still useful as a
simple demonstration of how to combine symbols: the placement of the
symbols added with @code{\\markup} can be tweaked by changing the
@code{\\translate-scaled} arguments.  @code{\\translate-scaled} is used
here rather than @code{\\translate} in order to let the positioning of
the symbol parts adapt to changes of @code{font-size}.

"
  doctitle = "Accordion-discant symbols"
} % begin verbatim

discant = \markup {
  \musicglyph "accordion.discant"
}
dot = \markup {
  \musicglyph "accordion.dot"
}

\layout { ragged-right = ##t }

% 16 voets register
accBasson = ^\markup {
  \combine
  \discant
  \translate-scaled #'(0 . 0.5) \dot
}

% een korig 8 en 16 voets register
accBandon = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 0.5) \dot
      \translate-scaled #'(0 . 1.5) \dot
}

accVCello = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 0.5) \dot
      \combine
        \translate-scaled #'(0 . 1.5) \dot
        \translate-scaled #'(1 . 1.5) \dot
}

% 4-8-16 voets register
accHarmon = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 0.5) \dot
      \combine
        \translate-scaled #'(0 . 1.5) \dot
        \translate-scaled #'(0 . 2.5) \dot
}

accTrombon = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 0.5) \dot
      \combine
        \translate-scaled #'(0 . 1.5) \dot
        \combine
          \translate-scaled #'(1 . 1.5) \dot
          \translate-scaled #'(-1 . 1.5) \dot
}

% eenkorig 4 en 16 voets register
accOrgan = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 0.5) \dot
      \translate-scaled #'(0 . 2.5) \dot
}

accMaster = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 0.5) \dot
      \combine
        \translate-scaled #'(0 . 1.5) \dot
        \combine
          \translate-scaled #'(1 . 1.5) \dot
          \combine
            \translate-scaled #'(-1 . 1.5) \dot
            \translate-scaled #'(0 . 2.5) \dot
}

accAccord = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 1.5) \dot
      \combine
        \translate-scaled #'(1 . 1.5) \dot
        \combine
          \translate-scaled #'(-1 . 1.5) \dot
          \translate-scaled #'(0 . 2.5) \dot
}

accMusette = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 1.5) \dot
      \combine
        \translate-scaled #'(1 . 1.5) \dot
        \translate-scaled #'(-1 . 1.5) \dot
}

accCeleste = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 1.5) \dot
      \translate-scaled #'(-1 . 1.5) \dot
}

accOboe = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 1.5) \dot
      \translate-scaled #'(0 . 2.5) \dot
}

accClarin = ^\markup {
  \combine
    \discant
    \translate-scaled #'(0 . 1.5) \dot
}

accPiccolo = ^\markup {
    \combine
       \discant
       \translate-scaled #'(0 . 2.5) \dot
}

accViolin = ^\markup {
  \combine
    \discant
    \combine
      \translate-scaled #'(0 . 1.5) \dot
      \combine
        \translate-scaled #'(1 . 1.5) \dot
        \translate-scaled #'(0 . 2.5) \dot
}

\relative c'' {
  c4 d\accBasson e f
  c4 d\accBandon e f
  c4 d\accVCello e f
  c4 d\accHarmon e f
  c4 d\accTrombon e f
  \break
  c4 d\accOrgan e f
  c4 d\accMaster e f
  c4 d\accAccord e f
  c4 d\accMusette e f
  c4 d\accCeleste e f
  \break
  c4 d\accOboe e f
  c4 d\accClarin e f
  c4 d\accPiccolo e f
  c4 d\accViolin e f
}
