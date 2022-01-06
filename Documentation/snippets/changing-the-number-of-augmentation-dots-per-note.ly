%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "expressive-marks, rhythms"

  texidoc = "
The number of augmentation dots on a single note can be changed
independently of the dots placed after the note.

"
  doctitle = "Changing the number of augmentation dots per note"
} % begin verbatim

\relative c' {
  c4.. a16 r2 |
  \override Dots.dot-count = #4
  c4.. a16 r2 |
  \override Dots.dot-count = #0
  c4.. a16 r2 |
  \revert Dots.dot-count
  c4.. a16 r2 |
}
