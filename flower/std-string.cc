/*
  This file is part of LilyPond, the GNU music typesetter.

  Copyright (C) 2006--2023  Jan Nieuwenhuizen <janneke@gnu.org>

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

#include "std-string.hh"
#include "string-convert.hh"
#include "std-vector.hh"

std::string
to_string (char const *format, ...)
{
  va_list args;
  va_start (args, format);
  std::string str = String_convert::vform_string (format, args);
  va_end (args);
  return str;
}

/*
  TODO: this O(n^2) in #occurrences of find, due to repeated copying.
 */
std::string &
replace_all (std::string *str, std::string const &find,
             std::string const &replace)
{
  ssize len = find.length ();
  ssize replen = replace.length ();
  for (ssize i = str->find (find); i != NPOS; i = str->find (find, i + replen))
    *str = str->replace (i, len, replace);
  return *str;
}

std::string &
replace_all (std::string *str, char find, char replace)
{
  for (ssize i = str->find (find); i != NPOS; i = str->find (find, i + 1))
    (*str)[i] = replace;
  return *str;
}

std::vector<std::string>
string_split (std::string str, char c)
{
  ssize i = str.find (c);

  std::vector<std::string> a;
  while (i != NPOS)
    {
      std::string s = str.substr (0, i);
      a.push_back (s);
      i++;
      str = str.substr (i);
      i = str.find (c);
    }
  if (str.length ())
    a.push_back (str);
  return a;
}

std::string
string_join (std::vector<std::string> const &strs, const std::string &infix)
{
  std::string result;
  for (vsize i = 0; i < strs.size (); i++)
    {
      if (i)
        result += infix;
      result += strs[i];
    }

  return result;
}
