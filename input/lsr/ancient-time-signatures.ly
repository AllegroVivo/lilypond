%% Do not edit this file; it is auto-generated from LSR http://lsr.dsi.unimi.it
%% This file is in the public domain.
\version "2.11.57"

\header {
  lsrtags = "ancient-notation"

  texidoces = "
Las indicaciones de compás también se pueden grabar en estilo antiguo.

"
  doctitlees = "Indicaciones de compás antiguas"

  texidoc = "
Time signatures may also be engraved in an old style.



"
  doctitle = "Ancient time signatures"
} % begin verbatim
{
  \override Staff.TimeSignature #'style = #'neomensural
  s1
}
