#!/usr/bin/env python
from runners import (
    CellposeRunner,
    ElephantRunner,
    StarDistRunner,
)
from utils import get_data


def main():
    (x_trn, y_trn), (x_val, y_val) = get_data()
    cellpose_runner = CellposeRunner(
        save_path="/src/models/cellpose/paper01",
        n_epochs=100,
    )
    elephant_runner = ElephantRunner(
        is_3d=False,
        model_dir="/src/models/elephant/paper01",
        log_dir="/src/models/elephant/paper01/logs",
        n_epochs=100,
    )
    train_batch_size = 8
    stardist_runner = StarDistRunner(
        grid=(2, 2),
        basedir="/src/models/stardist/paper01",
        use_gpu=False,
        train_epochs=100,
        train_patch_size=(224, 224),
        train_batch_size=train_batch_size,
        train_steps_per_epoch=len(x_trn) // train_batch_size + 1,
    )
    for runner in (cellpose_runner, elephant_runner, stardist_runner):
        for include_bg in (False, True):
            for mode in ("min", "max", "minmax"):
                runner.run(
                    x_trn,
                    y_trn,
                    x_val,
                    y_val,
                    mode=mode,
                    is_train=True,
                    is_eval=False,
                    include_bg=include_bg,
                )


if __name__ == "__main__":
    main()
