from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import PluginError
import os
import glob
import codecs
import logging
from pypugjs.ext.jinja import Compiler
from pypugjs import process


class MkDocsPug(BasePlugin):

    def on_pre_build(self, config):
        # some code to clean things up
        try:
            for root in config['theme'].dirs:
                for fname in glob.glob(os.path.join(root, '**.pug')):
                    with codecs.open(fname, mode='r', encoding='utf-8') as f:
                        template = f.read()
                    output = process(
                        template,
                        compiler=Compiler,
                        staticAttrs=True,
                        extension='.html',
                    )
                    fout = fname.replace('.pug', '.html')
                    if os.path.isfile(fout):
                        # this is to prevent infinite build loops because we synthesize html files
                        with codecs.open(fout, mode='r', encoding='utf-8') as f:
                            if f.read() == output:
                                # nothing to update
                                continue
                    with codecs.open(fout, mode='w', encoding='utf-8') as f:
                        f.write(output)
                    logging.info('built {}'.format(fout))
        except Exception as e:
            raise PluginError(str(e))
