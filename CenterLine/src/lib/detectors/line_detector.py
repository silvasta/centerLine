from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import numpy as np
from progress.bar import Bar
import time
import torch
import torch.nn as nn

from models.model import create_model, load_model
from utils.image import get_affine_transform
from models.utils import _gather_feat, _transpose_and_gather_feat
from utils.post_process import ctdet_post_process
from utils.metric import print_lines

class NewLineDetector():

    def __init__(self, opt):
        if opt.gpus[0] >= 0:
            opt.device = torch.device('cuda')
        else:
            opt.device = torch.device('cpu')

        print('Creating model...')
        self.model = create_model(opt.arch, opt.heads, opt.head_conv)
        self.model = load_model(self.model, opt.load_model)
        self.model = self.model.to(opt.device)
        self.model.eval()

        self.mean = np.array(opt.mean, dtype=np.float32).reshape(1, 1, 3)
        self.std = np.array(opt.std, dtype=np.float32).reshape(1, 1, 3)
        self.max_per_image = 100
        self.num_classes = opt.num_classes
        self.opt = opt
        self.pause = True

    def run(self, image, meta=None):
        
        img = cv2.imread(image)
        
        image, meta = self.pre_process(image)        
        

        image = image.to(self.opt.device)
        torch.cuda.synchronize()

        output, dets = self.process(image)
        torch.cuda.synchronize()
        
     
        dets = self.post_process(dets, meta)
        torch.cuda.synchronize()

        detections = []
        detections.append(dets)
        
        results = self.merge_outputs(detections)
        torch.cuda.synchronize()



        if self.opt.debug >= 1:
            save_results(self.opt, img, results, dataset=self.opt.dataset)

        
        return results

    def pre_process(self, image):

        image = cv2.imread(image)
        height, width = image.shape[0:2]

        inp_height = (height | self.opt.pad) + 1
        inp_width = (width | self.opt.pad) + 1
        c = np.array([width // 2, height // 2], dtype=np.float32)
        s = np.array([inp_width, inp_height], dtype=np.float32)

        trans_input = get_affine_transform(c, s, 0, [inp_width, inp_height])
        image = cv2.warpAffine(image, trans_input, (inp_width, inp_height),flags=cv2.INTER_LINEAR)

        image = ((image / 255. - self.mean) / self.std).astype(np.float32)
        image = image.transpose(2, 0, 1).reshape(1, 3, inp_height, inp_width)
        image = torch.from_numpy(image)

        meta = {'c': c, 's': s, 
            'out_height': inp_height // self.opt.down_ratio, 
            'out_width': inp_width // self.opt.down_ratio}

        return image, meta


    def process(self, image):

        with torch.no_grad():
            output = self.model(image)[-1]
            hm = output['hm'].sigmoid_()
            wh = output['wh']
            reg = output['reg']
        torch.cuda.synchronize()

        dets = decode(hm, wh, reg=reg,K=self.opt.K)
        
        
        return output, dets

    def post_process(self, dets, meta, scale=1):

        dets = dets.detach().cpu().numpy()
        dets = dets.reshape(1, -1, dets.shape[2])
        dets = ctdet_post_process(
            dets.copy(), [meta['c']], [meta['s']],
            meta['out_height'], meta['out_width'], self.opt.num_classes)
        for j in range(1, self.num_classes + 1):
            dets[0][j] = np.array(dets[0][j], dtype=np.float32).reshape(-1, 5)
            dets[0][j][:, :4] /= scale
        return dets[0]

    def merge_outputs(self, detections):
        results = {}
        for j in range(1, self.num_classes + 1):
            results[j] = np.concatenate(
            [detection[j] for detection in detections], axis=0).astype(np.float32)

        scores = np.hstack(
        [results[j][:, 4] for j in range(1, self.num_classes + 1)])
        if len(scores) > self.max_per_image:
            kth = len(scores) - self.max_per_image
            thresh = np.partition(scores, kth)[kth]
            for j in range(1, self.num_classes + 1):
                keep_inds = (results[j][:, 4] >= thresh)
                results[j] = results[j][keep_inds]
        return results



def decode(heat, wh, reg=None, K=100):

    batch, cat, height, width = heat.size()

    heat = _nms(heat)
      
    scores, inds, clses, ys, xs = _topk(heat, K=K)

    reg = _transpose_and_gather_feat(reg, inds)
    reg = reg.view(batch, K, 2)
    xs = xs.view(batch, K, 1) + reg[:, :, 0:1]
    ys = ys.view(batch, K, 1) + reg[:, :, 1:2]

    wh = _transpose_and_gather_feat(wh, inds)
    
    wh = wh.view(batch, K, 2)

    clses  = clses.view(batch, K, 1).float()
    scores = scores.view(batch, K, 1)
    bboxes = torch.cat([xs - wh[..., 0:1] / 2, 
                        ys - wh[..., 1:2] / 2,
                        xs + wh[..., 0:1] / 2, 
                        ys + wh[..., 1:2] / 2], dim=2)
    detections = torch.cat([bboxes, scores, clses], dim=2)
      
    return detections

def _nms(heat, kernel=3):

    pad = (kernel - 1) // 2

    hmax = nn.functional.max_pool2d(
        heat, (kernel, kernel), stride=1, padding=pad)
    keep = (hmax == heat).float()
    return heat * keep


def _topk(scores, K=40):
    batch, cat, height, width = scores.size()
      
    topk_scores, topk_inds = torch.topk(scores.view(batch, cat, -1), K)

    topk_inds = topk_inds % (height * width)
    topk_ys   = (topk_inds / width).int().float()
    topk_xs   = (topk_inds % width).int().float()
      
    topk_score, topk_ind = torch.topk(topk_scores.view(batch, -1), K)
    topk_clses = (topk_ind / K).int()
    topk_inds = _gather_feat(
        topk_inds.view(batch, -1, 1), topk_ind).view(batch, K)
    topk_ys = _gather_feat(topk_ys.view(batch, -1, 1), topk_ind).view(batch, K)
    topk_xs = _gather_feat(topk_xs.view(batch, -1, 1), topk_ind).view(batch, K)

    return topk_score, topk_inds, topk_clses, topk_ys, topk_xs


def save_results(opt, image, results, theme='black', dataset=None):

    colors = [(color_list[_]).astype(np.uint8) for _ in range(len(color_list))]
    colors = np.array(colors, dtype=np.uint8).reshape(len(colors), 1, 1, 3)
    
    if theme == 'white':
      colors = colors.reshape(-1)[::-1].reshape(len(colors), 1, 1, 3)
      colors = np.clip(colors, 0., 0.6 * 255).astype(np.uint8)
    

    if dataset == 'line_4_cat':
      names = ['horizontal', 'vertical', 'top_left', 'top_right']

    elif dataset == 'line_2_cat':
      names = ['top_left', 'top_right']

    else:
      names = ['line']
      num_class = 1

    num_classes = len(names)

    # imgs[img_id] = image.copy()
    for j in range(1, num_classes + 1):
      for line in results[j]:
        if line[4] > opt.vis_thresh:
          print()
          print("before add")
          print()
          print(j)
          image = add_lines(image,names[j-1],line[:4], cat=j, conf=line[4], img_id='line')
    save_all_imgs(image, path=opt.demo_out)


def add_lines(image, names, line, cat, conf=1,show_txt=False, img_id='default'):
    line = np.array(line, dtype=np.int32)

    color = (0,0,255)

    txt = '{}{:.1f}'.format(names[cat-1], conf)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cat_size = cv2.getTextSize(txt, font, 0.5, 2)[0]
    
    if show_txt:
      cv2.rectangle(image,
                    (line[0], line[1] - cat_size[1] - 2),
                    (line[0] + cat_size[0], line[1] - 2), c, -1)
      cv2.putText(image[img_id], txt, (line[0], line[1] - 2), 
                  font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)
    
    if cat == 1:
        cv2.line(image, (line[0], line[1]),(line[2], line[3]), color, 5)
    elif cat == 2:
        cv2.line(image, (line[2], line[1]),(line[0], line[3]), color, 5)
    else:
        raise NotImplementedError

    cv2.rectangle(image, (line[0], line[1]), (line[2], line[3]), color, 2)

    return image

def save_all_imgs(image, path):

    try:
        idx = int(np.loadtxt(path + '/id.txt'))
    except:
        idx = 0
    prefix=idx
    print("path",path)
    print("image",image)
    np.savetxt(path + '/id.txt', np.ones(1) * (idx + 1), fmt='%d')
    cv2.imwrite(path + '/{}{}.png'.format(prefix, "_detected"), image)



color_list = np.array(
        [
            1.000, 1.000, 1.000,
            0.850, 0.325, 0.098,
            0.929, 0.694, 0.125,
            0.494, 0.184, 0.556,
            0.466, 0.674, 0.188,
            0.301, 0.745, 0.933,
            0.635, 0.078, 0.184,
            0.300, 0.300, 0.300,
            0.600, 0.600, 0.600,
            1.000, 0.000, 0.000,
            1.000, 0.500, 0.000,
            0.749, 0.749, 0.000,
            0.000, 1.000, 0.000,
            0.000, 0.000, 1.000,
            0.667, 0.000, 1.000,
            0.333, 0.333, 0.000,
            0.333, 0.667, 0.000,
            0.333, 1.000, 0.000,
            0.667, 0.333, 0.000,
            0.667, 0.667, 0.000,
            0.667, 1.000, 0.000,
            1.000, 0.333, 0.000,
            1.000, 0.667, 0.000,
            1.000, 1.000, 0.000,
            0.000, 0.333, 0.500,
            0.000, 0.667, 0.500,
            0.000, 1.000, 0.500,
            0.333, 0.000, 0.500,
            0.333, 0.333, 0.500,
            0.333, 0.667, 0.500,
            0.333, 1.000, 0.500,
            0.667, 0.000, 0.500,
            0.667, 0.333, 0.500,
            0.667, 0.667, 0.500,
            0.667, 1.000, 0.500,
            1.000, 0.000, 0.500,
            1.000, 0.333, 0.500,
            1.000, 0.667, 0.500,
            1.000, 1.000, 0.500,
            0.000, 0.333, 1.000,
            0.000, 0.667, 1.000,
            0.000, 1.000, 1.000,
            0.333, 0.000, 1.000,
            0.333, 0.333, 1.000,
            0.333, 0.667, 1.000,
            0.333, 1.000, 1.000,
            0.667, 0.000, 1.000,
            0.667, 0.333, 1.000,
            0.667, 0.667, 1.000,
            0.667, 1.000, 1.000,
            1.000, 0.000, 1.000,
            1.000, 0.333, 1.000,
            1.000, 0.667, 1.000,
            0.167, 0.000, 0.000,
            0.333, 0.000, 0.000,
            0.500, 0.000, 0.000,
            0.667, 0.000, 0.000,
            0.833, 0.000, 0.000,
            1.000, 0.000, 0.000,
            0.000, 0.167, 0.000,
            0.000, 0.333, 0.000,
            0.000, 0.500, 0.000,
            0.000, 0.667, 0.000,
            0.000, 0.833, 0.000,
            0.000, 1.000, 0.000,
            0.000, 0.000, 0.167,
            0.000, 0.000, 0.333,
            0.000, 0.000, 0.500,
            0.000, 0.000, 0.667,
            0.000, 0.000, 0.833,
            0.000, 0.000, 1.000,
            0.000, 0.000, 0.000,
            0.143, 0.143, 0.143,
            0.286, 0.286, 0.286,
            0.429, 0.429, 0.429,
            0.571, 0.571, 0.571,
            0.714, 0.714, 0.714,
            0.857, 0.857, 0.857,
            0.000, 0.447, 0.741,
            0.50, 0.5, 0
        ]
    ).astype(np.float32)
color_list = color_list.reshape((-1, 3)) * 255