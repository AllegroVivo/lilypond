/*
  This file is part of LilyPond, the GNU music typesetter.

  Copyright (C) 2002--2022 Juergen Reuter <reuter@ipd.uka.de>

  LilyPond is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  LilyPond is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with LilyPond.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "international.hh"

#include "engraver.hh"
#include "note-column.hh"
#include "tuplet-bracket.hh"
#include "spanner.hh"
#include "stream-event.hh"
#include "item.hh"

#include "translator.icc"

class Ligature_bracket_engraver : public Engraver
{
protected:
  virtual void process_music ();
  virtual void stop_translation_timestep ();
  void acknowledge_rest (Grob_info);
  void acknowledge_note_column (Grob_info);
  void listen_ligature (Stream_event *);
public:
  TRANSLATOR_DECLARATIONS (Ligature_bracket_engraver);

private:
  Drul_array<Stream_event *> events_drul_;
  Spanner *finished_ligature_ = nullptr;
  Spanner *ligature_ = nullptr;
  Stream_event *previous_start_event_ = nullptr;
};

void
Ligature_bracket_engraver::listen_ligature (Stream_event *ev)
{
  Direction d = from_scm<Direction> (get_property (ev, "span-direction"));
  assign_event_once (events_drul_[d], ev);
}

Ligature_bracket_engraver::Ligature_bracket_engraver (Context *c)
  : Engraver (c)
{
}

void
Ligature_bracket_engraver::process_music ()
{
  if (events_drul_[STOP])
    {
      if (!ligature_)
        {
          events_drul_[STOP]->warning (_ ("cannot find start of ligature"));
          return;
        }

      finished_ligature_ = ligature_;
      ligature_ = nullptr;
      previous_start_event_ = nullptr;
    }

  if (events_drul_[START])
    {
      if (ligature_)
        {
          events_drul_[START]->warning (_ ("already have a ligature"));
          return;
        }

      previous_start_event_ = events_drul_[START];
      ligature_ = make_spanner ("LigatureBracket", events_drul_[START]->self_scm ());
    }
}

void
Ligature_bracket_engraver::acknowledge_note_column (Grob_info info)
{
  if (ligature_)
    {
      // TODO: We might see a MultiMeasureRest here, which is a Spanner, when
      // called from acknowledge_rest ().  What then?  Is passing a null
      // pointer to these functions OK?
      Item *item = dynamic_cast<Item *> (info.grob ());
      Tuplet_bracket::add_column (ligature_, item);
      add_bound_item (ligature_, item);
    }
}

void
Ligature_bracket_engraver::acknowledge_rest (Grob_info info)
{
  acknowledge_note_column (info);
}

void
Ligature_bracket_engraver::stop_translation_timestep ()
{
  events_drul_ = {};
  finished_ligature_ = nullptr;
}

void
Ligature_bracket_engraver::boot ()
{
  ADD_LISTENER (ligature);
  ADD_ACKNOWLEDGER (rest);
  ADD_ACKNOWLEDGER (note_column);
}

ADD_TRANSLATOR (Ligature_bracket_engraver,
                /* doc */
                R"(
Handle @code{Ligature_events} by engraving @code{Ligature} brackets.
                )",

                /* create */
                R"(
LigatureBracket
                )",

                /* read */
                R"(

                )",

                /* write */
                R"(

                )");
