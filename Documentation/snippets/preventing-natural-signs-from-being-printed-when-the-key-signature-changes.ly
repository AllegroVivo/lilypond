%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "automatic-notation, pitches"

  texidoc = "
When the key signature changes, natural signs are automatically printed
to cancel any accidentals from previous key signatures.  This may be
prevented by setting to @code{f} the @code{printKeyCancellation}
property in the @code{Staff} context.

"
  doctitle = "Preventing natural signs from being printed when the key signature changes"
} % begin verbatim

\relative c' {
  \key d \major
  a4 b cis d
  \key g \minor
  a4 bes c d
  \set Staff.printKeyCancellation = ##f
  \key d \major
  a4 b cis d
  \key g \minor
  a4 bes c d
}
