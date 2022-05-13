import random
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import random


class ImageLoader:
    def __init__(self, args):
        self.args = args
        self.mnist = False

        if args.dataset == "cifar10":
            self.normalize = transforms.Normalize((0.491, 0.482, 0.446), (0.247, 0.243, 0.261))
            self.train_transform = transforms.Compose([
                transforms.RandomCrop(32, padding=4),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                self.normalize,])
            self.inference_transform = transforms.Compose([
                transforms.ToTensor(),
                self.normalize,])
            self.dataset_path = "data/cifar10"
            self.trainset_for_train = torchvision.datasets.CIFAR10(
                root=self.dataset_path, train=True, download=True, transform=self.train_transform)
            self.trainset_for_infer = torchvision.datasets.CIFAR10(
                root=self.dataset_path, train=True, download=True, transform=self.inference_transform)
            self.val_set = torchvision.datasets.CIFAR10(
                root=self.dataset_path, train=False, download=True, transform=self.inference_transform)

        elif args.dataset == "cifar100":
            self.normalize = transforms.Normalize((0.507, 0.486, 0.440), (0.267, 0.256, 0.276))
            self.train_transform = transforms.Compose([
                transforms.RandomCrop(32, padding=4),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                self.normalize,])
            self.inference_transform = transforms.Compose([
                transforms.ToTensor(),
                self.normalize,])
            self.dataset_path = "data/cifar100"
            self.trainset_for_train = torchvision.datasets.CIFAR100(
                root=self.dataset_path, train=True, download=True, transform=self.train_transform)
            self.trainset_for_infer = torchvision.datasets.CIFAR100(
                root=self.dataset_path, train=True, download=True, transform=self.inference_transform)
            self.val_set = torchvision.datasets.CIFAR100(
                root=self.dataset_path, train=False, download=True, transform=self.inference_transform)


    def get_loaders(self):
        trainset_loader_for_train = DataLoader(
            self.trainset_for_train, batch_size=self.args.batch_size, shuffle=True,
            worker_init_fn=lambda worker_id: random.seed(self.args.seed + worker_id))
        trainset_loader_for_infer = DataLoader(
            self.trainset_for_infer, batch_size=self.args.batch_size, shuffle=False,)
        valset_loader = DataLoader(
            self.val_set, batch_size=self.args.batch_size, shuffle=False,)

        return trainset_loader_for_train, trainset_loader_for_infer, valset_loader
