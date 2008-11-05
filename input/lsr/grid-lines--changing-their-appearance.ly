%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.11.62"

\header {
  lsrtags = "editorial-annotations"

  texidoces = "
Se puede cambiar el aspecto de las líneas de rejilla
sobreescribiendo algunas de sus propiedades.

"
  doctitlees = "Líneas de rejilla: modificar su aspecto"

  texidoc = "
The appearance of grid lines can be changed by overriding some of their
properties.

"
  doctitle = "Grid lines: changing their appearance"
} % begin verbatim

\layout {
 \context {
   \Staff
   % set up grids
   \consists "Grid_point_engraver"
   % set the grid interval to one quarter note
   gridInterval = #(ly:make-moment 1 4)
  }
}

\new Score \with {
 \consists "Grid_line_span_engraver"
 % this moves them to the right half a staff space
 \override NoteColumn #'X-offset = #-0.5
}

\new ChoirStaff <<
  \new Staff {
    \relative c'' {
      \stemUp
      c'4. d8 e8 f g4
    }
  }
  \new Staff {
    \relative c {
      % this moves them up one staff space from the default position
      \override Score.GridLine #'extra-offset = #'(0.0 . 1.0)
      \stemDown
      \clef bass
      \once \override Score.GridLine #'thickness = #5.0
      c4
      \once \override Score.GridLine #'thickness = #1.0
      g'
      \once \override Score.GridLine #'thickness = #3.0
      f
      \once \override Score.GridLine #'thickness = #5.0
      e
    }
  }
>>
