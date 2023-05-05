from abc import (
    ABC,
    abstractmethod,
)

from stardist.matching import matching_dataset

from utils import (
    plot_img_label,
    to_sparse,
)


class BaseRunner(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _train(self, x_trn, y_trn, x_val, y_val, description):
        pass

    @abstractmethod
    def _eval(self, x_val, description):
        pass

    def run(
        self,
        x_trn,
        y_trn,
        x_val,
        y_val,
        kths=(1, 4, 16, 64, 256),
        mode="minmax",
        is_train=True,
        is_eval=True,
        include_bg=False,
    ):
        stats_list = []
        for i, kth in enumerate(kths + ("full",)):
            suffix = f"{kth:03d}" if isinstance(kth, int) else kth
            description = f'{mode}_{suffix}{"_bg" if include_bg else ""}'
            if is_train:
                y_trn_s = (
                    to_sparse(x_trn, y_trn, kth, include_bg=include_bg, mode=mode)
                    if isinstance(kth, int)
                    else y_trn
                )
                self._train(x_trn, y_trn_s, x_val, y_val, description)
            if is_eval:
                y_val_pred = self._eval(x_val, description)
                if i == 0:
                    plot_img_label(x_val[0], y_val[0], lbl_title="GT")
                plot_img_label(x_val[0], y_val_pred[0], lbl_title=f"Pred {self.name()} {description}")
                stats_list.append(
                    matching_dataset(y_val, y_val_pred, thresh=0.5, show_progress=False)
                )
        return stats_list if is_eval else None
