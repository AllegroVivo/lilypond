%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "pitches, tweaks-and-overrides"

  texidoc = "
The following example shows how to force a natural sign before an
accidental.

"
  doctitle = "Force a cancellation natural before accidentals"
} % begin verbatim

\relative c' {
  \key es \major
  bes c des
  \tweak Accidental.restore-first ##t
  eis
}
