import sys
import os
import re
import argparse
import yaml
from copy import deepcopy
from lxml import etree
from msvcrt import getch
# Import custom modules
sys.path.append(os.path.abspath("..")) # make all Automation modules visible
from UEncoder import uencode # module for changing encoding and replacing ASCII HTML codes
from cis.logging import logging 


class CISParser(object):
    """
        CISParser is class with methods to process and manipulate with campaign xml from SAS Decision Services
        ```
        @param
        path : str - is single filename or directory name with xml files to process
        ```
        if directory specified - starts recursive processing all child directories
    """

    __ver__ = 'v1.0'

    def __init__(self, path, config=False, debug=False):
        """ Init method of class """
        self.files = self._checkpath(path)
        self.batch = len(self.files)
        self._logconfig(path, config, debug, self.batch, self.__ver__)
        if self.batch == 0:
            self.soft_exit(1, f'CISParser(): no files found by path: {path}')
        self.marked_nodes = set()

# -------------------------- static class methods ------------------------- #

    @staticmethod
    def soft_exit(exitcode=0, msg=''):
        """ Simple exit method with pause """
        if exitcode and msg:
            logging.error(msg)
        elif msg:
            logging.info(msg)
        logging.debug(f'ExitCode: {exitcode}\nExitMessage {msg}')
        print('\nPress any key to exit...')
        getch()
        sys.exit(exitcode)

# ------------------------- private class methods ------------------------- #

    def _checkpath(self, path):
        """ 
            Checks `path : str` for directory and existance 
            ```
            @return
            files : list of files to process 
            ``` 
        """
        files = []
        if os.path.isdir(path):
            for r,_,f in os.walk(path):
                for file in f:
                    if file.endswith('.xml'):
                        files.append(f"{r.replace(os.sep, '/')}/{file}")
        elif os.path.exists(path) and path.endswith('.xml'):
            files.append(path)
        return files

    def _logconfig(self, path, config, debug_flag, files_num, ver):
        """ Configurates logging class """
        logging()
        logging.debug_flag = debug_flag
        logging.add_header(logging, path, config, files_num, ver)

# -------------------- files processing static methods -------------------- #

    @staticmethod
    def get_filename(path):
        """ Returns the final component of path without extension """
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def get_file_data(filepath, codec='utf-8'):
        """ Returns read data from file """
        with open(filepath, 'r', encoding=codec) as f:
            return f.read()

    @staticmethod
    def rewrite_file(filename, data, codec='utf-8', comment=''):
        """ Rewrites file with data """
        logging.debug(f'Rewriting {filename} with new data {comment}')
        with open(filename, 'w', encoding=codec) as tmpfile:
            tmpfile.write(data)

# ------------------- cis raw format processing methods ------------------- #

    def del_xmlns(self, data):
        """ Removes xmlns attributes from data if exists """
        data = re.sub(r'\s*xmlns="[^"]*"\s*', '', data)
        return data

    def del_meta(self, data):
        """ Returns data with removed metadata """
        real_data = re.search('<FlowDefinition.*FlowDefinition>', data, flags=re.S)
        if real_data:
            data = real_data.group(0)
        else:
            self.soft_exit(1, 'CISParser::del_meta(): No FlowDefinition node found')
        return data

    def to_real_xml(self, file):
        """ Converts `file` to real xml format visible for parser """
        logging.info(f'Converting data of {self.get_filename(file)} to real xml fromat')
        data = self.get_file_data(file)
        data = self.del_meta(data)
        data = self.del_xmlns(data)
        self.rewrite_file(file, data, comment='real_xml')
        logging.info('Converted!')

# --------------------- cis xml iterate nodes methods --------------------- #

    def get_nodes_by_tag(self, subtree, nametag, pos=''):
        """ 
            Returns list of nodes from subtree by tag and position 
            ```
            @param
            subtree : etree     - xml sub tree where tag is searching
            nametag : str       - tag to search
            pos     : str|int   - tag selection position (exm: '<2' '>=3', 4)
            ```
        """
        if pos:
            pos = '=' + str(pos) if str(pos)[0].isdigit() else str(pos)
        nodes = subtree.xpath(f'./descendant::{nametag}[position(){pos}]')
        return nodes

    def get_node_by_id(self, id_node):
        """ Returns xml node by attribute id `@name` """
        node = self.tree.xpath(f"//*[@name='{id_node}']")
        if len(node) == 0:
            logging.error(f'No node by id ({id_node}) found')
            return -1
        if len(node) > 1:
            logging.error(f'More than one id ({id_node}) found, return first')
        return node[0]

    def get_node_id(self, node):
        """ Returns attribute `@name` of node if exists otherwise -1 """ 
        node_id = node.xpath(f"./@name")
        if node_id:
            return node_id[0]
        logging.error(f'No id for node {node.tag} found')
        return -1

    def get_node_next_ids(self, node):
        """ Returns list of destination node ids """ 
        ids = []
        for s in node.xpath('./descendant::DestinationNodeName'):
            ids.append(s.text)
        ids.sort()
        logging.debug(f"({node.tag}) {node.attrib['name']} → {ids}")
        if len(ids) == 0:
            logging.debug(f'No next ids found for {node}')
        return ids

    def get_next_nodes(self, node):
        """ Returns list destination nodes """
        ids = self.get_node_next_ids(node)
        next_nodes = []
        for i in ids:
            next_nodes.append(self.get_node_by_id(i))
        return next_nodes

    def get_nodes_group(self, node):
        """ Returns list of nodes with same `id_number_#` group """
        gnodes = []
        curid = self.get_node_id(node)
        if '_' in curid:
            return gnodes
        gnodes.append(node)
        while 1:
            next_ids = self.get_node_next_ids(node)
            if not next_ids or len(next_ids) > 1 or '_' not in next_ids[0]:
                break
            node = self.get_node_by_id(next_ids[0])
            gnodes.append(node)
            if len(gnodes) == 100:
                self.soft_exit(1, f'CISParser::get_nodes_group(): {len(gnodes)} nodes in one group, possible endless loop for {curid}')
        return gnodes

    def get_start_node(self):
        """ Returns start node by tag `StartNode` """
        start = self.tree.xpath('//StartNode')
        if not start:
            self.soft_exit(1, 'CISParser::get_start_node(): No campaign StartNode found!') 
        return start[0]

# ------------------- cis xml parse & generate methods -------------------- #

    def clean_meta_names(self):
        """ Cleans meta names if exists human readable attribute """
        logging.debug('Remove all meta names')
        for elem in self.tree.xpath('//*[@name and @displayName]'):
            del elem.attrib['name']
    
    def remove_node(self, cur_node, nametag='', pos=''):
        """ Removes nodes from cur_node by tag and position or cur_node itself """
        removed = []
        if nametag:
            nodes = self.get_nodes_by_tag(cur_node, nametag, pos)
            for n in nodes:
                logging.debug(f'Remove node {n} by condition {cur_node}|{nametag}|{pos}')
                n.getparent().remove(n)
                removed.append(n)
        else:
            logging.debug(f'Remove node {cur_node.tag}')
            cur_node.getparent().remove(cur_node)
            removed.append(cur_node)
        return removed

    def swap_nodes(self, node_1, node_2):
        """ Swaps nodes places """
        logging.debug(f'Swap nodes: {node_1.tag} ↔ {node_2.tag}')
        node_1.addnext(deepcopy(node_2))
        node_2.addnext(node_1)
        self.remove_node(node_2)

    def sort_campaign(self, cur_node):
        """ Sorts cis campaign in unique way """
        next_nodes = self.get_next_nodes(cur_node)
        self.marked_nodes.add(cur_node)
        if next_nodes:
            for node in next_nodes:
                if node not in self.marked_nodes:
                    cur_node.addnext(node)
                    self.sort_campaign(node)

    def save_xml(self, tree, tofile, encoding='utf-8'):
        """ Saves `tree` to xml file """
        if not tree:
            logging.error('save_xml: No tree found')
            return
        dirname = os.path.dirname(tofile)
        if not os.path.exists(dirname):
                os.mkdir(dirname)
        logging.info(f'Save builded xml tree to file {tofile}')
        tree.write(tofile, pretty_print=True, xml_declaration=True, encoding=encoding)

    def build_tree(self, nodes, sort_nodes=False, rootname='root', attribs={}, copy=False):
        """ 
            Builds new xml tree by nodes
            ```
            @params
            nodes       - list of elements of building tree
            sort_nodes  - sorting nodes by @name
            rootname    - name of root element 
            attribs     - node attributes
            copy        - deepcopy nodes
            ```
        """
        if not nodes:
            logging.info(f'Nothing to build for {rootname} tree, nodes list is empty')
            return None
        if sort_nodes:
            nodes.sort(key=lambda x: x.attrib['name'])
        root = etree.Element(rootname)
        for k, v in attribs.items():
            root.attrib[k] = v 
        tree = etree.ElementTree(root)
        for node in nodes:
            if copy:
                root.append(deepcopy(node))
            else:
                root.append(node)
        return tree, root

    def wrap_nodes(self, nodes, wraptag, attribs={}):
        """ Create tag around list of nodes with attributes """
        attribs_copy = deepcopy(attribs)
        if 'name' in attribs_copy:
            attribs_copy['name'] = attribs_copy['name'] + '_group'
        _, wrapped_node = self.build_tree(nodes, rootname=wraptag, attribs=attribs_copy, sort_nodes=False, copy=True)
        nodes[0].getprevious().addnext(wrapped_node)
        for n in nodes:
            n.getparent().remove(n)
        return wrapped_node

    def wrap_campaign(self, node):
        logging.info('Wrapping campaign starts')
        while node is not None:
            gnodes = self.get_nodes_group(node)
            if len(gnodes) > 1:
               node = self.wrap_nodes(gnodes, "StrategyNode", node.attrib)
            node = node.getnext()
        logging.info('Wrapped!')

    def detach_nodes(self, file, subtree, nametag='', pos='', sort_nodes=True):
        """ Detachs specific nodes from subtree and build new tree with them """
        logging.info(f'Detachs {nametag} starts')
        nodes = self.get_nodes_by_tag(subtree, nametag, pos)
        rootname = f"{nametag}s"
        tree, _ = self.build_tree(nodes, sort_nodes=sort_nodes, rootname=rootname, copy=False)
        self.save_xml(tree, f'{file[:-4]}/{nametag}.xml')

    def parse_raw_xml(self, file):
        """ Inits parser and starts parsing cis xml `file` """
        logging.info(f'Parsing file {self.get_filename(file)}')
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(file, parser)
        self.start_node = self.get_start_node()
        self.detach_nodes(file, self.tree, 'ProcessVariable')
        logging.info(f'Parsed!')

# -------------------------- cis magic converter -------------------------- #

    def magic_converter(self, encode=True, to_real_xml=True, parse_raw=True, sort_camp=True, wrap_camp=True):
        """
            Convering raw dummy xml from Decision Services to cool and smart xml format
            ```
            @params
            encode      : bool  - changing encoding to UTF-8 and removing ascii codes
            to_real_xml : bool  - removing meta data
            parse_raw   : bool  - parsing xml and modify format
            sort_camp   : bool  - sorting xml nodes by id
            wrap_camp   : bool  - wrapping group of nodes with StrategyNode
            ```
        """
        logging.info('CISParser: start magic processing')
        logging.debug(f"Parametrs: \n{'-'*20} \
                \nencode      : {encode} \
                \nto_real_xml : {to_real_xml} \
                \nparse_raw   : {parse_raw} \
                \nsort_camp   : {sort_camp} \n{'-'*20} \
                \nwrap_camp   : {wrap_camp} \n{'-'*20}")
        for file in self.files:
            logging.info(f'Process: {file}')
            if encode:
                logging.info('Start encoding utf-8 unescape=False')
                uencode.encode(file, 'utf-8', unescape=False) 
            if to_real_xml:
                self.to_real_xml(file)
            if parse_raw:
                self.parse_raw_xml(file)
            if sort_camp:
                logging.info(f'Sorting campaign {file}')
                self.sort_campaign(self.start_node)
                logging.info(f'Sorted!')
            if wrap_camp:
                self.wrap_campaign(self.start_node)
         
            self.save_xml(self.tree, file)

            if encode:
                logging.info('Start encoding utf-8 unescape=True')
                uencode.encode(file, 'utf-8', unescape=True)
            logging.info(f"Processed {file}! \n{'-'*100}")
        logging.info('CISParser: magic processing ended!')
        logging.add_footnote(logging)

# ------------------------- end of CISParser class ------------------------ #

def create_config(config):
    if not config.endswith('.yaml'): 
        CISParser.soft_exit(1, f'{config} file has not .yaml extension')

    if os.path.exists(config):
        CISParser.soft_exit(0, f'{config} file already exists')
    
    logging.info('Creating config template...')
    with open(config, 'w') as conf:
        conf.write(f"# Config file for CISParser \n")
        conf.write("# ----------------------------------- # \n")
        conf.write("debug: False   # Launch in debug mode \n")
        conf.write("# ----------------------------------- # \n")
        conf.write("path:   './'   # Set path to process \n")
        conf.write("config: True   # Path to config file \n")
        conf.write("encode: True   # Do not change encoding of files to UTF-8 and remove ASCII codes \n")
        conf.write("xml:    True   # Do not delete metadata and convert to real xml format \n")
        conf.write("parse:  True   # Do not parse CIS xml \n")
        conf.write("sort:   True   # Do not sort CIS campaign \n")
        conf.write("wrap:   True   # Do not wrap groups of nodes")
    logging.info(f'Created config template {config}')

def parse_conf(args):
    """ Parses config.yaml file if exists. Create with --config in args """
    if args.config:
        create_config('config.yaml')
        CISParser.soft_exit(0)
    if not os.path.exists('config.yaml'):
        return args

    with open('config.yaml', 'r') as stream:
        y = yaml.load(stream)
        try:
            args.config = True
            args.debug = y['debug']
            args.path = y['path']
            args.no_encode = y['encode']
            args.no_xml = y['xml']
            args.no_parse = y['parse']
            args.no_sort = y['sort']
            args.no_wrap = y['wrap']
        except KeyError as e:
            CISParser.soft_exit(1, f'Config unexpected key {e}')
    return args

def usage():
    """ Parse command line arguents """
    parser = argparse.ArgumentParser(description='CIS Parser')
    parser.add_argument('-p','--path', type=str, help='Set path to process. Default is current directory', default='./')
    parser.add_argument('--debug', help='Launch in debug mode', action='store_true')
    parser.add_argument('--no-encode', help='Do not change encoding to UTF-8 and remove ASCII codes', action='store_false')
    parser.add_argument('--no-xml', help='Do not delete metadata and convert to real xml format', action='store_false')
    parser.add_argument('--no-parse', help='Do not parse CIS xml', action='store_false')
    parser.add_argument('--no-sort', help='Do not sort CIS campaign', action='store_false')
    parser.add_argument('--no-wrap', help='Do not wrap groups of nodes', action='store_false')
    parser.add_argument('--config', help='Set to create config.yaml file in current directory. \
                                        If once created - starts parsing config by default', action='store_true')
    return parser.parse_args()

def main():
    """ Start function - launching CISParser magic processing on path """
    args = usage()
    args = parse_conf(args)
    cisparser = CISParser(args.path, config=args.config, debug=args.debug)
    s = input('Start processing? [y/n] ')
    if not s == 'y':
        sys.exit(0)
    cisparser.magic_converter(encode=args.no_encode, to_real_xml=args.no_xml,
                             parse_raw=args.no_parse, sort_camp=args.no_sort, wrap_camp=args.no_wrap)
    cisparser.soft_exit(0)

if __name__ == "__main__":
    logging() # init colorama
    main()
