import os
from xml.etree import ElementTree
from doxygen_snippets.node import Node
from doxygen_snippets.constants import Kind, Visibility
from doxygen_snippets.cache import Cache
from doxygen_snippets.xml_parser import XmlParser


class Doxygen:
	def __init__(self, index_path: str, parser: XmlParser, cache: Cache, options: dict = {}, debug: bool = False):
		self.debug = debug
		path = os.path.join(index_path, 'index.xml')
		if self.debug:
			print('Loading XML from: ' + path)
		xml = ElementTree.parse(path).getroot()

		self.parser = parser
		self.cache = cache
		self.options = options

		self.root = Node('root', None, self.cache, self.parser, None, options=self.options)
		self.groups = Node('root', None, self.cache, self.parser, None, options=self.options)
		self.files = Node('root', None, self.cache, self.parser, None, options=self.options)
		self.pages = Node('root', None, self.cache, self.parser, None, options=self.options)

		for compound in xml.findall('compound'):
			kind = Kind.from_str(compound.get('kind'))
			refid = compound.get('refid')
			if kind.is_language():
				node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root,
							options=self.options)
				node._visibility = Visibility.PUBLIC
				self.root.add_child(node)
			if kind == Kind.GROUP:
				node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root,
							options=self.options)
				node._visibility = Visibility.PUBLIC
				self.groups.add_child(node)
			if kind == Kind.FILE or kind == Kind.DIR:
				node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root,
							options=self.options)
				node._visibility = Visibility.PUBLIC
				self.files.add_child(node)
			if kind == Kind.PAGE:
				node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root,
							options=self.options)
				node._visibility = Visibility.PUBLIC
				self.pages.add_child(node)

		if self.debug:
			print('Deduplicating data... (may take a minute!)')
		for i, child in enumerate(self.root.children.copy()):
			self._fix_duplicates(child, self.root, [])

		for i, child in enumerate(self.groups.children.copy()):
			self._fix_duplicates(child, self.groups, [Kind.GROUP])

		for i, child in enumerate(self.files.children.copy()):
			self._fix_duplicates(child, self.files, [Kind.FILE, Kind.DIR])

		self._fix_parents(self.files)

		if self.debug:
			print('Sorting...')
		self._recursive_sort(self.root)
		self._recursive_sort(self.groups)
		self._recursive_sort(self.files)
		self._recursive_sort(self.pages)

	def _fix_parents(self, node: Node):
		if node.is_dir or node.is_root:
			for child in node.children:
				if child.is_file:
					child._parent = node
				if child.is_dir:
					self._fix_parents(child)

	def _recursive_sort(self, node: Node):
		node.sort_children()
		for child in node.children:
			self._recursive_sort(child)

	def _is_in_root(self, node: Node, root: Node):
		for child in root.children:
			if node.refid == child.refid:
				return True
		return False

	def _remove_from_root(self, refid: str, root: Node):
		for i, child in enumerate(root.children):
			if child.refid == refid:
				root.children.pop(i)
				return

	def _fix_duplicates(self, node: Node, root: Node, filter: [Kind]):
		for child in node.children:
			if len(filter) > 0 and child.kind not in filter:
				continue
			if self._is_in_root(child, root):
				self._remove_from_root(child.refid, root)
			self._fix_duplicates(child, root, filter)

	def print(self):
		if self.debug:
			print('\n')
			print("Print root")
			for node in self.root.children:
				self.print_node(node, '')
			print('\n')

			print("Print groups")
			for node in self.groups.children:
				self.print_node(node, '')
			print('\n')

			print("Print files")
			for node in self.files.children:
				self.print_node(node, '')

	def print_node(self, node: Node, indent: str):
		if self.debug:
			print(indent, node.kind, node.name)
		for child in node.children:
			self.print_node(child, indent + '  ')
