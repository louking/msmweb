#!/usr/bin/python
###########################################################################################
#   applytemplate - apply a template to files in a directory
#
#   Date        Author      Reason
#   ----        ------      ------
#   04/21/13    Lou King    Create
#
#   Copyright 2013 Lou King
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###########################################################################################
'''
applytemplate - apply a template to files in a directory
===================================================
'''

# standard
import pdb
import argparse
import glob
import os.path
import ConfigParser

# pypi
import pystache

# github

# other

# home grown
#import version

TEMPLATESEC = 'template'
SUBSEC = 'substitutions'

#----------------------------------------------------------------------
def main():
#----------------------------------------------------------------------
    '''
    add key to key file
    '''

    #parser = argparse.ArgumentParser(version='{0} {1}'.format('loutilities',version.__version__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--extension',help='extension for files to be processed (default %(default)s)',default='htmli')
    args = parser.parse_args()
    
    # act on arguments
    extension = args.extension

    # get list of files with indicated extension
    files = glob.glob('*.{}'.format(extension))
    
    # process each file
    for f in files:
        # file is a config file
        cfg = ConfigParser.ConfigParser()
        cfg.read(f)
        
        templatefile = cfg.get(TEMPLATESEC,'templatefile')
        outputdir = cfg.get(TEMPLATESEC,'outputdir')
        outputext = cfg.get(TEMPLATESEC,'outputext')
        
        # determine output path
        thisbase,thisext = os.path.splitext(f)
        outputfile = thisbase + '.' + outputext
        outputpath = os.path.join(outputdir,outputfile)
        
        # each option within SUBSEC represents a substitution from the template file
        substitutions = {}
        for sub in cfg.options(SUBSEC):
            substitutions[sub] = cfg.get(SUBSEC,sub)
            
        # read the template and make the substitutions
        TEMPLATE = open(templatefile)
        template = TEMPLATE.read()
        outstring = pystache.render(template,**substitutions)
        TEMPLATE.close()
        
        # check if the file needs to be updated
        # update is needed if this is a new file, or if it has changed
        updateneeded = True
        if os.path.exists(outputpath):
            CURR = open(outputpath)
            curr = CURR.read()
            CURR.close()
            # if file hasn't change, squelch update
            if curr == outstring:
                updateneeded = False
            
        # update file, if new, or if it's changed
        if updateneeded:
            OUT = open(outputpath,'w')
            OUT.write(outstring)
            OUT.close()

# ###############################################################################
# ###############################################################################
if __name__ == "__main__":
    main()

