from unittest import TestCase
from tempfile import mkstemp

import sh
from reduc.stopspam.logfile import LogFile


class TestLogfile(TestCase):

    def setUp(self):
        file_, name = mkstemp()
        self.tmpfile = open(name, 'w')
        self.tmpfilename = name

    def tearDown(self):
        self.tmpfile.close()
        sh.rm(self.tmpfilename)
        try:
            sh.rm(self.tmpfilename + '.1')
        except:
            pass

    def test_first_read(self):
        """read() should return the whole content at the begining."""
        txt = 'a\nb\nc\n'
        self.tmpfile.write(txt)
        self.tmpfile.flush()
        log = LogFile(self.tmpfilename)
        self.assertEquals(log.read(), txt)

    def test_next_read(self):
        """read() should return the content added since last read()."""
        txt1 = 'a\nb\nc\n'
        self.tmpfile.write(txt1)
        self.tmpfile.flush()
        log = LogFile(self.tmpfilename)
        log.read()

        txt2 = 'd\ne\nf\n'
        self.tmpfile.write(txt2)
        self.tmpfile.flush()
        self.assertEquals(log.read(), txt2)

    def test_read_after_rotate(self):
        """read() should return the full content after rotation."""
        txt1 = 'a\nb\nc\n'
        self.tmpfile.write(txt1)
        self.tmpfile.flush()
        log = LogFile(self.tmpfilename)

        self.rotate()
        txt2 = 'd\ne\nf\n'
        self.tmpfile.write(txt2)
        self.tmpfile.flush()
        text = log.read()
        self.assertEquals(text, txt1 + txt2)

    def rotate(self):
        """rotates the log."""
        sh.mv(self.tmpfilename, self.tmpfilename + '.1')
        self.tmpfile.close()
        self.tmpfile = open(self.tmpfilename, 'w')
