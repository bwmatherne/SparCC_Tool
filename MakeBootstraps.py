#!/usr/bin/env python

'''
@author: jonathanfriedman

Script for making simulated datasets used to get pseudo p-values.
'''
import os
from analysis_methods import permute_w_replacement
from io_methods import read_txt, write_txt
    
def kwargs_callback(option, opt, value, parser,**kwargs):
    d = kwargs['d']
    d[option.dest] = value
    return d

def make_bootstraps(counts, nperm, perm_template, outpath='./', iprint=0):
    '''
    Make n simulated datasets used to get pseudo p-values. 
    Simulated datasets are generated by assigning each OTU in each sample 
    an abundance that is randomly drawn (w. replacement) from the 
    abundances of the OTU in all samples. 
    Simulated datasets are either written out as txt files.

    Parameters
    ----------
    counts : DataFrame
        Inferred correlations whose p-values are to be computed.
    nperm : int
        Number of permutations to produce.
    perm_template : str
        Template for the permuted data file names.
        Should not include the path, which is specified using the 
        outpath parameter.
        The iteration number is indicated with a "#".
        For example: 'permuted/counts.permuted_#.txt'
    outpath : str (default './')
        The path to which permuted data will be written.
        If not provided files will be written to the cwd.
    iprint : int (default = 0)
        The interval at which iteration number is printed out.
        If iprint<=0 no printouts are made.
    '''
    if not os.path.exists(outpath): os.makedirs(outpath)
    for i in xrange(nperm):
        if iprint>0:
            if not i%iprint: print i
        counts_perm = permute_w_replacement(counts) 
        ## write out cors
        outfile = outpath + perm_template.replace('#', '%d'%i)
        write_txt(counts_perm, outfile)

def main(counts_file, nperm, perm_template, outpath='./'):
    '''
    Make n simulated datasets used to get pseudo p-values. 
    Simulated datasets are generated by assigning each OTU in each sample 
    an abundance that is randomly drawn (w. replacement) from the 
    abundances of the OTU in all samples. 
    Simulated datasets are either written out as txt files.
    '''
    if perm_template is None:
        perm_template = counts_file + '.permuted_#.txt'
    ## read counts data
    counts = read_txt(counts_file)
    ## make permutated data
    make_bootstraps(counts, nperm, perm_template, outpath=outpath)

if __name__ == '__main__':
    ## parse input arguments
    from optparse import OptionParser
    kwargs = {}
    usage  = ('Make n simulated datasets used to get pseudo p-values.\n' 
              'Simulated datasets are generated by assigning each OTU in each sample an abundance that is randomly drawn (w. replacement) from the abundances of the OTU in all samples.\n' 
              'Simulated datasets are either written out as txt files. \n'
              '\n'
              'Usage:   python MakeBootstraps.py counts_file [options]\n'
              'Example: python MakeBootstraps.py example/fake_data.txt -n 5 -t permutation_#.txt -p example/pvals/')
    parser = OptionParser(usage)
    parser.add_option("-n", dest="n", default=100, type = 'int',
                      help="Number of simulated datasets to create (100 default).")
    parser.add_option("-t", "--template", dest="perm_template", default=None, type = 'str',
                      help="The template for the permuted data file names.\n"
                           "Should not include the path, which is specified using the -p option.\n"
                           'The iteration number is indicated with a "#".\n'
                           "For example: 'permuted/counts.permuted_#.txt'" 
                           "If not provided a '.permuted_#.txt' suffix will be added to the counts file name.\n")
    parser.add_option("-p", "--path", dest="outpath", default='./', type = 'str',
                      help="The path to which permuted data will be written.\n" 
                           "If not provided files will be written to the cwd.\n")
    (options, args) = parser.parse_args()
    counts_file     = args[0]
    n               = options.n
    outpath         = options.outpath
    perm_template   = options.perm_template
    
    main(counts_file, n, perm_template, outpath)
    

