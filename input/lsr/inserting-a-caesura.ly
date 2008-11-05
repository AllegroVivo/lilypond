%% Do not edit this file; it is auto-generated from input/new
%% This file is in the public domain.
\version "2.11.62"
\header {
  texidoces = "
Las marcas de cesura se pueden crear sobreescribiendo la propiedad
@code{'text} del objeto @code{BreathingSign}.  También está disponible
una marca de cesura curva.

"
  doctitlees = "Insertar una cesura"

  lsrtags = "expressive-marks,tweaks-and-overrides"
  texidoc = "
Caesura marks can be created by overriding the @code{'text}
property of the @code{BreathingSign} object.  A curved caesura
mark is also available.
"
  doctitle = "Inserting a caesura"
} % begin verbatim


\relative c'' {
  \override BreathingSign #'text = \markup {
    \musicglyph #"scripts.caesura.straight"
  }
  c8 e4. \breathe g8. e16 c4

  \override BreathingSign #'text = \markup {
    \musicglyph #"scripts.caesura.curved"
  }
  g8 e'4. \breathe g8. e16 c4
}
