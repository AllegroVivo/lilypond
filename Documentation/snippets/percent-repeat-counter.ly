%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "repeats"

  texidoc = "
Measure repeats of more than two repeats can get a counter when the
convenient property is switched, as shown in this example:

"
  doctitle = "Percent repeat counter"
} % begin verbatim

\relative c'' {
  \set countPercentRepeats = ##t
  \repeat percent 4 { c1 }
}
