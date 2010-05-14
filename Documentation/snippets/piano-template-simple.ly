%% Do not edit this file; it is automatically
%% generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.13.16"

\header {
  lsrtags = "keyboards, template"

%% Translation of GIT committish: d2119a9e5e951c6ae850322f41444ac98d1ed492
  texidoces = "
Presentamos a continuación una plantilla de piano sencilla con algunas
notas.

"
  doctitlees = "Plantilla de piano (sencilla)"

%% Translation of GIT committish: 0a868be38a775ecb1ef935b079000cebbc64de40
  texidocde = "
Hier ein einfaches Klaviersystem.

"
  doctitlede = "Vorlage für einfache Klaviernotation"
%% Translation of GIT committish: ceb0afe7d4d0bdb3d17b9d0bff7936bb2a424d16
  texidocfr = "
Voici une simple partition pour piano avec quelques notes.

"
  doctitlefr = "Piano -- cannevas simple"

  texidoc = "
Here is a simple piano staff with some notes.

"
  doctitle = "Piano template (simple)"
} % begin verbatim

upper = \relative c'' {
  \clef treble
  \key c \major
  \time 4/4

  a4 b c d
}

lower = \relative c {
  \clef bass
  \key c \major
  \time 4/4

  a2 c
}

\score {
  \new PianoStaff <<
    \set PianoStaff.instrumentName = #"Piano  "
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
  \layout { }
  \midi { }
}

