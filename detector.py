import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os

FRAME_DIR = "frames"

model = models.resnet18(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])


def analyze_frames(frames):

    scores = []

    for frame in frames:

        path = os.path.join(FRAME_DIR, frame)

        img = Image.open(path).convert("RGB")

        tensor = transform(img).unsqueeze(0)

        with torch.no_grad():
            output = model(tensor)

        prob = torch.softmax(output, dim=1).max().item()

        scores.append(prob)

    if len(scores) == 0:
        return 0

    return sum(scores) / len(scores)