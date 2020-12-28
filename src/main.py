from typing import Type

import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import get_class, instantiate
from omegaconf import OmegaConf

from backends import Backend
from backends.pytorch import PyTorchConfig
from config import BenchmarkConfig

# Register configurations
cs = ConfigStore.instance()
cs.store(name="benchmark", node=BenchmarkConfig)
cs.store(group="backend", name="pytorch", node=PyTorchConfig)
cs.store(group="backend", name="torchscript", node=PyTorchConfig)


# def factory(config: BenchmarkConfig) -> Backend:
#     if config.backend.name == PyTorchBackend.NAME:
#         return PyTorchBackend(config.model)
#     else:
#         raise ValueError(
#             f"Unknown backend {config.backend.name} "
#             f"possible values are {[PyTorchBackend.NAME]}"
#         )


@hydra.main(config_path="../configs", config_name="benchmark")
def run(config: BenchmarkConfig) -> None:
    print(OmegaConf.to_yaml(config))

    backend_factory: Type[Backend] = get_class(config.backend._target_)
    backend = backend_factory.allocate(config)
    benchmark = backend.execute(config)

    # Export the result
    df = benchmark.to_pandas()
    df.to_csv("results.csv", index_label="run")


if __name__ == '__main__':
    run()