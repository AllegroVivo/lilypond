%% DO NOT EDIT this file manually; it was automatically
%% generated from the LilyPond Snippet Repository
%% (http://lsr.di.unimi.it).
%%
%% Make any changes in the LSR itself, or in
%% `Documentation/snippets/new/`, then run
%% `scripts/auxiliar/makelsr.pl`.
%%
%% This file is in the public domain.

\version "2.24.0"

\header {
  lsrtags = "spacing, tweaks-and-overrides, workaround"

  texidoc = "
By default, LilyPond uses @code{DynamicLineSpanner} grobs to vertically
align successive dynamic objects like hairpins and dynamic
text.  However, this is not always wanted.  By inserting
@code{\\breakDynamicSpan}, which ends the alignment spanner
prematurely, this vertical alignment can be avoided.
"

  doctitle = "Breaking vertical alignment of dynamics and textscripts"
} % begin verbatim


{ g1\< |
  e''\f\> |
  c'\p }

{ g1\< |
  e''\breakDynamicSpan\f\> |
  c'\p }
