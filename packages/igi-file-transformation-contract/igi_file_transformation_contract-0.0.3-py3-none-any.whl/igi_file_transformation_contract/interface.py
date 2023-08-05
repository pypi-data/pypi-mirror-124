"""
This is intended to serve as an interface for File Transformations. 
Specifically for attributes that are intended for use with a web UI.
We can then use a standard template and inject details from the 
specific transformation as we know the methods and properties available.
"""
from abc import ABC, abstractmethod, abstractproperty
from typing import Optional

from igi_file_transformation_contract.result import TransformationResult

UNASSIGNED_OUT_PATH = "<AutoAssign>"


class IFileTransformer(ABC):
    """
    Base class for IGI File Transformers. Acts as an interface/contract.

    Please note this interface specifies requirements for use in a web service.
    Additional methods e.g. for console use can be included in sub-classes, but
    are not required to implement this interface.
    """

    @abstractmethod
    def try_transform_file(
        self, in_path: str, out_path: str = UNASSIGNED_OUT_PATH, **kwargs
    ) -> TransformationResult:
        pass

    @abstractmethod
    def transform_file(
        self, in_path: str, out_path: str = UNASSIGNED_OUT_PATH, **kwargs
    ) -> str:
        pass

    @abstractproperty
    def title(self) -> str:
        pass

    @abstractproperty
    def user_description(self) -> str:
        """
        A user friendly description of the transformation that can be displayed on the
        webpage.
        """
        pass

    @abstractproperty
    def result_disclaimer(self) -> str:
        """
        E.g. We have tried to map the headers to the IGI property model correctly, but
        cannot anticipate all possible inputs, so please check the indication, uom etc
        assigned in the headers to ensure that you are happy with the mapping.
        Please send any corrections to ...
        """
        pass

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
