%% DO NOT EDIT this file manually; it is automatically
%% generated from LSR http://lsr.dsi.unimi.it
%% Make any changes in LSR itself, or in Documentation/snippets/new/ ,
%% and then run scripts/auxiliar/makelsr.py
%%
%% This file is in the public domain.
\version "2.14.0"

\header {
  lsrtags = "unfretted-strings, template"

%% Translation of GIT committish: 615cbf212fdaf0b220b3330da417d0c3602494f2
  texidoces = "
Esta plantilla muestra un cuarteto de cuerda normal. También utiliza
una sección @code{\\global} para el compás y la armadura

"
  doctitlees = "Plantilla de cuarteto de cuerda (sencilla)"


%% Translation of GIT committish: fa1aa6efe68346f465cfdb9565ffe35083797b86
  texidocja = "
これは簡単な弦楽四重奏のためのテンプレートです。これは拍子記号と調号のために
@code{@bs{}global} セクションを使っています。
"

%% Translation of GIT committish: 0a868be38a775ecb1ef935b079000cebbc64de40
  texidocde = "
Dieses Beispiel demonstriert die Partitur für ein Streichquartett. Hier
wird auch eine @qq{@code{\\global}}-Variable für Taktart und
Vorzeichen benutzt.
"

  doctitlede = "Vorlage für Streichquartett (einfach)"


%% Translation of GIT committish: bdfe3dc8175a2d7e9ea0800b5b04cfb68fe58a7a
  texidocfr = "
Voici un canevas pour quatuor à cordes.  Notez l'utilisation de la
variable @code{\\global} pour traiter la métrique et la tonalité.

"
  doctitlefr = "Quatuor à cordes (conducteur)"

  texidoc = "
This template demonstrates a simple string quartet. It also uses a
@code{\\global} section for time and key signatures

"
  doctitle = "String quartet template (simple)"
} % begin verbatim

global= {
  \time 4/4
  \key c \major
}

violinOne = \new Voice \relative c'' {
  \set Staff.instrumentName = #"Violin 1 "

  c2 d
  e1

  \bar "|."
}

violinTwo = \new Voice \relative c'' {
  \set Staff.instrumentName = #"Violin 2 "

  g2 f
  e1

  \bar "|."
}

viola = \new Voice \relative c' {
  \set Staff.instrumentName = #"Viola "
  \clef alto

  e2 d
  c1

  \bar "|."
}

cello = \new Voice \relative c' {
  \set Staff.instrumentName = #"Cello "
  \clef bass

  c2 b
  a1

  \bar "|."
}

\score {
  \new StaffGroup <<
    \new Staff << \global \violinOne >>
    \new Staff << \global \violinTwo >>
    \new Staff << \global \viola >>
    \new Staff << \global \cello >>
  >>
  \layout { }
  \midi { }
}

