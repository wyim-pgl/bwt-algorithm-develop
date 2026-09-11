"""Negative tests run validators in throwaway trees; no deposited file is edited."""
import subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path.cwd()
class Guards(unittest.TestCase):
    def run_case(self,change,main=False):
        with tempfile.TemporaryDirectory() as d:
            tmp=Path(d)
            for path in ROOT.iterdir():
                if path.name not in ('manuscript.md','supplementary.md','.git'):
                    (tmp/path.name).symlink_to(path,target_is_directory=path.is_dir())
            for name in ('manuscript.md','supplementary.md'):
                text=(ROOT/name).read_text()
                if (name=='manuscript.md')==main:text=change(text)
                (tmp/name).write_text(text)
            result=subprocess.run([sys.executable,str(ROOT/'docs/2026-09-10-appnote/check_conversion.py')],cwd=tmp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            return result.returncode
    def test_valid(self):self.assertEqual(self.run_case(lambda s:s),0)
    def test_changed_cell(self):
        self.assertNotEqual(self.run_case(lambda s:s.replace('| 962,837 |','| 962,838 |',1)),0)
    def test_duplicate_row(self):
        def dup(s):
            row=next(l for l in s.splitlines(keepends=True) if l.startswith('| TRF | 962,837 |'))
            return s.replace(row,row+row,1)
        self.assertNotEqual(self.run_case(dup),0)
    def test_changed_command(self):self.assertNotEqual(self.run_case(lambda s:s.replace('MAXP -ngs -h','MAXP -ngs -x',1)),0)
    def test_changed_minus_sign(self):self.assertNotEqual(self.run_case(lambda s:s.replace('−17.84','17.84',1)),0)
    def test_duplicate_caption(self):self.assertNotEqual(self.run_case(lambda s:s.replace('**Supplementary Table S1.','**Supplementary Table S2.',1)),0)
    def test_deleted_caveat(self):self.assertNotEqual(self.run_case(lambda s:s.replace('These observations do not establish matched cross-tool speedups.',''),True),0)
if __name__=='__main__':unittest.main()
