from pathlib import Path
from .path_util import\
	extension_to_str,\
	get_file_stem


class PathChecker:
	"""
	This class contains a pathlib.Path object (property path) and the extension
	that the path is supposed to have (property extension). PathChecker can
	verify whether the path has the right extension, whether it exists and
	whether it is a directory or a file.

	In Pathlib, a file's stem is defined as its name without the extension's
	last suffix. In this class, however, a stem is a file name without the
	extension.
	"""

	def __init__(self, a_path, extension):
		"""
		The constructor needs a file path and the expected extension. If a_path
		is a string, it will be converted to a pathlib.Path object. If it is of
		type pathlib.Path, the instance will store its reference. The expected
		extension must start with a '.'.

		Args:
			a_path (pathlib.Path or str): the path that this instance will
				check
			extension (str): the extension that the path is supposed to have.
				If the path is not supposed to have an extension, set this
				argument to an empty string.

		Raises:
			TypeError: if a_path is not an instance of str or pathlib.Path
		"""
		self._extension = extension
		self._set_path(a_path)

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False

		return self._path == other._path\
			and self._extension == other._extension

	def __repr__(self):
		return self.__class__.__name__ + "('" + str(self._path) + "', '"\
			+ self._extension + "')"

	@property
	def extension(self):
		"""
		This read-only property is the extension (str) that path is supposed to
		have. If path is not supposed to have an extension, this property is an
		empty string.
		"""
		return self._extension

	def extension_is_correct(self):
		"""
		Indicates whether path's extension matches the expected extension.

		Returns:
			bool: True if path has the right extension, False otherwise
		"""
		return extension_to_str(self._path) == self._extension

	def get_file_name(self):
		"""
		Provides the name of the file that path points to.

		Returns:
			str: the name of the file that path points to
		"""
		return self._path.name

	def get_file_stem(self):
		"""
		Provides the stem of the file that path points to. A file's stem is its
		name without the extension.

		Returns:
			str: the stem of the file that path points to
		"""
		return get_file_stem(self._path)

	@property
	def path(self):
		"""
		This read-only property is the path (pathlib.Path) that this object
		checks.
		"""
		return self._path

	def path_exists(self):
		"""
		Indicates whether path points to an existent directory or file.

		Returns:
			bool: True if path exists, False otherwise
		"""
		return self._path.exists()

	def path_is_dir(self):
		"""
		Indicates whether path points to a directory.

		Returns:
			bool: True if path exists and is a directory, False otherwise
		"""
		return self._path.is_dir()

	def path_is_file(self):
		"""
		Indicates whether path points to a file.

		Returns:
			bool: True if path exists and is a file, False otherwise
		"""
		return self._path.is_file()

	def _set_path(self, a_path):
		"""
		Sets the path checked by this object. If a_path is a string, it will
		be converted to a pathlib.Path object. If it is of type pathlib.Path,
		this instance will store its reference.

		Args:
			a_path (pathlib.Path or str): the path that this object must check

		Raises:
			TypeError: if a_path is not an instance of pathlib.Path or str
		"""
		if isinstance(a_path, Path):
			self._path = a_path

		elif isinstance(a_path, str):
			self._path = Path(a_path)

		else:
			raise TypeError(
				"The given path must be an instance of pathlib.Path or str.")
