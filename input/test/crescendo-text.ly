\version "1.3.146"


fragment = \notes {
  \context Voice {
    \property Voice.crescendoText = "cresc."
    \property Voice.crescendoSpanner = #'dashed-line
    a''2\mf\< a a \!a
  }
}

\paper { linewidth = -1. } 

\score {
  \notes\relative c \fragment
  \paper { }  
}
