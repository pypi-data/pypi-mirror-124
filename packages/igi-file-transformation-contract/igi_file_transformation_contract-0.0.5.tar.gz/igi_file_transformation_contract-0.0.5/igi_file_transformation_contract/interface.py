"""
This is intended to serve as an interface for File Transformations. 
Specifically for attributes that are intended for use with a web UI.
We can then use a standard template and inject details from the 
specific transformation as we know the methods and properties available.
"""
from abc import ABC, abstractmethod, abstractproperty
import os
from typing import Optional

from igi_file_transformation_contract.result import TransformationResult


class IFileTransformer(ABC):
    """
    Base class for IGI File Transformers. Acts as an interface/contract.

    Please note this interface specifies requirements for use in a web service.
    Additional methods e.g. for console use can be included in sub-classes, but
    are not required to implement this interface.
    """

    @abstractproperty
    def title(self) -> str:
        pass

    @abstractproperty
    def user_description(self) -> str:
        """
        A user friendly description of the task that can be displayed on the webpage.
        """
        pass

    @abstractmethod
    def try_transform_file(self, in_path: str, out_path: str, **kwargs) -> TransformationResult:
        pass

    @abstractmethod
    def transform_file(self, in_path: str, out_path: str, **kwargs) -> str:
        pass

    @abstractproperty
    def result_disclaimer(self) -> str:
        """
        Advice on what to check in output etc.
        """
        pass

    @property
    def target_file_ext(self) -> str:
        """
        Extention for target output file - any overrides should include the . prefix
        """
        return '.xlsx'

    @property
    def user_description_image_uri(self) -> Optional[str]:
        """
        Optional image uri to be displayed with user description.
        """
        return None

    @property
    def result_disclaimer_image_uri(self) -> Optional[str]:
        """
        Optional image uri to be displayed with result disclaimer.
        """
        return None

    def has_user_description_image(self) -> bool:
        return bool(self.user_description_image_uri)

    def has_result_disclaimer_image_uri(self) -> bool:
        return bool(self.result_disclaimer_image_uri)

    def get_default_output_path(self, in_path, suffix: str='_transformed') -> str:
        directory, filename = os.path.split(in_path)
        output_filename = self.get_default_output_filename(filename, suffix)
        return os.path.join(directory, output_filename)

    def get_default_output_filename(self, in_fname: str, suffix: str='_transformed') -> str:
        base_name, _ = os.path.splitext(in_fname)
        out_fname = f"{base_name}{suffix}{self.target_file_ext}"
        return out_fname
