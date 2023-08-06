"""__main__.py: 
Entry point for this package.
"""
   
__author__      = "HarshaRani"
__copyright__   = "Copyright 2021 HillTau, NCBS"
__maintainer__  = "HarshaRani"
__email__       = "hrani@ncbs.res.in"

def run():
    from HillTau.CppCode import hillTau
    hillTau.main()

def run_htgraph():
    from HillTau import htgraph
    htgraph.main()

def run_ht2sbml():
    from HillTau import ht2sbml
    ht2sbml.main() 

def run_mash():
    from HillTau import mash
    mash.main()
     
if __name__ == '__main__':
    run()
    

