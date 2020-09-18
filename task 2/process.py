import json
import os
from PIL import Image
from sys import argv
import torch
from torchvision import transforms
from torch.utils.data import Dataset


class MaleFemaleDataset(Dataset):
    def __init__(self, folder, transform=None):
        self.transform = transform
        self.folder = folder

    def __len__(self):
        return len(os.listdir(self.folder))

    def __getitem__(self, index):
        img_id = os.listdir(self.folder)[index]
        img_path = os.path.join(self.folder, img_id)
        img = Image.open(img_path)
        if self.transform:
            img = self.transform(img)
        return img, img_id


path = argv[-1]
data = MaleFemaleDataset(path, transform=transforms.Compose([
                                            transforms.Resize((112, 112)),
                                            transforms.ToTensor(),
                                            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                  std=[0.229, 0.224, 0.225])                         
                                                       ]))
batch_size = 256
loader = torch.utils.data.DataLoader(data, batch_size=batch_size)

model = torch.load('model', map_location=torch.device('cpu'))
model.eval()
final_prediction = {}
for x, y in loader:
    pred = model(x)
    prediction = torch.max(pred, 1)[-1]
    prediction = list(map(lambda x: 'female' if x == 0 else 'male', prediction.tolist()))
    temp_dictionary = dict(zip(y, prediction))
    final_prediction.update(temp_dictionary)

with open('process_results.json', 'w') as fp:
    json.dump(final_prediction, fp)

