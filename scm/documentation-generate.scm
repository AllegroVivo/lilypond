;;;; This file is part of LilyPond, the GNU music typesetter.
;;;;
;;;; Copyright (C) 2000--2022 Han-Wen Nienhuys <hanwen@xs4all.nl>
;;;; Jan Nieuwenhuizen <janneke@gnu.org>
;;;;
;;;; LilyPond is free software: you can redistribute it and/or modify
;;;; it under the terms of the GNU General Public License as published by
;;;; the Free Software Foundation, either version 3 of the License, or
;;;; (at your option) any later version.
;;;;
;;;; LilyPond is distributed in the hope that it will be useful,
;;;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;;;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;;; GNU General Public License for more details.
;;;;
;;;; You should have received a copy of the GNU General Public License
;;;; along with LilyPond.  If not, see <http://www.gnu.org/licenses/>.

;;; File entry point for generated documentation
;;; Running LilyPond on this file generates the documentation

;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;; TODO : make modules of these!
;;;;;;;;;;;;;;;;

;; todo: naming: grob vs. layout property

(use-modules (lily accreg))

(for-each ly:load '("documentation-lib"
                    "lily-sort"
                    "document-functions"
                    "document-translation"
                    "document-music"
                    "document-type-predicates"
                    "document-identifiers"
                    "document-context-mods"
                    "document-backend"
                    "document-markup"
                    "document-outside-staff-priorities"
                    "document-paper-sizes"
                    "hyphenate-internal-words"))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;(display
;; (markup-doc-string)
;; (open-output-file "markup-commands.tely"))

(display
 ;; ugly hack to remove the @node... @appendixsec... portion
 (substring
  (call-with-output-string
   (lambda (port)
     (dump-node (markup-doc-node) port 2)))
  ;; magic number to remove the initial part.  63 comes from:
  ;; "\nnode Text markup commands\n@appendixsec Text markup commands\n\n\n\n"
  ;; which is generated by (dump-node...) in documentation-lib.scm
  63
  )
 (open-output-file "markup-commands.tely"))

(display
 (markup-list-doc-string)
 (open-output-file "markup-list-commands.tely"))

(display
 type-predicates-doc-string
 (open-output-file "type-predicates.tely"))

(display
 (identifiers-doc-string)
 (open-output-file "identifiers.tely"))

(display
 context-mods-doc-string
 (open-output-file "context-mod-identifiers.tely"))

(display
 outside-staff-priorities-doc-string
 (open-output-file "outside-staff-priorities.tely"))

(display
 paper-sizes-doc-string
 (open-output-file "paper-sizes.tely"))

(display
 hyphenation-rules-string
 (open-output-file "hyphenation.itexi"))

(define file-name "internals")
(define outname (string-append file-name ".texi"))

(define out-port (open-output-file outname))

;; Don't output Latin1.
(cond-expand
 (guile-2 (set-port-encoding! out-port "UTF-8"))
 (else))

(writing-wip outname)

(display
 (string-append
   "\\input texinfo @c -*-texinfo-*-\n"
   "@setfilename " file-name ".info\n"
   "@documentlanguage en\n"
   "@documentencoding UTF-8\n"
   "

@include en/macros.itexi

@iftex
@afourpaper
@tableindent=@itemindent
@end iftex

@finalout

@titlepage
@title LilyPond
@subtitle The music typesetter
@titlefont{Internals Reference}
@author The LilyPond development team

@c `Internals Reference' was born 2000-10-21 with this commit:
@c patch::: 1.3.96.jcn9
@c author: Jan Nieuwenhuizen
@c commit: 8ecd09ad7514d57630fb611d38c161f3c3c708db
@c   file: scm/generate-documentation.scm
Copyright @copyright{} 2000--2022 by the authors

@vskip 20pt

For LilyPond version @version{}
@end titlepage

@contents

@ifnottex")
 out-port)

(define top-node
  (make <texi-node>
    #:name "GNU LilyPond -- Internals Reference"
    #:text
    (string-append  "@end ifnottex

@ifhtml
@ifclear bigpage
This document is also available as a
@uref{../internals.pdf,PDF} and as
@uref{../internals-big-page.html,one big page}.
@end ifclear
@ifset bigpage
This document is also available as a
@uref{internals.pdf,PDF} and as a
@uref{internals/index.html,HTML indexed multiple pages}.
@end ifset
@end ifhtml

This is the Internals Reference (IR) for version "
                    (lilypond-version)
                    " of LilyPond, the GNU music typesetter.")

    #:children
    (list
     (music-doc-node)
     (translation-doc-node)
     (backend-doc-node)
     (all-functions-doc)
     (make <texi-node>
       #:appendix #t
       #:name "Indices"
       #:text "
@appendixsec Concept index

@printindex cp

@appendixsec Function index

@printindex fn

\n@bye"))))

(dump-node top-node out-port 0)
(newline (current-error-port))
