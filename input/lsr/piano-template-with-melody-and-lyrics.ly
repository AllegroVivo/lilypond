%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.11.62"

\header {
  lsrtags = "vocal-music, keyboards, template"

  texidoces = "
He aquí el típico formato dde una canción: un pentagrama con la
melodía y la letra, y el acompañamiento de piano por debajo.

"
  doctitlees = "Plantilla de piano con melodía y letra"
  
  texidocde = "
Das nächste Beispiel ist typisch für ein Lied: Im oberen System die 
Melodie mit Text, darunter Klavierbegleitung.
"

  texidoc = "
Here is a typical song format: one staff with the melody and lyrics,
with piano accompaniment underneath. 

"
  doctitle = "Piano template with melody and lyrics"
} % begin verbatim

melody = \relative c'' {
  \clef treble
  \key c \major
  \time 4/4
  
  a b c d  
}

text = \lyricmode {
  Aaa Bee Cee Dee
}

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
  <<
    \new Voice = "mel" { \autoBeamOff \melody }
    \new Lyrics \lyricsto mel \text    
    \new PianoStaff <<
      \new Staff = "upper" \upper
      \new Staff = "lower" \lower
    >>
  >>
  \layout {
    \context { \RemoveEmptyStaffContext }
  }
  \midi { }
}
