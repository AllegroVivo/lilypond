%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.di.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.23.6"

\header {
  lsrtags = "fretted-strings, staff-notation"

  texidoc = "
In tablatures usually the first string is printed topmost. If you want
to have it at the bottom change the
@code{stringOneTopmost}-context-property. For a context-wide setting
this could be done in @code{layout} as well.

"
  doctitle = "Let TabStaff print the topmost string at bottom"
} % begin verbatim

%
%\layout {
%  \context {
%    \Score
%    stringOneTopmost = ##f
%  }
%  \context {
%    \TabStaff
%    tablatureFormat = #fret-letter-tablature-format
%  }
%}

m = {
  \cadenzaOn
  e, b, e gis! b e'
  \bar "||"
}

<<
  \new Staff { \clef "G_8" <>_"default" \m <>_"italian (historic)"\m }
  \new TabStaff
  {
    \m
    \set Score.stringOneTopmost = ##f
    \set TabStaff.tablatureFormat = #fret-letter-tablature-format
    \m
  }
>>
