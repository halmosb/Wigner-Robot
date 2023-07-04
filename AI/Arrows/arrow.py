from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
import os
from PIL import Image
losses = []
testloss = []
accuracy = []

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 3, 4, 1)
        self.conv2 = nn.Conv2d(3, 3, 4, 1)
        self.conv3 = nn.Conv2d(3, 3, 4, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(45, 20)
        self.fc2 = nn.Linear(20, 4)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.conv3(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        #x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        #x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_list = os.listdir(self.root_dir)

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        img_name = self.image_list[idx]
        img_path = os.path.join(self.root_dir, img_name)
        image = Image.open(img_path).convert('L').resize((64, 48))
        #image.show()
        #exit()
        
        if self.transform is not None:
            image = self.transform(image)
        
        if "u" in img_name:
            label = 0
        elif "d" in img_name:
            label = 1
        elif "l" in img_name:
            label = 2
        elif "r" in img_name:
            label = 3        
        
        return image, label

def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            losses.append(loss.item())
            if args.dry_run:
                break


def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
    testloss.append(test_loss)
    accuracy.append(100. * correct / len(test_loader.dataset))


def main():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=100, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    
    parser.add_argument('--epochs', type=int, default=2, metavar='N',
                        help='number of epochs to train (default: 14)')
    
    parser.add_argument('--lr', type=float, default=4.0, metavar='LR',
                        help='learning rate (default: 4.0)')
    parser.add_argument('--gamma', type=float, default=0.7, metavar='M',
                        help='Learning rate step gamma (default: 0.7)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--no-mps', action='store_true', default=False,
                        help='disables macOS GPU training')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='quickly check a single pass')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=True,
                        help='For Saving the current Model')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    use_mps = not args.no_mps and torch.backends.mps.is_available()

    torch.manual_seed(args.seed)

    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    train_kwargs = {'batch_size': args.batch_size}
    test_kwargs = {'batch_size': args.test_batch_size}
    if use_cuda:
        cuda_kwargs = {'num_workers': 1,
                       'pin_memory': True,
                       'shuffle': True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    #dataset1 = datasets.MNIST('../data', train=True, download=True,
    #                   transform=transform)
    #dataset2 = datasets.MNIST('../data', train=False,
    #                   transform=transform)
    train_loader = torch.utils.data.DataLoader(CustomDataset("D:/ROBOTSTUFF/Data/AI/Arrow/frames", transform=transform),**train_kwargs)
    test_loader = torch.utils.data.DataLoader(CustomDataset("D:/ROBOTSTUFF/Data/AI/Arrow/test", transform=transform), **test_kwargs)

    model = Net().to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=args.lr)

    scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)
    for epoch in range(1, args.epochs + 1):
        #args.lr /= args.lrc
        for g in optimizer.param_groups:
           #g['lr'] = args.lr
            print(f"learning rate = {g['lr']}")
        train(args, model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)
        scheduler.step()

    #"index";"comment";"learning rate";"gamma";"epoch";"batch size";"seed";"log interval";"optimizer";transform";"stepLRsize";"loss";"test loss";"accuracy"

    if args.save_model:
        #torch.save(model.state_dict(), "newer_arrow.pt")
        model_scripted = torch.jit.script(model) # Export to TorchScript
        dir = os.listdir("Models")
        dir = filter(lambda name: ".model" in name, dir)
        index = int(max(dir)[:-6])+1
        
        model_scripted.save(f'Models/{index:04}.model')

        comment = "Arrows with generates imeges"

        with open('Models/parameters.csv', "a") as file:
            file.write(";".join([str(y) for y in [index,comment,args.lr,args.gamma,args.epochs,args.batch_size,args.seed,args.log_interval,"Adadelta",str(transform).replace("\n",""),1,losses,testloss,accuracy]]))
            file.write("\n")


if __name__ == '__main__':
    main()