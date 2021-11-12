/*
  This file is part of LilyPond, the GNU music typesetter.

  Copyright (C) 1997--2021 Han-Wen Nienhuys <hanwen@xs4all.nl>

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

#include "rational.hh"

#include <cmath>
#include <cassert>
#include <cstdlib>
#include <utility>

using std::string;

Rational::operator double () const
{
  if (sign_ == -1 || sign_ == 1 || sign_ == 0)
// FIXME: workaround: In GUB, g++ 4.9.4 for darwin-x86,
// it seems that static cast from `unsigned long long` to `double`
// by x86 SSE2 raises an internal compile error.
// However, static cast from `signed long long` to `double`
// does not raise the error.
// So we use it for a workaround.
#if defined (__i386__) && defined (__SSE2_MATH__) && __GNUC__ < 5
    {
      I64 inum = num_;
      I64 iden = den_;
      return static_cast<double> (sign_) *
             static_cast<double> (inum) / static_cast<double> (iden);
    }
#else
    return static_cast<double> (sign_) * static_cast<double> (num_) / static_cast<double> (den_);
#endif
  if (sign_ == -2)
    return -HUGE_VAL;
  else if (sign_ == 2)
    return HUGE_VAL;
  else
    assert (false);

  return 0.0;
}

Rational
Rational::abs () const
{
  return Rational (::abs (sign_), num_, den_);
}

I64
Rational::trunc_int () const
{
  U64 i = num_ / den_;
  return static_cast<I64> (i) * sign_;
}

Rational
Rational::trunc_rat () const
{
  if (isinf (*this))
    return *this;
  return Rational ((num_ - (num_ % den_)) * sign_, den_);
}

Rational::Rational (I64 n, I64 d)
{
  // use sign of n when d=0
  sign_ = ::sign (n) * (std::signbit (d) ? -1 : 1);
  num_ = static_cast<U64> (::abs (n));
  if (n || d)
    {
      den_ = static_cast<U64> (::abs (d));
      normalize ();
    }
  else
    {
      // Treat initialization with {0, 0} as if it were {0} because parts of
      // LilyPond depend on this behavior.  It would make more sense to treat
      // {0, 0} as NaN, but it might not be easy to change.
      den_ = 1;
    }
}

Rational::Rational (long long n)
{
  sign_ = ::sign (n);
  num_ = static_cast<U64> (::abs (n));
  den_ = 1;
}

Rational::Rational (unsigned long long n)
{
  sign_ = ::sign (n);
  num_ = n;
  den_ = 1;
}

Rational
Rational::div_rat (Rational div) const
{
  Rational r (*this);
  r /= div;
  return r.trunc_rat ();
}

Rational
Rational::mod_rat (Rational div) const
{
  Rational r (*this);
  if (!isinf (div))
    r = (r / div - r.div_rat (div)) * div;
  return r;
}

/*
  copy & paste from scm_gcd (GUILE).
 */
static I64
gcd (I64 u, I64 v)
{
  I64 result = 0;
  if (u == 0)
    result = v;
  else if (v == 0)
    result = u;
  else
    {
      I64 k = 1;
      I64 t;
      /* Determine a common factor 2^k */
      while (!(1 & (u | v)))
        {
          k <<= 1;
          u >>= 1;
          v >>= 1;
        }
      /* Now, any factor 2^n can be eliminated */
      if (u & 1)
        t = -v;
      else
        {
          t = u;
b3:
          t = t >> 1;
        }
      if (!(1 & t))
        goto b3;
      if (t > 0)
        u = t;
      else
        v = -t;
      t = u - v;
      if (t != 0)
        goto b3;
      result = u * k;
    }

  return result;
}

void
Rational::normalize ()
{
  if (den_)
    {
      if (!sign_)
        {
          den_ = 1;
          num_ = 0;
        }
      else if (!num_)
        {
          sign_ = 0;
          den_ = 1;
        }
      else
        {
          I64 g = gcd (num_, den_);

          num_ /= g;
          den_ /= g;
        }
    }
  else if (num_)
    {
      *this = std::signbit (sign_) ? -infinity () : infinity ();
    }
  else // NaN mustn't keep sign 0
    {
      if (!sign_)
        sign_ = 1;
    }
}
int
Rational::sign () const
{
  return ::sign (sign_);
}

int
Rational::compare (Rational const &r, Rational const &s)
{
  if (r.sign_ < s.sign_)
    return -1;
  else if (r.sign_ > s.sign_)
    return 1;
  else if (isinf (r)) // here s is also infinite with the same sign
    return 0;
  else if (r.sign_ == 0) // here s.sign_ is also zero
    return 0;

  U64 left = r.num_ * s.den_;
  U64 right = s.num_ * r.den_;
  if (left < right)
    {
      return -r.sign_;
    }
  else if (left > right)
    {
      return r.sign_;
    }

  return 0;
}

int
compare (Rational const &r, Rational const &s)
{
  return Rational::compare (r, s);
}

Rational &
Rational::operator %= (Rational r)
{
  *this = mod_rat (r);
  return *this;
}

Rational &
Rational::operator += (Rational r)
{
  if (r.sign_ == 0)
    ;
  else if (sign_ == 0)
    *this = r;
  else if (isinf (*this))
    ;
  else if (isinf (r))
    *this = r;
  else
    {
      I64 lcm = (den_ / gcd (r.den_, den_)) * r.den_;
      I64 n = sign_ * num_ * (lcm / den_) + r.sign_ * r.num_ * (lcm / r.den_);
      I64 d = lcm;
      sign_ = ::sign (n) * ::sign (d);
      num_ = static_cast<U64> (::abs (n));
      den_ = static_cast<U64> (::abs (d));
      normalize ();
    }
  return *this;
}

/*
  copied from libg++ 2.8.0
*/
Rational::Rational (double x)
{
  if (x != 0.0)
    {
      if (std::isinf (x))
        {
          *this = std::signbit (x) ? -infinity () : infinity ();
          return;
        }
      else if (std::isnan (x))
        {
          *this = nan ();
          return;
        }

      sign_ = ::sign (x);
      x *= sign_;

      int expt;
      double mantissa = frexp (x, &expt);

      const int FACT = 1 << 20;

      /*
        Thanks to Afie for this too simple  idea.

        do not blindly substitute by libg++ code, since that uses
        arbitrary-size integers.  The rationals would overflow too
        easily.
      */

      num_ = static_cast<U64> (mantissa * FACT);
      den_ = static_cast<U64> (FACT);
      normalize ();
      if (expt < 0)
        den_ <<= -expt;
      else
        num_ <<= expt;
      normalize ();
    }
  else
    {
      num_ = 0;
      den_ = 1;
      sign_ = 0;
      normalize ();
    }
}

Rational &
Rational::operator *= (Rational r)
{
  sign_ *= ::sign (r.sign_);
  if (isinf (r))
    {
      sign_ = sign () * 2;
      goto exit_func;
    }

  num_ *= r.num_;
  den_ *= r.den_;

  normalize ();
exit_func:
  return *this;
}

Rational &
Rational::operator /= (Rational r)
{
  if (isinf (r))
    {
      r = {};
    }
  else
    {
      std::swap (r.num_, r.den_);
      if (!r.den_)
        {
          if (!r.sign_)
            r.sign_ = 1; // NaN mustn't have sign = 0
        }
    }

  return *this *= r;
}

void
Rational::negate ()
{
  sign_ *= -1;
}

Rational &
Rational::operator -= (Rational r)
{
  r.negate ();
  return (*this += r);
}

string
Rational::to_string () const
{
  if (isinf (*this))
    {
      return string (sign_ > 0 ? "" : "-") + "infinity";
    }

  if (isnan (*this))
    {
      return string (sign_ > 0 ? "" : "-") + "nan";
    }

  string s = std::to_string (num ());
  if (den () != 1 && num ())
    s += "/" + std::to_string (den ());
  return s;
}

int
sign (Rational r)
{
  return r.sign ();
}
