"""
Train file Annotation results reviewer and modifier
wumengxi@umich.edu
"""
import csv, os, json, codecs
from urllib.request import urlretrieve
from matplotlib import patches
import matplotlib.pyplot as plt
import matplotlib.image as img 
from PIL import Image

reader = codecs.getreader("utf-8")
input_path = '/Users/wumengxi/Desktop/Ground_Truth/'
output_path = '/Users/wumengxi/Desktop/Grouth_Truth_Adjusted/'
filename = 'P7'

def inspect(filename):
    with open(input_path + filename + '.csv', encoding="utf-8", errors='replace') as csvfile:
        result = []
        reader = csv.DictReader(csvfile)
        image_index = 1
        for row in reader:
            url = row['Input.URL']
            data = json.loads(row['Answer.annotation_data'])
            print('URL:',url)
            urlretrieve(url, 'pic.jpg')
            print('Error1')
            pic = img.imread('pic.jpg')
            print('Error2')
            image_width = Image.open('pic.jpg').size[0]
            image_height = Image.open('pic.jpg').size[1]
            fig, ax = plt.subplots()
            ax.imshow(pic, extent=[0, image_width, 0, image_height])
            print('Orignal Data:')
            print(data)
            for index in range(10):
                if str(index) in data:
                    pos = data[str(index)]
                    top, left, height, width = pos['top'], pos['left'], pos['height'], pos['width']
                    id, label, label2 = pos['id'], pos['label'], pos['label2']
                    p = patches.Rectangle((left, image_height-(top+height)), width, height, fill = False, color="#33FFE0")
                    ax.add_patch(p)
                    ax.text(left, image_height-height, str(id)+'.'+ label, color='#33FFE0')
                    ax.text(left, image_height-top, str(id)+'.'+ label2, color='#33FFE0')
            if 'relationships' in data:
                rel = data['relationships']
                for obj1 in rel:
                    for obj2 in rel[obj1]:
                        object1 = (data[obj1]['left']+data[obj1]['width']/2, image_height-data[obj1]['top']-data[obj1]['height']/2)
                        object2 = (data[obj2]['left']+data[obj2]['width']/2, image_height-data[obj2]['top']-data[obj2]['height']/2)
                        #Add arrow to notify the relation
                        ax.arrow(object1[0], object2[1], object1[0]-object2[0], object1[1]-object2[1], head_width=10, head_length=5, color="#33FFE0")
                        #Put relation label at the midpoint of two subjects
                        ax.text((object1[0]+object2[0])/2, (object1[1]+object2[1])/2,rel[obj1][obj2],horizontalalignment='center', verticalalignment='center',color="#000000",size=10,backgroundcolor="#ffffff")
            plt.show()
            os.system('rm pic.jpg')
            add_to_train = ''
            while not (add_to_train == 'y' or add_to_train == 'n'):
                add_to_train = input(str(image_index)+'.Add to Train? (y/n)')
            if add_to_train == 'y':
                new_json = ''
                need_modify = input(str(image_index)+'.Need modify?')
                if need_modify == 'y':
                     new_json = input(str(image_index)+'.Modify Json:\n')
                     print('Modified Json:', new_json)
                result.append(['y', '', new_json])
            else:
                result.append(['', 'not proper label',''])
            image_index = image_index + 1
    
        with open(output_path + filename + '+reviewed.csv', 'w') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(result)

if __name__ == "__main__":
    inspect(filename)


