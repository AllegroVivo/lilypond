\version "1.3.146"

\header {
texidoc  = " Ez-notation prints names in note heads."
}

\include "paper26.ly"
\paper { \paperTwentysix }

\score {
        \notes { c'2 e'4 f' | g'1 }
        \paper { \translator { \EasyNotation } } 
}
