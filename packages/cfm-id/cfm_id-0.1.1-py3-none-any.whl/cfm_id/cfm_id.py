from pathlib import Path
from typing import Optional, Tuple, List, Union
from abc import ABC, abstractmethod
from collections.abc import Iterable
import subprocess
import shlex
from matchms import Spectrum
from .config import config, CFMID_PATH, CFMID_IMAGE
from .matchms import load_from_cfm_id


class CfmIdBase(ABC):
    def __init__(
        self,
        cfm_id_cmd: Optional[str] = None,
        param: List[str] = ["param_output.log"],
        conf: List[str] = ["param_config.txt"],
    ):
        cfm_id_cmd = cfm_id_cmd or config.get(self.get_path_env_key())
        self.cfm_id_cmd = cfm_id_cmd
        self.param_path = Path(*param)
        self.conf_path = Path(*conf)

    @abstractmethod
    def get_path_env_key(self) -> str:
        """
        Returns:
            Key of environement variable to use for path
        """

    @abstractmethod
    def get_cmd(self, name: str) -> str:
        """
        Args:
            name: name of command to execute such as 'cfm-predict'
        Returns:
            Path to execute cfm-id command
        """

    @abstractmethod
    def get_params(self) -> Tuple[str, str]:
        """
        Args:
            name: name of command to execute such as 'cfm-predict'
        Returns:
            Path to execute cfm-id command
        """

    def predict(
        self,
        smiles: Union[str, List[str]],
        prob_thresh_for_prune: float = 0.001,
        include_annotations: bool = False,
        raw_format: bool = False,
    ) -> Union[str, List[Spectrum]]:
        if isinstance(smiles, str):
            return self._predict_single(
                smiles, prob_thresh_for_prune, include_annotations, raw_format
            )
        elif isinstance(smiles, Iterable):
            if raw_format:
                raise AttributeError(
                    "Raw format option is available only for single smiles"
                )
            spectra: List[Spectrum] = []
            for sm in smiles:
                spectra += self._predict_single(
                    sm, prob_thresh_for_prune, include_annotations, raw_format=False
                )
            return spectra
        else:
            raise AttributeError("smiles must be a str or an iterable of str")

    def _predict_single(
        self,
        smiles: str,
        prob_thresh_for_prune: float,
        include_annotations: bool,
        raw_format: bool,
    ) -> Union[str, List[Spectrum]]:
        raw_text = self._predict_raw_text(
            smiles, prob_thresh_for_prune, include_annotations
        )
        metadata = {
            "SMILES": smiles,
        }
        if raw_format:
            return raw_text
        spectra = load_from_cfm_id(raw_text, metadata=metadata)
        return spectra

    def _predict_raw_text(
        self, smiles: str, prob_thresh_for_prune: float, include_annotations: bool
    ) -> str:
        bin_path = self.get_cmd("cfm-predict")
        cmd = [
            *shlex.split(str(bin_path)),
            smiles,
            str(prob_thresh_for_prune),
            *self.get_params(),
            str(int(include_annotations)),
        ]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        return stdout.decode()


class CfmId(CfmIdBase):
    def get_path_env_key(self) -> str:
        return CFMID_PATH

    def get_cmd(self, name: str) -> str:
        return str(Path(self.cfm_id_cmd, name))

    def get_params(self) -> Tuple[str, str]:
        return (
            str(Path(self.cfm_id_cmd) / self.param_path),
            str(Path(self.cfm_id_cmd) / self.conf_path),
        )


class CfmIdDocker(CfmIdBase):
    def get_path_env_key(self) -> str:
        return CFMID_IMAGE

    def get_cmd(self, name: str) -> str:
        return f"docker run {self.cfm_id_cmd} {name}"

    def get_params(self) -> Tuple[str, str]:
        return (str(self.param_path), str(self.conf_path))
