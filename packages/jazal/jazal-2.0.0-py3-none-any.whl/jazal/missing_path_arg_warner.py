from .path_checker import PathChecker
from .reactive_path_checker import ReactivePathChecker


class MissingPathArgWarner:
	"""
	This class's main purpose is to warn the programmer that a path was not
	provided to a function or a script as an argument. If a path is given, the
	class allows to instantiate PathChecker or ReactivePathChecker. This class
	needs the name of the argument that the path is the value of
	(property arg_name) and the extension that the path is supposed to have
	(property extension).
	"""

	def __init__(self, arg_name, extension):
		"""
		The constructor requires a path argument name and the file extension
		expected from the path.

		Args:
			arg_name (str): the name of a path argument
			extension (str): the extension expected from the path argument. It
				must start with a '.'. If the path is not supposed to have an
				extension, set this argument to an empty string.
		"""
		self._extension = extension
		self._arg_name = arg_name

	@property
	def arg_name(self):
		"""
		This read-only property is the name (str) of the path argument that may
		be missing.
		"""
		return self._arg_name

	@property
	def extension(self):
		"""
		This read-only property is the extension (str) that the path argument
		is supposed to have. If that path is not supposed to have an extension,
		this property is an empty string.
		"""
		return self._extension

	def make_missing_arg_msg(self):
		"""
		The message created by this method tells that the argument named
		<property arg_name>, the path to a file with extension <property
		extension>, is needed. It is relevant if the argument was not provided.

		Returns:
			str: a message telling that the argument is needed
		"""
		return self._arg_name + ": the path to a file with extension '"\
			+ self._extension + "' must be provided."

	def make_path_checker(self, path):
		"""
		Creates a PathChecker instance with property extension and the given
		file path.

		Args:
			path (pathlib.Path or str): the value of the path argument
				associated with this object

		Returns:
			PathChecker: an object able to verify the path argument's value
		"""
		return PathChecker(path, self._extension)

	def make_reactive_path_checker(self, path):
		"""
		Creates a ReactivePathChecker instance with properties extension and
		arg_name and the given file path.

		Args:
			path (pathlib.Path or str): the value of the path argument
				associated with this object

		Returns:
			ReactivePathChecker: an object able to verify the path argument's
				value
		"""
		return ReactivePathChecker(path, self._extension, self._arg_name)
