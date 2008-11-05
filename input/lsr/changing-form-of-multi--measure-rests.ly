%% Do not edit this file; it is auto-generated from input/new
%% This file is in the public domain.
\version "2.11.62"
\header {
 doctitlees = "Cambiar la forma de los silencios multicompás"
 texidoces = "
Si hay diez compases de silencio o menos, se imprime en el pentagrama
una serie de silencios de breve y longa (conocidos en alemán como
\"Kirchenpausen\", «silencios eclesiásticos»); en caso contrario se
muestra una barra normal.  Este número predeterminado de diez se
puede cambiar sobreescribiendo la propiedad @code{expand-limit}:

"
  lsrtags = "rhythms,tweaks-and-overrides"
  texidoc = "
If there are ten or fewer measures of rests, a series of longa
and breve rests (called in German \"Kirchenpausen\" - church rests)
is printed within the staff; otherwise a simple line is shown.
This default number of ten may be changed by overriding the
@code{expand-limit} property:
"
  doctitle = "Changing form of multi-measure rests"
} % begin verbatim


\relative c'' {
  \compressFullBarRests
  R1*2 | R1*5 | R1*9
  \override MultiMeasureRest #'expand-limit = #3
  R1*2 | R1*5 | R1*9
}
