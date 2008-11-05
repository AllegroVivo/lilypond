%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.11.62"

\header {
  lsrtags = "vocal-music, chords, template"

  texidoces = "
Esta plantilla facilita la preparación de una canción con melodía,
letra y acordes.

"
  doctitlees = "Plantilla de pentagrama único con música, letra y acordes"
  
  texidocde = "
Mit diesem Beispiel können Sie einen Song mit Melodie, 
Text und Akkorden schreiben.
"

  texidoc = "
This template allows the preparation of a song with melody, words, and
chords. 

"
  doctitle = "Single staff template with notes, lyrics, and chords"
} % begin verbatim

melody = \relative c' {
  \clef treble
  \key c \major
  \time 4/4
  
  a4 b c d
}

text = \lyricmode {
  Aaa Bee Cee Dee
}

harmonies = \chordmode {
  a2 c
}

\score {
  <<
    \new ChordNames {
      \set chordChanges = ##t
      \harmonies
    }
    \new Voice = "one" { \autoBeamOff \melody }
    \new Lyrics \lyricsto "one" \text
  >>
  \layout { }
  \midi { }
}
