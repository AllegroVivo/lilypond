/*
  stem.hh -- part of LilyPond

  (c) 1996 Han-Wen Nienhuys
*/

#ifndef STEM_HH
#define STEM_HH
#include "item.hh"

/// the rule attached to the ball
struct Stem : public Item {
    // heads the stem encompasses (positions)
    int minnote, maxnote;

    int staff_center;

    // extent of the stem (positions)
    int bot, top;
    
    // flagtype? 4 none, 8 8th flag, 0 = beam.
    int flag;
    
    /****************/
    
    void postprocess();
    Stem(int center);
    void print() const;
    Interval width() const;
private:
    void calculate();
    void brew_molecole();
};
/**
  takes care of:

  \begin{itemize}
  \item the rule
  \item the flag
  \item up/down position.
  \end{itemize}
  */

#endif
