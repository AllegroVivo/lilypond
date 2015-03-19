\version "2.18.0"

\header {

  lsrtags = "scheme-language, midi"

  texidoc = "The following example shows how to create a dynamic
  marking, not included in the default list, and assign it a specific
  value so that it can be used to affect MIDI output.

  The dynamic mark @code{\rfz} (@notation{rinforzando}) is assigned a
  value of @code{0.9}."

  doctitle = "Creating custom dynamics in MIDI output"
}

#(define (myDynamics dynamic)
    (if (equal? dynamic "rfz")
      0.9
      (default-dynamic-absolute-volume dynamic)))

\score {
  \new Staff {
    \set Staff.midiInstrument = #"cello"
    \set Score.dynamicAbsoluteVolumeFunction = #myDynamics
    \new Voice {
      \relative c'' {
        a4\pp b c-\rfz
      }
    }
  }
  \layout {}
  \midi {}
}
