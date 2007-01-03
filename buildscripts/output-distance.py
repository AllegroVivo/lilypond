#!@TARGET_PYTHON@
import sys
import optparse
import os
import math

## so we can call directly as buildscripts/output-distance.py
me_path = os.path.abspath (os.path.split (sys.argv[0])[0])
sys.path.insert (0, me_path + '/../python/')


import safeeval


X_AXIS = 0
Y_AXIS = 1
INFTY = 1e6

OUTPUT_EXPRESSION_PENALTY = 1
ORPHAN_GROB_PENALTY = 1
options = None

def shorten_string (s):
    threshold = 15 
    if len (s) > 2*threshold:
        s = s[:threshold] + '..' + s[-threshold:]
    return s

def max_distance (x1, x2):
    dist = 0.0

    for (p,q) in zip (x1, x2):
        dist = max (abs (p-q), dist)
        
    return dist


empty_interval = (INFTY, -INFTY)
empty_bbox = (empty_interval, empty_interval)

def interval_is_empty (i):
    return i[0] > i[1]

def interval_length (i):
    return max (i[1]-i[0], 0) 
    
def interval_union (i1, i2):
    return (min (i1[0], i2[0]),
            max (i1[1], i2[1]))

def interval_intersect (i1, i2):
    return (max (i1[0], i2[0]),
            min (i1[1], i2[1]))

def bbox_is_empty (b):
    return (interval_is_empty (b[0])
            or interval_is_empty (b[1]))

def bbox_union (b1, b2):
    return (interval_union (b1[X_AXIS], b2[X_AXIS]),
            interval_union (b2[Y_AXIS], b2[Y_AXIS]))
            
def bbox_intersection (b1, b2):
    return (interval_intersect (b1[X_AXIS], b2[X_AXIS]),
            interval_intersect (b2[Y_AXIS], b2[Y_AXIS]))

def bbox_area (b):
    return interval_length (b[X_AXIS]) * interval_length (b[Y_AXIS])

def bbox_diameter (b):
    return max (interval_length (b[X_AXIS]),
                interval_length (b[Y_AXIS]))
                

def difference_area (a, b):
    return bbox_area (a) - bbox_area (bbox_intersection (a,b))

class GrobSignature:
    def __init__ (self, exp_list):
        (self.name, self.origin, bbox_x,
         bbox_y, self.output_expression) = tuple (exp_list)
        
        self.bbox = (bbox_x, bbox_y)
        self.centroid = (bbox_x[0] + bbox_x[1], bbox_y[0] + bbox_y[1])

    def __repr__ (self):
        return '%s: (%.2f,%.2f), (%.2f,%.2f)\n' % (self.name,
                                                   self.bbox[0][0],
                                                   self.bbox[0][1],
                                                   self.bbox[1][0],
                                                   self.bbox[1][1])
                                                 
    def axis_centroid (self, axis):
        return apply (sum, self.bbox[axis])  / 2 
    
    def centroid_distance (self, other, scale):
        return max_distance (self.centroid, other.centroid) / scale 
        
    def bbox_distance (self, other):
        divisor = bbox_area (self.bbox) + bbox_area (other.bbox)

        if divisor:
            return (difference_area (self.bbox, other.bbox) +
                    difference_area (other.bbox, self.bbox)) / divisor
        else:
            return 0.0
        
    def expression_distance (self, other):
        if self.output_expression == other.output_expression:
            return 0
        else:
            return 1

################################################################
# single System.

class SystemSignature:
    def __init__ (self, grob_sigs):
        d = {}
        for g in grob_sigs:
            val = d.setdefault (g.name, [])
            val += [g]

        self.grob_dict = d
        self.set_all_bbox (grob_sigs)

    def set_all_bbox (self, grobs):
        self.bbox = empty_bbox
        for g in grobs:
            self.bbox = bbox_union (g.bbox, self.bbox)

    def closest (self, grob_name, centroid):
        min_d = INFTY
        min_g = None
        try:
            grobs = self.grob_dict[grob_name]

            for g in grobs:
                d = max_distance (g.centroid, centroid)
                if d < min_d:
                    min_d = d
                    min_g = g


            return min_g

        except KeyError:
            return None
    def grobs (self):
        return reduce (lambda x,y: x+y, self.grob_dict.values(), [])

################################################################
## comparison of systems.

class SystemLink:
    def __init__ (self, system1, system2):
        self.system1 = system1
        self.system2 = system2
        
        self.link_list_dict = {}
        self.back_link_dict = {}


        ## pairs
        self.orphans = []

        ## pair -> distance
        self.geo_distances = {}

        ## pairs
        self.expression_changed = []

        self._geometric_distance = None
        self._expression_change_count = None
        self._orphan_count = None
        
        for g in system1.grobs ():

            ## skip empty bboxes.
            if bbox_is_empty (g.bbox):
                continue
            
            closest = system2.closest (g.name, g.centroid)
            
            self.link_list_dict.setdefault (closest, [])
            self.link_list_dict[closest].append (g)
            self.back_link_dict[g] = closest


    def calc_geometric_distance (self):
        total = 0.0
        for (g1,g2) in self.back_link_dict.items ():
            if g2:
                d = g1.bbox_distance (g2)
                if d:
                    self.geo_distances[(g1,g2)] = d

                total += d

        self._geometric_distance = total
    
    def calc_orphan_count (self):
        count = 0
        for (g1, g2) in self.back_link_dict.items ():
            if g2 == None:
                self.orphans.append ((g1, None))
                
                count += 1

        self._orphan_count = count
    
    def calc_output_exp_distance (self):
        d = 0
        for (g1,g2) in self.back_link_dict.items ():
            if g2:
                d += g1.expression_distance (g2)

        self._expression_change_count = d

    def output_expression_details_string (self):
        return ', '.join ([g1.name for g1 in self.expression_changed])
    
    def geo_details_string (self):
        results = [(d, g1,g2) for ((g1, g2), d) in self.geo_distances.items()]
        results.sort ()
        results.reverse ()
        
        return ', '.join (['%s: %f' % (g1.name, d) for (d, g1, g2) in results])

    def orphan_details_string (self):
        return ', '.join (['%s-None' % g1.name for (g1,g2) in self.orphans if g2==None])

    def geometric_distance (self):
        if self._geometric_distance == None:
            self.calc_geometric_distance ()
        return self._geometric_distance
    
    def orphan_count (self):
        if self._orphan_count == None:
            self.calc_orphan_count ()
            
        return self._orphan_count
    
    def output_expression_change_count (self):
        if self._expression_change_count == None:
            self.calc_output_exp_distance ()
        return self._expression_change_count
        
    def distance (self):
        return (self.output_expression_change_count (),
                self.orphan_count (),
                self.geometric_distance ())
    
def read_signature_file (name):
    print 'reading', name
    
    entries = open (name).read ().split ('\n')
    def string_to_tup (s):
        return tuple (map (float, s.split (' '))) 

    def string_to_entry (s):
        fields = s.split('@')
        fields[2] = string_to_tup (fields[2])
        fields[3] = string_to_tup (fields[3])

        return tuple (fields)
    
    entries = [string_to_entry (e) for e in entries
               if e and not e.startswith ('#')]

    grob_sigs = [GrobSignature (e) for e in entries]
    sig = SystemSignature (grob_sigs)
    return sig


################################################################
# different systems of a .ly file.
def read_pipe (c):
    print 'pipe' , c
    return os.popen (c).read ()

def system (c):
    print 'system' , c
    s = os.system (c)
    if s :
        raise Exception ("failed")
    return

def compare_png_images (old, new, dir):
    def png_dims (f):
        m = re.search ('([0-9]+) x ([0-9]+)', read_pipe ('file %s' % f))
        
        return tuple (map (int, m.groups ()))

    dest = os.path.join (dir, new.replace ('.png', '.compare.jpeg'))
    try:
        dims1 = png_dims (old)
        dims2 = png_dims (new)
    except AttributeError:
        ## hmmm. what to do?
        system ('touch %(dest)s' % locals ())
        return
    
    dims = (min (dims1[0], dims2[0]),
            min (dims1[1], dims2[1]))

    system ('convert -depth 8 -crop %dx%d+0+0 %s crop1.png' % (dims + (old,)))
    system ('convert -depth 8 -crop %dx%d+0+0 %s crop2.png' % (dims + (new,)))

    system ('compare -depth 8 crop1.png crop2.png diff.png')

    system ("convert  -depth 8 diff.png -blur 0x3 -negate -channel alpha,blue -type TrueColorMatte -fx 'intensity'    matte.png")

    system ("composite -quality 65 matte.png %(new)s %(dest)s" % locals ())

class FileLink:
    def __init__ (self):
        self._distance = None

    def text_record_string (self):
        return '%-30f %-20s\n' % (self.distance (),
                                  self.name ())
    def calc_distance (self):
        return 0.0

    def distance (self):
        if self._distance == None:
           self._distance = self.calc_distance ()

        return self._distance
    
    def name (self):
        return '<undefined>'
    
    def link_files_for_html (self, old_dir, new_dir, dest_dir):
        pass

    def write_html_system_details (self, dir1, dir2, dest_dir):
        pass
        
    def html_record_string (self,  old_dir, new_dir):
        return ''

class FileCompareLink (FileLink):
    def __init__ (self, f1, f2):
        FileLink.__init__ (self)
        self.files = (f1, f2)
        self.contents = (self.get_content (self.files[0]),
                         self.get_content (self.files[1]))
        
    def link_files_for_html (self, old_dir, new_dir, dest_dir):
        for f in self.files:
            link_file (f, os.path.join (dest_dir, f))

    def name (self):
        name = os.path.basename (self.files[0])
        name = os.path.splitext (name)[0]
        return name
        
    def calc_distance (self):
        ## todo: could use import MIDI to pinpoint
        ## what & where changed.

        if self.contents[0] == self.contents[1]:
            return 0.0
        else:
            return 100.0;
        
    def html_record_string (self, d1, d2):
        (dist, f1, f2) = (self.distance(),) + self.files
        b1 = os.path.basename (f1)
        b2 = os.path.basename (f2)
        
        return '''<tr>
<td>
%(dist)f
</td>
<td><a href="%(f1)s"><tt>%(b1)s</tt></td>
<td><a href="%(f2)s"><tt>%(b2)s</tt></td>
</tr>''' % locals ()

    def get_content (self, f):
        print 'reading', f
        s = open (f).read ()
        return s
    
        
class TextFileCompareLink (FileCompareLink):
    def calc_distance (self):
        import difflib
        diff = difflib.unified_diff (self.contents[0].strip().split ('\n'),
                                     self.contents[1].strip().split ('\n'),
                                     fromfiledate = self.files[0],
                                     tofiledate = self.files[1]
                                     )

        self.diff_lines =  [l for l in diff]
        return float (len (self.diff_lines))
        
    def link_files_for_html (self, old_dir, new_dir, dest_dir):
        str = '\n'.join ([d.replace ('\n','') for d in self.diff_lines])
        f = os.path.join (new_dir, self.name ()) + '.diff.txt'
        f = os.path.join (dest_dir, f)
        open_write_file (f).write (str)
     
    def html_record_string (self, d1, d2):
        (dist, f1, f2) = (self.distance(),) + self.files
        b1 = os.path.basename (f1)
        b2 = os.path.basename (f2)
        
        return '''<tr>
<td>
%f
</td>
<td><tt>%s</tt></td>
<td><a href="%s.diff.txt"><tt>%s</tt></a></td>
</tr>''' % (dist,
            b1,
            os.path.join (d2, self.name ()),
            b2)


class ProfileFileLink (TextFileCompareLink):
    def calc_distance (self):
        TextFileCompareLink.calc_distance (self)
        
        r = [{},{}]
        for oldnew in (0,1):
            def note_info (m):
                r[oldnew][m.group(1)] = float (m.group (2))
            
            re.sub ('([a-z]+): ([-0-9.]+)\n',
                    note_info, self.contents[oldnew])

        dist = 0.0
        factor = {'time': 1.0 ,
                  'cells': 10.0,
                  }
        
        for k in ('time', 'cells'):
            (v1,v2) = (r[0].get (k , -1),
                       r[1].get (k , -1))

            if v1 <= 0 or v2 <= 0:
                continue

            ratio = abs (v2 - v1) / float (v1+v2)
            dist += math.exp (ratio * factor[k]) - 1

        dist = min (dist, 100)
        
        return dist

class MidiFileLink (FileCompareLink):
    def get_content (self, f):
        s = FileCompareLink.get_content (self, f)
        s = re.sub ('LilyPond [0-9.]+', '', s)
        return s

class SignatureFileLink (FileLink):
    def __init__ (self):
        FileLink.__init__ (self)
        self.original_name = ''
        self.base_names = ('','')
        self.system_links = {}
        
    def name (self):
        return os.path.splitext (self.original_name)[0]
    
    def add_system_link (self, link, number):
        self.system_links[number] = link

    def calc_distance (self):
        d = 0.0

        orphan_distance = 0.0
        for l in self.system_links.values ():
            d = max (d, l.geometric_distance ())
            orphan_distance += l.orphan_count ()
            
        return d + orphan_distance

    def source_file (self):
        for ext in ('.ly', '.ly.txt'):
            if os.path.exists (self.base_names[1] + ext):
                return self.base_names[1] + ext
        return ''
    
    def add_file_compare (self, f1, f2):
        system_index = [] 

        def note_system_index (m):
            system_index.append (int (m.group (1)))
            return ''
        
        base1 = re.sub ("-([0-9]+).signature", note_system_index, f1)
        base2 = re.sub ("-([0-9]+).signature", note_system_index, f2)

        self.base_names = (os.path.normpath (base1),
                           os.path.normpath (base2))

        def note_original (match):
            self.original_name = match.group (1)
            return ''
        
        if not self.original_name:
            self.original_name = os.path.split (base1)[1]

            ## ugh: drop the .ly.txt
            for ext in ('.ly', '.ly.txt'):
                try:
                    re.sub (r'\\sourcefilename "([^"]+)"',
                            note_original, open (base1 + ext).read ())
                except IOError:
                    pass
                
        s1 = read_signature_file (f1)
        s2 = read_signature_file (f2)

        link = SystemLink (s1, s2)

        self.add_system_link (link, system_index[0])

    
    def create_images (self, old_dir, new_dir, dest_dir):

        files_created = [[], []]
        for oldnew in (0, 1):
            pat = self.base_names[oldnew] + '.eps'

            for f in glob.glob (pat):
                infile = f
                outfile = (dest_dir + '/' + f).replace ('.eps', '.png')

                mkdir (os.path.split (outfile)[0])
                cmd = ('gs -sDEVICE=png16m -dGraphicsAlphaBits=4 -dTextAlphaBits=4 '
                       ' -r101 '
                       ' -sOutputFile=%(outfile)s -dNOSAFER -dEPSCrop -q -dNOPAUSE '
                       ' %(infile)s  -c quit '  % locals ())

                files_created[oldnew].append (outfile)
                system (cmd)

        return files_created
    
    def link_files_for_html (self, old_dir, new_dir, dest_dir):
        to_compare = [[], []]

        exts = ['.ly']
        if options.create_images:
            to_compare = self.create_images (old_dir, new_dir, dest_dir)
        else:
            exts += ['.png', '-page*png']
        
        for ext in exts:            
            for oldnew in (0,1):
                for f in glob.glob (self.base_names[oldnew] + ext):
                    dst = dest_dir + '/' + f
                    link_file (f, dst)

                    if f.endswith ('.png'):
                        to_compare[oldnew].append (f)
                        
        if options.compare_images:                
            for (old, new) in zip (to_compare[0], to_compare[1]):
                compare_png_images (old, new, dest_dir)

                
    def html_record_string (self,  old_dir, new_dir):
        def img_cell (ly, img, name):
            if not name:
                name = 'source'
            else:
                name = '<tt>%s</tt>' % name
                
            return '''
<td align="center">
<a href="%(img)s">
<img src="%(img)s" style="border-style: none; max-width: 500px;">
</a><br>
<font size="-2">(<a href="%(ly)s">%(name)s</a>)
</font>
</td>
''' % locals ()
        def multi_img_cell (ly, imgs, name):
            if not name:
                name = 'source'
            else:
                name = '<tt>%s</tt>' % name

            imgs_str = '\n'.join (['''<a href="%s">
<img src="%s" style="border-style: none; max-width: 500px;">
</a><br>''' % (img, img) 
                                  for img in imgs])


            return '''
<td align="center">
%(imgs_str)s
<font size="-2">(<a href="%(ly)s">%(name)s</a>)
</font>
</td>
''' % locals ()



        def cell (base, name):
            pat = base + '-page*.png'
            pages = glob.glob (pat)

            if pages:
                return multi_img_cell (base + '.ly', sorted (pages), name)
            else:
                return img_cell (base + '.ly', base + '.png', name)
            

        html_2  = self.base_names[1] + '.html'
        name = self.original_name

        cell_1 = cell (self.base_names[0], name)
        cell_2 = cell (self.base_names[1], name)
        if options.compare_images:
            cell_2 = cell_2.replace ('.png', '.compare.jpeg')
        
        html_entry = '''
<tr>
<td>
%f<br>
(<a href="%s">details</a>)
</td>

%s
%s
</tr>
''' % (self.distance (), html_2, cell_1, cell_2)

        return html_entry


    def html_system_details_string (self):
        systems = self.system_links.items ()
        systems.sort ()

        html = ""
        for (c, link) in systems:
            e = '<td>%d</td>' % c
            for d in link.distance ():
                e += '<td>%f</td>' % d
            
            e = '<tr>%s</tr>' % e

            html += e

            e = '<td>%d</td>' % c
            for s in (link.output_expression_details_string (),
                      link.orphan_details_string (),
                      link.geo_details_string ()):
                e += "<td>%s</td>" % s

            
            e = '<tr>%s</tr>' % e
            html += e
            
        original = self.original_name
        html = '''<html>
<head>
<title>comparison details for %(original)s</title>
</head>
<body>
<table border=1>
<tr>
<th>system</th>
<th>output</th>
<th>orphan</th>
<th>geo</th>
</tr>

%(html)s
</table>

</body>
</html>
''' % locals ()
        return html

    def write_html_system_details (self, dir1, dir2, dest_dir):
        dest_file =  os.path.join (dest_dir, self.base_names[1] + '.html')

        details = open_write_file (dest_file)
        details.write (self.html_system_details_string ())

################################################################
# Files/directories

import glob
import re

def compare_signature_files (f1, f2):
    s1 = read_signature_file (f1)
    s2 = read_signature_file (f2)
    
    return SystemLink (s1, s2).distance ()

def paired_files (dir1, dir2, pattern):
    """
    Search DIR1 and DIR2 for PATTERN.

    Return (PAIRED, MISSING-FROM-2, MISSING-FROM-1)

    """
    
    files1 = dict ((os.path.split (f)[1], 1) for f in glob.glob (dir1 + '/' + pattern))
    files2 = dict ((os.path.split (f)[1], 1) for f in glob.glob (dir2 + '/' + pattern))

    pairs = []
    missing = []
    for f in files1.keys ():
        try:
            files2.pop (f)
            pairs.append (f)
        except KeyError:
            missing.append (f)

    return (pairs, files2.keys (), missing)
    
class ComparisonData:
    def __init__ (self):
        self.result_dict = {}
        self.missing = []
        self.added = []
        self.file_links = {}

    def compare_trees (self, dir1, dir2):
        self.compare_directories (dir1, dir2)
        
        (root, dirs, files) = os.walk (dir1).next ()
        for d in dirs:
            d1 = os.path.join (dir1, d)
            d2 = os.path.join (dir2, d)

            if os.path.islink (d1) or os.path.islink (d2):
                continue
            
            if os.path.isdir (d2):
                self.compare_trees (d1, d2)
    
    def compare_directories (self, dir1, dir2):
        for ext in ['signature', 'midi', 'log', 'profile']:
            (paired, m1, m2) = paired_files (dir1, dir2, '*.' + ext)

            self.missing += [(dir1, m) for m in m1] 
            self.added += [(dir2, m) for m in m2] 

            for p in paired:
                if (options.max_count
                    and len (self.file_links) > options.max_count):
                    
                    continue
                
                f2 = dir2 +  '/' + p
                f1 = dir1 +  '/' + p
                self.compare_files (f1, f2)

    def compare_files (self, f1, f2):
        if f1.endswith ('signature'):
            self.compare_signature_files (f1, f2)
        else:
            ext = os.path.splitext (f1)[1]
            klasses = {
                '.midi': MidiFileLink,
                '.log' : TextFileCompareLink,
                '.profile': ProfileFileLink,
                }
            
            if klasses.has_key (ext):
                self.compare_general_files (klasses[ext], f1, f2)

    def compare_general_files (self, klass, f1, f2):
        name = os.path.split (f1)[1]

        file_link = klass (f1, f2)
        self.file_links[name] = file_link
        
    def compare_signature_files (self, f1, f2):
        name = os.path.split (f1)[1]
        name = re.sub ('-[0-9]+.signature', '', name)
        
        file_link = None
        try:
            file_link = self.file_links[name]
        except KeyError:
            file_link = SignatureFileLink ()
            self.file_links[name] = file_link

        file_link.add_file_compare (f1, f2)

    def remove_changed (self, dir, threshold):
        (changed, below, unchanged) = self.thresholded_results (threshold)
        for link in changed:
            try:
                system ('rm -f %s*' % link.base_names[1])
            except AttributeError: ### UGH.
                system ('rm -f %s/%s*' % (dir, link.name ()))
    def thresholded_results (self, threshold):
        ## todo: support more scores.
        results = [(link.distance(), link)
                   for link in self.file_links.values ()]
        results.sort ()
        results.reverse ()

        unchanged = [r for (d,r) in results if d == 0.0]
        below = [r for (d,r) in results if threshold >= d > 0.0]
        changed = [r for (d,r) in results if d > threshold]

        return (changed, below, unchanged)
                
    def write_text_result_page (self, filename, threshold):
        out = None
        if filename == '':
            out = sys.stdout
        else:
            print 'writing "%s"' % filename
            out = open_write_file (filename)

        (changed, below, unchanged) = self.thresholded_results (threshold)

        
        for link in changed:
            out.write (link.text_record_string ())

        out.write ('\n\n')
        out.write ('%d below threshold\n' % len (below))
        out.write ('%d unchanged\n' % len (unchanged))
        
    def create_text_result_page (self, dir1, dir2, dest_dir, threshold):
        self.write_text_result_page (dest_dir + '/index.txt', threshold)
        
    def create_html_result_page (self, dir1, dir2, dest_dir, threshold):
        dir1 = dir1.replace ('//', '/')
        dir2 = dir2.replace ('//', '/')

        (changed, below, unchanged) = self.thresholded_results (threshold)


        html = ''
        old_prefix = os.path.split (dir1)[1]
        for link in changed:
            link.link_files_for_html (dir1, dir2, dest_dir) 
            link.write_html_system_details (dir1, dir2, dest_dir)
            
            html += link.html_record_string (dir1, dir2)


        short_dir1 = shorten_string (dir1)
        short_dir2 = shorten_string (dir2)
        html = '''<html>
<table rules="rows" border bordercolor="blue">
<tr>
<th>distance</th>
<th>%(short_dir1)s</th>
<th>%(short_dir2)s</th>
</tr>
%(html)s
</table>
</html>''' % locals()

        html += ('<p>')
        below_count = len (below)

        if below_count:
            html += ('<p>%d below threshold</p>' % below_count)
            
        html += ('<p>%d unchanged</p>' % len (unchanged))

        dest_file = dest_dir + '/index.html'
        open_write_file (dest_file).write (html)
        
    def print_results (self, threshold):
        self.write_text_result_page ('', threshold)

def compare_trees (dir1, dir2, dest_dir, threshold):
    data = ComparisonData ()
    data.compare_trees (dir1, dir2)
    data.print_results (threshold)

    if options.remove_changed:
        data.remove_changed (dir2, threshold)
        return
    
    if os.path.isdir (dest_dir):
        system ('rm -rf %s '% dest_dir)

    data.create_html_result_page (dir1, dir2, dest_dir, threshold)
    data.create_text_result_page (dir1, dir2, dest_dir, threshold)
    
################################################################
# TESTING

def mkdir (x):
    if not os.path.isdir (x):
        print 'mkdir', x
        os.makedirs (x)

def link_file (x, y):
    mkdir (os.path.split (y)[0])
    try:
        os.link (x, y)
    except OSError, z:
        print 'OSError', x, y, z
        raise OSError
    
def open_write_file (x):
    d = os.path.split (x)[0]
    mkdir (d)
    return open (x, 'w')


def system (x):
    
    print 'invoking', x
    stat = os.system (x)
    assert stat == 0


def test_paired_files ():
    print paired_files (os.environ["HOME"] + "/src/lilypond/scripts/",
                        os.environ["HOME"] + "/src/lilypond-stable/buildscripts/", '*.py')
                  
    
def test_compare_trees ():
    system ('rm -rf dir1 dir2')
    system ('mkdir dir1 dir2')
    system ('cp 20{-*.signature,.ly,.png,.eps,.log,.profile} dir1')
    system ('cp 20{-*.signature,.ly,.png,.eps,.log,.profile} dir2')
    system ('cp 20expr{-*.signature,.ly,.png,.eps,.log,.profile} dir1')
    system ('cp 19{-*.signature,.ly,.png,.eps,.log,.profile} dir2/')
    system ('cp 19{-*.signature,.ly,.png,.eps,.log,.profile} dir1/')
    system ('cp 19-1.signature 19-sub-1.signature')
    system ('cp 19.ly 19-sub.ly')
    system ('cp 19.profile 19-sub.profile')
    system ('cp 19.log 19-sub.log')
    system ('cp 19.png 19-sub.png')
    system ('cp 19.eps 19-sub.eps')

    system ('cp 20multipage* dir1')
    system ('cp 20multipage* dir2')
    system ('cp 19multipage-1.signature dir2/20multipage-1.signature')

    
    system ('mkdir -p dir1/subdir/ dir2/subdir/')
    system ('cp 19-sub{-*.signature,.ly,.png,.eps,.log,.profile} dir1/subdir/')
    system ('cp 19-sub{-*.signature,.ly,.png,.eps,.log,.profile} dir2/subdir/')
    system ('cp 20grob{-*.signature,.ly,.png,.eps,.log,.profile} dir2/')
    system ('cp 20grob{-*.signature,.ly,.png,.eps,.log,.profile} dir1/')

    ## introduce differences
    system ('cp 19-1.signature dir2/20-1.signature')
    system ('cp 19.profile dir2/20.profile')
    system ('cp 19.png dir2/20.png')
    system ('cp 19multipage-page1.png dir2/20multipage-page1.png')
    system ('cp 20-1.signature dir2/subdir/19-sub-1.signature')
    system ('cp 20.png dir2/subdir/19-sub.png')
    system ("sed 's/: /: 1/g'  20.profile > dir2/subdir/19-sub.profile")

    ## radical diffs.
    system ('cp 19-1.signature dir2/20grob-1.signature')
    system ('cp 19-1.signature dir2/20grob-2.signature')
    system ('cp 19multipage.midi dir1/midi-differ.midi')
    system ('cp 20multipage.midi dir2/midi-differ.midi')
    system ('cp 19multipage.log dir1/log-differ.log')
    system ('cp 19multipage.log dir2/log-differ.log &&  echo different >> dir2/log-differ.log &&  echo different >> dir2/log-differ.log')

    compare_trees ('dir1', 'dir2', 'compare-dir1dir2', 0.5)


def test_basic_compare ():
    ly_template = r"""

\version "2.10.0"
#(define default-toplevel-book-handler
  print-book-with-defaults-as-systems )

#(ly:set-option (quote no-point-and-click))

\sourcefilename "my-source.ly"
 
%(papermod)s
\header { tagline = ##f }
\score {
<<
\new Staff \relative c {
  c4^"%(userstring)s" %(extragrob)s
  }
\new Staff \relative c {
  c4^"%(userstring)s" %(extragrob)s
  }
>>
\layout{}
}

"""

    dicts = [{ 'papermod' : '',
               'name' : '20',
               'extragrob': '',
               'userstring': 'test' },
             { 'papermod' : '#(set-global-staff-size 19.5)',
               'name' : '19',
               'extragrob': '',
               'userstring': 'test' },
             { 'papermod' : '',
               'name' : '20expr',
               'extragrob': '',
               'userstring': 'blabla' },
             { 'papermod' : '',
               'name' : '20grob',
               'extragrob': 'r2. \\break c1',
               'userstring': 'test' },
             ]

    for d in dicts:
        open (d['name'] + '.ly','w').write (ly_template % d)
        
    names = [d['name'] for d in dicts]

    system ('lilypond -ddump-profile -dseparate-log-files -ddump-signatures --png -b eps ' + ' '.join (names))
    

    multipage_str = r'''
    #(set-default-paper-size "a6")
    \score {
      \relative {c1 \pageBreak c1 }
      \layout {}
      \midi {}
    }
    '''

    open ('20multipage', 'w').write (multipage_str.replace ('c1', 'd1'))
    open ('19multipage', 'w').write ('#(set-global-staff-size 19.5)\n' + multipage_str)
    system ('lilypond -dseparate-log-files -ddump-signatures --png 19multipage 20multipage ')
 
    test_compare_signatures (names)
    
def test_compare_signatures (names, timing=False):

    import time

    times = 1
    if timing:
        times = 100

    t0 = time.clock ()

    count = 0
    for t in range (0, times):
        sigs = dict ((n, read_signature_file ('%s-1.signature' % n)) for n in names)
        count += 1

    if timing:
        print 'elapsed', (time.clock() - t0)/count


    t0 = time.clock ()
    count = 0
    combinations = {}
    for (n1, s1) in sigs.items():
        for (n2, s2) in sigs.items():
            combinations['%s-%s' % (n1, n2)] = SystemLink (s1,s2).distance ()
            count += 1

    if timing:
        print 'elapsed', (time.clock() - t0)/count

    results = combinations.items ()
    results.sort ()
    for k,v in results:
        print '%-20s' % k, v

    assert combinations['20-20'] == (0.0,0.0,0.0)
    assert combinations['20-20expr'][0] > 0.0
    assert combinations['20-19'][2] < 10.0
    assert combinations['20-19'][2] > 0.0


def run_tests ():
    dir = 'test-output-distance'

    do_clean = not os.path.exists (dir)

    print 'test results in ', dir
    if do_clean:
        system ('rm -rf ' + dir)
        system ('mkdir ' + dir)
        
    os.chdir (dir)
    if do_clean:
        test_basic_compare ()
        
    test_compare_trees ()
    
################################################################
#

def main ():
    p = optparse.OptionParser ("output-distance - compare LilyPond formatting runs")
    p.usage = 'output-distance.py [options] tree1 tree2'
    
    p.add_option ('', '--test-self',
                  dest="run_test",
                  action="store_true",
                  help='run test method')
    
    p.add_option ('--max-count',
                  dest="max_count",
                  metavar="COUNT",
                  type="int",
                  default=0, 
                  action="store",
                  help='only analyze COUNT signature pairs')

    p.add_option ('', '--threshold',
                  dest="threshold",
                  default=0.3,
                  action="store",
                  type="float",
                  help='threshold for geometric distance')


    p.add_option ('--remove-changed',
                  dest="remove_changed",
                  default=False,
                  action="store_true",
                  help="Remove all files from tree2 that are over the threshold.")

    p.add_option ('--no-compare-images',
                  dest="compare_images",
                  default=True,
                  action="store_false",
                  help="Don't run graphical comparisons")

    p.add_option ('--create-images',
                  dest="create_images",
                  default=False,
                  action="store_true",
                  help="Create PNGs from EPSes")

    p.add_option ('-o', '--output-dir',
                  dest="output_dir",
                  default=None,
                  action="store",
                  type="string",
                  help='where to put the test results [tree2/compare-tree1tree2]')

    global options
    (options, a) = p.parse_args ()

    if options.run_test:
        run_tests ()
        sys.exit (0)

    if len (a) != 2:
        p.print_usage()
        sys.exit (2)

    name = options.output_dir
    if not name:
        name = a[0].replace ('/', '')
        name = os.path.join (a[1], 'compare-' + shorten_string (name))
    
    compare_trees (a[0], a[1], name, options.threshold)

if __name__ == '__main__':
    main()

