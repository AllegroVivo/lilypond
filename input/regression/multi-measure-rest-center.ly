\version "1.7.18"
\header
{
  texidoc = "The multimeasure rest is centered exactly between bar lines."

}

\score {
    \notes
    {
	\property Score.skipBars = ##t
	\property Staff.BarLine \set #'hair-thickness = #7.5
	\property Staff.MultiMeasureRest \set #'hair-thickness = #10

	c'1 R1*20 c'1
    }
    \paper { raggedright = ##t} 
}
	 
%% new-chords-done %%
