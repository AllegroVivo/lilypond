%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "really-simple, text, vocal-music"

  texidoc = "
Horizontal alignment for lyrics can be set by overriding the
@code{self-alignment-X} property of the @code{LyricText} object.
@code{#-1} is left, @code{#0} is center and @code{#1} is right;
however, you can use @code{#LEFT}, @code{#CENTER} and @code{#RIGHT} as
well.

"
  doctitle = "Lyrics alignment"
} % begin verbatim

\layout { ragged-right = ##f }
\relative c'' {
  c1
  c1
  c1
}
\addlyrics {
  \once \override LyricText.self-alignment-X = #LEFT
  "This is left-aligned"
  \once \override LyricText.self-alignment-X = #CENTER
  "This is centered"
  \once \override LyricText.self-alignment-X = #1
  "This is right-aligned"
}
