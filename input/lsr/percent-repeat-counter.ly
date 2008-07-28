%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.11.53"

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
