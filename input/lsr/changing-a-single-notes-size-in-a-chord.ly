%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.11.57"

\header {
  lsrtags = "simultaneous-notes, editorial-annotations, tweaks-and-overrides"

  texidoces = "
Se pueden modificar notas individuales de un acorde con la
instrucción @code{\tweak}, alterando la propiedad
@code{font-size}.

Dentro de un acorde (entre ángulos simples @code{< >}), antes de
la nota que queremos alterar, situamos la instrucción
@code{\tweak} seguida por @code{#'font-size} y definimos el
tamaño adecuado como @code{#-2} (una cabeza pequeña).

"
  doctitlees = "Modificar el tamaño de una nota suelta de un acorde"

  texidoc = "
Individual note heads in a chord can be modified with the
@code{\\tweak} command inside a chord, by altering the @code{font-size}
property.


Inside the chord (within the brackets @code{< >}), before the note to
be altered, place the @code{\\tweak} command, followed by
@code{#'font-size} and define the proper size like @code{#-2} (a tiny
notehead).



"
  doctitle = "Changing a single note's size in a chord"
} % begin verbatim
\layout { ragged-right = ##t }
\relative {
  <\tweak #'font-size #+2 c e g c \tweak #'font-size #-2 e>1^\markup { A tiny e }_\markup { A big c }
}
