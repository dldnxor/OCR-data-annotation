import os
import os.path as osp
import time
import math
from datetime import timedelta
from argparse import ArgumentParser
import random

import torch
from torch import cuda
from torch.utils.data import DataLoader
from torch.optim import lr_scheduler
from tqdm import tqdm

from east_dataset import EASTDataset
from dataset import SceneTextDataset
from model import EAST

from sklearn.metrics import f1_score, recall_score, precision_score
import numpy as np

import wandb


def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)

def parse_args():
    parser = ArgumentParser()

    # Conventional args
    parser.add_argument(
        "--data_dir",
        type=str,
        default=os.environ.get("SM_CHANNEL_TRAIN", "../input/data/ICDAR17_All"),
    )
    parser.add_argument(
        "--model_dir", type=str, default=os.environ.get("SM_MODEL_DIR", "trained_models")
    )

    parser.add_argument('--seed', type=int, default=1, help='random seed (default: 1)')
    parser.add_argument("--device", default="cuda" if cuda.is_available() else "cpu")
    parser.add_argument("--num_workers", type=int, default=4)

    parser.add_argument("--image_size", type=int, default=1024)
    parser.add_argument("--input_size", type=int, default=512)
    parser.add_argument("--batch_size", type=int, default=12)
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--max_epoch", type=int, default=200)
    parser.add_argument("--save_interval", type=int, default=5)
    parser.add_argument("-a", "--augments_name", type=str, dest="augments_name")

    args = parser.parse_args()

    if args.input_size % 32 != 0:
        raise ValueError("`input_size` must be a multiple of 32")

    return args


def do_training(
    data_dir,
    model_dir,
    seed,
    device,
    image_size,
    input_size,
    num_workers,
    batch_size,
    learning_rate,
    max_epoch,
    save_interval,
):
    seed_everything(seed)

    train_set = SceneTextDataset(
        data_dir, split="train", image_size=image_size, crop_size=input_size
    )
    train_set = EASTDataset(train_set)
    train_num_batches = math.ceil(len(train_set) / batch_size)
    train_loader = DataLoader(
        train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )

    valid_set = SceneTextDataset(
        data_dir, split="valid", image_size=image_size, crop_size=input_size
    )
    valid_set = EASTDataset(valid_set)
    valid_num_batches = math.ceil(len(valid_set) / batch_size)
    valid_loader = DataLoader(
        valid_set, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = EAST()
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = lr_scheduler.MultiStepLR(optimizer, milestones=[max_epoch // 2], gamma=0.1)

    model.train()
    for epoch in range(max_epoch):
        epoch_loss, val_epoch_loss, epoch_start = 0, 0, time.time()
        with tqdm(total=train_num_batches) as pbar:
            for img, gt_score_map, gt_geo_map, roi_mask in train_loader:
                pbar.set_description("[Epoch {}]".format(epoch + 1))

                loss, extra_info = model.train_step(img, gt_score_map, gt_geo_map, roi_mask)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                loss_val = loss.item()
                epoch_loss += loss_val

                pbar.update(1)
                val_dict = {
                    "Cls loss": extra_info["cls_loss"],
                    "Angle loss": extra_info["angle_loss"],
                    "IoU loss": extra_info["iou_loss"],
                }
                pbar.set_postfix(val_dict)
        wandb.log(
            {
                "Train/epoch_loss": epoch_loss,
                "Train/Cls loss": extra_info["cls_loss"],
                "Train/Angle loss": extra_info["angle_loss"],
                "Train/IoU loss": extra_info["iou_loss"],
            },
            step=epoch,
        )

        with torch.no_grad():
            print("Calculating validation results...")
            model.eval()
            with tqdm(total=valid_num_batches) as pbar:
                for img, gt_score_map, gt_geo_map, roi_mask in valid_loader:
                    pbar.set_description("[Epoch {}]".format(epoch + 1))

                    loss, extra_info = model.train_step(img, gt_score_map, gt_geo_map, roi_mask)

                    loss_val = loss.item()
                    val_epoch_loss += loss_val

                    pbar.update(1)
                    val_dict = {
                        "Valid Cls loss": extra_info["cls_loss"],
                        "Valid Angle loss": extra_info["angle_loss"],
                        "Valid IoU loss": extra_info["iou_loss"],
                    }
                    pbar.set_postfix(val_dict)
        wandb.log(
            {
                "Val/epoch_loss": val_epoch_loss,
                "Val/Cls loss": extra_info["cls_loss"],
                "Val/Angle loss": extra_info["angle_loss"],
                "Val/IoU loss": extra_info["iou_loss"],
            },
            step=epoch,
        )
        scheduler.step()

        print(
            "Mean loss: {:.4f} | Elapsed time: {}".format(
                epoch_loss / train_num_batches, timedelta(seconds=time.time() - epoch_start)
            )
        )

        if (epoch + 1) % save_interval == 0:
            if not osp.exists(model_dir):
                os.makedirs(model_dir)

            ckpt_fpath = osp.join(model_dir, "latest.pth")
            torch.save(model.state_dict(), ckpt_fpath)


def main(args):
    augments_name = args.__dict__.pop("augments_name")
    run = wandb.init(project="data-ann", entity="cv_09_dataannotation", name=augments_name)
    wandb.config.update(args)
    do_training(**args.__dict__)


if __name__ == "__main__":
    args = parse_args()
    main(args)
